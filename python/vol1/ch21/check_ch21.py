"""Chapter 21, question 10. Usage: python python/vol1/ch21/check_ch21.py <tokens in 'prospectus'> <tokens with 0 merges>"""
import sys
from collections import Counter
from pathlib import Path
sys.path[:0] = [str(Path(__file__).resolve().parents[1]), str(Path(__file__).resolve().parent)]
from bpe_tokenizer import N_MERGES, tokenize, tokenize_word, train_bpe  # noqa: E402
from part45_common import grade, prospectus_text, words  # noqa: E402
merges = train_bpe(Counter(words(prospectus_text())), N_MERGES)
grade(sys.argv[1:], [("10a", len(tokenize_word("prospectus", merges)), 0, "21.3"),
                     ("10b", len(tokenize(prospectus_text(), [])), 0, "21.3")])
