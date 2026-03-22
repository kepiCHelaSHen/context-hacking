"""cat-eng-stress-strain — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from eng_stress_strain_constants import *
IMPL = Path(__file__).parent.parent / "eng_stress_strain.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    """Catch the known LLM failure modes."""

    def test_true_stress_not_engineering(self):
        """True stress must differ from engineering stress — the #1 LLM error."""
        m = _i()
        sig_e = m.engineering_stress(F_REF, A0_REF)
        eps_e = m.engineering_strain(DL_REF, L0_REF)
        sig_t = m.true_stress(sig_e, eps_e)
        assert abs(sig_t - SIGMA_TRUE_REF) < 1.0
        assert abs(sig_t - SIGMA_TRUE_WRONG) > 1e6, \
            "true_stress == engineering_stress — forgot (1 + eps_eng) factor!"

    def test_true_strain_not_linear(self):
        """True strain = ln(1+eps_eng), NOT eps_eng itself."""
        m = _i()
        eps_e = m.engineering_strain(DL_REF, L0_REF)
        eps_t = m.true_strain(eps_e)
        assert abs(eps_t - EPS_TRUE_REF) < 1e-9
        assert abs(eps_t - EPS_TRUE_WRONG) > 1e-6, \
            "true_strain == engineering_strain — used dL/L0 instead of ln(1+eps_eng)!"

    def test_true_strain_uses_log(self):
        """At larger strain, the difference between log and linear is very clear."""
        m = _i()
        eps_eng_large = 0.5  # 50% extension
        eps_t = m.true_strain(eps_eng_large)
        expected = math.log(1.5)  # 0.40546...
        assert abs(eps_t - expected) < 1e-10, \
            "true_strain should use ln(1+eps_eng), not eps_eng"
        # Linear approximation would give 0.5, off by ~23%
        assert abs(eps_t - eps_eng_large) > 0.09

    def test_modulus_elastic_region(self):
        """Young's modulus computed in elastic region gives consistent E."""
        m = _i()
        sig_e = m.engineering_stress(F_REF, A0_REF)
        eps_e = m.engineering_strain(DL_REF, L0_REF)
        E = m.youngs_modulus(sig_e, eps_e)
        assert abs(E - E_REF) < 1.0


class TestCorrectness:
    """Verify numerical accuracy of all functions."""

    def test_engineering_stress_value(self):
        m = _i(); sig = m.engineering_stress(F_REF, A0_REF)
        assert abs(sig - 500e6) < 1.0

    def test_engineering_strain_value(self):
        m = _i(); eps = m.engineering_strain(DL_REF, L0_REF)
        assert abs(eps - 0.005) < 1e-12

    def test_true_stress_value(self):
        m = _i()
        sig_t = m.true_stress(SIGMA_ENG_REF, EPS_ENG_REF)
        assert abs(sig_t - 502.5e6) < 1.0

    def test_true_strain_value(self):
        m = _i()
        eps_t = m.true_strain(EPS_ENG_REF)
        assert abs(eps_t - math.log(1.005)) < 1e-12

    def test_youngs_modulus_value(self):
        m = _i(); E = m.youngs_modulus(SIGMA_ENG_REF, EPS_ENG_REF)
        assert abs(E - 100e9) < 1.0

    def test_true_stress_greater_than_engineering(self):
        """Under tension, true stress is always > engineering stress."""
        m = _i()
        sig_t = m.true_stress(SIGMA_ENG_REF, EPS_ENG_REF)
        assert sig_t > SIGMA_ENG_REF

    def test_true_strain_less_than_engineering(self):
        """For positive strain, true strain < engineering strain."""
        m = _i()
        eps_t = m.true_strain(EPS_ENG_REF)
        assert eps_t < EPS_ENG_REF

    def test_strain_converge_at_small_values(self):
        """At very small strain, true and engineering strain nearly equal."""
        m = _i()
        tiny_eps = 1e-6
        eps_t = m.true_strain(tiny_eps)
        assert abs(eps_t - tiny_eps) < 1e-12

    def test_stress_zero_strain(self):
        """At zero strain, true stress = engineering stress."""
        m = _i()
        sig_t = m.true_stress(500e6, 0.0)
        assert abs(sig_t - 500e6) < 1e-6
