"""Chapter 24, question 10. Usage: python python/vol1/ch24/check_ch24.py <messages in prompt 3> <roles in prompt 3, e.g. system,user,assistant,user>"""
import sys
from pathlib import Path
sys.path[:0] = [str(Path(__file__).resolve().parents[1]), str(Path(__file__).resolve().parent)]
from part45_common import grade  # noqa: E402
from prompts import PROMPTS  # noqa: E402
p = PROMPTS["3-few-shot"]
grade(sys.argv[1:], [("10a", len(p), 0, "24.3"), ("10b", ",".join(m["role"] for m in p), None, "24.3")])
