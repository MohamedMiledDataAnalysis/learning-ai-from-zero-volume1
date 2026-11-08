# The same question answered by a workflow (steps fixed in code) and by an agent. From the repository root:
#   Rscript r/vol1/ch34/workflow_vs_agent.R
source("r/agentcore/loop.R")
source("r/agentcore/brains.R")
source("r/vol1/ch29/shop_tools.R")
source("r/vol1/ch29/shop_rules.R")

shop_workflow <- function(basket) {          # a workflow: the programmer wrote the order of the steps
  total <- 0
  for (item in names(basket)) {
    total <- add(total, multiply(basket[[item]], get_price(item)$price_gbp)$result)$result
  }
  gbp_to_eur(total)$amount_eur
}

cat("WORKFLOW (steps fixed in code)\n")
cat(sprintf("  3 apples + 2 loaves of bread: €%.2f\n", shop_workflow(list(apple = 3, `loaf of bread` = 2))))
cat(sprintf("  1 milk + 2 cheese:            €%.2f\n", shop_workflow(list(milk = 1, cheese = 2))))
cat("AGENT (steps chosen by the brain at each turn)\n")
out <- run_agent("How much do 3 apples and 2 loaves of bread cost, in euros?", rule_brain(shop_rules),
                 SCHEMAS, call_tool, SYSTEM_PROMPT, log = function(m) NULL)
cat("  ", out$answer, "\n", sep = "")
cat("  Steps chosen:", paste(vapply(Filter(function(s) s$type == "tool", out$steps), `[[`, "", "name"), collapse = ", "), "\n")
