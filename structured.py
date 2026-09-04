import json

from probe import send_prompt


FENCE = "```"


def strip_fences(raw: str) -> str:
    """Remove markdown code fences the model wraps its JSON in."""
    text = raw.strip()
    if not text.startswith(FENCE):
        return text

    lines = text.splitlines()
    lines = lines[1:]
    if lines and lines[-1].strip().startswith(FENCE):
        lines = lines[:-1]
    return "\n".join(lines).strip()


def extract_json(raw: str) -> dict:
    """Turn a model's text reply into a dict, or raise ValueError."""
    text = strip_fences(raw)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError(f"No JSON object found in reply: {raw!r}")

    try:
        return json.loads(text[start:end + 1])
    except json.JSONDecodeError as exc:
        raise ValueError(f"Braces found but content invalid: {raw!r}") from exc


def ask_json(prompt: str, system: str, attempts: int = 2) -> dict:
    """Ask the model for JSON. Retry once before giving up."""
    last_error = None

    for attempt in range(1, attempts + 1):
        raw = send_prompt(prompt, system=system)
        try:
            return extract_json(raw)
        except ValueError as exc:
            last_error = exc
            print(f"[warn] attempt {attempt}/{attempts}: no valid JSON")

    raise ValueError(f"No JSON after {attempts} attempts") from last_error
