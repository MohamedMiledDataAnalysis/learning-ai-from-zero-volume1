"""Tests for Volume 1, Parts IV and V (chapters 21-27): the figures quoted in the text."""

import os
import subprocess
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
for sub in ["python/vol1", "python/vol1/ch21", "python/vol1/ch26", "python/vol1/ch27"]:
    sys.path.insert(0, str(REPO / sub))

from bpe_tokenizer import N_MERGES, tokenize, tokenize_word, train_bpe  # noqa: E402
from part45_common import PENDING, prospectus_text, words  # noqa: E402


def run(*cmd, env=None):
    cmd = [sys.executable if c == "python" else c for c in cmd]
    r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, env=env)
    assert r.returncode == 0, r.stderr
    return r.stdout


@pytest.fixture(scope="module")
def merges():
    return train_bpe(Counter(words(prospectus_text())), N_MERGES)


def test_ch21_bpe(merges):
    assert merges[:3] == [("e", "_"), ("s", "_"), ("t", "h")]
    assert tokenize_word("arrears", merges) == ["ar", "re", "ar", "s_"]
    assert len(tokenize(prospectus_text(), merges)) == 3868
    assert sum(Counter(words(prospectus_text())).values()) == 1876


def test_ch21_word_vectors():
    out = run("python", "python/vol1/ch21/word_vectors.py")
    assert "Closest to 'reserve': fund (0.99)" in out
    assert "91 words" in out


def test_ch22_attention_weights():
    out = run("python", "python/vol1/ch22/attention.py")
    assert "[0.401 0.198 0.401]" in out and "[0.284 0.14  0.576]" in out
    x = np.array([0.707, 0.0, 0.707])            # the hand calculation of section 22.3, row 1
    w = np.exp(x) / np.exp(x).sum()
    assert np.round(w, 3).tolist() == [0.401, 0.198, 0.401]


def test_ch23_temperature_and_context():
    out = run("python", "python/vol1/ch23/temperature.py")
    assert "t = 2.0: exceed 0.394" in out
    out = run("python", "python/vol1/ch23/context_window.py")
    assert "461,181 tokens  does NOT fit" in out


def test_ch24_and_ch27_replay_without_recordings_prints_one_line():
    for script in [["python/vol1/ch24/prompts.py", "ask"], ["python/vol1/ch27/ollama_embeddings.py"]]:
        if not (REPO / "python/recordings/vol1-ch27-ollama-embeddings.json").exists():
            out = run("python", *script)
            assert out.strip() == PENDING


def test_ch25_python_and_r_against_the_stand_in():
    out = run("python", "python/vol1/ch25/http_by_hand.py")
    assert "Status code   : 200" in out and "Requests the server received: 2" in out
    out = run("python", "python/vol1/ch25/run_r_against_stand_in.py")
    assert out.startswith("Reply: The 90+ day arrears ratio limit is 1.25%")
    assert "options: {'temperature': 0, 'seed': 42, 'num_ctx': 8192}" in out


def test_ch26_validation_python_and_r_agree():
    from validate_reply import REPLIES, validate
    verdicts = {k: not validate(v)[1] for k, v in REPLIES.items()}
    assert verdicts == {"A clean": True, "B fenced": True, "C percent": False, "D missing": False, "E broken": False}
    out = run("Rscript", "r/vol1/ch26/validate_reply.R")
    r_verdicts = {line[6:16].strip(): line.endswith("VALID") and "INVALID" not in line for line in out.splitlines()}
    assert r_verdicts == verdicts
    assert "Attempt 2: valid" in run("python", "python/vol1/ch26/retry.py")


def test_ch27_stemming_finds_page_7_and_lsa_does_not():
    out = run("python", "python/vol1/ch27/compare_search.py")
    assert "1. BM25, exact words: missed" in out
    assert "2. BM25 with stemming: FOUND" in out
    assert "(LSA, 20 dimensions): missed" in out
    assert "words the LSA vectors have never seen: ['were', 'eligible']" in out


def test_ch27_two_searches_retrieve_the_consequence_and_eval_rates():
    out = run("python", "python/vol1/ch27/rag_prompt.py", "show")
    assert "principal is paid sequentially" not in out          # one search misses the consequence
    assert "Consequence passage included: yes" in run("python", "python/vol1/ch27/rag_prompt.py", "split")
    out = run("python", "python/vol1/ch27/retrieval_eval.py")
    assert "exact words 7/8 = 88%, stemmed 8/8 = 100%" in out


def test_self_check_scripts_accept_the_printed_answers():
    cases = [
        (["python/vol1/ch21/check_ch21.py", "8", "9411"], "2/2"),
        (["python/vol1/ch22/check_ch22.py", "0.503", "1.503"], "2/2"),
        (["python/vol1/ch23/check_ch23.py", "0.903", "0.006"], "2/2"),
        (["python/vol1/ch24/check_ch24.py", "4", "system,user,assistant,user"], "2/2"),
        (["python/vol1/ch25/check_ch25.py", "25.59"], "1/1"),
        (["python/vol1/ch26/check_ch26.py",
          '{"period": 12, "test": "arrears_90_ratio", "value": 0.016403, "breached": true}'], "1/1"),
        (["python/vol1/ch27/check_ch27.py", "elig", "8"], "2/2"),
    ]
    for args, score in cases:
        assert f"Practical task: {score}" in run("python", *args), args
