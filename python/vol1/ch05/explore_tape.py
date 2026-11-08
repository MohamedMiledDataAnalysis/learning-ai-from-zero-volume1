"""Chapter 5 — a first look at the loan tape: its shape, one row, and the kinds of data in its columns."""

import pandas as pd

tape = pd.read_csv("data/loan_tape_cutoff.csv", keep_default_na=False)

print(f"Rows: {len(tape):,}   Columns: {tape.shape[1]}")
print()
print("One row, shown as a card (loan TAR00001):")
for column, value in tape.iloc[0].items():
    print(f"  {column:<22} {value}")
print()
kinds = {
    "identifier": ["loan_id"],
    "date": ["origination_date", "maturity_date"],
    "category": ["product", "vehicle_type", "fuel_type", "employment_status", "region", "postcode_area"],
    "whole number (discrete)": ["original_term_months", "remaining_term_months", "credit_score", "days_past_due"],
    "amount or ratio (decimal)": ["vehicle_value", "original_balance", "current_balance", "balloon_amount",
                                  "ltv_original_pct", "interest_rate_pct", "monthly_instalment", "annual_income"],
}
print("Columns by kind of data:")
for kind, cols in kinds.items():
    print(f"  {kind:<26} {len(cols):>2}  ({', '.join(cols[:3])}{', ...' if len(cols) > 3 else ''})")
print()
print("Loans by product:")
for product, n in tape["product"].value_counts().sort_index().items():
    print(f"  {product:<4} {n:>5,}")
print(f"Different regions written in the tape: {tape['region'].nunique()}")
print(f"Empty postcode cells: {(tape['postcode_area'] == '').sum()}")
print(f"Rows that are exact copies of another row: {tape.duplicated().sum()}")
