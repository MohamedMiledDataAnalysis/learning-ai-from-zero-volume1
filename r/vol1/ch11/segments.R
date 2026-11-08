# Chapter 11: group borrowers into segments with k-means.

loans <- read.csv("data/learning/loans_2026.csv")
columns <- c("credit_score", "annual_income", "interest_rate_pct", "original_balance")
X <- as.matrix(loans[, columns])

# Put every column on the same scale. R's sd() and scale() divide by n - 1; Python divides by n.
# To get the same numbers as Python we use the population standard deviation (divide by n).
pop_sd <- function(v) sqrt(mean((v - mean(v))^2))
Z <- sweep(sweep(X, 2, colMeans(X)), 2, apply(X, 2, pop_sd), "/")

start <- read.csv("data/learning/kmeans_start_rows.csv")$row     # row numbers, counted from 1

cat("k   within-cluster sum of squares   drop\n")
wcss <- sapply(2:8, function(k) kmeans(Z, centers = Z[start[1:k], , drop = FALSE],
                                       algorithm = "Lloyd", iter.max = 300)$tot.withinss)
drop <- c("-", sprintf("%.1f", -diff(wcss)))
cat(sprintf("%d   %10.1f   %8s\n", 2:8, wcss, drop), sep = "")

K <- 5
model <- kmeans(Z, centers = Z[start[1:K], , drop = FALSE], algorithm = "Lloyd", iter.max = 300)
loans$segment <- model$cluster
cat(sprintf("\nSegments with k = %d (averages in original units)\n", K))
cat("seg  loans  score   income   rate   balance  bad rate\n")
for (s in 1:K) {
  g <- loans[loans$segment == s, ]
  cat(sprintf("%3d  %5d  %5.0f  %7.0f  %5.2f  %8.0f  %6.2f%%\n", s, nrow(g), mean(g$credit_score),
              mean(g$annual_income), mean(g$interest_rate_pct), mean(g$original_balance), 100 * mean(g$bad)))
}
