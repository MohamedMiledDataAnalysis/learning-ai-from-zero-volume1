# Check your answer to the practical task of chapter 11 (size of the largest segment with k = 4).
# Run:  Rscript r/vol1/ch11/check_ch11.R <number of loans>, for example 1234
answer <- suppressWarnings(as.integer(commandArgs(trailingOnly = TRUE)[1]))
if (is.na(answer)) {
  cat("Give your answer as a number, for example:\n  Rscript r/vol1/ch11/check_ch11.R 1234\n")
  quit(save = "no", status = 2)
}
loans <- read.csv("data/learning/loans_2026.csv")
X <- as.matrix(loans[, c("credit_score", "annual_income", "interest_rate_pct", "original_balance")])
pop_sd <- function(v) sqrt(mean((v - mean(v))^2))
Z <- sweep(sweep(X, 2, colMeans(X)), 2, apply(X, 2, pop_sd), "/")
start <- read.csv("data/learning/kmeans_start_rows.csv")$row
largest <- max(kmeans(Z, centers = Z[start[1:4], ], algorithm = "Lloyd", iter.max = 300)$size)
if (identical(answer, as.integer(largest))) cat(sprintf("Correct: the largest segment has %d loans.\n", largest)) else
  cat("Not yet. Use the first 4 starting rows and the population standard deviation. Reread section 11.3.\n")
