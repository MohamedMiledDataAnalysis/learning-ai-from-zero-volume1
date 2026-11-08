# Check your answer to the practical task of chapter 9 (slope for used cars, training set only).
# Run:  Rscript r/vol1/ch09/check_ch09.R <your slope>, for example -0.0123
answer <- suppressWarnings(as.numeric(commandArgs(trailingOnly = TRUE)[1]))
if (is.na(answer)) {
  cat("Give your answer as a number, for example:\n  Rscript r/vol1/ch09/check_ch09.R -0.0123\n")
  quit(save = "no", status = 2)
}
loans <- read.csv("data/learning/loans_2026.csv")
used <- loans[loans$set == "train" & loans$used == 1, ]
slope <- coef(lm(interest_rate_pct ~ credit_score, data = used))[2]
if (abs(answer - round(slope, 4)) < 0.00005) cat(sprintf("Correct: the slope is %.4f.\n", slope)) else
  cat("Not yet. Check that you kept only used cars AND only the training set, then reread section 9.4.\n")
