"""cat-phys-angular-momentum — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from phys_angular_momentum_constants import *
IMPL = Path(__file__).parent.parent / "phys_angular_momentum.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

class TestPriorErrors:
    def test_L_conserved(self):
        m = _i(); L1 = m.angular_momentum_rotation(I1_SKATER, OMEGA1_SKATER)
        omega2 = m.conservation_omega(I1_SKATER, OMEGA1_SKATER, I2_SKATER)
        L2 = m.angular_momentum_rotation(I2_SKATER, omega2)
        assert abs(L1 - L2) < 0.001
    def test_KE_not_conserved(self):
        m = _i(); KE1 = m.rotational_ke(I1_SKATER, OMEGA1_SKATER)
        omega2 = m.conservation_omega(I1_SKATER, OMEGA1_SKATER, I2_SKATER)
        KE2 = m.rotational_ke(I2_SKATER, omega2)
        assert KE2 > KE1
class TestCorrectness:
    def test_skater_omega2(self):
        m = _i(); assert abs(m.conservation_omega(I1_SKATER, OMEGA1_SKATER, I2_SKATER) - OMEGA2_SKATER) < 0.01
    def test_particle_L_with_angle(self):
        m = _i(); L90 = m.angular_momentum_particle(1, 10, 1, 90)
        L45 = m.angular_momentum_particle(1, 10, 1, 45)
        assert L90 > L45
