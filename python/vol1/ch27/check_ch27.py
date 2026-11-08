"""Chapter 27, question 10. Usage: python python/vol1/ch27/check_ch27.py <stem of 'eligibility'> <page of the top passage for 'servicer fee'>"""
import sys
from pathlib import Path
sys.path[:0] = [str(Path(__file__).resolve().parents[1]), str(Path(__file__).resolve().parents[2]), str(Path(__file__).resolve().parent)]
from compare_search import stem  # noqa: E402
from part45_common import grade  # noqa: E402
from tar_agent.tools.prospectus import search_prospectus  # noqa: E402
grade(sys.argv[1:], [("10a", stem("eligibility"), None, "27.4"),
                     ("10b", search_prospectus("servicer fee")["results"][0]["page"], 0, "27.3")])
