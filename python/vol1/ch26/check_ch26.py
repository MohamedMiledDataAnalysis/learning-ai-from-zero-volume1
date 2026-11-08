"""Chapter 26, question 10. Usage: python python/vol1/ch26/check_ch26.py reply.json
Save a reply that is valid for the chapter's schema in a file (for example reply.json): it must report the
90+ day arrears ratio test of period 12, with its value as a ratio and whether the limit was breached.
A reply typed directly as one argument in quotes is also accepted."""
import sys
from pathlib import Path
sys.path[:0] = [str(Path(__file__).resolve().parents[1]), str(Path(__file__).resolve().parent)]
from validate_reply import validate  # noqa: E402

if len(sys.argv) != 2:
    raise SystemExit("Save your JSON reply in a file, for example reply.json, and run:\n"
                     "  python python/vol1/ch26/check_ch26.py reply.json")
arg = sys.argv[1]
text = Path(arg).read_text(encoding="utf-8") if Path(arg).is_file() else arg
data, problems = validate(text)
ok = (not problems and data["period"] == 12 and data["test"] == "arrears_90_ratio"
      and abs(data["value"] - 0.016403) < 0.0000005 and data["breached"] is True)
print("10: correct" if ok else f"10: not correct - {'; '.join(problems) or 'valid, but the values are wrong'}"
      " - reread section 26.3")
print(f"Practical task: {int(ok)}/1")
