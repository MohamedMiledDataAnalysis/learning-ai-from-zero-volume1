# The fake brain: fixed rules that answer one question, with no AI at all.

call <- function(name, ...) list(content = "", tool_calls = list(list(name = name, arguments = list(...))))

shop_rules <- function(memory) {
  tool_messages <- Filter(function(m) m$role == "tool", memory)
  results <- lapply(tool_messages, function(m) fromJSON(m$content))
  n <- length(results)                                      # how many tools have run so far
  if (n == 0) return(call("get_price", item = "apple"))
  if (n == 1) return(call("get_price", item = "loaf of bread"))
  if (n == 2) return(call("multiply", a = 3, b = results[[1]]$price_gbp))
  if (n == 3) return(call("multiply", a = 2, b = results[[2]]$price_gbp))
  if (n == 4) return(call("add", a = results[[3]]$result, b = results[[4]]$result))
  if (n == 5) return(call("gbp_to_eur", amount = results[[5]]$result))
  euros <- results[[6]]$amount_eur
  list(content = sprintf("3 apples and 2 loaves of bread cost €%.2f.", euros), tool_calls = list())
}
