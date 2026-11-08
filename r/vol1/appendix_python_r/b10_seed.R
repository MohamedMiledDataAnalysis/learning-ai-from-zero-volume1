# B.10 Random numbers and the seed.
set.seed(42)
print(sample(1:6, 5, replace = TRUE))  # five dice
set.seed(42)
print(sample(1:6, 5, replace = TRUE))  # same five
