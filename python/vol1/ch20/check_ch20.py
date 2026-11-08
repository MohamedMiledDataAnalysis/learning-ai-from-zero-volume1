"""Practical task (chapter 20): fit the straight line to all 12 periods and forecast period 13.
Give the forecast in £m with two decimals."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import json
import numpy as np
from part3_checker import check

files = sorted(pathlib.Path("data/investor_reports").glob("investor_report_2026_*.json"))
b = np.array([json.loads(f.read_text(encoding="utf-8"))["pool"]["closing_balance"] for f in files]) / 1e6
slope, intercept = np.polyfit(np.arange(1, 13), b, 1)
check(round(float(intercept + 13 * slope), 2), 0.005, "§ 20.3", " £m")
