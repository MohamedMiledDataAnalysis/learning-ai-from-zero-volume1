"""Chapter 12: one neuron, one loan, one step of gradient descent, every number printed."""

import math

# One loan with two inputs already put on a common scale (z-scores):
x1, x2 = -1.2, 1.0          # x1: credit score (1.2 standard deviations below average); x2: lives in the North West
y = 1                       # what happened: the loan fell 3 instalments behind
w1, w2, b = 0.5, 0.5, 0.0   # starting weights and bias
lr = 0.5                    # learning rate

z = w1 * x1 + w2 * x2 + b
p = 1 / (1 + math.exp(-z))
loss = -(y * math.log(p) + (1 - y) * math.log(1 - p))
print(f"Forward   z = {w1}*({x1}) + {w2}*{x2} + {b} = {z:.4f}")
print(f"          p = sigmoid(z) = 1 / (1 + e^-z) = {p:.4f}")
print(f"          loss = -ln(p) = {loss:.4f}")

error = p - y                                   # for sigmoid + cross-entropy, d loss / d z = p - y
g1, g2, gb = error * x1, error * x2, error
print(f"Backward  p - y = {error:.4f}")
print(f"          gradients: w1 {g1:.4f}   w2 {g2:.4f}   b {gb:.4f}")

w1, w2, b = w1 - lr * g1, w2 - lr * g2, b - lr * gb
z = w1 * x1 + w2 * x2 + b
p = 1 / (1 + math.exp(-z))
print(f"Update    w1 = {w1:.4f}   w2 = {w2:.4f}   b = {b:.4f}")
print(f"After     p = {p:.4f}   loss = {-math.log(p):.4f}")
