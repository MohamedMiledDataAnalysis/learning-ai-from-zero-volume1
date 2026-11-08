# Chapter 11, exercise 7: k-means with k = 5 on the raw columns, without scaling.
loans <- read.csv("data/learning/loans_2026.csv")
X <- as.matrix(loans[, c("credit_score", "annual_income", "interest_rate_pct", "original_balance")])
start <- read.csv("data/learning/kmeans_start_rows.csv")$row
model <- kmeans(X, centers = X[start[1:5], ], algorithm = "Lloyd", iter.max = 300)
loans$segment <- model$cluster
cat("seg  loans  score   income   balance  bad rate\n")
for (s in 1:5) {
  g <- loans[loans$segment == s, ]
  cat(sprintf("%3d  %5d  %5.0f  %7.0f  %8.0f  %6.2f%%\n", s, nrow(g), mean(g$credit_score),
              mean(g$annual_income), mean(g$original_balance), 100 * mean(g$bad)))
}
