"""Chapter 13 — a rule-based eligibility checker.

The prospectus (section 4) lists six eligibility criteria. Here each criterion
becomes one rule: a plain Python test written by a person. No learning happens:
the rules are the whole of the 'intelligence'.
"""

import pandas as pd

UK_REGIONS = {"London", "South East", "South West", "East of England", "East Midlands", "West Midlands",
              "North West", "North East", "Yorkshire and the Humber", "Wales", "Scotland", "Northern Ireland"}

# Each rule: (name, test). A test receives one loan (a row) and returns True when the loan passes.
RULES = [
    ("R1 borrower resident in the UK", lambda loan: loan["region"] in UK_REGIONS),
    ("R2 product is HP or PCP", lambda loan: loan["product"] in ("HP", "PCP")),
    ("R3 no arrears at cut-off", lambda loan: loan["days_past_due"] == 0),
    ("R4 at least 3 instalments paid",
     lambda loan: loan["original_term_months"] - loan["remaining_term_months"] >= 3),
    ("R5 at least 6 instalments left", lambda loan: loan["remaining_term_months"] >= 6),
    ("R6 original LTV 100% or less", lambda loan: loan["ltv_original_pct"] <= 100),
]


def check_loan(loan):
    """Return the names of the rules the loan fails (an empty list means eligible)."""
    return [name for name, test in RULES if not test(loan)]


def main():
    tape = pd.read_csv("data/loan_tape_cutoff.csv", keep_default_na=False)
    failures = {loan["loan_id"]: check_loan(loan) for _, loan in tape.iterrows()}
    failed = {lid: f for lid, f in failures.items() if f}
    print(f"Rows checked: {len(tape)}")
    print(f"Rows passing all six rules: {len(tape) - len(failed)}")
    print(f"Rows failing at least one rule: {len(failed)}")
    for lid, f in sorted(failed.items()):
        row = tape[tape.loan_id == lid].iloc[0]
        print(f"  {lid}: {', '.join(f)} (region recorded as '{row['region']}')")


if __name__ == "__main__":
    main()
