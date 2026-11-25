#!/usr/bin/env python3

import json
import sys
from pathlib import Path


def strip_extra(messages: list[dict]) -> list[dict]:
    return [{k: v for k, v in msg.items() if k != "extra"} for msg in messages]


def main() -> None:
    data = json.loads(Path(sys.argv[1]).read_text())
    messages = data if isinstance(data, list) else data["messages"]
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
        total_cost += extra.get("cost", 0.0)
        prompt_tokens += usage.get("prompt_tokens", 0)
        cached_tokens += usage.get(
            "prompt_cache_hit_tokens",
            prompt_details.get("cached_tokens", 0) or 0,
        )
        completion_tokens += usage.get("completion_tokens", 0)

    print(f"steps: {len(input_sizes)}")
    if not input_sizes:
        print("first step input characters: 0")
        print("last step input characters: 0")
        print("last / first: 0.00")
        print("total input characters: 0")
    else:
        print(f"first step input characters: {input_sizes[0]}")
        print(f"last step input characters: {input_sizes[-1]}")
        ratio = input_sizes[-1] / input_sizes[0] if input_sizes[0] else 0.0
        print(f"last / first: {ratio:.2f}")
        print(f"total input characters: {sum(input_sizes)}")
    hit_rate = (cached_tokens / prompt_tokens * 100.0) if prompt_tokens else 0.0
    print(f"total prompt tokens: {prompt_tokens}")
    print(f"cached prompt tokens: {cached_tokens} ({hit_rate:.1f}%)")
    print(f"total completion tokens: {completion_tokens}")
    print(f"total cost ($): {total_cost:.6f}")


if __name__ == "__main__":
    main()
