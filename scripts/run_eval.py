#!/usr/bin/env python3
"""Batch evaluation runner for mini-swe-agent cost-optimization experiments."""

import argparse
import os

os.environ.setdefault("LITELLM_LOCAL_MODEL_COST_MAP", "True")
import csv
import json
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from minisweagent.agents.default import DefaultAgent
from minisweagent.config import builtin_config_dir, get_config_from_spec
from minisweagent.environments.local import LocalEnvironment
from minisweagent.models import get_model
from minisweagent.utils.serialize import recursive_merge

sys.path.insert(0, str(Path(__file__).resolve().parent))
from traj_stats import compute_traj_stats  # noqa: E402

CSV_FIELDS = [
    "task_id",
    "policy",
    "passed",
    "exit_status",
    "steps",
    "first_chars",
    "last_chars",
    "last_first_ratio",
    "total_chars",
    "prompt_tokens",
    "cached_tokens",
    "cache_hit_rate",
    "completion_tokens",
    "cost",
    "elapsed_sec",
]


def discover_tasks(tasks_dir: Path, task_ids: set[str] | None) -> list[Path]:
    dirs = sorted(p for p in tasks_dir.iterdir() if p.is_dir() and (p / "task.json").exists())
    if task_ids:
        dirs = [p for p in dirs if p.name in task_ids or json.loads((p / "task.json").read_text())["id"] in task_ids]
    return dirs


def run_single_task(
    task_dir: Path,
    *,
    policy: str,
    output_dir: Path,
    model_name: str | None,
    step_limit: int,
    cost_limit: float,
) -> dict:
    task_meta = json.loads((task_dir / "task.json").read_text(encoding="utf-8"))
    task_id = task_meta["id"]
    trajs_dir = output_dir / "trajs"
    trajs_dir.mkdir(parents=True, exist_ok=True)
    traj_path = trajs_dir / f"{task_id}.traj.json"

    base_cfg = get_config_from_spec(str(builtin_config_dir / "mini.yaml"))
    overrides = {
        "agent": {
            "mode": "yolo",
            "confirm_exit": False,
            "step_limit": step_limit,
            "cost_limit": cost_limit,
            "output_path": str(traj_path),
        },
        "model": {},
        "environment": {"env": {"PATH": f"{Path(sys.executable).parent}:{os.environ.get('PATH', '')}"}},
    }
    if model_name:
        overrides["model"]["model_name"] = model_name

    workdir = Path(tempfile.mkdtemp(prefix=f"mswea_{policy}_{task_id}_"))
    t0 = time.time()
    exit_status = "Unknown"
    passed = False
    oracle_output = ""

    try:
        shutil.copytree(task_dir / "repo", workdir, dirs_exist_ok=True)
        overrides["environment"]["cwd"] = str(workdir)
        cfg = recursive_merge(base_cfg, overrides)

        model = get_model(cfg["model"].get("model_name"), cfg["model"])
        env = LocalEnvironment(**cfg["environment"])
        agent = DefaultAgent(model, env, **cfg["agent"])
        pinned_prompt = (
            f"Working directory: {workdir}\n"
            f"IMPORTANT: Only inspect and edit files inside `{workdir}`. Do not search outside it.\n\n"
            + task_meta["prompt"]
        )
        res = agent.run(task=pinned_prompt)
        exit_status = res.get("exit_status", "Unknown")

        oracle_dest = workdir / "oracle_tests"
        shutil.copytree(task_dir / "oracle_tests", oracle_dest, dirs_exist_ok=True)
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "oracle_tests"],
            cwd=workdir,
            capture_output=True,
            text=True,
            timeout=30,
        )
        passed = proc.returncode == 0
        oracle_output = (proc.stdout + "\n" + proc.stderr).strip()
    except Exception as e:
        exit_status = f"RunnerError:{type(e).__name__}"
        oracle_output = str(e)
    finally:
        shutil.rmtree(workdir, ignore_errors=True)

    elapsed_sec = round(time.time() - t0, 2)
    stats = compute_traj_stats(json.loads(traj_path.read_text(encoding="utf-8"))) if traj_path.exists() else {}

    record = {
        "task_id": task_id,
        "policy": policy,
        "passed": passed,
        "exit_status": exit_status,
        "steps": stats.get("steps", 0),
        "first_chars": stats.get("first_chars", 0),
        "last_chars": stats.get("last_chars", 0),
        "last_first_ratio": stats.get("last_first_ratio", 0.0),
        "total_chars": stats.get("total_chars", 0),
        "prompt_tokens": stats.get("prompt_tokens", 0),
        "cached_tokens": stats.get("cached_tokens", 0),
        "cache_hit_rate": stats.get("cache_hit_rate", 0.0),
        "completion_tokens": stats.get("completion_tokens", 0),
        "cost": stats.get("cost", 0.0),
        "elapsed_sec": elapsed_sec,
        "oracle_output": oracle_output,
    }
    (output_dir / f"{task_id}.result.json").write_text(
        json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return record


def write_csv(records: list[dict], csv_path: Path) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)


