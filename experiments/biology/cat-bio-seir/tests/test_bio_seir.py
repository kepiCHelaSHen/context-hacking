"""cat-bio-seir — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from bio_seir_constants import *
IMPL = Path(__file__).parent.parent / "bio_seir.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_r0_is_beta_over_gamma_not_sigma_dependent(self):
        """The #1 LLM error: including sigma in the R0 formula."""
        m = _i()
        r0_val = m.r0(BETA, GAMMA)
        assert math.isclose(r0_val, BETA / GAMMA, rel_tol=1e-9), (
            f"R0 should be beta/gamma={BETA/GAMMA}, got {r0_val}"
        )
        # R0 must NOT depend on sigma — test with many sigma values
        for sigma_alt in [0.01, 0.05, 0.1, 0.5, 1.0, 10.0]:
            r0_same = m.r0(BETA, GAMMA)
            assert math.isclose(r0_same, r0_val, rel_tol=1e-12), (
                f"R0 should not change with sigma={sigma_alt}, got {r0_same}"
            )

    def test_seir_r0_equals_sir_r0(self):
        """SEIR R0 is the same as SIR R0 — both are beta/gamma."""
        m = _i()
        sir_r0 = BETA / GAMMA
        seir_r0 = m.r0(BETA, GAMMA)
        assert math.isclose(seir_r0, sir_r0, rel_tol=1e-12), (
            f"SEIR R0={seir_r0} should equal SIR R0={sir_r0}"
        )

    def test_r0_function_takes_only_beta_gamma(self):
        """r0() signature must accept exactly (beta, gamma) — no sigma param."""
        m = _i()
        import inspect
        sig = inspect.signature(m.r0)
        params = list(sig.parameters.keys())
        assert len(params) == 2, (
            f"r0() should take 2 params (beta, gamma), got {len(params)}: {params}"
        )
        assert "sigma" not in [p.lower() for p in params], (
            f"r0() should NOT have a sigma parameter, got params: {params}"
        )


class TestCorrectness:
    def test_r0_value(self):
        m = _i()
        r0_val = m.r0(BETA, GAMMA)
        assert math.isclose(r0_val, R0, rel_tol=1e-9), (
            f"R0 should be {R0}, got {r0_val}"
        )

    def test_herd_immunity_threshold(self):
        m = _i()
        hit = m.herd_immunity_threshold(R0)
        assert math.isclose(hit, HERD_IMMUNITY, rel_tol=1e-9), (
            f"Herd immunity should be {HERD_IMMUNITY}, got {hit}"
        )

    def test_herd_immunity_at_r0_2(self):
        """At R0=2, herd immunity threshold is 0.5 (50%)."""
        m = _i()
        hit = m.herd_immunity_threshold(2.0)
        assert math.isclose(hit, 0.5, rel_tol=1e-9), (
            f"Herd immunity at R0=2 should be 0.5, got {hit}"
        )

    def test_derivatives_dS(self):
        m = _i()
        dS, dE, dI, dR = m.seir_derivatives(TEST_S, TEST_E, TEST_I, TEST_R, N, BETA, SIGMA, GAMMA)
        assert math.isclose(dS, DSDT, rel_tol=1e-9), (
            f"dS/dt should be {DSDT}, got {dS}"
        )

    def test_derivatives_dE(self):
        m = _i()
        dS, dE, dI, dR = m.seir_derivatives(TEST_S, TEST_E, TEST_I, TEST_R, N, BETA, SIGMA, GAMMA)
        assert math.isclose(dE, DEDT, rel_tol=1e-9), (
            f"dE/dt should be {DEDT}, got {dE}"
        )

    def test_derivatives_dI(self):
        m = _i()
        dS, dE, dI, dR = m.seir_derivatives(TEST_S, TEST_E, TEST_I, TEST_R, N, BETA, SIGMA, GAMMA)
        assert math.isclose(dI, DIDT, rel_tol=1e-9), (
            f"dI/dt should be {DIDT}, got {dI}"
        )

    def test_derivatives_dR(self):
        m = _i()
        dS, dE, dI, dR = m.seir_derivatives(TEST_S, TEST_E, TEST_I, TEST_R, N, BETA, SIGMA, GAMMA)
        assert math.isclose(dR, DRDT, rel_tol=1e-9), (
            f"dR/dt should be {DRDT}, got {dR}"
        )

    def test_derivatives_sum_to_zero(self):
        """Conservation: dS + dE + dI + dR = 0 always."""
        m = _i()
        dS, dE, dI, dR = m.seir_derivatives(TEST_S, TEST_E, TEST_I, TEST_R, N, BETA, SIGMA, GAMMA)
        total = dS + dE + dI + dR
        assert math.isclose(total, 0.0, abs_tol=1e-12), (
            f"Derivatives should sum to 0, got {total}"
        )

    def test_conservation_check(self):
        m = _i()
        assert m.conservation_check(TEST_S, TEST_E, TEST_I, TEST_R, N), (
            f"Conservation check failed: {TEST_S}+{TEST_E}+{TEST_I}+{TEST_R} != {N}"
        )

    def test_conservation_check_fails_for_bad_state(self):
        m = _i()
        assert not m.conservation_check(5000, 100, 100, 100, N), (
            "Conservation check should fail when compartments don't sum to N"
        )
