# Short-term memory size and trimming; long-term memory over two runs. From the repository root:
#   Rscript r/vol1/ch33/demo_memory.R
source("r/agentcore/loop.R")
source("r/agentcore/brains.R")
source("r/vol1/ch29/shop_tools.R")
source("r/vol1/ch29/shop_rules.R")
source("r/vol1/ch33/memory_tools.R")

GOAL <- "How much do 3 apples and 2 loaves of bread cost, in euros?"
quiet <- function(m) NULL

memory <- run_agent(GOAL, rule_brain(shop_rules), SCHEMAS, call_tool, SYSTEM_PROMPT, log = quiet)$memory
cat("PART 1 — SHORT-TERM MEMORY\n")
cat(sprintf("Messages: %d, estimated tokens: %d\n", length(memory), memory_size(memory)))
trimmed <- trim_memory(memory, keep_last_turns = 2)
cat(sprintf("Trimmed to the last 2 turns: %d messages, %d tokens\n", length(trimmed), memory_size(trimmed)))

# The brain skips get_price for any price it already knows from the system prompt.
remembering_rules <- function(memory) {
  marker <- "Facts saved from earlier runs: "
  system <- memory[[1]]$content
  prices <- if (grepl(marker, system, fixed = TRUE)) fromJSON(strsplit(system, marker, fixed = TRUE)[[1]][2]) else list()
  for (m in Filter(function(m) m$role == "tool" && m$tool_name == "get_price", memory)) {
    r <- fromJSON(m$content); prices[[r$item]] <- r$price_gbp
  }
  for (item in c("apple", "loaf of bread")) if (is.null(prices[[item]])) return(call("get_price", item = item))
  results <- lapply(Filter(function(m) m$role == "tool" && m$tool_name != "get_price", memory), function(m) fromJSON(m$content))
  n <- length(results)
  if (n == 0) return(call("multiply", a = 3, b = prices[["apple"]]))
  if (n == 1) return(call("multiply", a = 2, b = prices[["loaf of bread"]]))
  if (n == 2) return(call("add", a = results[[1]]$result, b = results[[2]]$result))
  if (n == 3) return(call("gbp_to_eur", amount = results[[3]]$result))
  list(content = sprintf("3 apples and 2 loaves of bread cost €%.2f.", results[[4]]$amount_eur), tool_calls = list())
}

cat("\nPART 2 — LONG-TERM MEMORY\n")
path <- tempfile(fileext = ".json")
for (run in 1:2) {
  store <- long_term_memory(path)                       # read the file again, as a new run would
  out <- run_agent(GOAL, rule_brain(remembering_rules), SCHEMAS, call_tool,
                   paste(SYSTEM_PROMPT, store$as_text()), log = quiet)
  tools <- vapply(Filter(function(s) s$type == "tool", out$steps), `[[`, "", "name")
  cat(sprintf("Run %d: %d tool calls (%s)\n       %s\n", run, length(tools), paste(tools, collapse = ", "), out$answer))
  for (s in Filter(function(s) s$type == "tool" && s$name == "get_price", out$steps)) {
    r <- fromJSON(s$result); store$remember(r$item, r$price_gbp)
  }
}
cat("Saved facts:", to_json(long_term_memory(path)$facts()), "\n")
