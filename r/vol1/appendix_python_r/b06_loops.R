# B.6 Loops: repeat a step for each item.
basket <- c("apple", "apple", "bread")
prices <- list(apple = 0.45, bread = 1.20)
total <- 0
for (item in basket) {
  total <- total + prices[[item]]
  cat(item, round(total, 2), "\n")
}
