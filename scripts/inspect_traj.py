#!/usr/bin/env python3
"""Print per-step token, KV-Cache, cost, and observation size breakdown for a trajectory."""

import json
import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: inspect_traj.py <path/to/traj.json>")
        sys.exit(1)

    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    msgs = data if isinstance(data, list) else data.get("messages", [])

    header = f"{'Step':>4} | {'Prompt':>7} | {'Cached':>7} | {'Hit%':>6} | {'Comp':>5} | {'Cost($)':>8} | {'ObsChars':>8} | Command"
    print(header)
    print("-" * len(header))

    step = 0
    for i, m in enumerate(msgs):
        if m.get("role") != "assistant":
            continue
        step += 1
        extra = m.get("extra") or {}
        u = (extra.get("response") or {}).get("usage") or {}
        pd = u.get("prompt_tokens_details") or {}
        pt = u.get("prompt_tokens", 0) or 0
        ct = u.get("prompt_cache_hit_tokens", pd.get("cached_tokens", 0) or 0) or 0
        comp = u.get("completion_tokens", 0) or 0
        cost = extra.get("cost", 0.0) or 0.0
        hit = (ct / pt * 100.0) if pt else 0.0
        obs_chars = (
            len(msgs[i + 1].get("content", ""))
            if i + 1 < len(msgs) and msgs[i + 1].get("role") in ("user", "tool")
            else 0
        )
        acts = extra.get("actions") or []
        cmd = acts[0].get("command", "").replace("\n", " ")[:40] if acts else ""
        print(f"{step:>4} | {pt:>7} | {ct:>7} | {hit:>5.1f}% | {comp:>5} | {cost:>8.6f} | {obs_chars:>8} | {cmd}")


if __name__ == "__main__":
    main()
