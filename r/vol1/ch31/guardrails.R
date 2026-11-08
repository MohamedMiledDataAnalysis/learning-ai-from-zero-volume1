# Guardrails for the Corner Shop agent: checks placed around the tools and around the brain.

# Guardrail 1: an unknown item comes back with the closest known name.
call_tool_with_suggestions <- function(name, arguments) {
  if (name == "get_price") {
    item <- tolower(trimws(arguments$item))
    if (!item %in% PRICES$item) {
      distances <- adist(item, PRICES$item)[1, ]
      hint <- if (min(distances) <= 2) sprintf(" — did you mean '%s'?", PRICES$item[which.min(distances)]) else ""
      return(to_json(list(error = sprintf("unknown item '%s'%s", item, hint))))
    }
  }
  call_tool(name, arguments)
}

numbers_in <- function(text) as.numeric(regmatches(text, gregexpr("-?[0-9]+(\\.[0-9]+)?", text))[[1]])

# Guardrails 2, 3 and 4: a wrapper around any brain that checks each reply.
guarded_brain <- function(inner, max_repeats = 3, allowed_numbers = numeric(0)) {
  known_numbers <- function(memory) {
    tools <- Filter(function(m) m$role == "tool", memory)
    c(allowed_numbers, unlist(lapply(tools, function(m) numbers_in(m$content))))
  }
  stop_with <- function(text) list(content = text, tool_calls = list())
  list(next_step = function(memory, schemas) {
    reply <- inner$next_step(memory, schemas)
    if (length(reply$tool_calls) > 0) {
      # Guardrail 2: the same call repeated max_repeats times in a row.
      new <- to_json(reply$tool_calls)
      previous <- vapply(Filter(function(m) m$role == "assistant" && length(m$tool_calls) > 0, memory),
                         function(m) to_json(lapply(m$tool_calls, `[[`, "function")), "")
      repeats <- 0
      for (p in rev(previous)) { if (p != new) break; repeats <- repeats + 1 }
      if (repeats >= max_repeats) {
        return(stop_with(sprintf("Stopped by guardrail: the same tool call was repeated %d times.", repeats)))
      }
      # Guardrail 3: every number passed to a tool must come from the question or a tool result.
      known <- known_numbers(memory)
      for (tc in reply$tool_calls) for (arg in names(tc$arguments)) {
        value <- tc$arguments[[arg]]
        if (is.numeric(value) && !any(abs(known - value) < 1e-9)) {
          return(stop_with(sprintf("Stopped by guardrail: %s(%s=%s) uses a number that no tool returned.",
                                   tc$name, arg, format(value))))
        }
      }
      return(reply)
    }
    # Guardrail 4: every number in the answer must come from a tool result.
    unknown <- Filter(function(x) !any(abs(known_numbers(memory) - x) < 1e-9), abs(numbers_in(reply$content)))
    if (length(unknown) > 0) {
      return(stop_with(sprintf("Answer blocked by guardrail: %s not found in any tool result.",
                               paste(unknown, collapse = ", "))))
    }
    reply
  })
}
