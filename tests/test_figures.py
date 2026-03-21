"""Tests for the figure generator."""

from pathlib import Path

import pytest

from context_hacking.figures import generate_figures, FIGURE_DESCRIPTIONS


class TestFigureDescriptions:
    def test_dict_not_empty(self):
        assert len(FIGURE_DESCRIPTIONS) > 10

    def test_known_keys(self):
        assert "schelling_comparison" in FIGURE_DESCRIPTIONS
        assert "lorenz_attractor" in FIGURE_DESCRIPTIONS
        assert "grover_amplitude" in FIGURE_DESCRIPTIONS
        assert "izhikevich_patterns" in FIGURE_DESCRIPTIONS
        assert "metal_vs_classical" in FIGURE_DESCRIPTIONS

    def test_descriptions_are_strings(self):
        for key, desc in FIGURE_DESCRIPTIONS.items():
            assert isinstance(desc, str)
            assert len(desc) > 5


class TestGenerateFigures:
    def test_returns_empty_for_nonexistent(self, tmp_path):
        paths = generate_figures("nonexistent-experiment", tmp_path)
        assert paths == []

    def test_returns_empty_for_no_simulation(self, tmp_path):
        # Create experiment dir without simulation code
        exp_dir = tmp_path / "schelling-segregation"
        exp_dir.mkdir()
        (exp_dir / "frozen").mkdir()
        paths = generate_figures("schelling-segregation", exp_dir)
        assert paths == []  # No schelling.py to import
