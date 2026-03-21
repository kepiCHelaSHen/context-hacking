# Blockchain Consensus — Chain Prompt

================================================================================
PROJECT IDENTITY
================================================================================

Name:       Blockchain Consensus / PBFT (CHP Showcase)
Purpose:    Demonstrate Prior-as-Detector catching Raft/Paxos contamination
            when the spec requires Byzantine fault tolerance.

================================================================================
CONFIRMED DESIGN DECISIONS
================================================================================

DD01 — Protocol: simplified PBFT. NOT Raft. NOT Paxos.
DD02 — Three phases: pre-prepare, prepare, commit. NOT two-phase.
DD03 — Quorum: 2f+1 = 7 for N=10. NOT f+1 = 4 (Raft) or N/2+1 = 6 (Paxos).
DD04 — Byzantine tolerance: handles equivocation (lying), not just crashes.
DD05 — Nodes: N=10, f_max=3. Primary rotates: round % N.
DD06 — Safety: no two honest nodes disagree. HARD guarantee (100%).
DD07 — 4 Byzantine strategies: equivocate, silent, delayed, colluding.

================================================================================
ARCHITECTURE RULES
================================================================================

- Pure library: NO print(), NO UI.
- All randomness (Byzantine target selection) via seeded numpy.random.Generator.
- Same seed = identical message sequence.
- Structured logging.
- Messages are dicts: {type, round, value, sender, recipients}.

================================================================================
FROZEN CODE
================================================================================

frozen/consensus_rules.md — DO NOT MODIFY.
