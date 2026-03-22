"""cat-phys-entropy — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from phys_entropy_constants import *
IMPL = Path(__file__).parent.parent / "phys_entropy.py"
def _import_impl():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; spec = importlib.util.spec_from_file_location("impl", IMPL); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

class TestPriorErrors:
    def test_mixing_positive(self):
        mod = _import_impl()
        ds = mod.entropy_mixing_ideal(1.0, [0.5, 0.5])
        assert ds > 0
    def test_uses_ln_not_log10(self):
        mod = _import_impl()
        ds = mod.entropy_isothermal_expansion(1.0, 1.0, 2.0)
        assert abs(ds - DS_ISOTHERMAL_DOUBLE) < 0.01
    def test_phase_transition_kelvin(self):
        mod = _import_impl()
        ds = mod.entropy_phase_transition(6010, 273.15)
        assert abs(ds - DS_ICE_MELTING) < 0.1
class TestCorrectness:
    def test_mixing_5050(self):
        mod = _import_impl()
        ds = mod.entropy_mixing_ideal(1.0, [0.5, 0.5])
        assert abs(ds - DS_MIXING_5050) < 0.01
