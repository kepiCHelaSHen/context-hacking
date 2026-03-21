# Blockchain Consensus — Innovation Log

---

## Expected Build Sequence

Turn 1: Foundation — nodes, message passing, 3-phase protocol, honest consensus (Milestone 1)
  → Watch for: Raft leader election (Dead End 1), f+1 quorum (Dead End 2)
  → Watch for: two-phase only (Dead End 3)
Turn 2: Byzantine injection — 4 strategies, safety verification (Milestone 2)
  → EXPECTED FALSE POSITIVE: consensus with silent faults but BROKEN under
    equivocation = Raft not PBFT
Turn 3: Fault threshold — f < N/3 succeeds, f >= N/3 may fail (Milestone 3)
Turn 4: Convergence battery — 30 seeds x 4 strategies x 3 fault levels (Milestone 4)
