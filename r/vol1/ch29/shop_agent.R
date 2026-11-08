# Run the Corner Shop agent with the fake brain. From the repository root:
#   Rscript r/vol1/ch29/shop_agent.R
source("r/agentcore/loop.R")
source("r/agentcore/brains.R")
source("r/vol1/ch29/shop_tools.R")
source("r/vol1/ch29/shop_rules.R")

QUESTION <- "How much do 3 apples and 2 loaves of bread cost, in euros?"

result <- run_agent(QUESTION, rule_brain(shop_rules), SCHEMAS, call_tool, SYSTEM_PROMPT, max_steps = 10)
cat("Answer: ", result$answer, "\n", sep = "")
cat("Stopped because: ", result$stopped_because, "\n", sep = "")
cat("Messages in memory: ", length(result$memory), "\n", sep = "")
