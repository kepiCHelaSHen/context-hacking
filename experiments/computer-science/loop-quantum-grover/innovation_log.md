# Grover's Algorithm — Innovation Log

---

## Expected Build Sequence

Turn 1: Foundation — state vector, Hadamard, phase-flip oracle (Milestone 1)
  → Watch for: boolean oracle (Dead End 2), no state vector (Dead End 1)
Turn 2: Diffusion — inversion about mean, full G = D * O (Milestone 2)
  → Watch for: missing diffusion (Dead End 3), reversed order (D * O not O * D)
  → EXPECTED FALSE POSITIVE: flat amplitude = no diffusion implemented
Turn 3: Verification — success vs k curve, N sweep (Milestone 3)
  → Watch for: k = sqrt(N) instead of floor(pi/4 * sqrt(N))
Turn 4: Convergence battery — 30 random targets (Milestone 4)
