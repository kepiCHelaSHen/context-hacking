# Blockchain Consensus — Dead Ends Log

---

## DEAD END 1 — Raft protocol (crash-fault only)

**What was attempted**: Builder generated a Raft-style protocol with leader
election (term numbers, RequestVote), log replication (AppendEntries), and
majority quorum (f+1 = 4 for N=10).

**Result**: Protocol reached consensus with 3 crashed (silent) nodes. But when
Byzantine nodes EQUIVOCATED (sent value=1 to half the nodes and value=2 to the
other half), two groups of honest nodes decided different values. Safety violated.

**Why this is a dead end**: Raft assumes nodes either work correctly or crash.
It has NO defense against equivocation (lying). The frozen spec requires PBFT
which handles arbitrary Byzantine behavior through 2f+1 quorum (7 for N=10)
and three-phase commit.

**Do NOT repeat**: Any protocol with f+1 quorum, leader election with term
numbers, or log replication. These are Raft patterns.

---

## DEAD END 2 — Quorum of f+1 instead of 2f+1

**What was attempted**: Builder implemented a three-phase protocol but used
quorum = f+1 = 4 (majority) instead of 2f+1 = 7.

**Result**: With f=3 Byzantine nodes equivocating, the honest nodes could form
two disjoint quorums of size 4 (since 7 honest nodes split into groups of 4
and 3). Both groups reached "consensus" on different values. Safety violated.

**Why this is a dead end**: 2f+1 quorum ensures that any two quorums overlap
in at least one honest node. With f+1 quorum, Byzantine nodes can participate
in two different quorums simultaneously, breaking safety.

**Do NOT repeat**: Any quorum smaller than 2f+1 = 2*floor((N-1)/3) + 1.

---

## DEAD END 3 — Two-phase protocol (missing COMMIT phase)

**What was attempted**: Builder implemented only PRE-PREPARE and PREPARE phases
(two-phase commit) without the COMMIT phase.

**Result**: With a Byzantine primary, the primary sent different PRE-PREPARE
values to different replicas. Some replicas prepared on value=1, others on
value=2. Without the COMMIT phase to confirm agreement, replicas decided
based on incomplete information. Safety violated in edge cases where exactly
2f+1 nodes prepared on different values across two views.

**Why this is a dead end**: The COMMIT phase is essential for PBFT. It confirms
that 2f+1 nodes AGREE they are prepared on the same value. Without it, the
protocol cannot distinguish between "I'm prepared" and "everyone is prepared."

**Do NOT repeat**: Any protocol with fewer than 3 phases.
