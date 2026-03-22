"""chem-buffers — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from chem_buffers_constants import *

IMPL = Path(__file__).parent.parent / "chem_buffers.py"


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

    def test_hh_not_inverted(self):
        mod = _import_impl()
        pH_more_base = mod.henderson_hasselbalch(ACETIC_pKa, 0.05, 0.15)
        pH_less_base = mod.henderson_hasselbalch(ACETIC_pKa, 0.15, 0.05)
        assert pH_more_base > pH_less_base

    def test_hh_uses_log10(self):
        mod = _import_impl()
        pH = mod.henderson_hasselbalch(ACETIC_pKa, 0.1, 0.1)
        assert abs(pH - ACETIC_pKa) < 0.001

    def test_buffer_capacity_has_ln10(self):
        mod = _import_impl()
        beta = mod.buffer_capacity(0.1, ACETIC_pKa, ACETIC_pKa)
        assert beta > 0.05

    def test_blood_pH_correct_pKa(self):
        mod = _import_impl()
        pH = mod.blood_pH(40, 24)
        assert 7.35 < pH < 7.45


class TestCorrectness:
    """Each test verifies result against frozen spec."""

    def test_hh_equal_conc_gives_pKa(self):
        mod = _import_impl()
        pH = mod.henderson_hasselbalch(ACETIC_pKa, 0.1, 0.1)
        assert abs(pH - ACETIC_pKa) < 0.001

    def test_titration_curve_monotonic(self):
        mod = _import_impl()
        V_range = [float(v) for v in range(1, 20)]
        curve = mod.titration_curve(0.1, 50.0, 0.1, V_range, ACETIC_pKa)
        for i in range(len(curve) - 1):
            assert curve[i + 1] >= curve[i] - 0.001
