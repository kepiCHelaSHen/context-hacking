"""chem-equilibrium — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from chem_equilibrium_constants import *

IMPL = Path(__file__).parent.parent / "chem_equilibrium.py"


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

    def test_kp_kc_differ_when_delta_n_nonzero(self):
        mod = _import_impl()
        Kc = mod.kp_to_kc(HABER_Kp_298, HABER_delta_n, 298.15)
        assert abs(Kc - HABER_Kp_298) / HABER_Kp_298 > 0.01

    def test_van_t_hoff_K_decreases_with_T_for_exothermic(self):
        mod = _import_impl()
        K700 = mod.van_t_hoff(HABER_Kp_298, 298.15, 700, HABER_dH)
        assert K700 < HABER_Kp_298

    def test_pH_water_varies_with_temperature(self):
        mod = _import_impl()
        assert mod.pH_from_Kw(310) < 7.0
        assert mod.pH_from_Kw(373) < mod.pH_from_Kw(310)

    def test_hi_kc_is_57_not_54(self):
        assert abs(HI_Kc_700K - 57.0) < 0.1


class TestCorrectness:
    """Each test verifies result against frozen spec."""

    def test_kp_kc_roundtrip(self):
        mod = _import_impl()
        Kc = mod.kp_to_kc(HABER_Kp_298, HABER_delta_n, 298.15)
        Kp_back = mod.kc_to_kp(Kc, HABER_delta_n, 298.15)
        assert abs(Kp_back - HABER_Kp_298) / HABER_Kp_298 < 0.001

    def test_van_t_hoff_matches_frozen_700K(self):
        mod = _import_impl()
        K700 = mod.van_t_hoff(HABER_Kp_298, 298.15, 700, HABER_dH)
        ratio = K700 / HABER_Kp_700
        assert 0.1 < ratio < 10  # within order of magnitude

    def test_pH_25C_near_7(self):
        mod = _import_impl()
        pH = mod.pH_from_Kw(298.15)
        assert abs(pH - 6.998) < 0.05
