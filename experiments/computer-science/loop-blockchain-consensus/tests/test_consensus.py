"""Tests for Simplified PBFT Consensus."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from consensus import PBFTNetwork, run_simulation


class TestNoFaultsConsensus:
    def test_f0_reaches_consensus(self):
        result = run_simulation(seed=42, n_nodes=10, n_byzantine=0)
        assert result["consensus_reached"] is True

    def test_f0_safety_not_violated(self):
        result = run_simulation(seed=42, n_nodes=10, n_byzantine=0)
        assert result["safety_violated"] is False


class TestByzantineTolerance:
    def test_f3_consensus_with_silent_byzantine(self):
        """With f=3 silent Byzantine nodes (N=10, quorum=7), consensus should still be reached."""
        result = run_simulation(seed=42, n_nodes=10, n_byzantine=3, byzantine_strategy="silent")
        assert result["consensus_reached"] is True

    def test_f3_safety_with_equivocating_byzantine(self):
        """Even with equivocating Byzantine nodes, safety should hold (no two honest nodes decide differently)."""
        result = run_simulation(seed=42, n_nodes=10, n_byzantine=3, byzantine_strategy="equivocate")
        assert result["safety_violated"] is False


class TestQuorum:
    def test_quorum_is_2f_plus_1(self):
        """Quorum must be 2f+1, not f+1 (which would be Raft, not PBFT)."""
        net = PBFTNetwork(n_nodes=10)
        f = net.f_max
        assert net.quorum_size == 2 * f + 1, \
            f"Quorum should be 2f+1={2*f+1}, got {net.quorum_size}"
        # f_max for N=10: (10-1)//3 = 3, quorum = 7
        assert net.quorum_size == 7
        assert net.quorum_size != f + 1, "Quorum must NOT be f+1 (that's Raft, not PBFT)"


class TestTooManyByzantine:
    def test_f4_no_consensus_but_safe(self):
        """With f=4 (> N/3), consensus should fail but safety should still hold."""
        result = run_simulation(seed=42, n_nodes=10, n_byzantine=4, byzantine_strategy="silent")
        # With 4 silent nodes out of 10, only 6 honest nodes remain
        # Quorum is 7, so 6 honest < 7 quorum => no consensus
        assert result["consensus_reached"] is False
        assert result["safety_violated"] is False


class TestThreeMessagePhases:
    def test_three_phases_executed(self):
        """PBFT has exactly 3 message phases: pre_prepare, prepare, commit."""
        result = run_simulation(seed=42, n_nodes=10, n_byzantine=0)
        phases = result["phases_executed"]
        assert "pre_prepare" in phases
        assert "prepare" in phases
        assert "commit" in phases
        assert len(phases) == 3
