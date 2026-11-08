# Check your answer to the practical task of chapter 10 (recall of the logistic model at threshold 0.20).
# Run:  Rscript r/vol1/ch10/check_ch10.R <your recall in percent>, for example 12.34
answer <- suppressWarnings(as.numeric(sub("%", "", commandArgs(trailingOnly = TRUE)[1], fixed = TRUE)))
if (is.na(answer)) {
  cat("Give your answer as a number, for example:\n  Rscript r/vol1/ch10/check_ch10.R 12.34\n")
  quit(save = "no", status = 2)
}
loans <- read.csv("data/learning/loans_2026.csv"); loans$income_k <- loans$annual_income / 1000
train <- loans[loans$set == "train", ]; test <- loans[loans$set == "test", ]
m <- glm(bad ~ credit_score + ltv_original_pct + income_k + used + north_west, data = train, family = binomial)
flagged <- predict(m, newdata = test, type = "response") >= 0.20
recall <- 100 * sum(flagged & test$bad == 1) / sum(test$bad == 1)
if (abs(answer - round(recall, 2)) < 0.005) cat(sprintf("Correct: recall at 0.20 is %.2f%%.\n", recall)) else
  cat("Not yet. Recall = TP / (TP + FN), counted on the test set only. Reread section 10.5.\n")
