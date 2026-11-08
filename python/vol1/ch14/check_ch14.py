"""Practical task (chapter 14): retrain the digits model with 12 hidden neurons instead of 32
(hidden_layer_sizes=(12,)), everything else unchanged. Give the test accuracy in percent, one decimal."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from part3_checker import check

d = load_digits()
Xtr, Xte, ytr, yte = train_test_split(d.data / 16.0, d.target, test_size=0.25, random_state=0, stratify=d.target)
m = MLPClassifier(hidden_layer_sizes=(12,), max_iter=1000, random_state=0).fit(Xtr, ytr)
check(round(m.score(Xte, yte) * 100, 1), 0.05, "§ 14.4", "%")
