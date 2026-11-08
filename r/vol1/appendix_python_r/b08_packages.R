# B.8 Packages: code other people wrote.
library(jsonlite)

print(sqrt(16))         # built into R
values <- c(2, 4, 9)
print(mean(values))
print(toJSON(list(mean = mean(values)), auto_unbox = TRUE))
