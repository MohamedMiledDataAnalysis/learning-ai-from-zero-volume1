"""Print the first request the agent sends to Ollama, without sending it.

    python python/vol1/ch30/show_request.py
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "ch29"))

from shop_tools import SCHEMAS, SYSTEM_PROMPT   # noqa: E402

request = {
    "model": "qwen2.5:7b",
    "messages": [{"role": "system", "content": SYSTEM_PROMPT},
                 {"role": "user", "content": "How much do 3 apples and 2 loaves of bread cost, in euros?"}],
    "tools": SCHEMAS[:1] + ["... 3 more tool descriptions ..."],
    "options": {"temperature": 0, "seed": 42, "num_ctx": 8192},
    "stream": False,
}
print(json.dumps(request, indent=2, ensure_ascii=False))
