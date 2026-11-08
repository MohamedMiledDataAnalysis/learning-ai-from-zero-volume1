"""Practical task of chapter 29: Cost of 2 boxes of eggs and 1 cheese, in euros.

    python python/vol1/ch29/check_ch29.py <your answer>
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from part6_checker import grade  # noqa: E402,F401

from shop_tools import add, gbp_to_eur, get_price, multiply
pounds = add(multiply(2, get_price('eggs')['price_gbp'])['result'], get_price('cheese')['price_gbp'])['result']
expected = gbp_to_eur(pounds)['amount_eur']

grade("Cost of 2 boxes of eggs and 1 cheese, in euros", expected, "§ 29.5")
