"""
Drake Equation — Frozen Constants
Source: Drake (1961), Kepler mission results, modern SETI estimates
DO NOT MODIFY.
"""

# === Drake Equation ===
# N = R* x f_p x n_e x f_l x f_i x f_c x L
#
# R* = mean rate of star formation in the Milky Way (stars/year)
# f_p = fraction of stars with planetary systems
# n_e = number of habitable planets per system with planets
# f_l = fraction of habitable planets that develop life
# f_i = fraction of life-bearing planets that develop intelligence
# f_c = fraction of intelligent civilizations that develop detectable communications
# L   = length of time (years) such civilizations release detectable signals

# === R* — Star formation rate ===
# Modern estimates: ~1.5-3 solar masses per year in the Milky Way
R_STAR_LOW = 1.5       # stars/year (conservative)
R_STAR_HIGH = 3.0      # stars/year (upper estimate)
R_STAR_DEFAULT = 2.0   # stars/year (commonly used)

# === f_p — Fraction of stars with planets ===
# KEY: f_p ~ 1.0 is now well-established from the Kepler mission!
# Old estimates of f_p = 0.1 to 0.5 are WRONG and outdated.
# Nearly all stars have planetary systems.
F_P_MODERN = 1.0       # Kepler result — nearly all stars have planets
F_P_OLD_WRONG = 0.2    # Pre-Kepler estimate — DO NOT USE (kept for error detection)

# === n_e — Habitable planets per system ===
# Kepler data suggests ~0.1 to 0.4 Earth-like planets in habitable zone per star
N_E_LOW = 0.1
N_E_HIGH = 0.4
N_E_DEFAULT = 0.2

# === f_l — Fraction developing life ===
# Completely unknown — ranges from very pessimistic to optimistic
F_L_LOW = 0.01         # pessimistic
F_L_HIGH = 1.0         # optimistic (life is inevitable given right conditions)
F_L_DEFAULT = 0.5      # moderate guess

# === f_i — Fraction developing intelligence ===
# Also highly uncertain
F_I_LOW = 0.01         # pessimistic
F_I_HIGH = 1.0         # optimistic
F_I_DEFAULT = 0.5      # moderate guess

# === f_c — Fraction that communicate ===
# What fraction develop technology that emits detectable signals?
F_C_LOW = 0.01         # pessimistic
F_C_HIGH = 0.2         # optimistic
F_C_DEFAULT = 0.1      # moderate

# === L — Lifetime of communicating civilizations (years) ===
# Most uncertain factor — ranges over many orders of magnitude
L_LOW = 100            # pessimistic (self-destruction)
L_HIGH = 1e8           # optimistic (long-lived civilization)
L_DEFAULT = 10000      # moderate estimate
L_DRAKE_ORIGINAL = 10000  # Drake's 1961 estimate

# === Drake's original 1961 estimate ===
# Drake used: R*=1, f_p=0.2-0.5, n_e=1-5, f_l=1, f_i=1, f_c=0.1-0.2, L=1000-1e8
# Result: N ~ 10 (at the meeting, participants agreed on ~10)
N_DRAKE_ORIGINAL = 10

# === Test vectors ===
# Optimistic: 2 * 1.0 * 0.2 * 1.0 * 0.5 * 0.1 * 10000 = 200
OPTIMISTIC_R_STAR = 2.0
OPTIMISTIC_F_P = 1.0
OPTIMISTIC_N_E = 0.2
OPTIMISTIC_F_L = 1.0
OPTIMISTIC_F_I = 0.5
OPTIMISTIC_F_C = 0.1
OPTIMISTIC_L = 10000
OPTIMISTIC_N = 200.0

# Pessimistic: 1.5 * 1.0 * 0.1 * 0.01 * 0.01 * 0.01 * 1000 = 0.00015
PESSIMISTIC_R_STAR = 1.5
PESSIMISTIC_F_P = 1.0
PESSIMISTIC_N_E = 0.1
PESSIMISTIC_F_L = 0.01
PESSIMISTIC_F_I = 0.01
PESSIMISTIC_F_C = 0.01
PESSIMISTIC_L = 1000
PESSIMISTIC_N = 0.00015

# === Known LLM errors ===
PRIOR_ERRORS = {
    "fp_low":              "Uses f_p = 0.1-0.5 — now known to be ~1.0 from Kepler mission. "
                           "Nearly all stars have planets. Old estimates are outdated.",
    "factors_independent": "Treats all Drake factors as well-known or narrowly constrained. "
                           "In reality, f_l, f_i, f_c, and L span orders of magnitude.",
    "n_is_definite":       "Claims the Drake Equation gives a definite answer for N. "
                           "It does not — it is a framework for organized uncertainty. "
                           "N ranges from ~0.00015 to 200+ depending on assumptions.",
}
