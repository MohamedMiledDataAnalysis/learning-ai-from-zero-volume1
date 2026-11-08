"""Tests for Volume 1 Part VI: every figure quoted in chapters 28 to 34."""

import json
import subprocess
import sys
from pathlib import Path

VOL1 = Path(__file__).resolve().parents[1] / "vol1"
REPO = VOL1.parents[1]
sys.path[:0] = [str(VOL1 / "ch29"), str(VOL1 / "ch31"), str(VOL1 / "ch32"), str(VOL1 / "ch33")]

from agent_core.brains import RuleBrain                                   # noqa: E402
from agent_core.loop import run_agent                                     # noqa: E402
from broken_brains import inventing_brain, looping_brain, missing_tool_brain, misspelling_brain  # noqa: E402
from guardrails import GuardedBrain, call_tool_with_suggestions           # noqa: E402
from memory_tools import memory_size, summarise_memory, trim_memory       # noqa: E402
from shop_rules import shop_rules                                         # noqa: E402
from shop_tools import SCHEMAS, SYSTEM_PROMPT, call_tool                  # noqa: E402
from validate_args import make_safe_call_tool, validate_arguments         # noqa: E402

GOAL = "How much do 3 apples and 2 loaves of bread cost, in euros?"
quiet = lambda m: None                                                     # noqa: E731


def run(brain, tools=call_tool, max_steps=10):
    return run_agent(GOAL, brain, SCHEMAS, tools, SYSTEM_PROMPT, max_steps=max_steps, log=quiet)


def tool_count(out):
    return sum(1 for s in out["steps"] if s["type"] == "tool")


def script(path, *args):
    r = subprocess.run([sys.executable, path, *args], cwd=REPO, capture_output=True, text=True, check=True)
    return r.stdout


def test_corner_shop_answer_and_memory():
    out = run(RuleBrain(shop_rules))
    assert out["answer"] == "3 apples and 2 loaves of bread cost €4.31."
    assert tool_count(out) == 6 and len(out["steps"]) == 7 and len(out["memory"]) == 15


def test_replay_without_recording_prints_the_pending_line():
    out = script("python/vol1/ch30/shop_agent_live.py")
    expected = "[Recording pending: run python record_all.py with Ollama installed, then rebuild]\n"
    assert out == expected or out.startswith("Answer:")


def test_rules_mode_in_chapter_30_matches_chapter_29():
    assert "€4.31" in script("python/vol1/ch30/shop_agent_live.py", "--mode", "rules")


def test_failures_without_guardrails():
    assert run(RuleBrain(misspelling_brain))["answer"] == "I could not find the price of apples."
    assert run(RuleBrain(missing_tool_brain))["answer"] == "£3.75 is €4.31."
    out = run(RuleBrain(looping_brain))
    assert out["stopped_because"] == "step limit" and tool_count(out) == 10
    assert run(RuleBrain(inventing_brain))["answer"] == "3 apples and 2 loaves of bread cost €3.74."


def test_guardrails_fix_each_failure_and_stay_silent_on_a_correct_run():
    assert run(GuardedBrain(RuleBrain(shop_rules), allowed_numbers=(3, 2)))["answer"].endswith("€4.31.")
    assert run(RuleBrain(misspelling_brain), tools=call_tool_with_suggestions)["answer"] == "One apple costs £0.45."
    out = run(GuardedBrain(RuleBrain(looping_brain)))
    assert tool_count(out) == 3 and out["answer"].startswith("Stopped by guardrail")
    out = run(GuardedBrain(RuleBrain(inventing_brain), allowed_numbers=(3, 2)))
    assert tool_count(out) == 2 and "add(b=1.9)" in out["answer"]


def test_answer_check_blocks_a_number_no_tool_returned():
    def guessing(memory):
        return {"content": "It costs €5.00.", "tool_calls": []}
    out = run(GuardedBrain(RuleBrain(guessing), allowed_numbers=(3, 2)))
    assert out["answer"].startswith("Answer blocked by guardrail: [5.0]")


def test_argument_validation():
    safe = make_safe_call_tool(SCHEMAS, call_tool)
    assert json.loads(safe("multiply", {"a": 3, "b": 0.45})) == {"result": 1.35}
    assert "missing required argument 'b'" in safe("multiply", {"a": 3})
    assert "must be a number, not bool" in safe("gbp_to_eur", {"amount": True})
    assert len(validate_arguments(SCHEMAS[1], {"b": "x", "c": 1})) == 3


def test_memory_figures():
    memory = run(RuleBrain(shop_rules))["memory"]
    assert memory_size(memory) == 234
    assert len(trim_memory(memory, 2)) == 5 and memory_size(trim_memory(memory, 2)) == 105
    assert len(summarise_memory(memory, 2)) == 6 and memory_size(summarise_memory(memory, 2)) == 168
    assert len(trim_memory(memory, 3)) == 7


def test_long_term_memory_demo():
    out = script("python/vol1/ch33/demo_memory.py")
    assert "Run 1: 6 tool calls" in out and "Run 2: 4 tool calls" in out
    assert 'Saved facts: {"apple": 0.45, "loaf of bread": 1.2}' in out


def test_workflow_figures():
    out = script("python/vol1/ch34/workflow_vs_agent.py")
    assert "€4.31" in out and "€7.53" in out


def test_check_scripts_accept_the_right_answers():
    for ch, answer in [("28", "15"), ("29", "7.99"), ("30", "4"), ("31", "2"), ("32", "3"), ("33", "7"), ("34", "5.92")]:
        assert script(f"python/vol1/ch{ch}/check_ch{ch}.py", answer).startswith("Correct"), ch
    assert script("python/vol1/ch29/check_ch29.py", "8").startswith("Not yet")
