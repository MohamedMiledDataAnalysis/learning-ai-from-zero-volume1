# B.9 Files and paths: read a table from data/.
path <- file.path("data", "learning", "loans_2026.csv")
loans <- read.csv(path)
print(dim(loans))        # rows, columns
print(head(loans[, c("loan_id", "credit_score")], 3))
print(round(mean(loans$credit_score), 2))
