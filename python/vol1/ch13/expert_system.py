"""Chapter 13 — a tiny expert system with forward chaining.

Facts are words in a set. A rule says: IF all these facts are known THEN add this
new fact. The engine applies the rules again and again until nothing new appears.
"""

RULES = [
    ({"missed_payment", "second_missed_payment"}, "two_instalments_in_arrears"),
    ({"two_instalments_in_arrears", "income_fell"}, "affordability_problem"),
    ({"affordability_problem"}, "offer_payment_plan"),
    ({"two_instalments_in_arrears", "no_contact"}, "send_field_agent"),
    ({"third_missed_payment", "two_instalments_in_arrears"}, "ninety_days_in_arrears"),
    ({"ninety_days_in_arrears"}, "report_in_arrears_90_bucket"),
]


def forward_chain(facts):
    facts = set(facts)
    trace = []
    changed = True
    while changed:                       # keep going while a rule still adds something new
        changed = False
        for conditions, conclusion in RULES:
            if conditions <= facts and conclusion not in facts:
                facts.add(conclusion)
                trace.append(f"{' + '.join(sorted(conditions))}  =>  {conclusion}")
                changed = True
    return facts, trace


def main():
    for case in [{"missed_payment", "second_missed_payment", "income_fell"},
                 {"missed_payment", "second_missed_payment", "third_missed_payment", "no_contact"}]:
        print("Starting facts:", ", ".join(sorted(case)))
        _, trace = forward_chain(case)
        for i, line in enumerate(trace, 1):
            print(f"  step {i}: {line}")
        print()


if __name__ == "__main__":
    main()
