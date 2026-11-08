# Four brains that go wrong on purpose. Each imitates a mistake real models make.

tool_results <- function(memory) {
  lapply(Filter(function(m) m$role == "tool", memory), function(m) fromJSON(m$content))
}
answer <- function(text) list(content = text, tool_calls = list())

misspelling_brain <- function(memory) {           # Failure 1: asks for 'aple'
  results <- tool_results(memory)
  if (length(results) == 0) return(call("get_price", item = "aple"))
  last <- results[[length(results)]]
  if (!is.null(last$error) && grepl("did you mean", last$error)) {
    return(call("get_price", item = strsplit(last$error, "'")[[1]][4]))
  }
  if (!is.null(last$error)) return(answer("I could not find the price of apples."))
  answer(sprintf("One apple costs £%.2f.", last$price_gbp))
}

missing_tool_brain <- function(memory) {          # Failure 2: calls a tool that does not exist
  results <- tool_results(memory)
  if (length(results) == 0) return(call("convert_to_euros", amount = 3.75))
  last <- results[[length(results)]]
  if (!is.null(last$error)) return(call("gbp_to_eur", amount = 3.75))
  answer(sprintf("£3.75 is €%.2f.", last$amount_eur))
}

looping_brain <- function(memory) call("get_price", item = "apple")   # Failure 3: never answers

inventing_brain <- function(memory) {             # Failure 4: invents £0.95 a loaf
  results <- tool_results(memory)
  n <- length(results)
  if (n == 0) return(call("get_price", item = "apple"))
  if (n == 1) return(call("multiply", a = 3, b = results[[1]]$price_gbp))
  if (n == 2) return(call("add", a = results[[2]]$result, b = 1.90))
  if (n == 3) return(call("gbp_to_eur", amount = results[[3]]$result))
  answer(sprintf("3 apples and 2 loaves of bread cost €%.2f.", results[[4]]$amount_eur))
}
