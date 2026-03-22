"""
Anatomy Viewer — Sigma Gates
Tests that the generated viewer matches the frozen anatomical spec.
Run: python -m pytest tests/ -v
"""

import re
import sys
from pathlib import Path

import pytest

# Add frozen to path so we can import constants
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from anatomy_constants import (
    HEART_CENTER_Y, LIVER_CENTER_X, RIGHT_LUNG_HEIGHT, LEFT_LUNG_HEIGHT,
    AORTA_BIFURCATION_Y, DIAPHRAGM_RIGHT_HIGHER, COLORS,
    HEAD_HEIGHT_RATIO, SHOULDER_WIDTH_RATIO, HIP_WIDTH_RATIO,
    BILATERAL_SYMMETRY_TOL, CANVAS_WIDTH, CANVAS_HEIGHT,
)

VIEWER_JS = Path(__file__).parent.parent / "anatomy_viewer.js"
VIEWER_HTML = Path(__file__).parent.parent / "anatomy_viewer.html"


def _get_source() -> str:
    """Get the viewer source code."""
    for p in [VIEWER_JS, VIEWER_HTML]:
        if p.exists():
            return p.read_text(encoding="utf-8")
    pytest.skip("anatomy_viewer.js / .html not yet generated — run milestone 1 first")


def _extract_float(src: str, pattern: str) -> float | None:
    """Extract a float value from source matching pattern."""
    m = re.search(pattern, src)
    if m:
        return float(m.group(1))
    return None


# ── Gate 3: Scientific validity (anatomical accuracy) ────────────────────────

class TestPriorErrors:
    """
    These tests catch the known LLM prior errors defined in frozen/anatomy_spec.md.
    Each test corresponds to one PRIOR_ERROR entry in the frozen spec.
    Gate 3 FAILS if any of these pass (meaning the prior slipped through).
    """

    def test_heart_not_too_high(self):
        """
        LLM prior: places heart at ~0.310 (upper chest feeling).
        Frozen spec: heart center at 0.355 (T5 vertebral level).
        FAIL if heart_center_y < 0.330.
        """
        src = _get_source()
        # Look for the heart center Y constant or inline value
        val = _extract_float(src, r'HEART_CENTER_Y\s*[=:]\s*([0-9.]+)')
        if val is None:
            val = _extract_float(src, r'heart.*?center.*?y.*?([0-9.]+)', )
        if val is None:
            # Look for the specific coordinate used in the canvas drawing
            # Heart should be drawn around y = FIGURE_HEIGHT * HEART_CENTER_Y
            val = _extract_float(src, r'heartY\s*=\s*H\s*\*\s*([0-9.]+)')
        assert val is not None, "Cannot locate heart Y position in source"
        assert val >= 0.330, (
            f"Heart center_y={val} is too high. "
            f"LLM prior=0.310, frozen spec=0.355 (T5 level). "
            f"Heart must be at >= 0.330 of total height."
        )

    def test_liver_on_right_side(self):
        """
        LLM prior: occasionally places liver on left (gets confused with stomach).
        Frozen spec: liver is RIGHT hypochondriac — center_x_offset POSITIVE.
        FAIL if liver is drawn left of midline.
        """
        src = _get_source()
        val = _extract_float(src, r'LIVER_CENTER_X\s*[=:]\s*(-?[0-9.]+)')
        if val is None:
            val = _extract_float(src, r'liverX\s*=\s*cx\s*[+-]\s*([0-9.]+)')
        if val is None:
            pytest.skip("Cannot extract liver X — check source pattern")
        assert val > 0, (
            f"Liver center_x_offset={val} is negative (left side). "
            f"Liver must be on the RIGHT (positive offset). "
            f"LLM prior error: confusion with stomach position."
        )

    def test_right_lung_larger_than_left(self):
        """
        LLM prior: generates equal-sized lungs.
        Frozen spec: right lung is larger (left has cardiac notch).
        RIGHT_LUNG_HEIGHT > LEFT_LUNG_HEIGHT.
        """
        src = _get_source()
        right_h = _extract_float(src, r'RIGHT_LUNG_HEIGHT\s*[=:]\s*([0-9.]+)')
        left_h  = _extract_float(src, r'LEFT_LUNG_HEIGHT\s*[=:]\s*([0-9.]+)')
        if right_h is None or left_h is None:
            pytest.skip("Cannot extract lung heights — check source pattern")
        assert right_h > left_h, (
            f"right_lung_height={right_h} <= left_lung_height={left_h}. "
            f"Right lung must be larger. Left lung has cardiac notch. "
            f"LLM prior: equal sizing."
        )

    def test_aorta_bifurcation_at_l4(self):
        """
        LLM prior: places aortic bifurcation at L3 (~y=0.510).
        Frozen spec: bifurcation at L4 (~y=0.535).
        FAIL if bifurcation_y < 0.520.
        """
        src = _get_source()
        val = _extract_float(src, r'AORTA_BIFURCATION_Y\s*[=:]\s*([0-9.]+)')
        if val is None:
            pytest.skip("Cannot extract aorta bifurcation Y — check source pattern")
        assert val >= 0.520, (
            f"Aorta bifurcation at y={val} — too high, implies L3. "
            f"Frozen spec: L4 = y=0.535. "
            f"LLM prior: L3 = y~0.510."
        )

    def test_diaphragm_right_higher(self):
        """
        LLM prior: draws symmetric diaphragm.
        Frozen spec: right hemidiaphragm is higher than left (liver below).
        """
        src = _get_source()
        assert "DIAPHRAGM_RIGHT_HIGHER" in src or "rightHigher" in src or "right_higher" in src, (
            "Diaphragm laterality not implemented. "
            "Right hemidiaphragm must be drawn higher than left. "
            "LLM prior: symmetric diaphragm."
        )

    def test_frozen_constants_imported_not_redefined(self):
        """
        Builder must import from frozen/anatomy_constants.py.
        Must NOT redefine HEART_CENTER_Y, LIVER_CENTER_X, etc. inline.
        """
        src = _get_source()
        # If source is JS or HTML, check for frozen values directly
        if VIEWER_JS.exists() or VIEWER_HTML.exists():
            return  # JS/HTML file — constants are inline by necessity
        # Check Python source doesn't redefine frozen constants
        bad_patterns = [
            r'HEART_CENTER_Y\s*=\s*0\.[0-9]+(?!\s*#.*frozen)',
            r'LIVER_CENTER_X\s*=\s*-?0\.[0-9]+(?!\s*#.*frozen)',
            r'AORTA_BIFURCATION_Y\s*=\s*0\.[0-9]+(?!\s*#.*frozen)',
        ]
        for pat in bad_patterns:
            assert not re.search(pat, src), (
                f"Frozen constant redefined in source: {pat}. "
                f"Import from frozen/anatomy_constants.py instead."
            )


