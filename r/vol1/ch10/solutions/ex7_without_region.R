# Chapter 10, exercise 7: what happens to the logistic regression without the North West indicator?
loans <- read.csv("data/learning/loans_2026.csv"); loans$income_k <- loans$annual_income / 1000
train <- loans[loans$set == "train", ]; test <- loans[loans$set == "test", ]
actual <- test$bad == 1
for (f in c("bad ~ credit_score + ltv_original_pct + income_k + used + north_west",
            "bad ~ credit_score + ltv_original_pct + income_k + used")) {
  m <- glm(as.formula(f), data = train, family = binomial)
  flagged <- predict(m, newdata = test, type = "response") >= 0.10
  tp <- sum(flagged & actual); fp <- sum(flagged & !actual)
  label <- if (grepl("north_west", f)) "with north_west" else "without north_west"
  cat(sprintf("%-20s threshold 0.10: TP=%2d FP=%3d  recall=%.2f%%\n", label, tp, fp, 100 * tp / sum(actual)))
}
