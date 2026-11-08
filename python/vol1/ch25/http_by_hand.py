"""Chapter 25 — one request to the Ollama API, first by hand, then with the ollama package.

So that this script gives the same output on every computer, it talks to the
book's test stand-in (python/agent_core/fake_ollama.py), which answers in
Ollama's exact format with a fixed reply. Change URL to http://localhost:11434
to talk to your real Ollama.
"""

import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agent_core import fake_ollama  # noqa: E402

# The stand-in's fixed reply (not written by a model):
script = [{"content": "The 90+ day arrears ratio limit is 1.25% (prospectus, page 9)."}] * 2
server, URL, received = fake_ollama.start(script)

# ---- 1. By hand: build the JSON body and POST it to /api/chat
body = {
    "model": "qwen2.5:7b",
    "messages": [{"role": "user", "content": "What is the 90+ day arrears ratio limit?"}],
    "options": {"temperature": 0, "seed": 42, "num_ctx": 8192},
    "stream": False,
}
request = urllib.request.Request(URL + "/api/chat", data=json.dumps(body).encode("utf-8"),
                                 headers={"Content-Type": "application/json"}, method="POST")
with urllib.request.urlopen(request) as response:
    status = response.status
    answer = json.loads(response.read())

print("Request sent  : POST /api/chat")
print("Request body  :", json.dumps(body))
print("Status code   :", status)
print("Response keys :", sorted(answer))
print("Reply (stand-in):", answer["message"]["content"])

# ---- 2. The same call with the ollama package, which builds the request for you
import ollama  # noqa: E402

client = ollama.Client(host=URL)
reply = client.chat(model="qwen2.5:7b", messages=body["messages"], options=body["options"])
print("\nSame call with the ollama package (stand-in reply):", reply["message"]["content"])
print("Requests the server received:", len(received))
server.shutdown()
