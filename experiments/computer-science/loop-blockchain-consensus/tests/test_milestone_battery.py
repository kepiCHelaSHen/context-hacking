"""
Blockchain Consensus (PBFT) — CHP Milestone Test Battery

4 milestones x 4 Byzantine strategies x 30 seeds.
Key test: safety holds under equivocation (catches Raft contamination).

Usage:
    pytest tests/test_milestone_battery.py -v
"""

import numpy as np
import pytest

try:
    from consensus import PBFTNetwork, run_simulation
    PBFT_AVAILABLE = True
except ImportError:
    PBFT_AVAILABLE = False

# ── Frozen coefficients ──────────────────────────────────────────────────────
N_NODES = 10
F_MAX = 3  # floor((10-1)/3)
QUORUM = 2 * F_MAX + 1  # = 7
N_PHASES = 3

SIGMA_THRESHOLD = 0.15
SEEDS_QUICK = [42, 137, 271]
SEEDS_FULL = list(range(1, 31))

STRATEGIES = ["equivocate", "silent", "delayed", "colluding"]


def _skip():
    if not PBFT_AVAILABLE:
        pytest.skip("consensus.py not yet built — run the CHP loop first")


def _run(seed: int, n_byzantine: int = 0, strategy: str = "silent") -> dict:
    _skip()
    return run_simulation(
        seed=seed, n_nodes=N_NODES, n_byzantine=n_byzantine,
        byzantine_strategy=strategy,
    )


# =============================================================================
# MILESTONE 1 — Foundation (honest-only consensus)
# =============================================================================

class TestMilestone1Foundation:

    def test_network_construction(self):
        _skip()
        net = PBFTNetwork(n_nodes=N_NODES, seed=42)
        assert len(net.nodes) == N_NODES

    def test_honest_consensus(self):
        """With zero faults, all nodes should agree."""
        _skip()
        r = _run(42, n_byzantine=0)
        assert r["consensus_reached"], "No consensus with 0 faults"
        assert not r["safety_violated"], "Safety violated with 0 faults!"

    def test_all_honest_same_value(self):
        _skip()
        r = _run(42, n_byzantine=0)
        assert r["decided_value"] is not None

    def test_three_phases(self):
        """Protocol must use 3 phases (pre-prepare, prepare, commit)."""
        _skip()
        r = _run(42, n_byzantine=0)
        phases = r.get("phases_executed", [])
        assert len(phases) >= 3, (
            f"Only {len(phases)} phases executed — PBFT requires 3 "
            f"(pre-prepare, prepare, commit). If 2: missing commit phase."
        )

    def test_quorum_is_2f_plus_1(self):
        """Quorum must be 2f+1 = 7 for N=10, NOT f+1 = 4."""
        _skip()
        net = PBFTNetwork(n_nodes=N_NODES, seed=42)
        q = net.quorum_size
        assert q == QUORUM, (
            f"Quorum is {q}, should be {QUORUM} (2f+1). "
            f"If {F_MAX + 1}: this is Raft/Paxos quorum (f+1), not PBFT."
        )

    def test_deterministic(self):
        _skip()
        r1 = _run(42, n_byzantine=0)
        r2 = _run(42, n_byzantine=0)
        assert r1["decided_value"] == r2["decided_value"]

    def test_message_complexity_quadratic(self):
        """PBFT message complexity is O(N^2) per round."""
        _skip()
        r = _run(42, n_byzantine=0)
        msg_count = r.get("message_count", 0)
        # With N=10: prepare phase alone sends N*(N-1) = 90 messages
        # Three phases: roughly 3 * N^2 = 300
        assert msg_count >= N_NODES * (N_NODES - 1), (
            f"Message count {msg_count} too low for O(N^2) complexity. "
            f"Expected >= {N_NODES * (N_NODES - 1)}. "
            f"Low message count suggests single-leader broadcast (Raft), not all-to-all (PBFT)."
        )


# =============================================================================
# MILESTONE 2 — Byzantine Fault Tolerance
# =============================================================================

