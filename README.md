# llm-scanner

Security testing for LLM-backed applications. Sends adversarial probes to an
LLM endpoint, scores the responses with a judge model, and maps findings to the
OWASP Top 10 for LLM Applications.

Status: v0.1 — probe, structured output layer, and judge working.

## Reliability

Same prompt run 10 times each, `temperature=1.0`, model `openai/gpt-oss-20b`.
Both parsers tested against the *same* reply on every run.

| Prompt style | raw `json.loads()` | after `extract_json()` |
|---|---|---|
| careful (system role + example shape + no-markdown rule) | 10/10 | 10/10 |
| careless (no system role, no shape) | 8/10 | 10/10 |

A carefully written prompt does most of the work. The repair layer is the floor
under it — it recovered both failures in the careless run. That matters because
a scanner firing varied probes at an endpoint it does not control is always
closer to the careless case than the careful one.

Reproduce with `python3 reliability.py`.
