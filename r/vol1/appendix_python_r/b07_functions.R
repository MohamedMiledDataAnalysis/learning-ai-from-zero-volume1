# B.7 Functions: a named, reusable step.
to_euros <- function(pounds, rate = 1.15) {
  # Convert pounds to euros at a fixed rate.
  round(pounds * rate, 2)
}

print(to_euros(3.75))
print(to_euros(10, rate = 1.20))