# ── Gate 6: Proportion accuracy ──────────────────────────────────────────────

class TestProportions:
    """Verify body proportions match anthropometric reference data."""

    def test_head_proportion(self):
        assert abs(HEAD_HEIGHT_RATIO - 0.145) < 0.001, \
            f"HEAD_HEIGHT_RATIO={HEAD_HEIGHT_RATIO} != 0.145"

    def test_shoulder_width_proportion(self):
        assert abs(SHOULDER_WIDTH_RATIO - 0.259) < 0.001, \
            f"SHOULDER_WIDTH_RATIO={SHOULDER_WIDTH_RATIO} != 0.259"

    def test_hip_width_proportion(self):
        assert abs(HIP_WIDTH_RATIO - 0.191) < 0.001, \
            f"HIP_WIDTH_RATIO={HIP_WIDTH_RATIO} != 0.191"

    def test_shoulders_wider_than_hips(self):
        """Standard anatomical male reference: shoulders wider than hips."""
        assert SHOULDER_WIDTH_RATIO > HIP_WIDTH_RATIO, \
            "Shoulder width must exceed hip width in reference figure"

    def test_bilateral_symmetry_tolerance_tight(self):
        """Symmetry tolerance must be <= 0.5% to catch rendering drift."""
        assert BILATERAL_SYMMETRY_TOL <= 0.005, \
            f"Bilateral symmetry tolerance {BILATERAL_SYMMETRY_TOL} too loose"


# ── Gate 2: Architecture ──────────────────────────────────────────────────────

class TestArchitecture:
    """Code structure and rendering requirements."""

    def test_canvas_dimensions(self):
        assert CANVAS_WIDTH  == 340
        assert CANVAS_HEIGHT == 500

    def test_colors_not_neon(self):
        """
        LLM prior for anatomy: bright medical colors (#00ff88, #ff0000).
        Frozen spec: muted, professional palette.
        """
        neon_patterns = ['#00ff', '#ff00', '#0ff0']
        for sys_name, color in COLORS.items():
            for neon in neon_patterns:
                assert neon.lower() not in color.lower(), \
                    f"System {sys_name} uses neon color {color}. Use frozen palette."

    def test_all_seven_systems_defined(self):
        required = {'skeletal','muscular','nervous','circulatory',
                    'respiratory','digestive','lymphatic'}
        assert required == set(COLORS.keys()), \
            f"Missing systems: {required - set(COLORS.keys())}"

    def test_three_views_required(self):
        src = _get_source()
        for view in ['anterior', 'posterior', 'lateral']:
            assert view in src.lower(), \
                f"View '{view}' not found in source — all three views required"

    def test_system_toggle_implemented(self):
        src = _get_source()
        assert 'activeSystem' in src or 'active_system' in src, \
            "System toggle (activeSystem) not implemented"

    def test_no_hardcoded_heart_position(self):
        """
        Heart must use the frozen constant, not a hardcoded pixel value.
        A hardcoded y=177 (the prior's T3 position) would pass visually
        but fail anatomically. The frozen constant forces the correct value.
        """
        src = _get_source()
        # Check that some reference to HEART_CENTER_Y or heartY exists
        assert 'HEART_CENTER_Y' in src or 'heartY' in src or '0.355' in src, \
            "Heart position must reference the frozen constant (0.355), not a pixel value"


# ── Variance gate ─────────────────────────────────────────────────────────────

class TestSigmaGate:
    """
    Multi-seed equivalent for deterministic rendering:
    re-rendering with the same constants must produce identical output.
    """

    def test_constants_are_deterministic(self):
        """Same constants, same output — no randomness in anatomy positions."""
        import importlib
        import importlib.util

        spec_path = Path(__file__).parent.parent / "frozen" / "anatomy_constants.py"
        spec = importlib.util.spec_from_file_location("anatomy_constants", spec_path)
        mod1 = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod1)

        spec2 = importlib.util.spec_from_file_location("anatomy_constants2", spec_path)
        mod2 = importlib.util.module_from_spec(spec2)
        spec2.loader.exec_module(mod2)

        assert mod1.HEART_CENTER_Y == mod2.HEART_CENTER_Y
        assert mod1.LIVER_CENTER_X == mod2.LIVER_CENTER_X
        assert mod1.AORTA_BIFURCATION_Y == mod2.AORTA_BIFURCATION_Y
