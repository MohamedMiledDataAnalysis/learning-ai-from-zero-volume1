# B.4 Named lists: values found by name.
prices <- list(apple = 0.45, bread = 1.20)
print(prices[["bread"]])
prices[["milk"]] <- 1.05  # add a new name
str(prices)
print("apple" %in% names(prices))
