# Chapter 11: two rounds of k-means on six points, printing every distance.
points <- rbind(A = c(-1.0, 0.5), B = c(-1.2, -0.3), C = c(0.8, 1.1), D = c(1.1, 0.9), E = c(0.2, -1.0),
                F = c(1.4, -0.2))
centres <- points[c("A", "C"), ]
for (r in 1:2) {
  cat(sprintf("Round %d: centres (%.3f, %.3f)  (%.3f, %.3f)\n", r, centres[1, 1], centres[1, 2],
              centres[2, 1], centres[2, 2]))
  group <- integer(0)
  for (name in rownames(points)) {
    d <- sqrt(rowSums((centres - matrix(points[name, ], 2, 2, byrow = TRUE))^2))
    group[name] <- which.min(d)
    cat(sprintf("  %s: distance to centre 1 = %.3f, to centre 2 = %.3f -> group %d\n", name, d[1], d[2],
                which.min(d)))
  }
  centres <- rbind(colMeans(points[group == 1, , drop = FALSE]), colMeans(points[group == 2, , drop = FALSE]))
  cat(sprintf("  groups: 1 = %s, 2 = %s\n", paste(names(group)[group == 1], collapse = ", "),
              paste(names(group)[group == 2], collapse = ", ")))
}
