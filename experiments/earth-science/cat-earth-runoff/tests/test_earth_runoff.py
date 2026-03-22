"""cat-earth-runoff — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from earth_runoff_constants import *

IMPL = Path(__file__).parent.parent / "earth_runoff.py"


def _i():
    if not IMPL.exists():
        pytest.skip("implementation not yet written")
    import importlib.util
    s = importlib.util.spec_from_file_location("m", IMPL)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


# ── Prior-error traps ─────────────────────────────────────────────

class TestPriorErrors:
    def test_c_must_be_at_most_1(self):
        """PRIOR_ERROR: c_gt_1 — C is dimensionless [0,1], not a flow rate."""
        m = _i()
        with pytest.raises(ValueError):
            m.rational_method(1.5, 1e-5, 1000.0)
        # Also ensure C=0 and C=1 are valid boundary values
        assert m.rational_method(0.0, 1e-5, 1000.0) == 0.0
        assert m.rational_method(1.0, 1e-5, 1000.0) == pytest.approx(1e-5 * 1000.0, rel=1e-9)

    def test_rational_units_consistency(self):
        """PRIOR_ERROR: rational_units_wrong — SI units must be consistent.
        i in m/s and A in m² must yield Q in m³/s (not mixing in/hr with m²)."""
        m = _i()
        # 50 mm/hr = 1.38889e-5 m/s — use correct conversion
        i_correct = REF_I_M_S
        Q = m.rational_method(REF_C, i_correct, REF_A_M2)
        assert Q == pytest.approx(REF_Q_M3S, rel=1e-4), (
            f"Q should be {REF_Q_M3S:.6f} m³/s, got {Q}"
        )

    def test_cn_formula_correct(self):
        """PRIOR_ERROR: cn_formula_wrong — S = 25400/CN - 254, not some other form."""
        m = _i()
        S = m.scs_storage(REF_CN)
        assert S == pytest.approx(REF_S_MM, rel=1e-4), (
            f"S should be {REF_S_MM:.3f} mm, got {S}"
        )


# ── Correctness tests ────────────────────────────────────────────

class TestRationalMethod:
    def test_reference_calculation(self):
        """C=0.5, i=1.389e-5 m/s, A=10000 m² → Q=0.06944 m³/s."""
        m = _i()
        Q = m.rational_method(REF_C, REF_I_M_S, REF_A_M2)
        assert Q == pytest.approx(REF_Q_M3S, rel=1e-4)

    def test_zero_coefficient(self):
        """C=0 → zero runoff regardless of intensity/area."""
        m = _i()
        assert m.rational_method(0.0, 1e-4, 50000.0) == 0.0

    def test_full_runoff(self):
        """C=1 → Q = i * A exactly."""
        m = _i()
        i, A = 2e-5, 5000.0
        Q = m.rational_method(1.0, i, A)
        assert Q == pytest.approx(i * A, rel=1e-9)

    def test_linearity_in_C(self):
        """Q is linear in C: doubling C doubles Q."""
        m = _i()
        Q1 = m.rational_method(0.3, 1e-5, 10000.0)
        Q2 = m.rational_method(0.6, 1e-5, 10000.0)
        assert Q2 == pytest.approx(2.0 * Q1, rel=1e-9)

    def test_linearity_in_area(self):
        """Q is linear in A: doubling A doubles Q."""
        m = _i()
        Q1 = m.rational_method(0.5, 1e-5, 5000.0)
        Q2 = m.rational_method(0.5, 1e-5, 10000.0)
        assert Q2 == pytest.approx(2.0 * Q1, rel=1e-9)

    def test_rejects_negative_C(self):
        m = _i()
        with pytest.raises(ValueError):
            m.rational_method(-0.1, 1e-5, 1000.0)


class TestSCS:
    def test_storage_reference(self):
        """CN=75 → S = 84.667 mm."""
        m = _i()
        S = m.scs_storage(REF_CN)
        assert S == pytest.approx(REF_S_MM, rel=1e-4)

    def test_storage_cn100(self):
        """CN=100 → S = 0 (impervious surface)."""
        m = _i()
        assert m.scs_storage(100.0) == pytest.approx(0.0, abs=1e-9)

    def test_storage_cn50(self):
        """CN=50 → S = 25400/50 - 254 = 508 - 254 = 254 mm."""
        m = _i()
        assert m.scs_storage(50.0) == pytest.approx(254.0, rel=1e-9)

    def test_runoff_reference(self):
        """P=100 mm, CN=75 → Q ≈ 41.1 mm."""
        m = _i()
        Q = m.scs_runoff(REF_P_MM, REF_CN)
        assert Q == pytest.approx(REF_Q_SCS_MM, rel=1e-3)

    def test_runoff_below_threshold(self):
        """P <= 0.2*S → zero runoff."""
        m = _i()
        S = m.scs_storage(REF_CN)
        Ia = 0.2 * S  # ~16.93 mm
        assert m.scs_runoff(Ia, REF_CN) == 0.0
        assert m.scs_runoff(Ia - 1.0, REF_CN) == 0.0

    def test_runoff_cn100(self):
        """CN=100 (S=0) → all precipitation becomes runoff."""
        m = _i()
        P = 50.0
        Q = m.scs_runoff(P, 100.0)
        assert Q == pytest.approx(P, rel=1e-6)

    def test_runoff_monotone_in_P(self):
        """More rain → more runoff (at fixed CN)."""
        m = _i()
        Q1 = m.scs_runoff(80.0, 75.0)
        Q2 = m.scs_runoff(120.0, 75.0)
        assert Q2 > Q1

    def test_rejects_invalid_cn(self):
        m = _i()
        with pytest.raises(ValueError):
            m.scs_storage(0.0)
        with pytest.raises(ValueError):
            m.scs_storage(101.0)


class TestCoefficientRange:
    def test_pavement_range(self):
        m = _i()
        lo, hi = m.runoff_coefficient_range("pavement")
        assert lo == C_PAVEMENT_MIN
        assert hi == C_PAVEMENT_MAX
        assert 0.0 <= lo <= hi <= 1.0

    def test_grass_range(self):
        m = _i()
        lo, hi = m.runoff_coefficient_range("grass")
        assert lo == C_GRASS_MIN
        assert hi == C_GRASS_MAX

    def test_forest_range(self):
        m = _i()
        lo, hi = m.runoff_coefficient_range("forest")
        assert lo == C_FOREST_MIN
        assert hi == C_FOREST_MAX

    def test_all_ranges_in_unit_interval(self):
        """Every surface type must have C in [0, 1]."""
        m = _i()
        for surf in ["pavement", "grass", "forest", "rooftop", "gravel"]:
            lo, hi = m.runoff_coefficient_range(surf)
            assert 0.0 <= lo <= hi <= 1.0, f"{surf}: ({lo}, {hi}) out of [0,1]"

    def test_unknown_surface_raises(self):
        m = _i()
        with pytest.raises(ValueError):
            m.runoff_coefficient_range("moon_dust")