class TestMilestone2Byzantine:

    def test_equivocation_safety(self):
        """CRITICAL: Safety must hold under equivocation with f=3.

        This is THE test that catches Raft contamination. Raft breaks under
        equivocation. PBFT does not.
        """
        _skip()
        for seed in SEEDS_QUICK:
            r = _run(seed, n_byzantine=F_MAX, strategy="equivocate")
            assert not r["safety_violated"], (
                f"SAFETY VIOLATED under equivocation (seed={seed}, f={F_MAX}). "
                f"If safety breaks under equivocation, the protocol is Raft "
                f"(crash-fault only), not PBFT (Byzantine-fault tolerant). "
                f"Check: is the quorum 2f+1={QUORUM}? Are there 3 phases?"
            )

    def test_silent_safety(self):
        """Safety holds with f=3 silent (crashed) Byzantine nodes."""
        _skip()
        for seed in SEEDS_QUICK:
            r = _run(seed, n_byzantine=F_MAX, strategy="silent")
            assert not r["safety_violated"]
            assert r["consensus_reached"]

    def test_colluding_safety(self):
        """Safety holds with f=3 colluding Byzantine nodes."""
        _skip()
        for seed in SEEDS_QUICK:
            r = _run(seed, n_byzantine=F_MAX, strategy="colluding")
            assert not r["safety_violated"]

    @pytest.mark.parametrize("strategy", STRATEGIES)
    def test_all_strategies_safe_at_f3(self, strategy):
        """All 4 strategies must maintain safety at f=3."""
        _skip()
        r = _run(42, n_byzantine=F_MAX, strategy=strategy)
        assert not r["safety_violated"], (
            f"Safety violated with strategy='{strategy}', f={F_MAX}"
        )

    def test_false_positive_raft_detector(self):
        """If equivocation breaks safety, the protocol is Raft, not PBFT.

        This is the pre-loaded false positive. Raft handles crash faults
        (silent strategy) but breaks under equivocation. PBFT handles both.
        """
        _skip()
        # First: silent should work (even Raft handles this)
        r_silent = _run(42, n_byzantine=F_MAX, strategy="silent")

        # Then: equivocation is the real test
        r_equiv = _run(42, n_byzantine=F_MAX, strategy="equivocate")

        if r_silent["consensus_reached"] and r_equiv["safety_violated"]:
            pytest.fail(
                "FALSE POSITIVE DETECTED: Protocol reaches consensus with "
                "crashed nodes but BREAKS under equivocation. This is Raft "
                "(crash-fault-tolerant), not PBFT (Byzantine-fault-tolerant). "
                "Check: quorum must be 2f+1, not f+1. Protocol must have "
                "3 phases (pre-prepare, prepare, commit), not 2."
            )


# =============================================================================
# MILESTONE 3 — Fault Threshold
# =============================================================================

class TestMilestone3Threshold:

    def test_below_threshold_succeeds(self):
        """f = 1, 2, 3: consensus should succeed."""
        _skip()
        for f in [1, 2, 3]:
            r = _run(42, n_byzantine=f, strategy="equivocate")
            assert r["consensus_reached"], (
                f"Consensus should succeed at f={f} < N/3={N_NODES/3:.1f}"
            )
            assert not r["safety_violated"]

    def test_at_threshold_may_fail(self):
        """f = 4 (>= N/3): consensus may fail but safety must not be violated.

        Above the threshold, the protocol should either:
        (a) Reach consensus correctly (if lucky), or
        (b) Report "no consensus" (timeout/deadlock).
        It must NOT decide on conflicting values.
        """
        _skip()
        n_consensus = 0
        n_safety_violation = 0
        for seed in SEEDS_FULL[:10]:
            r = _run(seed, n_byzantine=4, strategy="equivocate")
            if r["consensus_reached"]:
                n_consensus += 1
            if r["safety_violated"]:
                n_safety_violation += 1

        # Above threshold: OK to not reach consensus
        # NOT OK: to decide conflicting values
        assert n_safety_violation == 0, (
            f"Safety violated {n_safety_violation}/10 times at f=4. "
            f"Above threshold, liveness may fail but safety must hold."
        )

    def test_zero_faults_always_succeeds(self):
        """f=0: consensus always reached across 30 seeds."""
        _skip()
        for seed in SEEDS_FULL:
            r = _run(seed, n_byzantine=0)
            assert r["consensus_reached"]


