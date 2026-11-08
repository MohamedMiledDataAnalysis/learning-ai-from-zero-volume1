"""Chapter 25, question 10. Usage: python python/vol1/ch25/check_ch25.py <cost in pounds of 2,500 questions>
Example prices of section 25.6: £2.00 per million input tokens, £8.00 per million output tokens;
each question sends 3,918 input tokens and receives 300 output tokens."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from part45_common import grade  # noqa: E402
cost = 2500 * (3918 * 2.00 + 300 * 8.00) / 1_000_000
grade(sys.argv[1:], [("10", round(cost, 2), 0.005, "25.6")])
