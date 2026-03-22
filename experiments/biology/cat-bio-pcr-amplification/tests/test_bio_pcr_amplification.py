"""cat-bio-pcr-amplification — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from bio_pcr_amplification_constants import *
IMPL = Path(__file__).parent.parent / "bio_pcr_amplification.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_real_yield_less_than_ideal(self):
        """At E=0.95, real yield must be strictly less than ideal yield."""
        m = _i()
        real = m.pcr_yield(N0, E_TYPICAL, CYCLES)
        ideal = m.ideal_yield(N0, CYCLES)
        assert real < ideal, \
            f"Real yield {real} should be < ideal yield {ideal}"
        # The ratio should be roughly 0.47, nowhere near 1.0
        ratio = real / ideal
        assert ratio < 0.50, \
            f"Real/ideal ratio {ratio:.4f} is too high — efficiency < 1 matters!"

    def test_efficiency_must_be_at_most_1(self):
        """Efficiency E > 1 is physically impossible — must raise ValueError."""
        m = _i()
        with pytest.raises(ValueError):
            m.pcr_yield(1, 1.01, 30)
        with pytest.raises(ValueError):
            m.pcr_yield(1, 2.0, 30)
        with pytest.raises(ValueError):
            m.fold_amplification(1.5, 30)
        with pytest.raises(ValueError):
            m.cycles_needed(1e6, 1.1)

    def test_efficiency_must_be_positive(self):
        """Efficiency E ≤ 0 is invalid."""
        m = _i()
        with pytest.raises(ValueError):
            m.pcr_yield(1, 0.0, 30)
        with pytest.raises(ValueError):
            m.pcr_yield(1, -0.5, 30)

    def test_not_linear_growth(self):
        """PCR is exponential, not linear — doubling cycles must more than double yield."""
        m = _i()
        y15 = m.pcr_yield(N0, E_TYPICAL, 15)
        y30 = m.pcr_yield(N0, E_TYPICAL, 30)
        # If linear, y30 ≈ 2*y15. Exponential means y30 >> 2*y15.
        assert y30 > 2 * y15, \
            f"PCR must be exponential: yield(30)={y30} should be >> 2*yield(15)={2*y15}"
        # In fact y30 = y15^2 / N0 for exponential growth
        assert math.isclose(y30, y15 ** 2 / N0, rel_tol=1e-9), \
            "Exponential identity: N(2c) = N(c)^2 / N₀"


class TestCorrectness:
    def test_ideal_yield_30_cycles(self):
        m = _i()
        result = m.ideal_yield(N0, CYCLES)
        assert result == N_IDEAL_30, \
            f"Ideal yield at 30 cycles: {result}, expected {N_IDEAL_30}"

    def test_real_yield_30_cycles(self):
        m = _i()
        result = m.pcr_yield(N0, E_TYPICAL, CYCLES)
        assert math.isclose(result, N_REAL_30, rel_tol=1e-9), \
            f"Real yield at 30 cycles: {result}, expected {N_REAL_30}"

    def test_ratio_real_to_ideal(self):
        m = _i()
        real = m.pcr_yield(N0, E_TYPICAL, CYCLES)
        ideal = m.ideal_yield(N0, CYCLES)
        ratio = real / ideal
        assert math.isclose(ratio, RATIO, rel_tol=1e-9), \
            f"Ratio: {ratio}, expected {RATIO}"

    def test_fold_amplification(self):
        m = _i()
        fold = m.fold_amplification(E_TYPICAL, CYCLES)
        assert math.isclose(fold, (1 + E_TYPICAL) ** CYCLES, rel_tol=1e-9), \
            f"Fold: {fold}, expected {(1 + E_TYPICAL) ** CYCLES}"

    def test_cycles_needed_1M_fold(self):
        m = _i()
        c = m.cycles_needed(1e6, E_TYPICAL)
        assert c == CYCLES_FOR_1M_FOLD, \
            f"Cycles for 1M-fold: {c}, expected {CYCLES_FOR_1M_FOLD}"
        # Verify: (1+E)^c >= 1e6 but (1+E)^(c-1) < 1e6
        assert m.fold_amplification(E_TYPICAL, c) >= 1e6
        assert m.fold_amplification(E_TYPICAL, c - 1) < 1e6

    def test_pcr_yield_zero_cycles(self):
        m = _i()
        assert m.pcr_yield(100, E_TYPICAL, 0) == 100, \
            "Zero cycles should return N₀ unchanged"

    def test_ideal_yield_equals_pcr_yield_at_E1(self):
        """When E=1.0 (perfect efficiency), pcr_yield must equal ideal_yield."""
        m = _i()
        for c in [0, 1, 10, 20, 30]:
            assert m.pcr_yield(N0, 1.0, c) == m.ideal_yield(N0, c), \
                f"At E=1.0, pcr_yield and ideal_yield must agree (c={c})"

    def test_cycles_needed_validation(self):
        m = _i()
        with pytest.raises(ValueError):
            m.cycles_needed(0.5, E_TYPICAL)  # target_fold must be > 1
        with pytest.raises(ValueError):
            m.cycles_needed(1e6, 0.0)  # efficiency must be > 0
