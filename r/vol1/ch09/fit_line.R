# Chapter 9: linear regression on the whole training set, then tested on loans it has never seen.

loans <- read.csv("data/learning/loans_2026.csv")
train <- loans[loans$set == "train", ]
test  <- loans[loans$set == "test", ]

evaluate <- function(model) {
  # Error measures on the test set: loans the model did not learn from.
  errors <- test$interest_rate_pct - predict(model, newdata = test)
  rmse <- sqrt(mean(errors^2))
  r2 <- 1 - sum(errors^2) / sum((test$interest_rate_pct - mean(test$interest_rate_pct))^2)
  c(rmse = rmse, r2 = r2)
}

m1 <- lm(interest_rate_pct ~ credit_score, data = train)
e1 <- evaluate(m1)
cat("Model 1: rate = a + b x score\n")
cat(sprintf("  intercept a = %.4f   slope b = %.6f\n", coef(m1)[1], coef(m1)[2]))
cat(sprintf("  test RMSE = %.3f points   test R-squared = %.3f\n", e1["rmse"], e1["r2"]))

m2 <- lm(interest_rate_pct ~ credit_score + used, data = train)
e2 <- evaluate(m2)
cat("Model 2: rate = a + b x score + c x used\n")
cat(sprintf("  intercept a = %.4f   b = %.6f   c = %.4f\n", coef(m2)[1], coef(m2)[2], coef(m2)[3]))
cat(sprintf("  test RMSE = %.3f points   test R-squared = %.3f\n", e2["rmse"], e2["r2"]))

new_loan <- data.frame(credit_score = 700, used = 1)
cat(sprintf("Prediction for a used car, score 700: %.2f%%\n", predict(m2, newdata = new_loan)))
