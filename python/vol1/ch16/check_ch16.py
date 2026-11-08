"""Practical task (chapter 16): in the training text, which character most often follows 'e'?
Answer with the character; type space for a space."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from part3_checker import check
from ch16.markov_text import fit, training_text

c = fit(training_text(), 1)["e"].most_common(1)[0][0]
check("space" if c == " " else c, 0, "§ 16.2")
