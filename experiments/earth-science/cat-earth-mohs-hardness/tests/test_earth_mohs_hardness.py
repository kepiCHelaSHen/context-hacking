"""cat-earth-mohs-hardness — Sigma Gate Tests"""
import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from earth_mohs_hardness_constants import *
IMPL = Path(__file__).parent.parent / "earth_mohs_hardness.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    """Guard against known LLM confusions about the Mohs scale."""

    def test_not_linear(self):
        """Prior error: mohs_linear — Mohs is ordinal, NOT linear."""
        m = _i()
        assert m.is_linear() is False, "Mohs scale is ordinal, not linear"

    def test_diamond_not_10x_talc(self):
        """Prior error: diamond_10x_talc — diamond is ~1500x harder, not 10x."""
        m = _i()
        v_diamond = m.absolute_hardness_vickers(10)
        v_talc = m.absolute_hardness_vickers(1)
        ratio = v_diamond / v_talc
        assert ratio > 100, f"Diamond/talc Vickers ratio should be >>10, got {ratio}"
        assert ratio != 10, "Ratio must NOT be 10 — that's the Mohs number, not absolute hardness"

    def test_vickers_gap_9_to_10_is_largest(self):
        """Prior error: mohs_linear — the gap from corundum to diamond is the largest."""
        m = _i()
        gaps = []
        for mohs in range(1, 10):
            gap = m.absolute_hardness_vickers(mohs + 1) - m.absolute_hardness_vickers(mohs)
            gaps.append(gap)
        assert gaps[-1] == max(gaps), "Gap from 9->10 must be the largest Vickers gap"
        assert gaps[-1] > 500, f"Gap 9->10 should be >500 Vickers, got {gaps[-1]}"

    def test_mineral_order_correct(self):
        """Prior error: wrong_mineral_order — verify standard ordering."""
        m = _i()
        expected_order = [
            ("talc", 1), ("gypsum", 2), ("calcite", 3), ("fluorite", 4),
            ("apatite", 5), ("orthoclase", 6), ("quartz", 7), ("topaz", 8),
            ("corundum", 9), ("diamond", 10),
        ]
        for mineral, expected_mohs in expected_order:
            assert m.mohs_number(mineral) == expected_mohs, (
                f"{mineral} should be Mohs {expected_mohs}"
            )

    def test_vickers_nonlinear_spread(self):
        """The Vickers gap 1->2 should be tiny compared to 9->10."""
        m = _i()
        gap_low = m.absolute_hardness_vickers(2) - m.absolute_hardness_vickers(1)
        gap_high = m.absolute_hardness_vickers(10) - m.absolute_hardness_vickers(9)
        assert gap_high / gap_low > 100, (
            f"Gap 9->10 ({gap_high}) should be >100x gap 1->2 ({gap_low})"
        )


class TestMohsNumber:
    def test_all_ten_minerals(self):
        m = _i()
        for mineral, mohs in MOHS_SCALE.items():
            assert m.mohs_number(mineral) == mohs

    def test_case_insensitive(self):
        m = _i()
        assert m.mohs_number("DIAMOND") == 10
        assert m.mohs_number("Quartz") == 7
        assert m.mohs_number("  talc  ") == 1

    def test_unknown_mineral_raises(self):
        m = _i()
        with pytest.raises(KeyError):
            m.mohs_number("obsidian")


class TestCanScratch:
    def test_harder_scratches_softer(self):
        m = _i()
        assert m.can_scratch(7, 5.5) is True, "Quartz (7) scratches glass (5.5)"

    def test_softer_cannot_scratch_harder(self):
        m = _i()
        assert m.can_scratch(2, 7) is False, "Gypsum (2) cannot scratch quartz (7)"

    def test_equal_hardness_no_scratch(self):
        m = _i()
        assert m.can_scratch(5, 5) is False, "Equal hardness: cannot scratch"

    def test_fingernail_scratches_gypsum(self):
        m = _i()
        assert m.can_scratch(FINGERNAIL_HARDNESS, 2) is True, "Fingernail (2.5) scratches gypsum (2)"

    def test_fingernail_cannot_scratch_calcite(self):
        m = _i()
        assert m.can_scratch(FINGERNAIL_HARDNESS, 3) is False, "Fingernail (2.5) cannot scratch calcite (3)"


class TestAbsoluteHardness:
    def test_vickers_values_match_constants(self):
        m = _i()
        for mohs, expected in VICKERS_APPROX.items():
            assert m.absolute_hardness_vickers(mohs) == expected

    def test_invalid_mohs_raises(self):
        m = _i()
        with pytest.raises(KeyError):
            m.absolute_hardness_vickers(0)
        with pytest.raises(KeyError):
            m.absolute_hardness_vickers(11)

    def test_monotonically_increasing(self):
        m = _i()
        prev = 0
        for mohs in range(1, 11):
            v = m.absolute_hardness_vickers(mohs)
            assert v > prev, f"Vickers must increase: Mohs {mohs} ({v}) <= previous ({prev})"
            prev = v
