"""Build Volume 1's glossary appendix (book/vol1/appendix-glossary.md) from book/glossary/vol1-*.tsv.

    python python/vol1/build_glossary.py

The work is done by python/vol2/build_glossary.py, shared by both volumes.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "vol2"))
from build_glossary import build  # noqa: E402

build("vol1")
