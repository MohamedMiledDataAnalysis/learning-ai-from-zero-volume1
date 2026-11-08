# Global assessment, Part F — your Library agent (R). Copy this file and fill in every TODO.
#   cp r/vol1/global_assessment/library_starter.R r/vol1/global_assessment/library_agent.R
#   Rscript r/vol1/global_assessment/grade_library.R r/vol1/global_assessment/library_agent.R
#
# Data: data/learning/library/books.csv (book_id, title, author, due_date) and rules.json.
# What each part must return (the grader checks these exact names):
#   find_book(title)            -> list(book_id, title, author, due_date)  or  list(error = "...")
#   days_late(book_id, on_date) -> list(book_id, days_late)   (0 when the book is not late)
#   fine(days)                  -> list(days, fine_gbp)       (20p a day, never more than £5.00)
#   SCHEMAS                     -> one schema per tool, with its required arguments
#   call_tool(name, arguments)  -> JSON text; an unknown tool gives {"error": ...} as text
#   run_library(question, log)  -> the final answer text
# The grader loads r/agentcore/loop.R and r/agentcore/brains.R before this file.
library(jsonlite)

LIBRARY <- file.path("data", "learning", "library")
BOOKS <- read.csv(file.path(LIBRARY, "books.csv"), stringsAsFactors = FALSE)
RULES <- fromJSON(file.path(LIBRARY, "rules.json"))

find_book <- function(title) stop("TODO: find the book whose title matches, ignoring case")
days_late <- function(book_id, on_date) stop("TODO: days between due_date and on_date, never below 0")
fine <- function(days) stop("TODO: fine_per_day_gbp x days, capped at maximum_fine_gbp")
SCHEMAS <- list()   # TODO: three schemas, as in chapter 29
SYSTEM_PROMPT <- "TODO"
call_tool <- function(name, arguments) stop("TODO: run the tool, return JSON text, errors as text")
library_rules <- function(memory) stop("TODO: find_book, then days_late, then fine, then answer")
run_library <- function(question, log = function(msg) cat(msg, "\n", sep = "")) stop("TODO: run_agent with a step limit")
