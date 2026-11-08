# Grade Part F of the global assessment: your Library agent (R), out of 15 points.
# From the repository root:
#   Rscript r/vol1/global_assessment/grade_library.R path/to/library_agent.R
# Your file must define: find_book, days_late, fine, SCHEMAS, call_tool and run_library(question).

grade_library <- function(path) {
  env <- new.env()
  sys.source("r/agentcore/loop.R", envir = env)
  sys.source("r/agentcore/brains.R", envir = env)
  sys.source(path, envir = env)
  quiet <- function(msg) invisible(NULL)

  check <- function(points, label, test, reread) {
    ok <- tryCatch(isTRUE(test()), error = function(e) {
      msg <- conditionMessage(e)
      label <<- if (startsWith(msg, "TODO")) sprintf("%s (not written yet)", label) else sprintf("%s (crashed: %s)", label, msg)
      FALSE
    })
    cat(sprintf("%s  %d pt  %s%s\n", if (ok) "PASS" else "FAIL", points, label,
                if (ok) "" else paste0("  -> reread ", reread)))
    if (ok) points else 0
  }
  e <- env
  schema_names <- function() vapply(e$SCHEMAS, function(s) s[["function"]]$name, "")
  required <- function(name) {
    s <- Filter(function(s) s[["function"]]$name == name, e$SCHEMAS)[[1]]
    sort(unlist(s[["function"]]$parameters$required))
  }
  checks <- list(
    list(1, "find_book finds 'The Silent River' (B001, due 2026-10-20)",
         function() e$find_book("The Silent River")$book_id == "B001" &&
           e$find_book("the silent river")$due_date == "2026-10-20", "chapter 29"),
    list(1, "find_book returns an error for an unknown title",
         function() !is.null(e$find_book("The Missing Book")$error), "chapter 32"),
    list(1, "days_late('B001', '2026-11-02') = 13", function() e$days_late("B001", "2026-11-02")$days_late == 13,
         "chapter 29"),
    list(1, "days_late('B002', '2026-11-02') = 0 (not yet due)",
         function() e$days_late("B002", "2026-11-02")$days_late == 0, "chapter 32"),
    list(1, "days_late('B005', '2026-11-02') = 0 (due that day)",
         function() e$days_late("B005", "2026-11-02")$days_late == 0, "chapter 32"),
    list(1, "fine(13) = £2.60", function() abs(e$fine(13)$fine_gbp - 2.60) < 0.005, "chapter 29"),
    list(1, "fine(0) = £0.00", function() abs(e$fine(0)$fine_gbp) < 0.005, "chapter 29"),
    list(1, "fine(62) = £5.00 (the maximum)", function() abs(e$fine(62)$fine_gbp - 5.00) < 0.005, "chapter 32"),
    list(1, "SCHEMAS describes find_book, days_late and fine",
         function() setequal(schema_names(), c("find_book", "days_late", "fine")), "chapter 28"),
    list(1, "each schema lists its required arguments",
         function() identical(required("find_book"), "title") &&
           identical(required("days_late"), c("book_id", "on_date")) && identical(required("fine"), "days"),
         "chapter 32"),
    list(1, "call_tool returns an error as text for an unknown tool",
         function() !is.null(jsonlite::fromJSON(e$call_tool("renew_book", list()))$error), "chapter 32"),
    list(2, "run_library: 'The Silent River' on 2026-11-02 -> £2.60",
         function() grepl("£2.60", e$run_library("What fine is owed for 'The Silent River' on 2026-11-02?",
                                                    log = quiet), fixed = TRUE), "chapters 29 and 30"),
    list(2, "run_library: 'A Map of Small Islands' on 2026-11-02 -> £5.00",
         function() grepl("£5.00", e$run_library("What fine is owed for 'A Map of Small Islands' on 2026-11-02?",
                                                    log = quiet), fixed = TRUE), "chapters 29 and 31")
  )
  total <- sum(vapply(checks, function(c) check(c[[1]], c[[2]], c[[3]], c[[4]]), numeric(1)))
  cat(sprintf("\nPart F score: %d / 15\n", as.integer(total)))
  invisible(total)
}

if (sys.nframe() == 0) {
  args <- commandArgs(trailingOnly = TRUE)
  if (length(args) != 1) stop("usage: Rscript r/vol1/global_assessment/grade_library.R path/to/library_agent.R")
  grade_library(args[1])
}
