# B.9 Files and paths: read a table from data/.
from pathlib import Path
import pandas as pd

path = Path("data") / "learning" / "loans_2026.csv"
loans = pd.read_csv(path)
print(loans.shape)       # (rows, columns)
print(loans[["loan_id", "credit_score"]].head(3))
print(round(loans["credit_score"].mean(), 2))
