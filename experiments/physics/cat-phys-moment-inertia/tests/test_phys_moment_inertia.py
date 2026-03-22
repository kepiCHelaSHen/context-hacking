"""cat-phys-moment-inertia — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from phys_moment_inertia_constants import *
IMPL = Path(__file__).parent.parent / "phys_moment_inertia.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

class TestPriorErrors:
    def test_hollow_gt_solid(self):
        m = _i(); assert m.hollow_sphere(2, 0.1) > m.solid_sphere(2, 0.1)
    def test_rod_center_lt_end(self):
        m = _i(); assert m.rod_center(1, 1) < m.rod_end(1, 1)
    def test_parallel_axis_adds(self):
        m = _i(); I_cm = m.solid_sphere(2, 0.1); I_off = m.parallel_axis(I_cm, 2, 0.5)
        assert I_off > I_cm
class TestCorrectness:
    def test_solid_sphere_value(self):
        m = _i(); assert abs(m.solid_sphere(2, 0.1) - I_TEST_SOLID) < 1e-6
    def test_hollow_sphere_value(self):
        m = _i(); assert abs(m.hollow_sphere(2, 0.1) - I_TEST_HOLLOW) < 1e-5
