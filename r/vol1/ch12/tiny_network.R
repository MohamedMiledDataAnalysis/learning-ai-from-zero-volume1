# Chapter 12: a network with 4 inputs, 3 hidden neurons and 1 output, written in base R only.
library(jsonlite)

loans <- read.csv("data/learning/loans_2026.csv")
loans$income_k <- loans$annual_income / 1000
features <- c("credit_score", "ltv_original_pct", "income_k", "north_west")
train <- loans[loans$set == "train", ]
test  <- loans[loans$set == "test", ]

# Scale with the training mean and population standard deviation (divide by n, as in Python).
pop_sd <- function(v) sqrt(mean((v - mean(v))^2))
mu <- colMeans(train[, features]); s <- apply(train[, features], 2, pop_sd)
X_train <- sweep(sweep(as.matrix(train[, features]), 2, mu), 2, s, "/")
X_test  <- sweep(sweep(as.matrix(test[, features]), 2, mu), 2, s, "/")
y_train <- matrix(train$bad, ncol = 1)

start <- fromJSON("data/learning/nn_initial_weights.json")
W1 <- start$W1; b1 <- start$b1          # 4 x 3 and 3
W2 <- start$W2; b2 <- start$b2          # 3 x 1 and 1

sigmoid <- function(z) 1 / (1 + exp(-z))
forward <- function(X) {
  H <- sigmoid(sweep(X %*% W1, 2, b1, "+"))     # hidden layer
  P <- sigmoid(sweep(H %*% W2, 2, b2, "+"))     # output probability
  list(H = H, P = P)
}
loss <- function(P, y) -mean(y * log(P) + (1 - y) * log(1 - P))

lr <- 1.0; epochs <- 3000; n <- nrow(X_train)
cat("epoch   training loss\n")
for (epoch in 0:epochs) {
  f <- forward(X_train); H <- f$H; P <- f$P
  if (epoch %in% c(0, 1, 10, 100, 500, 1000, 2000, 3000)) cat(sprintf("%5d   %.5f\n", epoch, loss(P, y_train)))
  dZ2 <- (P - y_train) / n
  dW2 <- t(H) %*% dZ2; db2 <- colSums(dZ2)
  dZ1 <- (dZ2 %*% t(W2)) * H * (1 - H)
  dW1 <- t(X_train) %*% dZ1; db1 <- colSums(dZ1)
  W1 <- W1 - lr * dW1; b1 <- b1 - lr * db1; W2 <- W2 - lr * dW2; b2 <- b2 - lr * db2
}

p <- as.vector(forward(X_test)$P)
actual <- test$bad == 1
for (th in c(0.50, 0.10)) {
  flagged <- p >= th
  tp <- sum(flagged & actual); fp <- sum(flagged & !actual); fn <- sum(!flagged & actual)
  precision <- if (tp + fp > 0) tp / (tp + fp) else 0
  cat(sprintf("Test, threshold %.2f: TP=%d FP=%d FN=%d  precision=%.2f%%  recall=%.2f%%\n",
              th, tp, fp, fn, 100 * precision, 100 * tp / (tp + fn)))
}
cat(sprintf("Output weights W2: [%s]\n", paste(sprintf("%.4f", W2), collapse = ", ")))
