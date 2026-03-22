"""cat-bio-allometric-scaling — Sigma Gate Tests"""
import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from bio_allometric_scaling_constants import *
IMPL = Path(__file__).parent.parent / "bio_allometric_scaling.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_kleiber_exponent_is_three_quarters(self):
        """LLMs often use 2/3 (Rubner) instead of 3/4 (Kleiber)."""
        m = _i()
        assert abs(m.kleiber_exponent() - 0.75) < 1e-9

    def test_kleiber_not_two_thirds(self):
        """3/4 != 2/3 — these are distinct scaling laws."""
        m = _i()
        assert abs(m.kleiber_exponent() - m.rubner_exponent()) > 0.08

    def test_default_exponent_is_kleiber(self):
        """metabolic_rate default exponent must be 3/4, not 2/3."""
        m = _i()
        B_default = m.metabolic_rate(M_HUMAN)
        B_kleiber = m.metabolic_rate(M_HUMAN, exponent=KLEIBER_EXPONENT)
        assert abs(B_default - B_kleiber) < 0.01


class TestCorrectness:
    def test_mouse_metabolic_rate(self):
        m = _i()
        assert abs(m.metabolic_rate(M_MOUSE) - B_MOUSE) < 0.01

    def test_human_metabolic_rate(self):
        m = _i()
        assert abs(m.metabolic_rate(M_HUMAN) - B_HUMAN) < 0.1

    def test_elephant_metabolic_rate(self):
        m = _i()
        assert abs(m.metabolic_rate(M_ELEPHANT) - B_ELEPHANT) < 1.0

    def test_mass_specific_decreases_with_size(self):
        """Larger animals have lower per-kg metabolic rates."""
        m = _i()
        msr_mouse = m.mass_specific_rate(M_MOUSE)
        msr_human = m.mass_specific_rate(M_HUMAN)
        msr_elephant = m.mass_specific_rate(M_ELEPHANT)
        assert msr_mouse > msr_human > msr_elephant

    def test_wrong_exponent_underestimates(self):
        """Using 2/3 instead of 3/4 underestimates large-animal metabolism."""
        m = _i()
        B_correct = m.metabolic_rate(M_HUMAN, exponent=KLEIBER_EXPONENT)
        B_wrong = m.metabolic_rate(M_HUMAN, exponent=RUBNER_EXPONENT)
        assert B_wrong < B_correct
        ratio = B_wrong / B_correct
        assert 0.65 < ratio < 0.75  # ~30% underestimate
