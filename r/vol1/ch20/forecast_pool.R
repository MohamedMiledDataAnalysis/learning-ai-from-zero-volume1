# Chapter 20 — the straight-line forecast in R with lm().
library(jsonlite)
files <- sort(list.files("data/investor_reports", pattern = "\\.json$", full.names = TRUE))
balance <- sapply(files, function(f) fromJSON(f)$pool$closing_balance) / 1e6
known <- data.frame(period = 1:9, balance = unname(balance[1:9]))
model <- lm(balance ~ period, data = known)          # fit the straight line
forecast <- predict(model, newdata = data.frame(period = 10:12))
cat(sprintf("Straight line: balance = %.3f + (%.3f x period)\n", coef(model)[1], coef(model)[2]))
cat(sprintf("Period %d: forecast %.2f, actual %.2f\n", 10:12, forecast, unname(balance[10:12])), sep = "")
