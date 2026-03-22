"""Tests for Schroeder/Freeverb Reverb implementation."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from reverb import (
    Freeverb, CombFilter, AllpassFilter,
    COMB_DELAYS, ALLPASS_DELAYS, ALLPASS_FEEDBACK,
    run_simulation,
)


class TestCombDelays:
    def test_correct_comb_delays(self):
        """Comb delays must match Jezar's frozen values exactly."""
        expected = [1116, 1188, 1277, 1356, 1422, 1491, 1557, 1617]
        assert COMB_DELAYS == expected, f"Expected {expected}, got {COMB_DELAYS}"

    def test_freeverb_uses_correct_comb_delays(self):
        rv = Freeverb()
        actual = [c.delay_length for c in rv.combs_L]
        expected = [1116, 1188, 1277, 1356, 1422, 1491, 1557, 1617]
        assert actual == expected


class TestEightCombsNotFour:
    def test_eight_comb_filters(self):
        """Freeverb uses 8 parallel comb filters, NOT 4 (Schroeder textbook)."""
        rv = Freeverb()
        assert len(rv.combs_L) == 8, f"Expected 8 combs, got {len(rv.combs_L)}"
        assert len(rv.combs_R) == 8, f"Expected 8 combs (R), got {len(rv.combs_R)}"

    def test_run_simulation_reports_8_combs(self):
        result = run_simulation()
        assert result["n_comb_filters"] == 8


class TestFourAllpass:
    def test_four_allpass_filters(self):
        """Freeverb uses 4 series allpass filters."""
        rv = Freeverb()
        assert len(rv.allpasses_L) == 4, f"Expected 4 allpasses, got {len(rv.allpasses_L)}"
        assert len(rv.allpasses_R) == 4

    def test_allpass_delays(self):
        rv = Freeverb()
        actual = [a.delay_length for a in rv.allpasses_L]
        expected = [556, 441, 341, 225]
        assert actual == expected

    def test_run_simulation_reports_4_allpass(self):
        result = run_simulation()
        assert result["n_allpass_filters"] == 4


class TestFeedback:
    def test_allpass_feedback_is_0_5(self):
        """Allpass feedback coefficient must be 0.5 (Jezar's value)."""
        assert ALLPASS_FEEDBACK == 0.5
        rv = Freeverb()
        for ap in rv.allpasses_L:
            assert ap.feedback == 0.5, f"Expected feedback=0.5, got {ap.feedback}"


class TestFrozenCompliance:
    def test_comb_delay_match(self):
        result = run_simulation()
        assert result["comb_delay_match"] == 1.0, "Comb delays must match frozen spec exactly"

    def test_allpass_delay_match(self):
        result = run_simulation()
        assert result["allpass_delay_match"] == 1.0, "Allpass delays must match frozen spec exactly"
