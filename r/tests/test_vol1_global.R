# Tests for the Volume 1 global assessment (R): the Library agent grader.
library(testthat)

grade_quietly <- function(path) {
  old <- setwd(root); on.exit(setwd(old))
  source("r/vol1/global_assessment/grade_library.R", local = TRUE)
  out <- capture.output(score <- grade_library(path))
  list(score = score, out = out)
}

test_that("the R reference Library agent scores 15 out of 15", {
  r <- grade_quietly("solutions/vol1/global_assessment/library_agent.R")
  expect_equal(r$score, 15)
  expect_true(any(grepl("Part F score: 15 / 15", r$out, fixed = TRUE)))
})

test_that("the untouched R starter scores 0 and names the chapters to reread", {
  r <- grade_quietly("r/vol1/global_assessment/library_starter.R")
  expect_equal(r$score, 0)
  expect_true(any(grepl("reread chapter 29", r$out, fixed = TRUE)))
})

test_that("an R agent without the £5.00 maximum loses exactly 3 points", {
  src <- readLines(file.path(root, "solutions/vol1/global_assessment/library_agent.R"), encoding = "UTF-8")
  src <- sub("min(days * RULES$fine_per_day_gbp, RULES$maximum_fine_gbp)", "days * RULES$fine_per_day_gbp",
             src, fixed = TRUE)
  tmp <- tempfile(fileext = ".R"); writeLines(src, tmp, useBytes = TRUE)
  expect_equal(grade_quietly(tmp)$score, 12)
})
