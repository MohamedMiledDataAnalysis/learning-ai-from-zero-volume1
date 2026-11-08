# Run the four failures without guardrails, then with them. From the repository root:
#   Rscript r/vol1/ch31/demo_failures.R
source("r/agentcore/loop.R")
source("r/agentcore/brains.R")
source("r/vol1/ch29/shop_tools.R")
source("r/vol1/ch29/shop_rules.R")
source("r/vol1/ch31/broken_brains.R")
source("r/vol1/ch31/guardrails.R")

GOAL <- "How much do 3 apples and 2 loaves of bread cost, in euros?"
show <- function(title, brain, tools = call_tool, max_steps = 10) {
  out <- run_agent(GOAL, brain, SCHEMAS, tools, SYSTEM_PROMPT, max_steps = max_steps, log = function(m) NULL)
  n <- sum(vapply(out$steps, function(s) s$type == "tool", logical(1)))
  answer <- if (is.null(out$answer)) "NULL" else out$answer
  cat(sprintf("%-42s %2d %s | %s\n    answer: %s\n", title, n, if (n == 1) "tool call " else "tool calls", out$stopped_because, answer))
}

cat("WITHOUT GUARDRAILS\n")
show("1. Misspelt item", rule_brain(misspelling_brain))
show("2. Missing tool", rule_brain(missing_tool_brain))
show("3. Never-ending loop (step limit 10)", rule_brain(looping_brain))
show("4. Invented price", rule_brain(inventing_brain))
cat("\nWITH GUARDRAILS\n")
show("0. Correct brain (guardrails stay silent)", guarded_brain(rule_brain(shop_rules), allowed_numbers = c(3, 2)))
show("1. Misspelt item + suggestion", rule_brain(misspelling_brain), tools = call_tool_with_suggestions)
show("3. Never-ending loop + repeat guard", guarded_brain(rule_brain(looping_brain)))
show("4. Invented price + argument check", guarded_brain(rule_brain(inventing_brain), allowed_numbers = c(3, 2)))
