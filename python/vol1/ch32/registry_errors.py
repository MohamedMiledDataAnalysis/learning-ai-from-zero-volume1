"""The finance agent's registry (Volume 2) answering one good call and four bad ones.

    python python/vol1/ch32/registry_errors.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tar_agent.registry import call_tool, tool_schemas   # noqa: E402

print("Tools described to the model:", ", ".join(s["function"]["name"] for s in tool_schemas()))
good = json.loads(call_tool("run_trigger_tests", {"period": 10}))
print("run_trigger_tests(period=10) -> keys:", ", ".join(good))
for name, args in [("run_trigger_test", {"period": 10}), ("run_trigger_tests", {"month": 10}),
                   ("run_trigger_tests", {"period": 13}), ("run_trigger_tests", "{period: 10}")]:
    shown = args if isinstance(args, str) else json.dumps(args)
    print(f"{name}({shown})\n   -> {call_tool(name, args)}")
