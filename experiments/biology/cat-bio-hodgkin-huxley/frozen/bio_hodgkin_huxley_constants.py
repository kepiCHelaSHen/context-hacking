"""Hodgkin-Huxley Ionic Currents — Frozen Constants. Source: Hodgkin & Huxley 1952. DO NOT MODIFY."""
import math

# I_ion = g_Na * m^3 * h * (V - E_Na) + g_K * n^4 * (V - E_K) + g_L * (V - E_L)
# Na channel: m = activation (opens FAST), h = inactivation (closes SLOW) → m^3 * h
# K channel:  n = activation (opens SLOW) → n^4
# KEY: Na channel has BOTH activation (m) AND inactivation (h).
#   m RISES during depolarization (opens the channel)
#   h FALLS during depolarization (closes the channel after delay)
#   This produces the transient Na+ current underlying the action potential upstroke.

# Maximal conductances (mS/cm^2)
G_NA = 120.0    # sodium
G_K  = 36.0     # potassium
G_L  = 0.3      # leak

# Reversal potentials (mV)
E_NA = 50.0     # sodium (positive — Na+ flows inward)
E_K  = -77.0    # potassium (negative — K+ flows outward)
E_L  = -54.4    # leak

# Resting state (V ≈ -65 mV)
V_REST = -65.0
M_REST = 0.05   # m ≈ 0.05  (Na activation — mostly closed at rest)
H_REST = 0.6    # h ≈ 0.6   (Na inactivation — mostly available at rest)
N_REST = 0.32   # n ≈ 0.32  (K activation — partially open at rest)

# Precomputed reference currents at resting state
I_NA_REST = G_NA * M_REST**3 * H_REST * (V_REST - E_NA)   # ≈ -1.035 µA/cm²
I_K_REST  = G_K  * N_REST**4 * (V_REST - E_K)              # ≈  4.5298 µA/cm²
I_L_REST  = G_L  * (V_REST - E_L)                          # ≈ -3.18 µA/cm²
I_TOTAL_REST = I_NA_REST + I_K_REST + I_L_REST              # ≈  0.3148 µA/cm²

# Self-checks: sign and magnitude
assert I_NA_REST < 0, "Na current at rest must be inward (negative)"
assert I_K_REST  > 0, "K current at rest must be outward (positive)"
assert I_L_REST  < 0, "Leak current at rest must be inward (V < E_L)"
assert math.isclose(I_NA_REST, G_NA * M_REST**3 * H_REST * (V_REST - E_NA), rel_tol=1e-12)
assert math.isclose(I_K_REST,  G_K  * N_REST**4 * (V_REST - E_K),  rel_tol=1e-12)
assert math.isclose(I_L_REST,  G_L  * (V_REST - E_L),              rel_tol=1e-12)

# Verify Na uses m^3*h (not m^3 alone): removing h changes the value
_i_na_no_h = G_NA * M_REST**3 * (V_REST - E_NA)
assert not math.isclose(I_NA_REST, _i_na_no_h, rel_tol=1e-3), \
    "Na current MUST include h (inactivation gate)"

# Verify K uses n^4 (not n^3): exponent matters
_i_k_n3 = G_K * N_REST**3 * (V_REST - E_K)
assert not math.isclose(I_K_REST, _i_k_n3, rel_tol=1e-3), \
    "K current MUST use n^4, not n^3"

PRIOR_ERRORS = {
    "m_h_confusion":    "Confuses m (activation, rises) with h (inactivation, falls) during depolarization",
    "n_cubed_not_fourth": "Uses n^3 instead of n^4 for potassium conductance",
    "no_inactivation":  "Omits h from Na current, using g_Na*m^3*(V-E_Na) instead of g_Na*m^3*h*(V-E_Na)",
}
