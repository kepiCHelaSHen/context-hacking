"""cat-phys-thermodynamic-processes — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from phys_thermodynamic_processes_constants import *
IMPL = Path(__file__).parent.parent / "phys_thermodynamic_processes.py"
def _import_impl():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; spec = importlib.util.spec_from_file_location("impl", IMPL); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

class TestPriorErrors:
    def test_isothermal_uses_ln(self):
        mod = _import_impl()
        W = mod.isothermal_work(N_TEST, T_TEST, V1_TEST, V2_TEST)
        assert abs(W - W_ISOTHERMAL) / abs(W_ISOTHERMAL) < 0.001
    def test_work_positive_on_expansion(self):
        mod = _import_impl()
        assert mod.isothermal_work(1, 300, 0.001, 0.002) > 0
    def test_adiabatic_gamma_diatomic(self):
        mod = _import_impl()
        T2 = mod.adiabatic_final_T(T_TEST, V1_TEST, V2_TEST, GAMMA_DI)
        assert abs(T2 - T2_ADIABATIC_DI) < 1.0
class TestCorrectness:
    def test_isochoric_zero(self):
        mod = _import_impl()
        assert mod.isochoric_work() == 0.0
    def test_cv_cp_relation(self):
        mod = _import_impl()
        Cv = mod.cv_from_gamma(GAMMA_DI)
        Cp = mod.cp_from_gamma(GAMMA_DI)
        assert abs(Cp - Cv - R) < 0.01
