"""earth-richter-scale — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from earth_richter_scale_constants import *

IMPL = Path(__file__).parent.parent / "earth_richter_scale.py"


def _import_impl():
    if not IMPL.exists():
        pytest.skip("implementation not yet written")
    import importlib.util
    spec = importlib.util.spec_from_file_location("impl", IMPL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestPriorErrors:
    """Each test catches one known LLM prior error."""

    def test_energy_ratio_not_10x(self):
        """PRIOR_ERROR: 10x_energy — energy ratio per +1 Mw is ~31.6, not 10."""
        mod = _import_impl()
        ratio = mod.energy_ratio(1.0)
        # Must be ~31.623, NOT 10
        assert abs(ratio - 31.623) < 0.1, f"Energy ratio should be ~31.6, got {ratio}"
        assert ratio > 30.0, "Energy ratio must be >> 10"

    def test_moment_magnitude_not_richter(self):
        """PRIOR_ERROR: richter_not_moment — must use Mw formula, not ML."""
        mod = _import_impl()
        # M0 = 1e20 N·m should give Mw ~7.267 via moment magnitude formula
        Mw = mod.moment_magnitude(1e20)
        assert abs(Mw - 7.2667) < 0.01, f"Mw should be ~7.267, got {Mw}"

    def test_magnitude_is_logarithmic(self):
        """PRIOR_ERROR: magnitude_linear — magnitude is log scale."""
        mod = _import_impl()
        # 10x more seismic moment should give ~0.667 higher Mw (not 10x higher)
        Mw1 = mod.moment_magnitude(1e18)
        Mw2 = mod.moment_magnitude(1e19)
        delta = Mw2 - Mw1
        assert abs(delta - MW_COEFF) < 0.01, (
            f"10x M0 should add {MW_COEFF:.3f} to Mw, got delta={delta:.4f}"
        )


class TestCorrectness:
    """Each test verifies result against frozen spec."""

    def test_reference_moment_magnitude(self):
        """M0=1e20 N·m -> Mw = (2/3)*(20-9.1) = 7.2667."""
        mod = _import_impl()
        Mw = mod.moment_magnitude(REF_M0_NM)
        assert abs(Mw - REF_MW_EXPECTED) < 1e-4, f"Expected {REF_MW_EXPECTED}, got {Mw}"

    def test_energy_from_magnitude(self):
        """log10(E) = 1.5*Mw + 4.8."""
        mod = _import_impl()
        Mw = 7.0
        E = mod.energy_from_magnitude(Mw)
        expected_log = ENERGY_SLOPE * Mw + ENERGY_OFFSET
        assert abs(math.log10(E) - expected_log) < 1e-6

    def test_energy_ratio_unit_step(self):
        """Energy ratio for +1 Mw = 10^1.5 = 31.623."""
        mod = _import_impl()
        ratio = mod.energy_ratio(1.0)
        assert abs(ratio - REF_ENERGY_RATIO) < 0.001

    def test_energy_ratio_two_steps(self):
        """Energy ratio for +2 Mw = 10^3.0 = 1000."""
        mod = _import_impl()
        ratio = mod.energy_ratio(2.0)
        assert abs(ratio - 1000.0) < 0.01

    def test_amplitude_ratio(self):
        """+1 magnitude = 10x amplitude."""
        mod = _import_impl()
        assert abs(mod.amplitude_ratio(1.0) - AMPLITUDE_FACTOR_PER_UNIT) < 1e-9

    def test_amplitude_ratio_two_steps(self):
        """+2 magnitude = 100x amplitude."""
        mod = _import_impl()
        assert abs(mod.amplitude_ratio(2.0) - 100.0) < 1e-6

    def test_round_trip_M0_Mw(self):
        """M0 -> Mw -> M0 round-trip."""
        mod = _import_impl()
        M0_orig = 3.5e22
        Mw = mod.moment_magnitude(M0_orig)
        M0_back = mod.seismic_moment_from_Mw(Mw)
        assert abs(M0_back / M0_orig - 1.0) < 1e-9

    def test_energy_consistency(self):
        """energy_from_magnitude(Mw+1) / energy_from_magnitude(Mw) = energy_ratio(1)."""
        mod = _import_impl()
        E7 = mod.energy_from_magnitude(7.0)
        E8 = mod.energy_from_magnitude(8.0)
        ratio_direct = E8 / E7
        ratio_func = mod.energy_ratio(1.0)
        assert abs(ratio_direct / ratio_func - 1.0) < 1e-9
