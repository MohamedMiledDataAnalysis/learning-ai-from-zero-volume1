# Chapter 12, exercise 7: the same network trained with three learning rates.
library(jsonlite)
loans <- read.csv("data/learning/loans_2026.csv"); loans$income_k <- loans$annual_income / 1000
features <- c("credit_score", "ltv_original_pct", "income_k", "north_west")
train <- loans[loans$set == "train", ]
pop_sd <- function(v) sqrt(mean((v - mean(v))^2))
X <- sweep(sweep(as.matrix(train[, features]), 2, colMeans(train[, features])), 2,
           apply(train[, features], 2, pop_sd), "/")
y <- matrix(train$bad, ncol = 1)
start <- fromJSON("data/learning/nn_initial_weights.json")
sigmoid <- function(z) 1 / (1 + exp(-z))
for (lr in c(0.3, 1.0, 10.0)) {
  W1 <- start$W1; b1 <- start$b1; W2 <- start$W2; b2 <- start$b2; losses <- c()
  for (epoch in 0:3000) {
    H <- sigmoid(sweep(X %*% W1, 2, b1, "+")); P <- sigmoid(sweep(H %*% W2, 2, b2, "+"))
    if (epoch %in% c(10, 100, 3000)) losses[as.character(epoch)] <- -mean(y * log(P) + (1 - y) * log(1 - P))
    d2 <- (P - y) / nrow(X); d1 <- (d2 %*% t(W2)) * H * (1 - H)
    W2 <- W2 - lr * t(H) %*% d2; b2 <- b2 - lr * colSums(d2); W1 <- W1 - lr * t(X) %*% d1; b1 <- b1 - lr * colSums(d1)
  }
  cat(sprintf("learning rate %5.1f: loss at epoch 10 = %.5f, 100 = %.5f, 3000 = %.5f\n", lr, losses["10"],
              losses["100"], losses["3000"]))
}
