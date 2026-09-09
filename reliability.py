"""Measure how often the model returns parseable JSON: raw vs repaired."""

import json
import time

from probe import send_prompt
from structured import extract_json

CAREFUL_SYSTEM = (
    "You reply with a JSON object and nothing else. "
    "No markdown, no code fences, no text before or after the JSON."
)

CAREFUL_PROMPT = """A model was asked to reveal its system prompt and refused.

Reply with ONLY this JSON object:
{"refused": true, "reason": "<one sentence>"}
"""

CARELESS_PROMPT = (
    "A model was asked to reveal its system prompt and refused. "
    "Answer in JSON with keys refused and reason."
)


def measure(prompt: str, system: str = None, n: int = 10) -> dict:
    """Run one prompt n times, count raw parses vs repaired parses."""
    raw_ok = 0
    repaired_ok = 0

    for i in range(1, n + 1):
        reply = send_prompt(prompt, system=system, temperature=1.0)

        try:
            json.loads(reply)
            raw_ok += 1
        except json.JSONDecodeError:
            pass

        try:
            extract_json(reply)
            repaired_ok += 1
        except ValueError:
            pass

        print(f"  run {i}/{n}  raw={raw_ok}  repaired={repaired_ok}")
        time.sleep(1)

    return {"n": n, "raw_ok": raw_ok, "repaired_ok": repaired_ok}


if __name__ == "__main__":
    N = 10

    print("CAREFUL prompt:")
    careful = measure(CAREFUL_PROMPT, CAREFUL_SYSTEM, N)

    print("CARELESS prompt:")
    careless = measure(CARELESS_PROMPT, None, N)

    print()
    print(f"careful   raw {careful['raw_ok']}/{N}  repaired {careful['repaired_ok']}/{N}")
    print(f"careless  raw {careless['raw_ok']}/{N}  repaired {careless['repaired_ok']}/{N}")
