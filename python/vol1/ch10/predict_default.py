"""Chapter 10: which loans will fall 3 instalments behind (or default) in 2026?

Two models learn from the training set; both are judged on the test set.
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier, export_text

loans = pd.read_csv("data/learning/loans_2026.csv")
loans["income_k"] = loans.annual_income / 1000              # income in thousands of pounds
FEATURES = ["credit_score", "ltv_original_pct", "income_k", "used", "north_west"]
train, test = loans[loans.set == "train"], loans[loans.set == "test"]

print(f"Test set: {len(test)} loans, {test.bad.sum()} bad ({test.bad.mean():.2%})")
print(f"Model that always says 'good': accuracy {1 - test.bad.mean():.2%}, recall 0.00%")


def report(name, probabilities, threshold):
    """Confusion matrix, accuracy, precision and recall at one threshold."""
    flagged = probabilities >= threshold
    actual = test.bad.to_numpy() == 1
    tp = int((flagged & actual).sum()); fp = int((flagged & ~actual).sum())
    fn = int((~flagged & actual).sum()); tn = int((~flagged & ~actual).sum())
    precision = tp / (tp + fp) if tp + fp else 0.0
    print(f"{name}, threshold {threshold:.2f}: TP={tp} FP={fp} FN={fn} TN={tn}  "
          f"accuracy={(tp + tn) / len(test):.2%}  precision={precision:.2%}  recall={tp / (tp + fn):.2%}")


# Model 1: logistic regression (C=inf means no penalty, the same model as R's glm).
logit = LogisticRegression(C=np.inf, max_iter=100000, tol=1e-10).fit(train[FEATURES], train.bad)
print("\nLogistic regression coefficients")
print(f"  intercept         {logit.intercept_[0]:9.4f}")
for name, coef in zip(FEATURES, logit.coef_[0]):
    print(f"  {name:17s} {coef:9.4f}   odds x {np.exp(coef):.3f} per unit")
p_logit = logit.predict_proba(test[FEATURES])[:, 1]
for th in (0.50, 0.10):
    report("Logistic", p_logit, th)

# Model 2: a decision tree, 3 levels deep, at least 30 loans in every leaf.
tree = DecisionTreeClassifier(max_depth=3, min_samples_leaf=30, random_state=0).fit(train[FEATURES], train.bad)
print("\nDecision tree (weights = [good, bad] training loans in each leaf)")
print(export_text(tree, feature_names=FEATURES, show_weights=True, decimals=2).rstrip())
p_tree = tree.predict_proba(test[FEATURES])[:, 1]
for th in (0.50, 0.10):
    report("Tree", p_tree, th)
