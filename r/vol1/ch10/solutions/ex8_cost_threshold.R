# Chapter 10, exercise 8: choose the threshold that costs the least (FN costs £5,000, FP costs £200).
loans <- read.csv("data/learning/loans_2026.csv"); loans$income_k <- loans$annual_income / 1000
train <- loans[loans$set == "train", ]; test <- loans[loans$set == "test", ]
m <- glm(bad ~ credit_score + ltv_original_pct + income_k + used + north_west, data = train, family = binomial)
p <- predict(m, newdata = test, type = "response"); actual <- test$bad == 1
for (th in c(0.50, 0.20, 0.10, 0.05, 0.02)) {
  fp <- sum(p >= th & !actual); fn <- sum(p < th & actual)
  cat(sprintf("threshold %.2f: FP=%4d FN=%2d  cost = %d x 200 + %d x 5,000 = £%s\n", th, fp, fn, fp, fn,
              format(fp * 200 + fn * 5000, big.mark = ",")))
}
