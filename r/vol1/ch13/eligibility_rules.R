# Chapter 13 — the same six eligibility rules in R.
tape <- read.csv("data/loan_tape_cutoff.csv", stringsAsFactors = FALSE)
uk_regions <- c("London", "South East", "South West", "East of England", "East Midlands",
                "West Midlands", "North West", "North East", "Yorkshire and the Humber",
                "Wales", "Scotland", "Northern Ireland")

# Each rule is a column of TRUE (pass) or FALSE (fail), one value per loan.
rules <- data.frame(
  R1 = tape$region %in% uk_regions,
  R2 = tape$product %in% c("HP", "PCP"),
  R3 = tape$days_past_due == 0,
  R4 = tape$original_term_months - tape$remaining_term_months >= 3,
  R5 = tape$remaining_term_months >= 6,
  R6 = tape$ltv_original_pct <= 100
)
eligible <- apply(rules, 1, all)       # a loan is eligible when every rule is TRUE
cat("Rows checked:", nrow(tape), "\n")
cat("Rows passing all six rules:", sum(eligible), "\n")
cat("Rows failing at least one rule:", sum(!eligible), "\n")
print(tape[!eligible, c("loan_id", "region")], row.names = FALSE)
