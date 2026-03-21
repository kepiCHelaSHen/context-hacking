# Blockchain Consensus — Frozen Specification
# Grounded in: Castro & Liskov (1999) "Practical Byzantine Fault Tolerance"
#              Lamport, Shostak, Pease (1982) "The Byzantine Generals Problem"
# THIS FILE IS FROZEN. No agent may modify it.

================================================================================
OVERVIEW
================================================================================

A simplified PBFT-style (Practical Byzantine Fault Tolerance) consensus protocol
where N nodes agree on a value despite up to f < N/3 Byzantine (arbitrary) faults.
Byzantine nodes can lie, send conflicting messages, collude, and selectively
respond — they are adversarial, not just crashed.

The key scientific point: LLMs default to CRASH-FAULT-TOLERANT protocols
(Raft, Paxos) when asked for "consensus algorithm." Crash-fault protocols
handle nodes that STOP but not nodes that LIE. Byzantine fault tolerance
requires a fundamentally different protocol structure (3-phase commit with
2f+1 quorum instead of f+1). The Prior-as-Detector catches Raft/Paxos
contamination by injecting Byzantine behavior and checking if consensus
breaks.

================================================================================
PROTOCOL (simplified PBFT)
================================================================================

NODES: N nodes, each with a unique ID [0, N-1].
  Default: N = 10
  Maximum Byzantine: f = floor((N-1) / 3) = 3

ROLES:
  - PRIMARY: one designated leader who proposes values.
    Primary = round_number % N (rotates each round).
  - REPLICAS: all other nodes that validate and vote.

THREE PHASES per round:

  PHASE 1 — PRE-PREPARE (leader broadcast):
    The primary broadcasts <PRE-PREPARE, round, value> to all replicas.
    Byzantine primary may send DIFFERENT values to different replicas.

  PHASE 2 — PREPARE (replica broadcast):
    Each honest replica that receives a valid PRE-PREPARE broadcasts
    <PREPARE, round, value, node_id> to ALL other nodes.
    A node enters "prepared" state when it has received 2f+1 matching
    PREPARE messages (including its own) for the same (round, value).

    NOTE: The quorum is 2f+1, NOT f+1. This is the key difference from
    crash-fault protocols. LLMs commonly generate f+1 quorum (Raft).
    With f+1 quorum, a Byzantine minority can cause disagreement.

  PHASE 3 — COMMIT (prepared nodes broadcast):
    Each prepared node broadcasts <COMMIT, round, value, node_id> to all.
    A node decides (commits) the value when it has received 2f+1 matching
    COMMIT messages for the same (round, value).

VALUE: integer (proposed by primary). Default: primary proposes its own ID.

================================================================================
SAFETY AND LIVENESS PROPERTIES
================================================================================

SAFETY (must hold with f < N/3 Byzantine nodes):
  No two honest nodes decide different values in the same round.
  This must hold with probability 1.0 — it's a HARD guarantee, not probabilistic.

  NOTE: If any test case shows two honest nodes disagreeing, the protocol
  is BROKEN. This is the most critical safety property.

LIVENESS (must hold with f < N/3 and reliable network):
  Honest nodes eventually decide a value (consensus is reached).
  With synchronous messaging: within 3 message delays per round.

FAULT TOLERANCE THRESHOLD:
  f < N/3: consensus MUST succeed (safety + liveness).
  f >= N/3: consensus MAY fail (no guarantee). The protocol should detect
  this and report "no consensus" rather than deciding a wrong value.

  For N=10: f <= 3 → consensus succeeds. f >= 4 → may fail.

================================================================================
BYZANTINE BEHAVIORS (for testing)
================================================================================

Byzantine nodes can execute any of these strategies:

  EQUIVOCATE: Send different values to different replicas in the same phase.
    Primary sends value=1 to half the nodes and value=2 to the other half.
    This is the attack that breaks crash-fault protocols.

  SILENT: Stop responding (equivalent to crash fault).
    This is the WEAKEST Byzantine behavior — Raft can handle this.

  DELAYED: Respond correctly but late (after honest nodes have moved on).

  COLLUDING: All Byzantine nodes coordinate to maximize damage.
    f Byzantine nodes all send the same wrong value to create a
    minority block that confuses honest nodes.

================================================================================
METRICS
================================================================================

  consensus_reached: boolean — did all honest nodes decide the same value?
  decided_value: the value decided by honest nodes (or None if no consensus)
  rounds_to_consensus: number of rounds needed
  message_count: total messages sent across all phases
  message_complexity: messages per round (should be O(N^2) for PBFT)
  safety_violated: boolean — did any two honest nodes decide differently?
    MUST be False for all f < N/3 cases. If True: protocol is broken.
  byzantine_detected: number of Byzantine behaviors detected by honest nodes

================================================================================
RAFT/PAXOS CONTAMINATION WARNING
================================================================================

Raft and Paxos are CRASH-FAULT-TOLERANT protocols. They assume nodes either
work correctly or STOP (crash). They cannot handle nodes that LIE.

Signs of Raft contamination:
  - Leader election with term numbers (Raft-specific)
  - Log replication instead of value agreement
  - Quorum of f+1 instead of 2f+1
  - No PREPARE phase (Raft has only AppendEntries and RequestVote)
  - Protocol survives crash faults but breaks under equivocation

Signs of Paxos contamination:
  - Proposer/Acceptor/Learner roles (Paxos-specific)
  - Promise/Accept two-phase (Paxos), not Pre-prepare/Prepare/Commit (PBFT)
  - Quorum of floor(N/2)+1 (Paxos majority) instead of 2f+1

The frozen spec is PBFT: three phases, 2f+1 quorum, Byzantine tolerance.
If the protocol breaks under equivocation (different values to different
nodes), it's Raft/Paxos, not PBFT.

================================================================================
EXACT COEFFICIENTS (for drift detection)
================================================================================

  N_NODES: 10
  F_MAX: 3  (= floor((10-1) / 3))
  QUORUM: 7  (= 2*3 + 1 = 2f+1)
  PHASES: 3  (pre-prepare, prepare, commit)
  PRIMARY_ROTATION: round_number % N
  MESSAGE_COMPLEXITY: O(N^2) per phase, O(N^2) per round
  SAFETY: "no two honest nodes disagree" (hard guarantee)
  FAULT_THRESHOLD: "f < N/3 succeeds, f >= N/3 may fail"
