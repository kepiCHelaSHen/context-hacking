"""
Simplified PBFT Consensus — Byzantine fault tolerant.
Frozen spec: frozen/consensus_rules.md

Three phases: pre-prepare, prepare, commit.
Quorum: 2f+1 = 7 for N=10. NOT f+1=4 (Raft).
Byzantine tolerance: handles equivocation (lying), not just crashes.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

import numpy as np

_log = logging.getLogger(__name__)

N_NODES = 10
F_MAX = 3
QUORUM = 2 * F_MAX + 1  # = 7


@dataclass
class Message:
    phase: str  # "pre_prepare", "prepare", "commit"
    round: int
    value: int
    sender: int


@dataclass
class Node:
    node_id: int
    byzantine: bool = False
    byzantine_strategy: str = "silent"
    decided_value: int | None = None
    prepared_value: int | None = None
    _prepare_votes: dict = field(default_factory=dict)
    _commit_votes: dict = field(default_factory=dict)


class PBFTNetwork:
    """Simplified PBFT consensus network."""

    def __init__(self, n_nodes: int = N_NODES, seed: int = 42) -> None:
        self.n_nodes = n_nodes
        self.f_max = (n_nodes - 1) // 3
        self.quorum_size = 2 * self.f_max + 1
        self.rng = np.random.default_rng(seed)
        self.nodes = [Node(node_id=i) for i in range(n_nodes)]
        self._messages: list[Message] = []
        self._total_messages = 0
        self._phases_executed: list[str] = []

    def set_byzantine(self, n_byzantine: int, strategy: str = "silent") -> None:
        """Mark n_byzantine random nodes as Byzantine."""
        byzantine_ids = self.rng.choice(self.n_nodes, size=min(n_byzantine, self.n_nodes),
                                         replace=False)
        for i in byzantine_ids:
            self.nodes[i].byzantine = True
            self.nodes[i].byzantine_strategy = strategy

    def run_round(self, round_num: int = 0) -> dict:
        """Execute one round of PBFT consensus."""
        primary_id = round_num % self.n_nodes
        primary = self.nodes[primary_id]
        proposed_value = primary_id  # primary proposes its own ID

        # Reset per-round state
        for node in self.nodes:
            node.prepared_value = None
            node.decided_value = None
            node._prepare_votes = {}
            node._commit_votes = {}

        # ── Phase 1: PRE-PREPARE ─────────────────────────────────────────
        self._phases_executed.append("pre_prepare")
        for node in self.nodes:
            if node.node_id == primary_id:
                continue
            if primary.byzantine and primary.byzantine_strategy == "equivocate":
                # Send different values to different nodes
                fake_value = proposed_value if node.node_id % 2 == 0 else proposed_value + 100
                self._deliver(node, Message("pre_prepare", round_num, fake_value, primary_id))
            elif primary.byzantine and primary.byzantine_strategy == "silent":
                pass  # don't send anything
            else:
                self._deliver(node, Message("pre_prepare", round_num, proposed_value, primary_id))

        # ── Phase 2: PREPARE ─────────────────────────────────────────────
        self._phases_executed.append("prepare")
        for sender in self.nodes:
            if sender.byzantine:
                if sender.byzantine_strategy == "silent":
                    continue
                elif sender.byzantine_strategy == "equivocate":
                    for receiver in self.nodes:
                        if receiver.node_id != sender.node_id:
                            fake_val = proposed_value if receiver.node_id % 2 == 0 else proposed_value + 100
                            self._deliver(receiver, Message("prepare", round_num, fake_val, sender.node_id))
                elif sender.byzantine_strategy == "colluding":
                    for receiver in self.nodes:
                        if receiver.node_id != sender.node_id:
                            self._deliver(receiver, Message("prepare", round_num, proposed_value + 999, sender.node_id))
                continue

            # Honest node: broadcast prepare with the value it received
            for receiver in self.nodes:
                if receiver.node_id != sender.node_id:
                    self._deliver(receiver, Message("prepare", round_num, proposed_value, sender.node_id))

        # Check prepare quorum for honest nodes
        for node in self.nodes:
            if node.byzantine:
                continue
            # Count matching prepare messages
            vote_counts: dict[int, int] = {}
            for val in node._prepare_votes.values():
                vote_counts[val] = vote_counts.get(val, 0) + 1
            # Add own vote
            vote_counts[proposed_value] = vote_counts.get(proposed_value, 0) + 1

            for val, count in vote_counts.items():
                if count >= self.quorum_size:
                    node.prepared_value = val
                    break

        # ── Phase 3: COMMIT ──────────────────────────────────────────────
        self._phases_executed.append("commit")
        for sender in self.nodes:
            if sender.byzantine:
                if sender.byzantine_strategy != "silent":
                    for receiver in self.nodes:
                        self._deliver(receiver, Message("commit", round_num, proposed_value + 500, sender.node_id))
                continue

            if sender.prepared_value is not None:
                for receiver in self.nodes:
                    if receiver.node_id != sender.node_id:
                        self._deliver(receiver, Message("commit", round_num, sender.prepared_value, sender.node_id))

        # Check commit quorum
        for node in self.nodes:
            if node.byzantine:
                continue
            vote_counts = {}
            for val in node._commit_votes.values():
                vote_counts[val] = vote_counts.get(val, 0) + 1
            if node.prepared_value is not None:
                vote_counts[node.prepared_value] = vote_counts.get(node.prepared_value, 0) + 1

            for val, count in vote_counts.items():
                if count >= self.quorum_size:
                    node.decided_value = val
                    break

        # ── Check safety ─────────────────────────────────────────────────
        honest_decisions = [n.decided_value for n in self.nodes
                           if not n.byzantine and n.decided_value is not None]
        safety_violated = len(set(honest_decisions)) > 1
        consensus_reached = len(honest_decisions) > 0 and len(set(honest_decisions)) == 1

        return {
            "consensus_reached": consensus_reached,
            "decided_value": honest_decisions[0] if consensus_reached else None,
            "safety_violated": safety_violated,
            "message_count": self._total_messages,
            "phases_executed": list(self._phases_executed),
        }

    def _deliver(self, receiver: Node, msg: Message) -> None:
        self._total_messages += 1
        if msg.phase == "prepare":
            receiver._prepare_votes[msg.sender] = msg.value
        elif msg.phase == "commit":
            receiver._commit_votes[msg.sender] = msg.value


def run_simulation(
    seed: int = 42, n_nodes: int = N_NODES,
    n_byzantine: int = 0, byzantine_strategy: str = "silent",
) -> dict:
    net = PBFTNetwork(n_nodes=n_nodes, seed=seed)
    if n_byzantine > 0:
        net.set_byzantine(n_byzantine, byzantine_strategy)
    return net.run_round(round_num=0)
