"""cat-eng-fatigue — Sigma Gate Tests"""
import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from eng_fatigue_constants import *
IMPL = Path(__file__).parent.parent / "eng_fatigue.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    """Catch the known LLM failure modes."""

    def test_aluminum_no_endurance_limit(self):
        """Aluminum does NOT have a true endurance limit — the #1 LLM error."""
        m = _i()
        assert m.has_endurance_limit("aluminum") is False, \
            "WRONG: aluminum does NOT have an endurance limit — fatigue life is always finite!"

    def test_aluminum_case_insensitive(self):
        """Should reject endurance limit for aluminum regardless of case."""
        m = _i()
        assert m.has_endurance_limit("Aluminum") is False
        assert m.has_endurance_limit("ALUMINUM") is False

    def test_steel_has_endurance_limit(self):
        """Steel DOES have a true endurance limit."""
        m = _i()
        assert m.has_endurance_limit("steel") is True

    def test_endurance_not_equal_ultimate(self):
        """Se ≈ 0.5*Su, NOT Se = Su — common LLM error."""
        m = _i()
        Se = m.endurance_limit_steel(SU_STEEL_REF)
        assert abs(Se - SE_STEEL_REF) / SE_STEEL_REF < 1e-9
        assert abs(Se - SE_WRONG_EQUALS_SU) > 1e6, \
            "Using Se = Su instead of Se ≈ 0.5*Su!"

    def test_endurance_half_of_ultimate(self):
        """Se should be exactly half of Su for Su < 1400 MPa."""
        m = _i()
        Se = m.endurance_limit_steel(SU_STEEL_REF)
        ratio = Se / SU_STEEL_REF
        assert abs(ratio - 0.5) < 1e-12, f"Expected Se/Su = 0.5, got {ratio}"

    def test_miner_sum_equals_one(self):
        """Miner's failure criterion is Σ(nᵢ/Nᵢ) = 1, NOT some other value."""
        m = _i()
        # Full life at one stress level: n=N → damage = 1.0
        D = m.miner_damage([N_LIFE_1], [N_LIFE_1])
        assert abs(D - MINER_FAILURE_SUM) < 1e-12, \
            f"Single-level full life should give damage = 1.0, got {D}"

    def test_miner_two_level_failure(self):
        """Two-level loading should sum to 1.0 at failure."""
        m = _i()
        # 50k at level 1 + remaining at level 2
        n2 = N_REMAINING_2  # 250,000
        D = m.miner_damage([N_ACTUAL_1, n2], [N_LIFE_1, N_LIFE_2])
        assert abs(D - MINER_FAILURE_SUM) < 1e-12, \
            f"Two-level Miner sum should be 1.0, got {D}"


class TestCorrectness:
    """Verify numerical accuracy of all functions."""

    def test_endurance_limit_value(self):
        """Su=800 MPa → Se=400 MPa."""
        m = _i()
        Se = m.endurance_limit_steel(SU_STEEL_REF)
        assert abs(Se - 400e6) < 1.0  # within 1 Pa

    def test_endurance_limit_low_su(self):
        """Su=600 MPa → Se=300 MPa."""
        m = _i()
        Se = m.endurance_limit_steel(600e6)
        assert abs(Se - 300e6) < 1.0

    def test_endurance_limit_high_su(self):
        """Su >= 1400 MPa → Se capped at 700 MPa."""
        m = _i()
        Se = m.endurance_limit_steel(1600e6)
        assert abs(Se - 700e6) < 1.0

    def test_miner_damage_single_level(self):
        """50,000 cycles out of 100,000 → damage = 0.5."""
        m = _i()
        D = m.miner_damage([N_ACTUAL_1], [N_LIFE_1])
        assert abs(D - DAMAGE_1) < 1e-12

    def test_miner_damage_zero_cycles(self):
        """Zero cycles → zero damage."""
        m = _i()
        D = m.miner_damage([0], [N_LIFE_1])
        assert D == 0.0

    def test_remaining_life_value(self):
        """After damage=0.5, remaining at N=500,000 is 250,000."""
        m = _i()
        n = m.remaining_life(DAMAGE_1, N_LIFE_2)
        assert abs(n - N_REMAINING_2) < 1e-6

    def test_remaining_life_zero_damage(self):
        """Zero prior damage → full life remains."""
        m = _i()
        n = m.remaining_life(0.0, N_LIFE_2)
        assert abs(n - N_LIFE_2) < 1e-6

    def test_remaining_life_high_damage(self):
        """After damage=0.9, remaining at N=100,000 is 10,000."""
        m = _i()
        n = m.remaining_life(0.9, 100_000)
        assert abs(n - 10_000) < 1e-6

    def test_miner_length_mismatch(self):
        """Mismatched list lengths should raise ValueError."""
        m = _i()
        with pytest.raises(ValueError):
            m.miner_damage([1, 2], [100])

    def test_remaining_life_invalid_damage(self):
        """Damage >= 1.0 should raise ValueError."""
        m = _i()
        with pytest.raises(ValueError):
            m.remaining_life(1.0, 100_000)

    def test_unknown_material_raises(self):
        """Unknown material should raise ValueError."""
        m = _i()
        with pytest.raises(ValueError):
            m.has_endurance_limit("unobtainium")

    def test_copper_no_endurance(self):
        """Copper has no true endurance limit, like aluminum."""
        m = _i()
        assert m.has_endurance_limit("copper") is False

    def test_titanium_has_endurance(self):
        """Titanium, like steel, has an endurance limit."""
        m = _i()
        assert m.has_endurance_limit("titanium") is True
