"""
Milankovitch Cycles (Orbital Parameter Periodicity) — Frozen Constants
Source: Berger & Loutre 1991, Laskar et al. 2004 orbital solutions
DO NOT MODIFY.
"""

# ── Eccentricity ──────────────────────────────────────────────────
# Earth's orbital eccentricity varies with two dominant periods
ECCENTRICITY_PERIOD       = 100_000   # yr — dominant short eccentricity cycle
ECCENTRICITY_PERIOD_LONG  = 413_000   # yr — long eccentricity cycle
# Current eccentricity ≈ 0.0167 (nearly circular)

# ── Obliquity (axial tilt) ────────────────────────────────────────
OBLIQUITY_PERIOD       = 41_000    # yr — period of axial tilt oscillation
OBLIQUITY_MIN          = 22.1      # degrees — minimum tilt
OBLIQUITY_MAX          = 24.5      # degrees — maximum tilt
CURRENT_OBLIQUITY      = 23.44     # degrees — current value (decreasing)

# ── Precession ────────────────────────────────────────────────────
# CRITICAL DISTINCTION:
#   Axial precession (gyroscopic wobble) ≈ 26,000 yr
#   BUT climatic precession = axial precession modulated by apsidal precession
#   Climatic precession dominant periods: ~23,000 yr and ~19,000 yr
#
# The 26,000 yr value is axial precession ONLY.  For climate forcing,
# the relevant quantity is CLIMATIC precession (~23 kyr dominant).
# LLMs frequently cite 26,000 yr — that is the WRONG period for climate.

AXIAL_PRECESSION_PERIOD    = 26_000   # yr — gyroscopic wobble of rotation axis
CLIMATIC_PRECESSION_PERIOD = 23_000   # yr — dominant climatic precession period
CLIMATIC_PRECESSION_MINOR  = 19_000   # yr — secondary climatic precession period

PRIOR_ERRORS = {
    "precession_26k":          "Uses 26,000 yr (axial precession) instead of ~23,000 yr (climatic precession) — wrong period for climate forcing",
    "obliquity_wrong_range":   "Wrong tilt range — must be 22.1°–24.5°, not some other range",
    "eccentricity_period_wrong": "Uses 23k or 41k for eccentricity period — eccentricity is ~100 kyr (short) and ~413 kyr (long)",
}
