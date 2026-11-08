# Five tool calls through the validating wrapper. From the repository root:
#   Rscript r/vol1/ch32/demo_validation.R
source("r/agentcore/loop.R")
source("r/vol1/ch29/shop_tools.R")
source("r/vol1/ch32/validate_args.R")

safe <- make_safe_call_tool(SCHEMAS, call_tool)
calls <- list(
  list("multiply", list(a = 3, b = 0.45)),
  list("multiply", list(a = 3)),
  list("multiply", list(a = "three", b = 0.45)),
  list("get_price", list(item = "apple", shop = "Leeds")),
  list("gbp_to_eur", list(amount = TRUE))
)
for (c in calls) {
  cat(sprintf("%s(%s)\n   -> %s\n", c[[1]], to_json(c[[2]]), safe(c[[1]], c[[2]])))
}
