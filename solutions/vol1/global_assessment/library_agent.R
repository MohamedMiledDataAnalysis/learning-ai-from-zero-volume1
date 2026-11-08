# Reference solution — global assessment, Part F: the Library agent (R).
# From the repository root:
#   Rscript r/vol1/global_assessment/grade_library.R solutions/vol1/global_assessment/library_agent.R
# The grader sources r/agentcore/loop.R and r/agentcore/brains.R before this file.
library(jsonlite)

LIBRARY <- file.path("data", "learning", "library")
BOOKS <- read.csv(file.path(LIBRARY, "books.csv"), stringsAsFactors = FALSE)
RULES <- fromJSON(file.path(LIBRARY, "rules.json"))

# Part 3 — tools.
find_book <- function(title) {
  row <- BOOKS[tolower(BOOKS$title) == tolower(trimws(title)), ]
  if (nrow(row) == 0) return(list(error = sprintf("no book titled '%s'", title)))
  list(book_id = row$book_id, title = row$title, author = row$author, due_date = row$due_date)
}

days_late <- function(book_id, on_date) {
  row <- BOOKS[BOOKS$book_id == book_id, ]
  if (nrow(row) == 0) return(list(error = sprintf("unknown book_id '%s'", book_id)))
  late <- as.integer(as.Date(on_date) - as.Date(row$due_date))
  list(book_id = book_id, days_late = max(late, 0L))
}

fine <- function(days) {
  amount <- min(days * RULES$fine_per_day_gbp, RULES$maximum_fine_gbp)
  list(days = days, fine_gbp = round(amount, 2))
}

TOOLS <- list(find_book = find_book, days_late = days_late, fine = fine)

tool_schema <- function(name, description, properties, required) {
  list(type = "function", `function` = list(name = name, description = description,
       parameters = list(type = "object", properties = properties, required = as.list(required))))
}
SCHEMAS <- list(
  tool_schema("find_book", "Find a library book by its exact title.", list(title = list(type = "string")), "title"),
  tool_schema("days_late", "Days a book is late on a date (YYYY-MM-DD); 0 if not late.",
              list(book_id = list(type = "string"), on_date = list(type = "string")), c("book_id", "on_date")),
  tool_schema("fine", "The fine in pounds for a number of days late.", list(days = list(type = "integer")), "days")
)

# Part 1 — goal and instructions.
SYSTEM_PROMPT <- "You are the library assistant. Use the tools for every date and amount; never guess. Answer in one sentence."

# Part 4 — controller side: run one tool, return JSON text, errors included (Part 7 — guardrail).
call_tool <- function(name, arguments) {
  if (!name %in% names(TOOLS)) {
    return(to_json(list(error = sprintf("unknown tool '%s'. Available tools: %s", name,
                                        paste(sort(names(TOOLS)), collapse = ", ")))))
  }
  result <- tryCatch(do.call(TOOLS[[name]], arguments),
                     error = function(e) list(error = sprintf("wrong arguments for %s: %s", name, conditionMessage(e))))
  to_json(result)
}

call <- function(name, ...) list(content = "", tool_calls = list(list(name = name, arguments = list(...))))

# Part 2 — the brain (rules), reading the question and the tool results in memory (Part 5).
library_rules <- function(memory) {
  question <- Filter(function(m) m$role == "user", memory)[[1]]$content
  title <- sub(".*'([^']+)'.*", "\\1", question)
  on_date <- regmatches(question, regexpr("[0-9]{4}-[0-9]{2}-[0-9]{2}", question))
  results <- lapply(Filter(function(m) m$role == "tool", memory), function(m) fromJSON(m$content))
  n <- length(results)
  if (n == 0) return(call("find_book", title = title))
  if (!is.null(results[[n]]$error)) {                       # Part 6 — stop on an error, do not guess
    return(list(content = sprintf("I cannot answer: %s.", results[[n]]$error), tool_calls = list()))
  }
  if (n == 1) return(call("days_late", book_id = results[[1]]$book_id, on_date = on_date))
  if (n == 2) return(call("fine", days = results[[2]]$days_late))
  list(content = sprintf("The fine for '%s' on %s is £%.2f (%d days late).", results[[1]]$title, on_date,
                         results[[3]]$fine_gbp, results[[2]]$days_late), tool_calls = list())
}

# Part 6 — stopping rule: at most 6 steps. Part 8 — log: every step is printed.
run_library <- function(question, log = function(msg) cat(msg, "\n", sep = "")) {
  run_agent(question, rule_brain(library_rules), SCHEMAS, call_tool, SYSTEM_PROMPT, max_steps = 6, log = log)$answer
}
