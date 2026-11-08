# Check your answer to the practical task of chapter 12 (training loss at epoch 3000 with LR = 0.1).
# Run:  Rscript r/vol1/ch12/check_ch12.R <your loss>, for example 0.12345
answer <- suppressWarnings(as.numeric(commandArgs(trailingOnly = TRUE)[1]))
if (is.na(answer)) {
  cat("Give your answer as a number, for example:\n  Rscript r/vol1/ch12/check_ch12.R 0.12345\n")
  quit(save = "no", status = 2)
}
expected <- 0.10518   # computed by python/vol1/ch12/check_ch12.py and r/vol1/ch12/tiny_network.R with lr <- 0.1
if (abs(answer - expected) < 0.000005) cat(sprintf("Correct: the loss at epoch 3000 is %.5f.\n", expected)) else
  cat("Not yet. Change only lr, and read the loss printed for epoch 3000. Reread section 12.4.\n")
