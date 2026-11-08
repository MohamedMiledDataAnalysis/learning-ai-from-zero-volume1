"""Chapter 26 — ask again, with the error, when a reply is invalid.

The 'model' here is a script that plays back two fixed replies (the first
invalid, the second valid), so you can see the retry logic work the same way
every time. With a real model, replace scripted_model by a call to ask_model.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_reply import REPLIES, validate  # noqa: E402

script = [REPLIES["C percent"], REPLIES["A clean"]]     # fixed replies, not written by a model


def scripted_model(messages):
    return script.pop(0)


def ask_until_valid(messages, model, max_tries=3):
    for attempt in range(1, max_tries + 1):
        reply = model(messages)
        data, problems = validate(reply)
        print(f"Attempt {attempt}: {'valid' if not problems else 'invalid - ' + '; '.join(problems)}")
        if not problems:
            return data
        # Tell the model exactly what was wrong, then ask again.
        messages = messages + [
            {"role": "assistant", "content": reply},
            {"role": "user", "content": "Your reply was not valid: " + "; ".join(problems)
                                        + ". Reply again with JSON only, fixing these problems."},
        ]
    raise RuntimeError(f"no valid reply after {max_tries} attempts")


if __name__ == "__main__":
    first = [{"role": "user", "content": "Summarise the October 90+ day arrears test as JSON."}]
    result = ask_until_valid(first, scripted_model)
    print("Accepted:", result)
