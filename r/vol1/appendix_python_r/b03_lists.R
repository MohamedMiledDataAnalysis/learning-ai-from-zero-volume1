# B.3 Vectors: several values in order.
scores <- c(741, 759, 612)
print(scores[1])        # first item: position 1
print(length(scores))   # how many items
scores <- c(scores, 680) # add one at the end
print(scores)
print(sum(scores) / length(scores))
