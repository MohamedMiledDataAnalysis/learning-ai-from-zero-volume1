# Chapter 26 - the same JSON checks in R, with jsonlite.
library(jsonlite)

extract_json <- function(text) {
  # Keep only the part between the first "{" and the last "}" (removes ```json fences and sentences).
  m <- regmatches(text, regexpr("\\{.*\\}", text))
  if (length(m) == 0) stop("no JSON object found in the reply")
  fromJSON(m, simplifyVector = FALSE)
}

check <- function(data) {
  problems <- character(0)
  need <- c("period", "test", "value", "breached")
  for (k in setdiff(need, names(data))) problems <- c(problems, sprintf("missing key '%s'", k))
  for (k in setdiff(names(data), need)) problems <- c(problems, sprintf("unexpected key '%s'", k))
  if (!is.null(data$period) && !(is.numeric(data$period) && data$period == round(data$period)
                                 && data$period >= 1 && data$period <= 12))
    problems <- c(problems, "'period' should be a whole number from 1 to 12")
  if (!is.null(data$test) && !(data$test %in% c("cumulative_default_ratio", "arrears_90_ratio")))
    problems <- c(problems, "'test' is not a known test name")
  if (!is.null(data$value) && !(is.numeric(data$value) && data$value >= 0 && data$value <= 1))
    problems <- c(problems, sprintf("'value' should be a number from 0 to 1, got %s", format(data$value)))
  if (!is.null(data$breached) && !is.logical(data$breached))
    problems <- c(problems, "'breached' should be true or false")
  problems
}

validate <- function(text) {
  data <- tryCatch(extract_json(text), error = function(e) NULL)
  if (is.null(data)) return("not valid JSON")
  check(data)
}

replies <- c(
  "A clean"   = '{"period": 10, "test": "arrears_90_ratio", "value": 0.01321, "breached": true}',
  "B fenced"  = 'Here is the summary:\n```json\n{"period": 10, "test": "arrears_90_ratio", "value": 0.01321, "breached": true}\n```',
  "C percent" = '{"period": 10, "test": "arrears_90_ratio", "value": "1.32%", "breached": true}',
  "D missing" = '{"period": 10, "test": "arrears_90_ratio", "value": 0.01321}',
  "E broken"  = "{'period': 10, 'test': 'arrears_90_ratio'}"
)

for (name in names(replies)) {
  p <- validate(replies[[name]])
  cat(sprintf("Reply %-10s -> %s\n", name, if (length(p) == 0) "VALID" else paste("INVALID:", paste(p, collapse = "; "))))
}
