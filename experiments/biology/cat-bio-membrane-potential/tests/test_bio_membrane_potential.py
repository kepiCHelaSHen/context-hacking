"""cat-bio-membrane-potential — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from bio_membrane_potential_constants import *
IMPL = Path(__file__).parent.parent / "bio_membrane_potential.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

class TestPriorErrors:
    def test_chloride_potential_is_negative(self):
        """z_always_1: E_Cl must be negative (z=-1 flips sign)."""
        m = _i()
        e_cl = m.nernst(Z_CL, CL_OUT, CL_IN)
        assert e_cl < 0, "E_Cl must be negative; z=-1 flips the sign"

    def test_uses_kelvin_not_celsius(self):
        """celsius_not_kelvin: RT/F at 310.15 K ~ 0.02673 V, not at 37."""
        m = _i()
        rtf_correct = m.rt_over_f(310.15)
        rtf_celsius_bug = m.rt_over_f(37.0)
        assert abs(rtf_correct - 0.02673) < 0.001
        assert rtf_celsius_bug < 0.005, "RT/F at T=37 (Celsius bug) would be tiny"

    def test_wrong_ratio_direction_flips_sign(self):
        """wrong_ratio_direction: using in/out instead of out/in reverses sign."""
        m = _i()
        e_k_correct = m.nernst(Z_K, K_OUT, K_IN)
        e_k_flipped = m.nernst(Z_K, K_IN, K_OUT)
        assert e_k_correct < 0
        assert e_k_flipped > 0
        assert abs(e_k_correct + e_k_flipped) < 0.1

class TestCorrectness:
    def test_rt_over_f(self):
        m = _i()
        computed = m.rt_over_f(T)
        assert abs(computed - RT_OVER_F) < 1e-6
        assert abs(computed * 1000 - 26.73) < 0.1

    def test_potassium_equilibrium(self):
        m = _i()
        e_k = m.nernst(Z_K, K_OUT, K_IN)
        assert abs(e_k - E_K) < 0.5

    def test_sodium_equilibrium(self):
        m = _i()
        e_na = m.nernst(Z_NA, NA_OUT, NA_IN)
        assert abs(e_na - E_NA) < 0.5

    def test_chloride_equilibrium(self):
        m = _i()
        e_cl = m.nernst(Z_CL, CL_OUT, CL_IN)
        assert abs(e_cl - E_CL) < 0.5

    def test_valence_zero_raises(self):
        m = _i()
        with pytest.raises(ValueError):
            m.nernst(0, 140, 4)

    def test_negative_concentration_raises(self):
        m = _i()
        with pytest.raises(ValueError):
            m.nernst(1, -5, 140)
