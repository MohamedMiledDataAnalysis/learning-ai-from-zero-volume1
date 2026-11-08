# Check a tool call's arguments against the tool's schema before running it.

type_ok <- function(value, type) {
  switch(type,
         number = is.numeric(value) && length(value) == 1,
         integer = is.numeric(value) && length(value) == 1 && value == round(value),
         string = is.character(value) && length(value) == 1,
         boolean = is.logical(value) && length(value) == 1,
         TRUE)
}

validate_arguments <- function(schema, arguments) {
  params <- schema$`function`$parameters
  allowed <- params$properties
  problems <- character(0)
  for (name in unlist(params$required)) {                          # 1. every required argument is present
    if (is.null(arguments[[name]])) problems <- c(problems, sprintf("missing required argument '%s'", name))
  }
  for (name in names(arguments)) {
    value <- arguments[[name]]
    if (!name %in% names(allowed)) {                                # 2. no unknown argument
      problems <- c(problems, sprintf("unknown argument '%s' (allowed: %s)", name,
                                      paste(sort(names(allowed)), collapse = ", ")))
      next
    }
    rule <- allowed[[name]]
    if (!type_ok(value, rule$type)) {                               # 3. the right type
      problems <- c(problems, sprintf("'%s' must be a %s, not %s", name, rule$type, deparse(value)))
      next
    }
    if (!is.null(rule$enum) && !value %in% unlist(rule$enum)) {     # 4. one of the allowed values
      problems <- c(problems, sprintf("'%s' must be one of %s", name, paste(unlist(rule$enum), collapse = ", ")))
    }
    if (!is.null(rule$minimum) && value < rule$minimum) problems <- c(problems, sprintf("'%s' must be at least %s", name, rule$minimum))
    if (!is.null(rule$maximum) && value > rule$maximum) problems <- c(problems, sprintf("'%s' must be at most %s", name, rule$maximum))
  }
  problems
}

make_safe_call_tool <- function(schemas, call_tool) {
  by_name <- setNames(schemas, vapply(schemas, function(s) s$`function`$name, ""))
  function(name, arguments) {
    if (name %in% names(by_name)) {
      problems <- validate_arguments(by_name[[name]], arguments)
      if (length(problems) > 0) {
        return(to_json(list(error = paste0("invalid call to ", name, ": ", paste(problems, collapse = "; ")))))
      }
    }
    call_tool(name, arguments)
  }
}
