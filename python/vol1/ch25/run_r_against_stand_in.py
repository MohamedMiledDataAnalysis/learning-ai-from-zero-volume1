"""Chapter 25 — run the R client against the book's Ollama stand-in, so the output is the same everywhere."""

import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "python"))
from agent_core import fake_ollama  # noqa: E402

server, url, received = fake_ollama.start([{"content": "The 90+ day arrears ratio limit is 1.25% (prospectus, page 9)."}])
out = subprocess.run(["Rscript", "r/vol1/ch25/ollama_chat.R"], cwd=REPO, capture_output=True, text=True,
                     env={**os.environ, "OLLAMA_HOST": url})
server.shutdown()
print(out.stdout.strip() or out.stderr)
print("Model requested by R:", received[0]["model"], "| options:", received[0]["options"])
