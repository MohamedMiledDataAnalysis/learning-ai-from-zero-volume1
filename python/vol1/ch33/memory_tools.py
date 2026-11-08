"""Short-term memory (the message list) and long-term memory (a JSON file kept between runs)."""

import json
from pathlib import Path


def approx_tokens(text):
    """A planning estimate: about 4 characters per token for English text. The exact count needs the model's tokeniser."""
    return max(1, round(len(text) / 4))


def memory_size(memory):
    return sum(approx_tokens(m.get("content", "") + json.dumps(m.get("tool_calls", []))) for m in memory)


def trim_memory(memory, keep_last_turns):
    """Keep the system message, the goal, and the last turns. A turn is one assistant message
    and the tool results that answer it: the two are never separated."""
    head, rest = memory[:2], memory[2:]
    turns, current = [], []
    for m in rest:
        if m["role"] == "assistant" and current:
            turns.append(current)
            current = []
        current.append(m)
    if current:
        turns.append(current)
    kept = [m for turn in turns[-keep_last_turns:] for m in turn]
    return head + kept


def summarise_memory(memory, keep_last_turns):
    """Replace the oldest turns by one short note listing the facts they produced."""
    trimmed = trim_memory(memory, keep_last_turns)
    dropped = [m for m in memory[2:] if m not in trimmed]
    facts = []
    for m in dropped:
        if m["role"] == "tool":
            facts.append(f"{m['tool_name']} -> {m['content']}")
    note = {"role": "system", "content": "Facts from earlier steps: " + "; ".join(facts)}
    return trimmed[:2] + [note] + trimmed[2:]


class LongTermMemory:
    """Facts saved in a JSON file, so the next run starts with them."""

    def __init__(self, path):
        self.path = Path(path)
        self.facts = json.loads(self.path.read_text(encoding="utf-8")) if self.path.exists() else {}

    def remember(self, key, value):
        self.facts[key] = value
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.facts, indent=2, sort_keys=True), encoding="utf-8")

    def as_text(self):
        if not self.facts:
            return "No facts saved from earlier runs."
        return "Facts saved from earlier runs: " + json.dumps(self.facts, sort_keys=True)
