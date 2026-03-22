"""cat-phys-waves — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from phys_waves_constants import *
IMPL = Path(__file__).parent.parent / "phys_waves.py"
def _import_impl():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; spec = importlib.util.spec_from_file_location("impl", IMPL); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

class TestPriorErrors:
    def test_closed_pipe_odd_only(self):
        mod = _import_impl()
        harmonics = mod.closed_pipe_harmonics(L_TEST, 3)
        ratios = [h / harmonics[0] for h in harmonics]
        for r in ratios:
            assert r % 2 == 1  # all odd multiples
    def test_closed_fundamental_lower(self):
        mod = _import_impl()
        f_open = mod.open_pipe_harmonics(L_TEST, 1)[0]
        f_closed = mod.closed_pipe_harmonics(L_TEST, 1)[0]
        assert abs(f_closed / f_open - 0.5) < 0.01
    def test_beat_uses_difference(self):
        mod = _import_impl()
        assert mod.beat_frequency(440, 442) == 2
class TestCorrectness:
    def test_open_pipe_values(self):
        mod = _import_impl()
        f1 = mod.open_pipe_harmonics(L_TEST, 1)[0]
        assert abs(f1 - F1_OPEN) < 0.1
