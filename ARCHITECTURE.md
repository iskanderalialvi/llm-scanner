cat > ARCHITECTURE.md << 'EOF'
# Architecture

probe.py — sends a prompt to the model over the internet and returns just the
model's text reply.

structured.py — turns that text into data the code can use, even when the model
wraps it in backticks or adds chatter, and gives up cleanly after two tries.

judge.py — fills a form with the attack, the reply and the pass criterion, then
asks a second model whether the first one failed.

Call chain:
judge() -> ask_json() -> send_prompt() -> Groq API
                      -> extract_json() -> strip_fences()

Imports point one way: structured.py imports probe.py, never the reverse,
because structured.py needs send_prompt to fetch replies, while probe.py needs
nothing from structured.py and runs fine alone. If both imported each other,
Python would hit a circular import.

