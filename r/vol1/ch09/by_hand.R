# Chapter 9: fit a straight line through 5 loans, step by step, as you would on paper.

loans <- read.csv("data/learning/loans_2026.csv")
# The first 5 new-car loans in the training set.
five <- head(loans[loans$used == 0 & loans$set == "train", ], 5)
x <- five$credit_score          # input: credit score
y <- five$interest_rate_pct     # output: interest rate in percent

x_mean <- mean(x); y_mean <- mean(y)
cat(sprintf("Step 1  mean score = %.1f   mean rate = %.3f\n", x_mean, y_mean))

sxy <- sum((x - x_mean) * (y - y_mean))
sxx <- sum((x - x_mean)^2)
slope <- sxy / sxx
intercept <- y_mean - slope * x_mean
cat(sprintf("Step 3  slope = %.3f / %.2f = %.5f\n", sxy, sxx, slope))
cat(sprintf("Step 4  intercept = %.3f\n", intercept))
cat(sprintf("Check   lm() gives intercept %.3f and slope %.5f\n",
            coef(lm(y ~ x))[1], coef(lm(y ~ x))[2]))
