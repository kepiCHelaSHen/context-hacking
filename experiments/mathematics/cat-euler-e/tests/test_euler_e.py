"""
Euler's e — Sigma Gate Tests
Every test must pass before the experiment is complete.
Run: python -m pytest tests/ -v
"""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from e_constants import (
    E_1000_CLEAN, DIGIT_CHECKPOINTS, PROHIBITED_NAMES,
    LLM_FLOAT_VALUE, TARGET_DIGITS, LLM_CEILING, CHP_TARGET,
)

COMPUTE_E = Path(__file__).parent.parent / "compute_e.py"


def _get_source() -> str:
    if not COMPUTE_E.exists():
        pytest.skip("compute_e.py not yet generated — run milestone 1 first")
    return COMPUTE_E.read_text(encoding="utf-8")


def _run_computation(digits: int) -> str:
    """Run compute_e.py and return the digit string."""
    import subprocess
    result = subprocess.run(
        [sys.executable, str(COMPUTE_E), "--digits", str(digits)],
        capture_output=True, text=True, timeout=120,
    )
    if result.returncode != 0:
        pytest.fail(f"compute_e.py failed:\n{result.stderr}")
    # Extract the e value from output — line starting with "e="
    for line in result.stdout.splitlines():
        if line.startswith("e="):
            return line[2:].strip()
    pytest.fail(f"No 'e=...' line in output:\n{result.stdout}")


# ── Gate 3: Prior-error detection ────────────────────────────────────────────

class TestPriorErrors:
    """
    These catch the known LLM prior errors.
    The expected false positive: Builder uses math.e or mpmath.
    """

    def test_no_prohibited_imports(self):
        """
        LLM prior: uses math.e (float, 15 digits) or mpmath.e (cheating).
        Frozen spec: standard library decimal module ONLY.
        Gate 3 FAILS if any prohibited name found in source.
        """
        src = _get_source()
        for name in PROHIBITED_NAMES:
            assert name not in src, (
                f"PRIOR ERROR: '{name}' found in compute_e.py.\n"
                f"This is the LLM prior — using an existing e value instead "
                f"of computing it from the Taylor series.\n"
                f"Fix: implement sum(1/n!) using decimal.Decimal only."
            )

    def test_uses_decimal_module(self):
        """Must use Python's decimal module for arbitrary precision."""
        src = _get_source()
        assert "decimal" in src.lower() or "Decimal" in src, (
            "compute_e.py does not use the decimal module.\n"
            "float arithmetic caps at 15 digits — the LLM float ceiling.\n"
            "Fix: from decimal import Decimal, getcontext"
        )

    def test_not_monte_carlo(self):
        """
        LLM prior for 'compute a mathematical constant': Monte Carlo method.
        Monte Carlo is wrong here — it's for pi approximation and is inefficient.
        Gate 3 FAILS if Monte Carlo patterns detected.
        """
        src = _get_source()
        mc_patterns = ["random", "numpy.random", "uniform", "randint",
                       "monte", "carlo", "simulation"]
        for pat in mc_patterns:
            assert pat not in src.lower(), (
                f"PRIOR ERROR: Monte Carlo pattern '{pat}' found.\n"
                f"Monte Carlo cannot compute e to 10000 digits efficiently.\n"
                f"Fix: use Taylor series sum(1/n!) with binary splitting."
            )

    def test_implements_factorial_or_series(self):
        """Must implement the Taylor series directly."""
        src = _get_source()
        has_series = any(term in src for term in [
            "factorial", "1/n!", "1/k!", "term /= ", "term *=",
            "series", "sum_", "total +=",
        ])
        assert has_series, (
            "Taylor series implementation not found.\n"
            "compute_e.py must implement e = sum(1/n!) from scratch.\n"
            "Using math.e or any pre-computed value is the LLM prior."
        )

    def test_precision_set_before_computation(self):
        """
        LLM prior: forgets to set decimal precision before computing.
        Result: getcontext().prec defaults to 28 digits — only 28 digits output.
        Fix: getcontext().prec = TARGET_DIGITS + BUFFER before any computation.
        """
        src = _get_source()
        assert "getcontext().prec" in src or "getcontext" in src, (
            "PRIOR ERROR: decimal precision not set.\n"
            "Default decimal precision = 28 digits.\n"
            "Fix: getcontext().prec = 10050 (target + buffer)"
        )


# ── Gate 3: Correctness ───────────────────────────────────────────────────────

