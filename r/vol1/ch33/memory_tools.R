# Short-term memory (the message list) and long-term memory (a JSON file kept between runs).
# Count characters, not bytes, even when the session is not UTF-8 (the answer contains "€").
if (!isTRUE(l10n_info()[["UTF-8"]])) invisible(suppressWarnings(Sys.setlocale("LC_CTYPE", "C.UTF-8")))

approx_tokens <- function(text) max(1, round(nchar(text) / 4))   # planning estimate: about 4 characters per token

memory_size <- function(memory) {
  sum(vapply(memory, function(m) {
    calls <- if (length(m$tool_calls) > 0) to_json(m$tool_calls) else "[]"
    approx_tokens(paste0(m$content, calls))
  }, numeric(1)))
}

# Keep the system message, the goal and the last turns. A turn is one assistant
# message and the tool results that answer it: the two are never separated.
trim_memory <- function(memory, keep_last_turns) {
  head <- memory[1:2]
  rest <- memory[-(1:2)]
  turn_id <- cumsum(vapply(rest, function(m) m$role == "assistant", logical(1)))
  keep <- turn_id > max(turn_id) - keep_last_turns
  c(head, rest[keep])
}

long_term_memory <- function(path) {
  facts <- if (file.exists(path)) fromJSON(path, simplifyVector = FALSE) else named_list()
  list(
    remember = function(key, value) {
      facts[[key]] <<- value
      facts <<- facts[order(names(facts))]
      writeLines(jsonlite::toJSON(facts, auto_unbox = TRUE, pretty = TRUE, digits = NA), path)
    },
    as_text = function() {
      if (length(facts) == 0) return("No facts saved from earlier runs.")
      paste("Facts saved from earlier runs:", to_json(facts))
    },
    facts = function() facts
  )
}
