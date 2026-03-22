"""Signal Filtering (LP/HP) — Frozen Constants. Source: Horowitz & Hill 3rd Ed Ch 1, Sedra/Smith. DO NOT MODIFY."""
import math

# RC Low-pass filter:  f_c = 1/(2*pi*R*C), output taken across C
# RC High-pass filter: f_c = 1/(2*pi*R*C), output taken across R
# KEY: Same cutoff formula — the difference is the OUTPUT TAP.
#   LP: output across C  (passes low, blocks high)
#   HP: output across R  (passes high, blocks low)
#
# Transfer functions:
#   LP: H(jw) = 1 / (1 + jwRC)
#   HP: H(jw) = jwRC / (1 + jwRC)
#
# At cutoff frequency:
#   gain = 1/sqrt(2) ~ 0.7071 = -3.0103 dB
#   phase: LP = -45 deg, HP = +45 deg

# LLM prior errors (the traps we test for):
PRIOR_ERRORS = {
    "lp_hp_tap_swap":       "Takes output from wrong element (LP across R or HP across C)",
    "fc_no_2pi":            "Uses f_c = 1/(RC) instead of 1/(2*pi*RC) — off by factor 2*pi",
    "gain_at_cutoff_wrong": "Claims 0 dB or -6 dB at cutoff instead of -3 dB",
}

# ── Reference component values ──
R_REF = 10_000.0   # 10 kOhm
C_REF = 10e-9       # 10 nF

# ── Derived cutoff frequency ──
RC_REF = R_REF * C_REF                           # 1e-4 s
FC_REF = 1.0 / (2.0 * math.pi * RC_REF)          # 1591.5494... Hz
FC_WRONG_NO_2PI = 1.0 / RC_REF                    # 10000 Hz — WRONG (missing 2*pi)

# ── Gain at cutoff: -3 dB point ──
GAIN_AT_CUTOFF = 1.0 / math.sqrt(2.0)             # 0.70710678...
DB_AT_CUTOFF = 20.0 * math.log10(GAIN_AT_CUTOFF)  # -3.01029995... dB

# ── LP gain at f = 10*fc  (deep into stop-band) ──
# |H_LP| = 1/sqrt(1 + (f/fc)^2) = 1/sqrt(1+100) = 1/sqrt(101)
LP_GAIN_AT_10FC = 1.0 / math.sqrt(1.0 + 10.0**2)          # 0.09950...
LP_DB_AT_10FC   = 20.0 * math.log10(LP_GAIN_AT_10FC)       # -20.043... dB

# ── HP gain at f = 0.1*fc  (deep into stop-band) ──
# |H_HP| = (f/fc)/sqrt(1 + (f/fc)^2) = 0.1/sqrt(1+0.01) = 0.1/sqrt(1.01)
HP_GAIN_AT_01FC = 0.1 / math.sqrt(1.0 + 0.1**2)           # 0.09950...
HP_DB_AT_01FC   = 20.0 * math.log10(HP_GAIN_AT_01FC)       # -20.043... dB

# ── Design check: given fc and R, solve for C ──
# C = 1/(2*pi*fc*R)
FC_DESIGN_TARGET = 1000.0  # Hz
R_DESIGN = 10_000.0        # 10 kOhm
C_DESIGN = 1.0 / (2.0 * math.pi * FC_DESIGN_TARGET * R_DESIGN)  # 1.5915e-8 F ~ 15.915 nF

# ── Phase at cutoff ──
LP_PHASE_AT_CUTOFF = -45.0  # degrees
HP_PHASE_AT_CUTOFF = +45.0  # degrees
