"""Tests for Metal Harmony Analyzer."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from metal_analyzer import (
    Chord, analyze_riff, run_simulation, detect_mode, MODES,
    pantera_walk, pantera_cowboys,
)


class TestReturnStructure:
    def test_returns_riff_results(self):
        result = run_simulation()
        assert "riff_results" in result
        assert isinstance(result["riff_results"], dict)
        assert len(result["riff_results"]) == 5  # 5 Pantera reference riffs

    def test_all_riffs_have_expected_fields(self):
        result = run_simulation()
        for riff_name, riff_data in result["riff_results"].items():
            assert "mode" in riff_data
            assert "classical_errors_count" in riff_data
            assert "metal_assessment" in riff_data


class TestPowerChords:
    def test_power_chord_root_plus_fifth(self):
        """Power chord = root + perfect fifth (7 semitones), no third."""
        chord = Chord(notes=[38, 45, 50])  # D2, A2, D3 -> intervals {0, 7}
        assert chord.is_power_chord is True

    def test_not_power_chord_with_third(self):
        """A chord with a third is NOT a power chord."""
        chord = Chord(notes=[40, 44, 47])  # E, Ab, B -> has minor third
        assert chord.is_power_chord is False

    def test_walk_all_power_chords(self):
        """Walk riff should be all power chords."""
        analysis = pantera_walk()
        for c in analysis.chords:
            assert c.is_power_chord, f"Chord {c.name} in Walk should be a power chord"


class TestNoFunctionalContamination:
    def test_is_functional_false(self):
        """Metal analysis should be modal, NOT functional (no Roman numerals)."""
        result = run_simulation()
        assert result["functional_contamination"] == 0.0, \
            "Metal riffs should not be analyzed with functional harmony"

    def test_each_riff_not_functional(self):
        result = run_simulation()
        for riff_name, riff_data in result["riff_results"].items():
            assert riff_data["is_functional"] is False, \
                f"Riff {riff_name} should not be marked as functional"


class TestCorrectModes:
    def test_all_modes_are_valid(self):
        """All detected modes should be valid mode names from the MODES dict."""
        result = run_simulation()
        valid_modes = set(MODES.keys()) | {"chromatic"}
        for riff_name, riff_data in result["riff_results"].items():
            assert riff_data["mode"] in valid_modes, \
                f"Riff {riff_name}: {riff_data['mode']} is not a valid mode"

    def test_domination_and_five_minutes_are_phrygian(self):
        """Domination and 5 Minutes Alone should detect as phrygian."""
        result = run_simulation()
        assert result["riff_results"]["domination"]["mode"] == "phrygian"
        assert result["riff_results"]["five_minutes"]["mode"] == "phrygian"

    def test_mode_confidence_above_zero(self):
        """Mode confidence for all riffs should be > 0."""
        result = run_simulation()
        for riff_name, riff_data in result["riff_results"].items():
            assert riff_data["mode_confidence"] > 0, \
                f"Riff {riff_name}: mode_confidence should be > 0"


class TestClassicalErrors:
    def test_classical_errors_greater_than_zero(self):
        """Metal riffs should trigger classical theory 'errors' (parallel fifths, etc.)."""
        result = run_simulation()
        total_errors = sum(
            riff_data["classical_errors_count"]
            for riff_data in result["riff_results"].values()
        )
        assert total_errors > 0, "Metal riffs should generate classical theory errors"

    def test_parallel_fifths_flagged(self):
        """Walk riff should have parallel fifths flagged."""
        analysis = pantera_walk()
        assert analysis.has_parallel_fifths is True
        # But in metal, parallel fifths are correct
        assert analysis.parallel_fifths_correct is True
