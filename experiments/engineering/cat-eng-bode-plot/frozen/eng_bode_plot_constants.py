"""Bode Plot — Frozen Constants. Source: Ogata 5th Ed, Franklin et al. DO NOT MODIFY."""
import math

# ── First-order low-pass: H(s) = 1 / (1 + s/ω₀) ──────────────────────────
# Gain magnitude: |H(jω)| = 1 / √(1 + (ω/ω₀)²)
# Gain in dB:     20·log₁₀(|H(jω)|)
# Phase:          φ(ω) = −arctan(ω/ω₀)  [degrees]
#
# KEY FACT: At the pole frequency ω = ω₀, phase = −45° (NOT −90°!)
#   Phase reaches −90° only asymptotically as ω → ∞.
#   LLM prior: claims −90° at ω₀ — this is the dominant error.
#
# First-order pole:  gain slope −20 dB/decade,  phase 0° → −90°
# First-order zero:  gain slope +20 dB/decade,  phase 0° → +90°

# Reference pole frequency
OMEGA_0 = 100.0  # rad/s

# ── Frozen values at ω = ω₀ (pole frequency) ──────────────────────────────
GAIN_DB_AT_POLE = 20.0 * math.log10(1.0 / math.sqrt(2.0))  # −3.010299957 dB
PHASE_AT_POLE   = -45.0                                      # degrees (EXACTLY)

# ── Frozen values at ω = 10·ω₀  (one decade above) ────────────────────────
GAIN_DB_AT_10X = 20.0 * math.log10(1.0 / math.sqrt(101.0))  # −20.043214 dB
PHASE_AT_10X   = -math.degrees(math.atan(10.0))              # −84.289407°

# ── Frozen values at ω = 0.1·ω₀ (one decade below) ────────────────────────
GAIN_DB_AT_01X = 20.0 * math.log10(1.0 / math.sqrt(1.01))   # −0.043214 dB
PHASE_AT_01X   = -math.degrees(math.atan(0.1))               # −5.710593°

# ── dB conversion references ──────────────────────────────────────────────
DB_OF_HALF     = 20.0 * math.log10(0.5)   # −6.020600 dB
DB_OF_DOUBLE   = 20.0 * math.log10(2.0)   #  6.020600 dB
LINEAR_OF_0DB  = 1.0
LINEAR_OF_M3DB = 10.0 ** (GAIN_DB_AT_POLE / 20.0)  # ≈ 0.70711 = 1/√2

# ── Wrong answers that LLMs commonly produce ──────────────────────────────
WRONG_PHASE_AT_POLE = -90.0   # WRONG: −90° at pole (should be −45°)
WRONG_GAIN_LINEAR   = 1.0 / math.sqrt(2.0)  # Correct linear, but WRONG if used as dB
WRONG_POLE_SLOPE    = +20.0   # WRONG: pole gives +20dB/dec (should be −20)

PRIOR_ERRORS = {
    "phase_at_pole_90":     "Claims phase = −90° at pole frequency; correct is −45°",
    "gain_linear_not_db":   "Returns gain as linear ratio instead of converting to dB",
    "pole_zero_slope_swap": "Assigns +20 dB/dec slope to a pole instead of −20 dB/dec",
}
