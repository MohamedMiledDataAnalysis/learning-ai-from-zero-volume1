# Chapter 9, exercise 7: add a third input (PCP or HP) and compare the test error.
loans <- read.csv("data/learning/loans_2026.csv")
train <- loans[loans$set == "train", ]; test <- loans[loans$set == "test", ]
for (f in c("interest_rate_pct ~ credit_score + used", "interest_rate_pct ~ credit_score + used + pcp")) {
  m <- lm(as.formula(f), data = train)
  rmse <- sqrt(mean((test$interest_rate_pct - predict(m, newdata = test))^2))
  cat(sprintf("%-46s test RMSE = %.4f\n", f, rmse))
}
