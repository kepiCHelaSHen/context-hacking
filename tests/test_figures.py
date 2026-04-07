"""Tests for the figure generator."""

from pathlib import Path

import pytest

from context_hacking.figures import FIGURE_DESCRIPTIONS, generate_figures


class TestFigureDescriptions:
    def test_dict_not_empty(self):
        assert len(FIGURE_DESCRIPTIONS) >= 27

    def test_known_keys(self):
        assert "schelling_comparison" in FIGURE_DESCRIPTIONS
        assert "lorenz_attractor" in FIGURE_DESCRIPTIONS
        assert "grover_amplitude" in FIGURE_DESCRIPTIONS
        assert "izhikevich_patterns" in FIGURE_DESCRIPTIONS
        assert "metal_vs_classical" in FIGURE_DESCRIPTIONS
        # New keys from Drift 2 fix
        assert "lorenz_chp_story" in FIGURE_DESCRIPTIONS
        assert "cluster_map" in FIGURE_DESCRIPTIONS
        assert "r0_distribution" in FIGURE_DESCRIPTIONS
        assert "lyapunov_convergence" in FIGURE_DESCRIPTIONS
        assert "phase_portrait" in FIGURE_DESCRIPTIONS
        assert "cooperation_rate" in FIGURE_DESCRIPTIONS

    def test_descriptions_are_strings(self):
        for key, desc in FIGURE_DESCRIPTIONS.items():
            assert isinstance(desc, str)
            assert len(desc) > 5


class TestFigureStyle:
    def test_no_dark_colors_in_source(self):
        """figures.py must use white-style colors, not dark-style."""
        fig_path = Path(__file__).parent.parent / "context_hacking" / "figures.py"
        src = fig_path.read_text(encoding="utf-8")
        assert "#0a0a1a" not in src, "Dark background color found — should be white"
        assert "#0d0d20" not in src, "Dark surface color found — should be white"
        assert "#00ff88" not in src, "Neon green found — should be #065F46"


class TestDashboardSync:
    def test_dashboard_imports_not_defines_figure_descriptions(self):
        """app.py must import FIGURE_DESCRIPTIONS, not define its own."""
        app_path = Path(__file__).parent.parent / "dashboard" / "app.py"
        if not app_path.exists():
            pytest.skip("dashboard/app.py not found")
        app_src = app_path.read_text(encoding="utf-8")
        assert "FIGURE_DESCRIPTIONS: dict" not in app_src, (
            "dashboard/app.py defines its own FIGURE_DESCRIPTIONS — "
            "it must import from context_hacking.figures instead"
        )
        assert "from context_hacking.figures import" in app_src, (
            "dashboard/app.py must import FIGURE_DESCRIPTIONS from context_hacking.figures"
        )

    def test_no_dead_patch_file(self):
        """health_patch.py must not exist as an unimported dead file."""
        patch_path = Path(__file__).parent.parent / "dashboard" / "health_patch.py"
        if patch_path.exists():
            app_path = Path(__file__).parent.parent / "dashboard" / "app.py"
            app_src = app_path.read_text(encoding="utf-8")
            assert "health_patch" in app_src, (
                "dashboard/health_patch.py exists but is never imported in app.py — "
                "either import it or delete it"
            )


class TestGenerateFigures:
    def test_returns_empty_for_nonexistent(self, tmp_path):
        paths = generate_figures("nonexistent-experiment", tmp_path)
        assert paths == []

    def test_returns_empty_for_no_simulation(self, tmp_path):
        exp_dir = tmp_path / "schelling-segregation"
        exp_dir.mkdir()
        (exp_dir / "frozen").mkdir()
        paths = generate_figures("schelling-segregation", exp_dir)
        assert paths == []
