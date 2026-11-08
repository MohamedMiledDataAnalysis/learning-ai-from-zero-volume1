"""Chapter 14 — recognise handwritten digits.

scikit-learn ships with 1,797 small images of handwritten digits (8x8 pixels,
values 0 to 16). No download is needed. We train a small neural network and test
it on images it has never seen.
"""

import numpy as np
from sklearn.datasets import load_digits
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

digits = load_digits()
print("Images:", digits.images.shape[0], "| pixels per image:", digits.images.shape[1] * digits.images.shape[2])

print("\nThe first image as numbers (it is a 0):")
for row in digits.images[0].astype(int):
    print(" ".join(f"{v:2d}" for v in row))

X = digits.data / 16.0            # scale pixels to 0..1
y = digits.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)

model = MLPClassifier(hidden_layer_sizes=(32,), max_iter=1000, random_state=0)
model.fit(X_train, y_train)
pred = model.predict(X_test)

print(f"\nTraining images: {len(X_train)} | test images: {len(X_test)}")
print(f"Accuracy on the test images: {accuracy_score(y_test, pred):.1%}")
cm = confusion_matrix(y_test, pred)
errors = [(int(t), int(p), int(cm[t, p])) for t in range(10) for p in range(10) if t != p and cm[t, p] > 0]
errors.sort(key=lambda e: (-e[2], e[0], e[1]))
print("Most frequent confusions (true -> predicted: count):")
for t, p, n in errors[:3]:
    print(f"  {t} -> {p}: {n}")
