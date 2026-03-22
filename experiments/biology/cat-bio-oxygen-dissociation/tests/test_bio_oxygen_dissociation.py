"""cat-bio-oxygen-dissociation — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from bio_oxygen_dissociation_constants import *
IMPL = Path(__file__).parent.parent / "bio_oxygen_dissociation.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_p50_is_26_6_not_27(self):
        """P50 at normal pH 7.4 must be 26.6, not 27."""
        assert P50_NORMAL == 26.6, f"P50 should be 26.6, got {P50_NORMAL}"
        assert P50_NORMAL != 27.0, "P50 must NOT be 27"
        assert P50_NORMAL != 27, "P50 must NOT be 27"

    def test_p50_is_26_6_not_30(self):
        """P50 at normal pH 7.4 must be 26.6, not 30."""
        assert P50_NORMAL != 30.0, "P50 at normal pH is 26.6, NOT 30"
        assert P50_NORMAL != 30, "P50 at normal pH is 26.6, NOT 30"

    def test_bohr_effect_shifts_p50(self):
        """Bohr effect must shift P50: lower pH -> higher P50."""
        m = _i()
        p50_acidic = m.p50_at_ph(7.2)
        p50_normal = m.p50_at_ph(7.4)
        p50_alkaline = m.p50_at_ph(7.6)
        assert p50_acidic > p50_normal, \
            f"pH 7.2 P50 ({p50_acidic}) should be > pH 7.4 P50 ({p50_normal})"
        assert p50_alkaline < p50_normal, \
            f"pH 7.6 P50 ({p50_alkaline}) should be < pH 7.4 P50 ({p50_normal})"

    def test_bohr_not_ignored(self):
        """P50 must NOT be the same at all pH values (ignores_bohr error)."""
        m = _i()
        vals = {m.p50_at_ph(ph) for ph in [7.0, 7.2, 7.4, 7.6, 7.8]}
        assert len(vals) > 1, "P50 should vary with pH (Bohr effect)"

    def test_hill_coefficient_not_4(self):
        """Hill coefficient n must be ~2.8, NOT 4 (binding sites)."""
        assert N_HILL != HB_BINDING_SITES, \
            f"n={N_HILL} must not equal binding sites={HB_BINDING_SITES}"
        assert math.isclose(N_HILL, 2.8, rel_tol=1e-9), \
            f"Hill coefficient should be 2.8, got {N_HILL}"


class TestCorrectness:
    def test_saturation_at_p50_is_half(self):
        """Y(P50) must equal 0.5 for any n (definition of P50)."""
        m = _i()
        for n in [1.0, 2.0, 2.8, 4.0]:
            Y = m.o2_saturation(P50_NORMAL, P50_NORMAL, n)
            assert math.isclose(Y, 0.5, rel_tol=1e-9), \
                f"Y(P50) should be 0.5 for n={n}, got {Y}"

    def test_arterial_saturation(self):
        """Y(100 mmHg) at normal pH should be ~97 % (arterial blood)."""
        m = _i()
        Y = m.o2_saturation(100.0, P50_NORMAL, N_HILL)
        assert math.isclose(Y, Y_AT_100, rel_tol=1e-6), \
            f"Y(100) = {Y}, expected {Y_AT_100}"
        assert Y > 0.95, f"Arterial saturation should be > 95 %, got {Y}"

    def test_venous_saturation(self):
        """Y(40 mmHg) at normal pH should be ~75 % (venous blood)."""
        m = _i()
        Y = m.o2_saturation(40.0, P50_NORMAL, N_HILL)
        assert math.isclose(Y, Y_AT_40, rel_tol=1e-6), \
            f"Y(40) = {Y}, expected {Y_AT_40}"
        assert 0.70 < Y < 0.85, f"Venous saturation should be ~75 %, got {Y}"

    def test_zero_pO2_gives_zero(self):
        """Y(0) must be 0."""
        m = _i()
        Y = m.o2_saturation(0.0, P50_NORMAL, N_HILL)
        assert Y == 0.0, f"Y(0) should be 0, got {Y}"

    def test_bohr_direction_right(self):
        """pH < 7.4 should give a right shift."""
        m = _i()
        assert m.bohr_shift_direction(7.2) == "right"
        assert m.bohr_shift_direction(7.0) == "right"

    def test_bohr_direction_left(self):
        """pH > 7.4 should give a left shift."""
        m = _i()
        assert m.bohr_shift_direction(7.6) == "left"
        assert m.bohr_shift_direction(7.8) == "left"

    def test_bohr_direction_none(self):
        """pH == 7.4 should give no shift."""
        m = _i()
        assert m.bohr_shift_direction(7.4) == "none"

    def test_p50_at_ph_values(self):
        """P50 at specific pH values should match frozen constants."""
        m = _i()
        assert math.isclose(m.p50_at_ph(7.4), P50_PH_7_4, rel_tol=1e-9)
        assert math.isclose(m.p50_at_ph(7.2), P50_PH_7_2, rel_tol=1e-6)
        assert math.isclose(m.p50_at_ph(7.6), P50_PH_7_6, rel_tol=1e-6)

    def test_saturation_monotonic(self):
        """O2 saturation must increase monotonically with pO2."""
        m = _i()
        prev = 0.0
        for pO2 in [0, 10, 20, 30, 40, 60, 80, 100, 150]:
            Y = m.o2_saturation(float(pO2), P50_NORMAL, N_HILL)
            assert Y >= prev, f"Y({pO2}) = {Y} < Y(prev) = {prev}"
            prev = Y
