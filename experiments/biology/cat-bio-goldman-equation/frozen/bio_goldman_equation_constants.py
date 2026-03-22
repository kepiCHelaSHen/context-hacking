"""Goldman-Hodgkin-Katz Equation — Frozen Constants. Source: Goldman 1943, Hodgkin & Katz 1949. DO NOT MODIFY."""
import math

# V_m = (RT/F) * ln( (P_K[K]_o + P_Na[Na]_o + P_Cl[Cl]_i) / (P_K[K]_i + P_Na[Na]_i + P_Cl[Cl]_o) )
#
# KEY: Anions (Cl⁻) have REVERSED inside/outside compared to cations in GHK equation!
#   Cations (K⁺, Na⁺): [outside] in numerator, [inside] in denominator
#   Anions  (Cl⁻):      [inside] in numerator, [outside] in denominator
# This reversal arises because anions carry negative charge — their electrochemical
# gradient reverses relative to cations.

# Physical constants
R = 8.314462618       # J/(mol·K)  — gas constant
F = 96485.33212       # C/mol      — Faraday constant

# Physiological temperature
T = 310.15            # K  (37 °C)

# RT/F in mV
RT_F_MV = (R * T / F) * 1000.0   # ≈ 26.727 mV

# Permeability ratios at rest: P_K : P_Na : P_Cl ≈ 1 : 0.04 : 0.45
P_K  = 1.0
P_NA = 0.04
P_CL = 0.45

# Typical mammalian ion concentrations (mM)
K_O   = 4.0      # extracellular K⁺
K_I   = 140.0    # intracellular K⁺
NA_O  = 145.0    # extracellular Na⁺
NA_I  = 12.0     # intracellular Na⁺
CL_O  = 120.0    # extracellular Cl⁻
CL_I  = 4.0      # intracellular Cl⁻

# Precomputed reference: GHK numerator & denominator
# Numerator:   P_K*[K]_o  + P_Na*[Na]_o + P_Cl*[Cl]_i   (anion uses INSIDE)
# Denominator: P_K*[K]_i  + P_Na*[Na]_i + P_Cl*[Cl]_o   (anion uses OUTSIDE)
GHK_NUMERATOR   = P_K * K_O + P_NA * NA_O + P_CL * CL_I    # = 11.6
GHK_DENOMINATOR = P_K * K_I + P_NA * NA_I + P_CL * CL_O    # = 194.48

# Resting membrane potential
V_M_REST = RT_F_MV * math.log(GHK_NUMERATOR / GHK_DENOMINATOR)  # ≈ -75.35 mV

# Wrong values (Cl⁻ treated like a cation — a common LLM error)
GHK_NUM_WRONG_CL = P_K * K_O + P_NA * NA_O + P_CL * CL_O   # = 63.8  (WRONG)
GHK_DEN_WRONG_CL = P_K * K_I + P_NA * NA_I + P_CL * CL_I   # = 142.28 (WRONG)
V_M_WRONG_CL = RT_F_MV * math.log(GHK_NUM_WRONG_CL / GHK_DEN_WRONG_CL)  # ≈ -21.4 mV

# V_m without Cl⁻ (K⁺ and Na⁺ only)
GHK_NUM_NO_CL = P_K * K_O + P_NA * NA_O        # = 9.8
GHK_DEN_NO_CL = P_K * K_I + P_NA * NA_I        # = 140.48
V_M_NO_CL = RT_F_MV * math.log(GHK_NUM_NO_CL / GHK_DEN_NO_CL)  # ≈ -71.16 mV

# Self-checks: verify numerator/denominator components
assert math.isclose(GHK_NUMERATOR,   11.6,    rel_tol=1e-9), f"Numerator {GHK_NUMERATOR} != 11.6"
assert math.isclose(GHK_DENOMINATOR, 194.48,  rel_tol=1e-9), f"Denominator {GHK_DENOMINATOR} != 194.48"

# Self-check: V_m in correct range (strongly negative, near -75 mV)
assert -80.0 < V_M_REST < -70.0, f"V_m = {V_M_REST:.2f} mV not in [-80, -70] range"

# Self-check: wrong Cl handling gives too-depolarized result
assert -25.0 < V_M_WRONG_CL < -18.0, f"V_m_wrong = {V_M_WRONG_CL:.2f} mV not near -21 mV"

# Self-check: correct V_m is much more negative than wrong
assert V_M_REST < V_M_WRONG_CL - 40.0, \
    "Correct V_m must be >40 mV more negative than wrong-Cl version"

# Verify anion reversal: Cl_i appears in numerator, Cl_o in denominator
# If we swap them (treat Cl like cation) the result changes drastically
assert not math.isclose(V_M_REST, V_M_WRONG_CL, abs_tol=5.0), \
    "Swapping Cl_i/Cl_o must produce a very different V_m"

PRIOR_ERRORS = {
    "cl_like_cation":      "Treats Cl⁻ same as cations — puts [Cl]_o in numerator and [Cl]_i in denominator (yields ≈-21 mV instead of ≈-75 mV)",
    "permeability_ignored": "Uses equal permeabilities for all ions instead of P_K:P_Na:P_Cl = 1:0.04:0.45",
    "missing_anion":       "Forgets Cl⁻ entirely, computing GHK with only K⁺ and Na⁺ (yields ≈-71 mV)",
}
