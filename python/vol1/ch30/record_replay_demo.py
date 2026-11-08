"""Record a run, look inside the recording, then replay it — using the fake brain, so it works without Ollama.

    python python/vol1/ch30/record_replay_demo.py
"""

import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent / "ch29"), str(HERE.parents[1])]

from agent_core.brains import RecordingBrain, ReplayBrain, RuleBrain   # noqa: E402
from agent_core.loop import run_agent                                  # noqa: E402
from shop_rules import shop_rules                                      # noqa: E402
from shop_tools import SCHEMAS, SYSTEM_PROMPT, call_tool               # noqa: E402

QUESTION = "How much do 3 apples and 2 loaves of bread cost, in euros?"
quiet = lambda m: None                                                  # noqa: E731

with tempfile.TemporaryDirectory() as folder:
    path = Path(folder) / "demo.jsonl"
    first = run_agent(QUESTION, RecordingBrain(RuleBrain(shop_rules), path), SCHEMAS, call_tool, SYSTEM_PROMPT, log=quiet)
    lines = path.read_text(encoding="utf-8").splitlines()
    print(f"The recording has {len(lines)} lines, one per brain reply:")
    for number, line in enumerate(lines, start=1):
        print(f"{number}: {line}")
    second = run_agent(QUESTION, ReplayBrain(path), SCHEMAS, call_tool, SYSTEM_PROMPT, log=quiet)
    print("Replayed answer:", second["answer"])
    print("Identical memory in both runs:", first["memory"] == second["memory"])
