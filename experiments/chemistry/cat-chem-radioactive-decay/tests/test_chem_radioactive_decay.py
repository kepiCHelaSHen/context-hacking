"""chem-radioactive-decay — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from chem_radioactive_decay_constants import *

IMPL = Path(__file__).parent.parent / "chem_radioactive_decay.py"


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

    def test_c14_uses_5730_not_5568(self):
        mod = _import_impl()
        age = mod.c14_age(0.5)
        assert abs(age - 5730) < 10
        assert abs(age - C14_LIBBY_WRONG) > 100

    def test_secular_eq_not_equal_atoms(self):
        mod = _import_impl()
        lam1 = mod.decay_constant(U238_HALF_LIFE)
        lam2 = mod.decay_constant(TH234_HALF_LIFE)
        ratio = mod.secular_eq_ratio(lam1, lam2)
        assert ratio < 1e-6
        assert ratio != 1.0


class TestCorrectness:
    """Each test verifies result against frozen spec."""

    def test_half_life_gives_half(self):
        mod = _import_impl()
        N = mod.n_remaining(1000, C14_HALF_LIFE, C14_HALF_LIFE)
        assert abs(N - 500) < 0.1

    def test_ra226_exactly_1600(self):
        assert abs(RA226_HALF_LIFE - 1600.0) < 0.01