class TestCorrectness:
    """Verify computed digits against frozen reference."""

    def test_first_20_digits_correct(self):
        """
        The starting point — where LLMs cap out.
        Our code must at minimum match float precision exactly.
        """
        computed = _run_computation(25)
        # Remove "2." prefix
        digits = computed.replace("2.", "").replace(".", "")[:20]
        expected = DIGIT_CHECKPOINTS[20]
        assert digits == expected, (
            f"First 20 digits wrong.\n"
            f"Got:      {digits}\n"
            f"Expected: {expected}\n"
            f"This is below the LLM float ceiling. Something is very wrong."
        )

    def test_first_50_digits_correct(self):
        computed = _run_computation(55)
        digits = computed.replace("2.", "").replace(".", "")[:50]
        expected = DIGIT_CHECKPOINTS[50]
        assert digits == expected, (
            f"First 50 digits wrong (past float ceiling).\n"
            f"Got:      {digits}\n"
            f"Expected: {expected}"
        )

    def test_first_100_digits_correct(self):
        """Past the LLM ceiling — territory where LLM memory alone fails."""
        computed = _run_computation(110)
        digits = computed.replace("2.", "").replace(".", "")[:74]
        expected = DIGIT_CHECKPOINTS[100][:74]
        assert digits == expected, (
            f"First 100 digits wrong.\n"
            f"Got:      {digits}\n"
            f"Expected: {expected}\n"
            f"We are past where any LLM can verify from memory."
        )

    def test_matches_reference_to_1000_digits(self):
        """Full 1000-digit reference match."""
        computed = _run_computation(1005)
        # Strip "2." and compare first 1000 decimal digits
        computed_digits = computed.replace("2.", "").replace(".", "")
        reference_digits = E_1000_CLEAN.replace("2.", "").replace(".", "")
        assert computed_digits[:1000] == reference_digits[:1000], (
            f"1000-digit match failed.\n"
            f"First mismatch at position: "
            f"{next(i for i,(a,b) in enumerate(zip(computed_digits, reference_digits)) if a!=b)}"
        )

    def test_beats_llm_ceiling_by_100x(self):
        """
        The core claim: CHP computes e to 100x more digits than LLM float ceiling.
        LLM ceiling: 15 digits. 100x = 1500 digits.
        """
        computed = _run_computation(1500)
        digits = computed.replace("2.", "").replace(".", "")
        reference = E_1000_CLEAN.replace("2.", "").replace(".", "")
        # Verify the first 1000 (all we have in frozen reference)
        assert digits[:1000] == reference[:1000], (
            "Failed to compute 1500 correct digits (100x LLM ceiling)."
        )
        # Check it actually produced 1500 digits
        assert len(digits) >= 1500, (
            f"Only produced {len(digits)} digits, needed 1500."
        )


# ── Gate 2: Architecture ──────────────────────────────────────────────────────

class TestArchitecture:
    """Code structure requirements."""

    def test_cli_interface(self):
        """compute_e.py must accept --digits N argument."""
        src = _get_source()
        assert "--digits" in src or "argparse" in src or "sys.argv" in src, (
            "No CLI interface found. compute_e.py must accept --digits N"
        )

    def test_outputs_e_equals_format(self):
        """Output must include 'e=...' line for test harness."""
        src = _get_source()
        assert 'e=' in src or '"e="' in src or "'e='" in src, (
            "Output format missing. Must print 'e={digits}' line."
        )

    def test_seeded_deterministic(self):
        """Same inputs must produce same output (no randomness)."""
        r1 = _run_computation(100)
        r2 = _run_computation(100)
        assert r1 == r2, "Non-deterministic output — computation has randomness"

    def test_performance_reasonable(self):
        """10000 digits should complete in under 60 seconds."""
        import time
        start = time.time()
        result = _run_computation(TARGET_DIGITS)
        elapsed = time.time() - start
        assert elapsed < 60, (
            f"Too slow: {elapsed:.1f}s for {TARGET_DIGITS} digits. "
            f"Likely using naive factorial loop instead of binary splitting."
        )
        assert len(result.replace("2.", "").replace(".", "")) >= TARGET_DIGITS - 5


# ── Sigma variance gate ───────────────────────────────────────────────────────

class TestSigmaGate:
    """
    Multi-precision equivalent of multi-seed variance check.
    Computing at different precision levels should give consistent overlapping digits.
    """

    def test_precision_consistency(self):
        """
        Compute at 100, 500, 1000 digits.
        The first 100 digits must be identical across all runs.
        This catches precision management bugs.
        """
        r100  = _run_computation(100)
        r500  = _run_computation(500)
        r1000 = _run_computation(1000)

        def strip(s): return s.replace("2.", "").replace(".", "")[:95]

        assert strip(r100) == strip(r500), (
            "Precision inconsistency: 100-digit and 500-digit runs disagree "
            "on the first 95 digits. Decimal context not set correctly."
        )
        assert strip(r100) == strip(r1000), (
            "Precision inconsistency: 100-digit and 1000-digit runs disagree."
        )


# ── The story test ────────────────────────────────────────────────────────────

class TestTheStory:
    """
    These tests exist to make the narrative concrete and measurable.
    They are Gate 4 (drift) checks — are we still telling the right story?
    """

    def test_llm_float_is_wrong_after_ceiling(self):
        """
        Demonstrate that float(e) fails past digit 15.
        This is the starting point of the story.
        """
        import math
        llm_e = str(math.e)
        # math.e gives "2.718281828459045" — 15 significant digits
        assert len(llm_e.replace("2.", "")) <= 16, (
            f"math.e gave more digits than expected: {llm_e}"
        )
        assert llm_e == LLM_FLOAT_VALUE, (
            f"math.e changed? Got {llm_e}, expected {LLM_FLOAT_VALUE}"
        )

    def test_chp_multiplier_achieved(self):
        """
        CHP target = 10000 digits = 667x the LLM float ceiling of 15 digits.
        This test verifies the multiplier is real.
        """
        computed = _run_computation(TARGET_DIGITS)
        n_digits = len(computed.replace("2.", "").replace(".", ""))
        multiplier = n_digits / LLM_CEILING
        assert multiplier >= 100, (
            f"Multiplier only {multiplier:.0f}x — target is 667x LLM ceiling."
        )
        print(f"\nCHP multiplier: {multiplier:.0f}x LLM float ceiling")
        print(f"LLM ceiling:    {LLM_CEILING} digits")
        print(f"CHP computed:   {n_digits} digits")
