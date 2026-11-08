# Volume 1, Part II: the figures quoted in chapters 9 to 12, computed in R.
# Run from the repository root: Rscript -e "testthat::test_dir('r/tests')"
library(testthat)

repo <- normalizePath(file.path(testthat::test_path(), "..", ".."))
run_r <- function(script) {
  old <- setwd(repo); on.exit(setwd(old))
  paste(system2("Rscript", script, stdout = TRUE), collapse = "\n")
}

test_that("chapter 9 regression", {
  out <- run_r("r/vol1/ch09/fit_line.R")
  expect_match(out, "slope b = -0.011916", fixed = TRUE)
  expect_match(out, "score 700: 10.88%", fixed = TRUE)
})

test_that("chapter 10 logistic regression and tree", {
  out <- run_r("r/vol1/ch10/predict_default.R")
  expect_match(out, "Logistic, threshold 0.10: TP=29 FP=100 FN=15", fixed = TRUE)
  expect_match(out, "Tree, threshold 0.10: TP=28 FP=140 FN=16", fixed = TRUE)
})

test_that("chapter 11 k-means", {
  out <- run_r("r/vol1/ch11/segments.R")
  expect_match(out, "8335.2", fixed = TRUE)
})

test_that("chapter 12 network", {
  out <- run_r("r/vol1/ch12/tiny_network.R")
  expect_match(out, " 3000   0.10217", fixed = TRUE)
  expect_match(out, "recall=68.18%", fixed = TRUE)
})
