# Blockchain Consensus — CHP Experiment Specification

## Research Question

Does the PBFT protocol maintain safety (no disagreement) with f < N/3 Byzantine
nodes across all 4 Byzantine strategies? At what f does safety break?

## What to Build

1. `consensus.py` — Simplified PBFT consensus engine
   - Node class with message sending/receiving
   - Three-phase protocol: pre-prepare, prepare, commit
   - 2f+1 quorum requirement
   - Byzantine node injection (equivocate, silent, delayed, colluding)
   - Metrics: consensus_reached, safety_violated, message_count
   - All randomness (Byzantine target selection) via seeded numpy.random.Generator

2. `run_experiment.py` — Experiment runner
   - Condition A: No faults (f=0), 30 seeds — baseline
   - Condition B: f=1,2,3 Byzantine (equivocating), 30 seeds each — within threshold
   - Condition C: f=4 Byzantine (equivocating), 30 seeds — above threshold (should fail)
   - Condition D: f=3, all 4 strategies compared, 30 seeds each
   - Output: per-seed safety/liveness results

3. `tests/test_milestone_battery.py` — Sigma-gated test battery

## Milestones

1. FOUNDATION — Node, message passing, 3-phase protocol, honest-only consensus
2. BYZANTINE — Fault injection (4 strategies), safety verification
3. THRESHOLD — f < N/3 succeeds, f >= N/3 fails
4. CONVERGENCE BATTERY — 30 seeds x 4 strategies x 3 fault levels

## Expected False Positive

At Milestone 1, the Builder implements Raft (crash-fault-tolerant only) with
f+1 quorum. The protocol reaches consensus with silent (crashed) nodes. At
Milestone 2, the Critic injects EQUIVOCATING Byzantine nodes (sending different
values to different replicas). Raft breaks — two groups of honest nodes decide
different values. Safety violated.

The Builder reports "consensus achieved with 3 faulty nodes." But it only works
with CRASH faults, not BYZANTINE faults. The equivocation test catches this.
