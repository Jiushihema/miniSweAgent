#!/usr/bin/env python3

import json
import sys
from pathlib import Path


def strip_extra(messages: list[dict]) -> list[dict]:
    return [{k: v for k, v in msg.items() if k != "extra"} for msg in messages]


def compute_traj_stats(data: list[dict] | dict) -> dict:
    messages = data if isinstance(data, list) else data.get("messages", [])
    clean_messages = strip_extra(messages)
    input_sizes = []
    total_cost = 0.0
    prompt_tokens = 0
    cached_tokens = 0
    completion_tokens = 0

    for i, message in enumerate(messages):
        if message.get("role") != "assistant":
            continue
        input_sizes.append(len(json.dumps(clean_messages[:i], ensure_ascii=False)))
        extra = message.get("extra") or {}
        response = extra.get("response")
        usage = (response.get("usage") or {}) if isinstance(response, dict) else {}
        prompt_details = usage.get("prompt_tokens_details") or {}
        total_cost += extra.get("cost", 0.0) or 0.0
        prompt_tokens += usage.get("prompt_tokens", 0) or 0
        cached_tokens += (
            usage.get(
                "prompt_cache_hit_tokens",
                prompt_details.get("cached_tokens", 0) or 0,
            )
            or 0
        )
        completion_tokens += usage.get("completion_tokens", 0) or 0

    first_chars = input_sizes[0] if input_sizes else 0
    last_chars = input_sizes[-1] if input_sizes else 0
    ratio = (last_chars / first_chars) if first_chars else 0.0
    total_chars = sum(input_sizes)
    hit_rate = (cached_tokens / prompt_tokens * 100.0) if prompt_tokens else 0.0

    return {
        "steps": len(input_sizes),
        "first_chars": first_chars,
        "last_chars": last_chars,
        "last_first_ratio": round(ratio, 2),
        "total_chars": total_chars,
        "prompt_tokens": prompt_tokens,
        "cached_tokens": cached_tokens,
        "cache_hit_rate": round(hit_rate, 2),
        "completion_tokens": completion_tokens,
        "cost": round(total_cost, 6),
    }


def main() -> None:
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    s = compute_traj_stats(data)
    print(f"steps: {s['steps']}")
    print(f"first step input characters: {s['first_chars']}")
    print(f"last step input characters: {s['last_chars']}")
    print(f"last / first: {s['last_first_ratio']:.2f}")
    print(f"total input characters: {s['total_chars']}")
    print(f"total prompt tokens: {s['prompt_tokens']}")
    print(f"cached prompt tokens: {s['cached_tokens']} ({s['cache_hit_rate']:.1f}%)")
    print(f"total completion tokens: {s['completion_tokens']}")
    print(f"total cost ($): {s['cost']:.6f}")


if __name__ == "__main__":
    main()