# =============================================================================
# MILESTONE 4 — Convergence Battery
# =============================================================================

class TestMilestone4ConvergenceBattery:

    @pytest.mark.slow
    @pytest.mark.parametrize("strategy", ["equivocate", "silent"])
    def test_safety_30_seeds(self, strategy):
        """Safety must hold in 30/30 seeds for each strategy at f=3."""
        _skip()
        violations = 0
        for seed in SEEDS_FULL:
            r = _run(seed, n_byzantine=F_MAX, strategy=strategy)
            if r["safety_violated"]:
                violations += 1

        assert violations == 0, (
            f"Safety violated in {violations}/30 seeds with strategy='{strategy}'. "
            f"Safety is a HARD guarantee (0 violations required)."
        )

    @pytest.mark.slow
    def test_liveness_30_seeds(self):
        """Consensus reached in >= 90% of 30 seeds at f=3 (silent)."""
        _skip()
        reached = 0
        for seed in SEEDS_FULL:
            r = _run(seed, n_byzantine=F_MAX, strategy="silent")
            if r["consensus_reached"]:
                reached += 1

        rate = reached / len(SEEDS_FULL)
        assert rate >= 0.90, (
            f"Consensus reached in only {reached}/30 seeds ({rate:.0%}). "
            f"Expected >= 90% at f={F_MAX} with silent faults."
        )

    @pytest.mark.slow
    def test_message_count_30_seeds_sigma(self):
        """Message count across 30 seeds: std/mean < sigma threshold."""
        _skip()
        counts = []
        for seed in SEEDS_FULL:
            r = _run(seed, n_byzantine=0)
            counts.append(r.get("message_count", 0))

        mean_c = np.mean(counts)
        std_c = np.std(counts)
        cv = std_c / max(mean_c, 1)

        assert cv < SIGMA_THRESHOLD, (
            f"Message count CV={cv:.4f} exceeds {SIGMA_THRESHOLD}. "
            f"High variance suggests non-deterministic message ordering."
        )


# =============================================================================
# COEFFICIENT DRIFT CHECKS
# =============================================================================

class TestCoefficientDrift:

    def test_n_nodes_is_10(self):
        _skip()
        net = PBFTNetwork(n_nodes=N_NODES, seed=42)
        assert len(net.nodes) == 10

    def test_quorum_is_7(self):
        _skip()
        net = PBFTNetwork(n_nodes=N_NODES, seed=42)
        assert net.quorum_size == 7, (
            f"Quorum is {net.quorum_size}, should be 7 (2f+1). "
            f"If 4: this is Raft quorum (f+1=4), not PBFT."
        )

    def test_f_max_is_3(self):
        _skip()
        net = PBFTNetwork(n_nodes=N_NODES, seed=42)
        assert net.f_max == 3

    def test_no_raft_patterns(self):
        """Source should not contain Raft-specific patterns."""
        _skip()
        import inspect
        source = inspect.getsource(PBFTNetwork)
        raft_signs = ["term_number", "RequestVote", "AppendEntries",
                      "log_replication", "leader_election"]
        for sign in raft_signs:
            assert sign not in source, (
                f"Raft pattern '{sign}' found in source — "
                f"this should be PBFT, not Raft"
            )

    def test_no_paxos_patterns(self):
        """Source should not contain Paxos-specific patterns."""
        _skip()
        import inspect
        source = inspect.getsource(PBFTNetwork)
        paxos_signs = ["Proposer", "Acceptor", "Learner", "Promise", "promise"]
        for sign in paxos_signs:
            assert sign not in source, (
                f"Paxos pattern '{sign}' found in source — "
                f"this should be PBFT, not Paxos"
            )

    def test_three_phase_names(self):
        """Protocol must have pre-prepare, prepare, commit phases."""
        _skip()
        import inspect
        source = inspect.getsource(PBFTNetwork).lower()
        assert "pre_prepare" in source or "preprepare" in source, "Missing PRE-PREPARE phase"
        assert "prepare" in source, "Missing PREPARE phase"
        assert "commit" in source, "Missing COMMIT phase"
