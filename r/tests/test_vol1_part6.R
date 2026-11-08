# Tests for Volume 1 Part VI (R): the figures quoted in chapters 29 to 34.
library(testthat)
old <- setwd(root)                                   # the scripts read data/ relative to the repository root
source("r/agentcore/loop.R"); source("r/agentcore/brains.R")
source("r/vol1/ch29/shop_tools.R"); source("r/vol1/ch29/shop_rules.R")
source("r/vol1/ch31/broken_brains.R"); source("r/vol1/ch31/guardrails.R")
source("r/vol1/ch32/validate_args.R"); source("r/vol1/ch33/memory_tools.R")
setwd(old)

GOAL <- "How much do 3 apples and 2 loaves of bread cost, in euros?"
run <- function(brain, tools = call_tool) run_agent(GOAL, brain, SCHEMAS, tools, SYSTEM_PROMPT, log = function(m) NULL)
tool_count <- function(out) sum(vapply(out$steps, function(s) s$type == "tool", logical(1)))

test_that("the Corner Shop agent answers in seven steps", {
  out <- run(rule_brain(shop_rules))
  expect_equal(out$answer, "3 apples and 2 loaves of bread cost €4.31.")
  expect_equal(tool_count(out), 6)
  expect_equal(length(out$memory), 15)
})

test_that("failures and guardrails match the Python results", {
  expect_equal(run(rule_brain(missing_tool_brain))$answer, "£3.75 is €4.31.")
  expect_equal(run(rule_brain(inventing_brain))$answer, "3 apples and 2 loaves of bread cost €3.74.")
  expect_equal(run(rule_brain(misspelling_brain), tools = call_tool_with_suggestions)$answer, "One apple costs £0.45.")
  expect_equal(tool_count(run(guarded_brain(rule_brain(looping_brain)))), 3)
  expect_match(run(guarded_brain(rule_brain(inventing_brain), allowed_numbers = c(3, 2)))$answer, "add\\(b=1.9\\)")
  expect_match(run(guarded_brain(rule_brain(shop_rules), allowed_numbers = c(3, 2)))$answer, "4.31")
})

test_that("argument validation finds three problems", {
  expect_length(validate_arguments(SCHEMAS[[2]], list(b = "x", c = 1)), 3)
})

test_that("trimming keeps whole turns", {
  memory <- run(rule_brain(shop_rules))$memory
  expect_length(trim_memory(memory, 2), 5)
  expect_length(trim_memory(memory, 3), 7)
})

test_that("the demo scripts run", {
  withr_dir <- function(code) { o <- setwd(root); on.exit(setwd(o)); code }
  out <- withr_dir(system2("Rscript", "r/vol1/ch33/demo_memory.R", stdout = TRUE))
  expect_true(any(grepl("Run 2: 4 tool calls", out)))
  out <- withr_dir(system2("Rscript", "r/vol1/ch34/workflow_vs_agent.R", stdout = TRUE))
  expect_true(any(grepl("7.53", out)))
})
