"""eng-reynolds-number — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from eng_reynolds_number_constants import *

IMPL = Path(__file__).parent.parent / "eng_reynolds_number.py"


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

    def test_uses_diameter_not_radius(self):
        """PRIOR_ERROR: uses_radius — must use D, not r."""
        mod = _import_impl()
        Re = mod.reynolds_number(WATER_RHO, TEST_VELOCITY, TEST_DIAMETER, WATER_MU)
        # Correct value ~49800; radius error gives ~24900
        assert abs(Re - TEST_RE_CORRECT) < 1.0, (
            f"Re={Re:.1f}, expected {TEST_RE_CORRECT} — did you use radius instead of diameter?"
        )

    def test_laminar_transition_at_2300(self):
        """PRIOR_ERROR: wrong_transition — laminar limit is 2300, not 2000 or 4000."""
        mod = _import_impl()
        # Re = 2200 is laminar (below 2300)
        assert mod.flow_regime(2200) == "laminar"
        # Re = 2300 is transition (at boundary)
        assert mod.flow_regime(2300) == "transition"
        # Re = 2100 is still laminar (rejects 2000 boundary)
        assert mod.flow_regime(2100) == "laminar"

    def test_viscosity_not_swapped(self):
        """PRIOR_ERROR: viscosity_swap — μ and ν give same Re when consistent."""
        mod = _import_impl()
        Re_dynamic = mod.reynolds_number(WATER_RHO, TEST_VELOCITY, TEST_DIAMETER, WATER_MU)
        Re_kinematic = mod.reynolds_kinematic(TEST_VELOCITY, TEST_DIAMETER, WATER_NU)
        # Both must agree within 0.5% (small diff from rounded ν)
        assert abs(Re_dynamic - Re_kinematic) / Re_dynamic < 0.005, (
            f"Dynamic Re={Re_dynamic:.1f} vs Kinematic Re={Re_kinematic:.1f} — viscosity confusion?"
        )


class TestCorrectness:
    """Each test verifies result against frozen spec."""

    def test_reynolds_pipe_flow(self):
        mod = _import_impl()
        Re = mod.reynolds_number(WATER_RHO, TEST_VELOCITY, TEST_DIAMETER, WATER_MU)
        assert abs(Re - TEST_RE_CORRECT) < 1.0

    def test_flow_regime_boundaries(self):
        mod = _import_impl()
        assert mod.flow_regime(1000) == "laminar"
        assert mod.flow_regime(2299) == "laminar"
        assert mod.flow_regime(2300) == "transition"
        assert mod.flow_regime(3000) == "transition"
        assert mod.flow_regime(4000) == "transition"
        assert mod.flow_regime(4001) == "turbulent"
        assert mod.flow_regime(50000) == "turbulent"

    def test_reynolds_kinematic(self):
        mod = _import_impl()
        Re = mod.reynolds_kinematic(TEST_VELOCITY, TEST_DIAMETER, WATER_NU)
        assert abs(Re - TEST_RE_CORRECT) / TEST_RE_CORRECT < 0.005

    def test_hydraulic_diameter_circular(self):
        """Dh of a circle = D (sanity check)."""
        mod = _import_impl()
        A = math.pi * TEST_DIAMETER**2 / 4
        P = math.pi * TEST_DIAMETER
        Dh = mod.hydraulic_diameter(A, P)
        assert abs(Dh - TEST_DIAMETER) < 1e-10

    def test_hydraulic_diameter_square(self):
        """Dh of a square duct with side s = s (4*s²/(4s) = s)."""
        mod = _import_impl()
        s = 0.05
        Dh = mod.hydraulic_diameter(s**2, 4 * s)
        assert abs(Dh - s) < 1e-10

    def test_turbulent_regime_for_test_case(self):
        """The standard test case (Re≈49800) must be turbulent."""
        mod = _import_impl()
        Re = mod.reynolds_number(WATER_RHO, TEST_VELOCITY, TEST_DIAMETER, WATER_MU)
        assert mod.flow_regime(Re) == "turbulent"
