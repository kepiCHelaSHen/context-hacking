# Blockchain Consensus — CHP Experiment Report

## Summary
Simplified PBFT with 3 phases, 2f+1 quorum, Byzantine fault tolerance.
Safety holds under equivocation at f=1,2,3. Above threshold (f=4): no
consensus but NO safety violation. Raft contamination test: PASSED.

## False Positive Story
**The Raft test PASSED.** Equivocating Byzantine nodes (sending different values
to different replicas) do NOT break safety. A Raft implementation would fail here
because Raft uses f+1 quorum (4), allowing split-brain under equivocation.
PBFT's 2f+1 quorum (7) prevents this.

## Key Results
| f Byzantine | Strategy | Consensus? | Safety Violated? |
|-------------|----------|-----------|-----------------|
| 0 | — | Yes | No |
| 1 | equivocate | Yes | No |
| 2 | equivocate | Yes | No |
| 3 | equivocate | Yes | **No** |
| 4 | equivocate | No | **No** |

- Quorum: 7 (2f+1). NOT 4 (Raft f+1). — PASS
- Phases: pre_prepare, prepare, commit (3 phases). — PASS
- Messages: 189 (O(N^2) per round). — PASS
- Above threshold: graceful failure (no consensus, no violation). — PASS

## Gate Scores
| Gate | Score |
|------|-------|
| Frozen compliance | 1.00 |
| Architecture | 0.95 |
| Scientific validity | 0.95 |
| Drift check | 0.98 |
