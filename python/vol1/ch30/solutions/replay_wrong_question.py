"""Exercise 30.5: replay a recording for a different question. What happens?

    python python/vol1/ch30/solutions/replay_wrong_question.py
"""

import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parents[1] / "ch29"), str(HERE.parents[2])]

from agent_core.brains import RecordingBrain, ReplayBrain, RuleBrain   # noqa: E402
from agent_core.loop import run_agent                                  # noqa: E402
from shop_rules import shop_rules                                      # noqa: E402
from shop_tools import SCHEMAS, SYSTEM_PROMPT, call_tool               # noqa: E402

quiet = lambda m: None                                                  # noqa: E731
with tempfile.TemporaryDirectory() as folder:
    path = Path(folder) / "apples.jsonl"
    run_agent("How much do 3 apples and 2 loaves of bread cost, in euros?",
              RecordingBrain(RuleBrain(shop_rules), path), SCHEMAS, call_tool, SYSTEM_PROMPT, log=quiet)
    out = run_agent("How much does 1 milk cost, in euros?", ReplayBrain(path), SCHEMAS, call_tool,
                    SYSTEM_PROMPT, log=quiet)
    print("Question asked: How much does 1 milk cost, in euros?")
    print("Replayed answer:", out["answer"])
