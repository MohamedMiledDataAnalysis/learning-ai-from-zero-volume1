# The Corner Shop agent with a real language model. From the repository root:
#   Rscript r/vol1/ch30/shop_agent_live.R --mode replay   (default; also live, record, rules)
source("r/agentcore/loop.R")
source("r/agentcore/brains.R")
source("r/vol1/ch29/shop_tools.R")
source("r/vol1/ch29/shop_rules.R")

QUESTION <- "How much do 3 apples and 2 loaves of bread cost, in euros?"
RECORDING <- file.path("r", "recordings", "vol1-ch30-shop.jsonl")

args <- commandArgs(trailingOnly = TRUE)
mode <- if (length(args) >= 2 && args[1] == "--mode") args[2] else "replay"

if (mode == "replay" && !(file.exists(RECORDING) && file.size(RECORDING) > 0)) {
  cat("[Recording pending: run python record_all.py with Ollama installed, then rebuild]\n")
  quit(status = 0)
}

brain <- make_brain(mode, RECORDING, rules = shop_rules)   # the only line that differs from chapter 29
result <- run_agent(QUESTION, brain, SCHEMAS, call_tool, SYSTEM_PROMPT, max_steps = 10)
cat("Answer: ", result$answer, "\n", sep = "")
cat("Stopped because: ", result$stopped_because, "\n", sep = "")
