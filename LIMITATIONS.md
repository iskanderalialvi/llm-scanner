# Limitations

## The judge is vulnerable to indirect prompt injection

The judge is a second LLM call that receives the target's response as part of
its prompt. A malicious target can therefore attempt to manipulate the judge by
embedding instructions in its reply — closing the delimiter block early and
issuing its own verdict.

Delimiters (`---RESPONSE---`) are a weak mitigation, not a fix. To a language
model there is no boundary between instructions and data; everything in the
context window is one stream of text.

Status: known, unmitigated. Probe candidate for the Phase 3 library
(LLM01 — indirect injection against the scoring layer).

