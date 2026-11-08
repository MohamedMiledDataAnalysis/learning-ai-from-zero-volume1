# Chapter 25 - call the Ollama chat API from R with httr2.
# The address comes from the OLLAMA_HOST environment variable (default: your own computer).
library(httr2)

ollama_chat <- function(messages, model = "qwen2.5:7b",
                        host = Sys.getenv("OLLAMA_HOST", "http://localhost:11434")) {
  if (!grepl("^https?://", host)) host <- paste0("http://", host)   # OLLAMA_HOST may omit the scheme
  body <- list(model = model, messages = messages,
               options = list(temperature = 0, seed = 42, num_ctx = 8192), stream = FALSE)
  response <- request(host) |>
    req_url_path("/api/chat") |>
    req_body_json(body, auto_unbox = TRUE) |>   # turn the R list into JSON
    req_perform()                               # send the POST request and wait
  reply <- resp_body_json(response)             # turn the JSON reply back into an R list
  reply$message$content
}

if (sys.nframe() == 0) {                        # run only when the file is executed, not sourced
  messages <- list(list(role = "user", content = "What is the 90+ day arrears ratio limit?"))
  cat("Reply:", ollama_chat(messages), "\n")
}
