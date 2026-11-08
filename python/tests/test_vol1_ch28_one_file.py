"""Tests for the one-file agent of chapter 28, in Python and in R."""

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from agent_core import fake_ollama

REPO = Path(__file__).resolve().parents[2]
PY = [sys.executable, "python/vol1/ch28/agent_8_pieces.py"]
R = ["Rscript", "r/vol1/ch28/agent_8_pieces.R"]
needs_r = pytest.mark.skipif(shutil.which("Rscript") is None, reason="R is not installed")


def run(cmd, *args, env=None):
    return subprocess.run(cmd + list(args), cwd=REPO, capture_output=True, text=True, env=env, check=True).stdout


def test_rule_brain_reaches_the_answer_in_seven_steps():
    lines = run(PY).splitlines()
    assert len(lines) == 7
    assert lines[-1] == "[8 LOG] step 7  [6 STOP] final answer: 3 apples and 2 loaves of bread cost €4.31."
    assert all(tag in run(PY) for tag in ["[2 MODEL]", "[3 TOOL]", "[5 MEMORY]", "[6 STOP]", "[8 LOG]"])


def test_guardrail_blocks_an_invented_price():
    out = run(PY, "--mode", "inventing")
    assert "[7 GUARD] blocked: [0.5] did not come from the goal or a tool" in out


@needs_r
@pytest.mark.parametrize("mode", ["rules", "inventing"])
def test_r_prints_exactly_what_python_prints(mode):
    assert run(R, "--mode", mode) == run(PY, "--mode", mode)


@pytest.mark.parametrize("cmd", [PY, pytest.param(R, marks=needs_r)], ids=["python", "r"])
def test_live_mode_speaks_to_ollama(cmd):
    script = [{"content": "", "tool_calls": [{"name": "get_price", "arguments": {"item": "apple"}}]},
              {"content": "An apple costs £0.45.", "tool_calls": []}]
    server, url, received = fake_ollama.start(script)
    try:
        out = run(cmd, "--mode", "live", env={**os.environ, "OLLAMA_HOST": url})
    finally:
        server.shutdown()
    assert "[3 TOOL] -> {\"item\": \"apple\", \"price_gbp\": 0.45}" in out
    assert out.strip().endswith("final answer: An apple costs £0.45.")
    assert received[0]["model"] == "qwen2.5:7b" and received[0]["options"]["num_ctx"] == 8192
    assert [t["function"]["name"] for t in received[0]["tools"]] == ["get_price", "multiply", "add", "gbp_to_eur"]