def print_summary(records: list[dict], policy: str) -> None:
    total = len(records)
    solved = sum(1 for r in records if r["passed"])
    total_cost = sum(r["cost"] for r in records)
    total_prompt = sum(r["prompt_tokens"] for r in records)
    total_cached = sum(r["cached_tokens"] for r in records)
    avg_steps = (sum(r["steps"] for r in records) / total) if total else 0.0
    resolve_rate = (solved / total * 100.0) if total else 0.0
    cost_per_solved = (total_cost / solved) if solved else float("inf")
    hit_rate = (total_cached / total_prompt * 100.0) if total_prompt else 0.0

    print(f"\n=== Eval Summary [{policy}] ===")
    print(f"Resolve Rate       : {solved}/{total} ({resolve_rate:.1f}%)")
    print(f"Total Cost ($)     : {total_cost:.6f}")
    print(f"Cost / Solved ($)  : {cost_per_solved:.6f}")
    print(f"KV Cache Hit Rate  : {hit_rate:.1f}% ({total_cached}/{total_prompt})")
    print(f"Avg Steps          : {avg_steps:.2f}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Batch eval runner for mini-swe-agent")
    parser.add_argument("--tasks-dir", type=Path, default=Path("eval/tasks"))
    parser.add_argument("--task-ids", type=str, default="", help="Comma-separated task IDs")
    parser.add_argument("--policy", type=str, default="baseline")
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--model", type=str, default=None)
    parser.add_argument("--step-limit", type=int, default=25)
    parser.add_argument("--cost-limit", type=float, default=0.20)
    parser.add_argument("--resume", action="store_true", help="Skip tasks with existing result.json")
    args = parser.parse_args()

    output_dir = args.output_dir or Path("results") / args.policy
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = Path("results") / f"{args.policy}.csv"
    task_ids = {t.strip() for t in args.task_ids.split(",") if t.strip()} if args.task_ids else None
    task_dirs = discover_tasks(args.tasks_dir, task_ids)

    if not task_dirs:
        print(f"No tasks found in {args.tasks_dir}", file=sys.stderr)
        sys.exit(1)

    records: list[dict] = []
    for task_dir in task_dirs:
        task_id = json.loads((task_dir / "task.json").read_text(encoding="utf-8"))["id"]
        result_file = output_dir / f"{task_id}.result.json"
        if args.resume and result_file.exists():
            rec = json.loads(result_file.read_text(encoding="utf-8"))
            print(f"[SKIP] {task_id} (cached: passed={rec['passed']}, cost=${rec['cost']:.6f})")
        else:
            print(f"[RUN ] {task_id} (policy={args.policy})...")
            rec = run_single_task(
                task_dir,
                policy=args.policy,
                output_dir=output_dir,
                model_name=args.model,
                step_limit=args.step_limit,
                cost_limit=args.cost_limit,
            )
            print(
                f"[DONE] {task_id}: passed={rec['passed']} steps={rec['steps']} "
                f"hit={rec['cache_hit_rate']:.1f}% cost=${rec['cost']:.6f} ({rec['exit_status']})"
            )
        records.append(rec)
        write_csv(records, csv_path)

    print_summary(records, args.policy)


if __name__ == "__main__":
    main()
