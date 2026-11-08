# The whole Corner Shop agent in one file, with its eight pieces labelled.
#
#   Rscript r/vol1/ch28/agent_8_pieces.R                  the rule brain (no AI, always the same)
#   Rscript r/vol1/ch28/agent_8_pieces.R --mode live      a real model (needs Ollama and qwen2.5:7b)
#   Rscript r/vol1/ch28/agent_8_pieces.R --mode inventing a brain that invents a price (piece 7 at work)
#
# Run it from the repository folder.
library(jsonlite)

DATA <- file.path("data", "learning", "corner_shop")

# Write a list as JSON text exactly as Python's json.dumps does, so both languages print the same log.
as_json <- function(x) {
  show <- function(v) if (is.character(v)) paste0('"', v, '"') else as.character(v)
  paste0("{", paste0('"', names(x), '": ', vapply(x, show, ""), collapse = ", "), "}")
}

# ── PIECE 1 — GOAL AND INSTRUCTIONS ── (the flight plan)
GOAL <- "How much do 3 apples and 2 loaves of bread cost, in euros?"
INSTRUCTIONS <- paste("You are the Corner Shop assistant. Always use the tools for prices and arithmetic;",
                      "never guess a number. Give the final answer in one sentence.")

# ── PIECE 3 — TOOLS and their descriptions ── (the labelled controls)
prices <- read.csv(file.path(DATA, "prices.csv"), stringsAsFactors = FALSE)
PRICES <- setNames(prices$price_gbp, prices$item)
RATE <- fromJSON(file.path(DATA, "exchange_rate.json"))$rate

TOOLS <- list(
  get_price  = function(item) list(item = item, price_gbp = unname(PRICES[item])),
  multiply   = function(a, b) list(result = round(a * b, 2)),
  add        = function(a, b) list(result = round(a + b, 2)),
  gbp_to_eur = function(amount) list(amount_eur = round(amount * RATE, 2))
)
describe <- function(name, description, properties) {   # what the model reads to know a tool exists
  list(type = "function", `function` = list(name = name, description = description,
       parameters = list(type = "object", properties = properties)))
}
num <- list(type = "number")
DESCRIPTIONS <- list(
  describe("get_price", "Price in pounds of one item.", list(item = list(type = "string"))),
  describe("multiply", "Multiply two numbers.", list(a = num, b = num)),
  describe("add", "Add two numbers.", list(a = num, b = num)),
  describe("gbp_to_eur", "Convert pounds to euros.", list(amount = num))
)

# ── PIECE 2 — AI MODEL ── (the pilot)
ask <- function(name, ...) list(content = "", tool_calls = list(list(name = name, arguments = list(...))))

rule_brain <- function(memory) {
  # A stand-in for the model: fixed rules, so the run is always the same. Chapter 29 explains it.
  results <- lapply(Filter(function(m) m$role == "tool", memory), function(m) fromJSON(m$content))
  n <- length(results)                                   # how many tools have run so far
  if (n == 0) return(ask("get_price", item = "apple"))
  if (n == 1) return(ask("get_price", item = "loaf of bread"))
  if (n == 2) return(ask("multiply", a = 3, b = results[[1]]$price_gbp))
  if (n == 3) return(ask("multiply", a = 2, b = results[[2]]$price_gbp))
  if (n == 4) return(ask("add", a = results[[3]]$result, b = results[[4]]$result))
  if (n == 5) return(ask("gbp_to_eur", amount = results[[5]]$result))
  list(content = sprintf("3 apples and 2 loaves of bread cost €%.2f.", results[[6]]$amount_eur),
       tool_calls = list())
}

inventing_brain <- function(memory) {
  # A faulty brain that skips the price list and invents £0.50 for an apple.
  if (!any(vapply(memory, function(m) m$role == "tool", TRUE))) return(ask("multiply", a = 3, b = 0.50))
  list(content = "I could not finish.", tool_calls = list())
}

ollama_brain <- function(memory) {
  # A real language model on your computer. Swapping the brain is the only change.
  body <- list(model = "qwen2.5:7b", messages = memory, tools = DESCRIPTIONS, stream = FALSE,
               options = list(temperature = 0, seed = 42, num_ctx = 8192))
  reply <- httr2::request(paste0(Sys.getenv("OLLAMA_HOST", "http://localhost:11434"), "/api/chat")) |>
    httr2::req_body_json(body, auto_unbox = TRUE) |> httr2::req_perform() |>
    httr2::resp_body_json()
  calls <- lapply(reply$message$tool_calls, function(c) list(name = c$`function`$name,
                                                              arguments = c$`function`$arguments))
  list(content = if (is.null(reply$message$content)) "" else reply$message$content, tool_calls = calls)
}

# ── PIECE 7 — GUARDRAIL ── (the checklists)
guardrail <- function(name, arguments, memory) {
  # Refuse any number that the goal or an earlier tool result did not contain.
  seen <- c(3, 2)                                        # the quantities in the goal
  for (m in memory) if (m$role == "tool") seen <- c(seen, unlist(Filter(is.numeric, fromJSON(m$content))))
  invented <- unlist(Filter(function(v) is.numeric(v) && !(v %in% seen), arguments))
  if (length(invented)) sprintf("blocked: [%s] did not come from the goal or a tool",
                                paste(invented, collapse = ", ")) else NULL
}

# ── PIECE 8 — LOG ── (the black box)
log_step <- function(step, text) cat(sprintf("[8 LOG] step %d  %s\n", step, text))

# ── PIECE 4 — CONTROLLER LOOP ── (fly-by-wire)
run <- function(brain, max_steps) {
  # ── PIECE 5 — MEMORY ── (the flight log)
  memory <- list(list(role = "system", content = INSTRUCTIONS), list(role = "user", content = GOAL))
  for (step in seq_len(max_steps)) {
    reply <- brain(memory)                                       # the pilot decides
    memory[[length(memory) + 1]] <- list(role = "assistant", content = reply$content,
                                         tool_calls = lapply(reply$tool_calls, function(c) list(`function` = c)))
    # ── PIECE 6 — STOPPING RULES ── (landing)
    if (length(reply$tool_calls) == 0) {
      log_step(step, paste("[6 STOP] final answer:", reply$content))
      return(reply$content)
    }
    for (call in reply$tool_calls) {
      refusal <- guardrail(call$name, call$arguments, memory)
      result <- if (is.null(refusal)) do.call(TOOLS[[call$name]], call$arguments) else list(error = refusal)
      memory[[length(memory) + 1]] <- list(role = "tool", content = as_json(result))
      shown <- paste(vapply(call$arguments, function(v) if (is.character(v)) paste0('"', v, '"')
                            else as.character(v), ""), collapse = ", ")
      log_step(step, sprintf("[2 MODEL] asks %s(%s)  %s  [5 MEMORY] %d messages", call$name, shown,
                             if (is.null(refusal)) paste("[3 TOOL] ->", as_json(result))
                             else paste("[7 GUARD]", refusal), length(memory)))
    }
  }
  log_step(max_steps, sprintf("[6 STOP] step limit of %d reached: no answer", max_steps))
  NULL
}

args <- commandArgs(trailingOnly = TRUE)
mode <- if ("--mode" %in% args) args[which(args == "--mode") + 1] else "rules"
brain <- switch(mode, rules = rule_brain, live = ollama_brain, inventing = inventing_brain)
invisible(run(brain, max_steps = 10))
