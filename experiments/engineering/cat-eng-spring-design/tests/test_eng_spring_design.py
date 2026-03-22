"""cat-eng-spring-design — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from eng_spring_design_constants import *
IMPL = Path(__file__).parent.parent / "eng_spring_design.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    """Catch the known LLM failure modes."""

    def test_wahl_factor_applied(self):
        """Corrected stress must differ from basic stress — Wahl factor must be applied."""
        m = _i()
        tau_b = m.basic_shear_stress(F_REF, D_REF, D_WIRE_REF)
        tau_c = m.corrected_shear_stress(F_REF, D_REF, D_WIRE_REF)
        assert tau_c > tau_b * 1.05, "Corrected stress should be significantly higher than basic — Wahl factor missing!"

    def test_corrected_stress_matches_reference(self):
        """tau_corrected must match K_W * 8FD/(pi*d^3), not just 8FD/(pi*d^3)."""
        m = _i()
        tau_c = m.corrected_shear_stress(F_REF, D_REF, D_WIRE_REF)
        assert abs(tau_c - TAU_CORRECTED_REF) / TAU_CORRECTED_REF < 1e-9
        # Must NOT equal uncorrected value
        assert abs(tau_c - TAU_BASIC_REF) / TAU_BASIC_REF > 0.1, "Returning basic stress without Wahl correction!"

    def test_spring_index_not_inverted(self):
        """C = D/d, NOT d/D. For D=30mm d=5mm, C=6 not 0.167."""
        m = _i()
        C = m.spring_index(D_REF, D_WIRE_REF)
        assert abs(C - C_REF) < 1e-12
        assert abs(C - C_WRONG_INVERTED) > 1.0, "C is inverted! Using d/D instead of D/d!"

    def test_wahl_factor_not_from_inverted_c(self):
        """K_W from correct C=6 should be ~1.25, not ~3.79 from inverted C."""
        m = _i()
        K_W = m.wahl_factor(C_REF)
        assert abs(K_W - K_W_REF) < 1e-9
        assert abs(K_W - K_W_WRONG_INVERTED) > 1.0, "Wahl factor computed from inverted C!"

    def test_spring_rate_d_to_fourth(self):
        """Spring rate k = Gd^4/(8D^3N) — must use d^4, not d^3."""
        m = _i()
        k = m.spring_rate(G_REF, D_WIRE_REF, D_REF, N_COILS_REF)
        assert abs(k - K_RATE_REF) / K_RATE_REF < 1e-9
        assert abs(k - K_RATE_WRONG_D3) / K_RATE_WRONG_D3 > 0.5, "Using d^3 instead of d^4 in spring rate!"

    def test_spring_rate_D_cubed(self):
        """Spring rate k = Gd^4/(8D^3N) — must use D^3, not D^2."""
        m = _i()
        k = m.spring_rate(G_REF, D_WIRE_REF, D_REF, N_COILS_REF)
        assert abs(k - K_RATE_WRONG_D2) / K_RATE_WRONG_D2 > 0.5, "Using D^2 instead of D^3 in spring rate!"


class TestCorrectness:
    """Verify numerical accuracy of all functions."""

    def test_spring_index_value(self):
        m = _i(); C = m.spring_index(D_REF, D_WIRE_REF)
        assert abs(C - 6.0) < 1e-12

    def test_spring_index_proportionality(self):
        """Doubling D should double C."""
        m = _i()
        C1 = m.spring_index(D_REF, D_WIRE_REF)
        C2 = m.spring_index(2 * D_REF, D_WIRE_REF)
        assert abs(C2 / C1 - 2.0) < 1e-12

    def test_wahl_factor_value(self):
        m = _i(); K_W = m.wahl_factor(C_REF)
        assert abs(K_W - 1.2525) < 1e-9

    def test_wahl_factor_always_gt_one(self):
        """K_W > 1 for all practical spring indices C=4..12."""
        m = _i()
        for C in [4, 5, 6, 7, 8, 10, 12]:
            K_W = m.wahl_factor(C)
            assert K_W > 1.0, f"K_W={K_W} <= 1 at C={C}!"

    def test_wahl_factor_decreases_with_c(self):
        """K_W decreases as C increases (larger C = less curvature effect)."""
        m = _i()
        Kw_prev = m.wahl_factor(4)
        for C in [5, 6, 7, 8, 10, 12]:
            Kw = m.wahl_factor(C)
            assert Kw < Kw_prev, f"K_W should decrease: K_W({C})={Kw} >= K_W(prev)={Kw_prev}"
            Kw_prev = Kw

    def test_basic_shear_stress_value(self):
        m = _i(); tau = m.basic_shear_stress(F_REF, D_REF, D_WIRE_REF)
        assert abs(tau - TAU_BASIC_REF) / TAU_BASIC_REF < 1e-9

    def test_basic_shear_stress_magnitude(self):
        """tau_basic should be ~61 MPa for reference spring."""
        m = _i(); tau = m.basic_shear_stress(F_REF, D_REF, D_WIRE_REF)
        assert 60e6 < tau < 63e6, f"Expected ~61 MPa, got {tau/1e6:.2f} MPa"

    def test_corrected_stress_value(self):
        m = _i(); tau = m.corrected_shear_stress(F_REF, D_REF, D_WIRE_REF)
        assert abs(tau - TAU_CORRECTED_REF) / TAU_CORRECTED_REF < 1e-9

    def test_corrected_stress_magnitude(self):
        """tau_corrected should be ~76.5 MPa for reference spring."""
        m = _i(); tau = m.corrected_shear_stress(F_REF, D_REF, D_WIRE_REF)
        assert 75e6 < tau < 78e6, f"Expected ~76.5 MPa, got {tau/1e6:.2f} MPa"

    def test_correction_ratio(self):
        """Corrected/basic ratio must equal K_W."""
        m = _i()
        tau_b = m.basic_shear_stress(F_REF, D_REF, D_WIRE_REF)
        tau_c = m.corrected_shear_stress(F_REF, D_REF, D_WIRE_REF)
        assert abs(tau_c / tau_b - K_W_REF) < 1e-9

    def test_spring_rate_value(self):
        m = _i(); k = m.spring_rate(G_REF, D_WIRE_REF, D_REF, N_COILS_REF)
        assert abs(k - K_RATE_REF) / K_RATE_REF < 1e-9

    def test_spring_rate_magnitude(self):
        """k should be ~22.9 kN/m for reference spring."""
        m = _i(); k = m.spring_rate(G_REF, D_WIRE_REF, D_REF, N_COILS_REF)
        assert 20e3 < k < 25e3, f"Expected ~22.9 kN/m, got {k/1e3:.2f} kN/m"

    def test_stress_proportional_to_force(self):
        """Doubling F should double both basic and corrected stress."""
        m = _i()
        tb1 = m.basic_shear_stress(F_REF, D_REF, D_WIRE_REF)
        tb2 = m.basic_shear_stress(2 * F_REF, D_REF, D_WIRE_REF)
        assert abs(tb2 / tb1 - 2.0) < 1e-12
        tc1 = m.corrected_shear_stress(F_REF, D_REF, D_WIRE_REF)
        tc2 = m.corrected_shear_stress(2 * F_REF, D_REF, D_WIRE_REF)
        assert abs(tc2 / tc1 - 2.0) < 1e-12

    def test_spring_rate_inversely_proportional_to_N(self):
        """Doubling active coils should halve spring rate."""
        m = _i()
        k1 = m.spring_rate(G_REF, D_WIRE_REF, D_REF, N_COILS_REF)
        k2 = m.spring_rate(G_REF, D_WIRE_REF, D_REF, 2 * N_COILS_REF)
        assert abs(k1 / k2 - 2.0) < 1e-12
