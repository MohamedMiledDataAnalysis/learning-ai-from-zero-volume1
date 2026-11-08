"""Chapter 2 — check that your computer has everything the book needs.

Run it from the repository folder:

    python python/vol1/ch02/check_ch02.py

Each line says OK or MISSING. Fix every MISSING line, then run the script again.
"""

import importlib.metadata
import shutil
import subprocess
import sys
from pathlib import Path

ok = True


def report(passed, what, fix=""):
    global ok
    ok = ok and passed
    print(f"{'OK     ' if passed else 'MISSING'}  {what}" + ("" if passed else f"  ->  {fix}"))


# 1. Python itself
report(sys.version_info >= (3, 13), f"Python {sys.version.split()[0]} (3.13 or later needed)",
       "install Python 3.13 from python.org (Section 2.2)")

# 2. Python packages, at the exact versions listed in requirements.txt
repo = Path(__file__).resolve().parents[3]
for line in (repo / "requirements.txt").read_text(encoding="utf-8").split("\n"):
    if "==" not in line or line.startswith("#"):
        continue
    name, version = line.strip().split("==")
    try:
        have = importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        have = "not installed"
    report(have == version, f"Python package {name} {version}",
           f"you have {have}; run: pip install -r requirements.txt (Section 2.5)")

# 3. Programs the book calls from the command line
for program, section in [("git", "2.4"), ("Rscript", "2.3"), ("ollama", "2.6")]:
    report(shutil.which(program) is not None, f"program {program}", f"install it (Section {section})")

# 4. The repository's data
for name in ["data/loan_tape_cutoff.csv", "data/loan_performance.csv", "data/prospectus/prospectus.pdf"]:
    report((repo / name).exists(), f"file {name}", "clone the repository again (Section 2.4)")

# 5. The pinned language model (only if Ollama is installed)
if shutil.which("ollama"):
    listed = subprocess.run(["ollama", "list"], capture_output=True, text=True).stdout
    report("qwen2.5:7b" in listed, "model qwen2.5:7b in Ollama", "run: ollama pull qwen2.5:7b (Section 2.6)")

print()
print("Everything is ready." if ok else "Fix the MISSING lines, then run this script again.")
