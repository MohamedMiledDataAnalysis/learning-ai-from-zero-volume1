# Chapter 12: one neuron, one loan, one step of gradient descent, every number printed.

x1 <- -1.2; x2 <- 1.0      # credit score (z-score) and North West indicator
y <- 1                     # the loan fell 3 instalments behind
w1 <- 0.5; w2 <- 0.5; b <- 0.0
lr <- 0.5

z <- w1 * x1 + w2 * x2 + b
p <- 1 / (1 + exp(-z))
cat(sprintf("Forward   z = %.4f   p = %.4f   loss = %.4f\n", z, p, -log(p)))
error <- p - y
g1 <- error * x1; g2 <- error * x2; gb <- error
cat(sprintf("Backward  p - y = %.4f   gradients: w1 %.4f   w2 %.4f   b %.4f\n", error, g1, g2, gb))
w1 <- w1 - lr * g1; w2 <- w2 - lr * g2; b <- b - lr * gb
p <- 1 / (1 + exp(-(w1 * x1 + w2 * x2 + b)))
cat(sprintf("Update    w1 = %.4f   w2 = %.4f   b = %.4f\n", w1, w2, b))
cat(sprintf("After     p = %.4f   loss = %.4f\n", p, -log(p)))
