# Chapter 10: which loans will fall 3 instalments behind (or default) in 2026?
library(rpart)

loans <- read.csv("data/learning/loans_2026.csv")
loans$income_k <- loans$annual_income / 1000           # income in thousands of pounds
train <- loans[loans$set == "train", ]
test  <- loans[loans$set == "test", ]
formula <- bad ~ credit_score + ltv_original_pct + income_k + used + north_west

cat(sprintf("Test set: %d loans, %d bad (%.2f%%)\n", nrow(test), sum(test$bad), 100 * mean(test$bad)))

report <- function(name, probabilities, threshold) {
  # Confusion matrix, accuracy, precision and recall at one threshold.
  flagged <- probabilities >= threshold
  actual <- test$bad == 1
  tp <- sum(flagged & actual); fp <- sum(flagged & !actual)
  fn <- sum(!flagged & actual); tn <- sum(!flagged & !actual)
  precision <- if (tp + fp > 0) tp / (tp + fp) else 0
  cat(sprintf("%s, threshold %.2f: TP=%d FP=%d FN=%d TN=%d  accuracy=%.2f%%  precision=%.2f%%  recall=%.2f%%\n",
              name, threshold, tp, fp, fn, tn, 100 * (tp + tn) / nrow(test), 100 * precision,
              100 * tp / (tp + fn)))
}

# Model 1: logistic regression.
logit <- glm(formula, data = train, family = binomial)
cat("\nLogistic regression coefficients\n")
cat(sprintf("  %-17s %9.4f\n", "intercept", coef(logit)[1]))
for (name in names(coef(logit))[-1]) {
  cat(sprintf("  %-17s %9.4f   odds x %.3f per unit\n", name, coef(logit)[name], exp(coef(logit)[name])))
}
p_logit <- predict(logit, newdata = test, type = "response")
for (th in c(0.50, 0.10)) report("Logistic", p_logit, th)

# Model 2: a decision tree, 3 levels deep, at least 30 loans in every leaf.
# cp = -1 lets rpart keep splits that do not change the majority class (every leaf here is mostly 'good').
tree <- rpart(factor(bad) ~ credit_score + ltv_original_pct + income_k + used + north_west, data = train,
              method = "class", control = rpart.control(maxdepth = 3, minbucket = 30, minsplit = 60,
                                                        cp = -1, xval = 0))
cat("\nDecision tree\n")
print(tree, digits = 5)
p_tree <- predict(tree, newdata = test, type = "prob")[, "1"]
for (th in c(0.50, 0.10)) report("Tree", p_tree, th)
