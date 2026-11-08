# The Corner Shop tools: four plain functions, their descriptions for the model, and call_tool.
# Every amount is money, so every result is rounded to the penny (2 decimal places).
library(jsonlite)

SHOP <- file.path("data", "learning", "corner_shop")
PRICES <- read.csv(file.path(SHOP, "prices.csv"), stringsAsFactors = FALSE)
RATE <- fromJSON(file.path(SHOP, "exchange_rate.json"))$rate

get_price <- function(item) {
  key <- tolower(trimws(item))
  row <- PRICES[PRICES$item == key, ]
  if (nrow(row) == 0) return(list(error = sprintf("unknown item '%s'", item)))
  list(item = key, price_gbp = row$price_gbp, unit = row$unit)
}

multiply <- function(a, b) list(result = round(a * b, 2))
add <- function(a, b) list(result = round(a + b, 2))
gbp_to_eur <- function(amount) list(amount_gbp = amount, rate = RATE, amount_eur = round(amount * RATE, 2))

TOOLS <- list(get_price = get_price, multiply = multiply, add = add, gbp_to_eur = gbp_to_eur)

number <- list(type = "number")
tool_schema <- function(name, description, properties, required) {
  list(type = "function", `function` = list(name = name, description = description,
       parameters = list(type = "object", properties = properties, required = as.list(required))))
}
SCHEMAS <- list(
  tool_schema("get_price", "Price in pounds of one unit of an item sold in the shop.",
              list(item = list(type = "string", description = "Item name, e.g. 'apple'.")), "item"),
  tool_schema("multiply", "Multiply two numbers (result rounded to 2 decimals).", list(a = number, b = number), c("a", "b")),
  tool_schema("add", "Add two numbers (result rounded to 2 decimals).", list(a = number, b = number), c("a", "b")),
  tool_schema("gbp_to_eur", "Convert an amount in pounds to euros at the shop's fixed rate.", list(amount = number), "amount")
)

SYSTEM_PROMPT <- paste("You are the Corner Shop assistant. Answer questions about the cost of shopping.",
                       "Always use the tools for prices and arithmetic; never guess a number.",
                       "Give the final answer in one sentence.")

# Run one tool and return its result as JSON text. Errors are returned as text too.
call_tool <- function(name, arguments) {
  if (!name %in% names(TOOLS)) {
    return(to_json(list(error = sprintf("unknown tool '%s'. Available tools: %s", name,
                                        paste(sort(names(TOOLS)), collapse = ", ")))))
  }
  result <- tryCatch(do.call(TOOLS[[name]], arguments),
                     error = function(e) list(error = sprintf("wrong arguments for %s: %s", name, conditionMessage(e))))
  to_json(result)
}
