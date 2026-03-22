"""One-Compartment Pharmacokinetics — Frozen Constants. Source: Gibaldi & Perrier 1982. DO NOT MODIFY."""
import math
# C(t) = C₀ * e^(-ke*t)  (first-order elimination)
# t½ = ln(2)/ke = 0.693/ke  (NOT 1/ke!)
# KEY: half-life uses ln(2), not 1
# If you wrongly use t½ = 1/ke:  for ke=0.1 hr⁻¹, wrong t½=10hr, correct t½=6.93hr
# Vd = Dose/C₀,  CL = ke * Vd
# Steady state: ~5 half-lives to reach ~97% of Css
# Test: C₀=100 mg/L, ke=0.1 hr⁻¹, Dose=500mg
#   t½ = ln(2)/0.1 = 6.9315 hr
#   Wrong t½ = 1/0.1 = 10 hr
#   C(6.93) = 100*e^(-0.693) = 50 mg/L  (half of C₀ at true t½ ✓)
#   C(10)   = 100*e^(-1.0)   = 36.79 mg/L  (NOT 50, so t½≠10)
#   Vd = 500/100 = 5 L
#   CL = 0.1 * 5 = 0.5 L/hr
C0 = 100.0            # mg/L — initial concentration
KE = 0.1              # hr⁻¹ — elimination rate constant
DOSE = 500.0          # mg — administered dose
HALF_LIFE = math.log(2) / KE          # 6.931471805599453 hr (correct)
WRONG_HALF_LIFE = 1.0 / KE            # 10.0 hr (the common LLM mistake)
VD = DOSE / C0                         # 5.0 L — volume of distribution
CL = KE * VD                           # 0.5 L/hr — clearance
C_AT_HALF_LIFE = C0 * math.exp(-KE * HALF_LIFE)   # 50.0 mg/L (exactly C₀/2)
C_AT_10HR = C0 * math.exp(-KE * 10.0)             # 36.7879… mg/L
assert math.isclose(HALF_LIFE, 6.931471805599453, rel_tol=1e-9), "t½ must be ln(2)/ke"
assert math.isclose(C_AT_HALF_LIFE, 50.0, rel_tol=1e-9), "C at t½ must be C₀/2"
assert not math.isclose(WRONG_HALF_LIFE, HALF_LIFE, rel_tol=0.01), "Wrong t½ must differ"
assert not math.isclose(C_AT_10HR, 50.0, rel_tol=0.01), "C at wrong t½ must NOT be C₀/2"
PRIOR_ERRORS = {
    "half_life_1_over_ke":   "Uses 1/ke instead of ln(2)/ke for half-life",
    "wrong_steady_state":    "Claims 3 half-lives (not 5) to reach steady state",
    "clearance_formula":     "Uses CL=Vd/ke instead of CL=ke*Vd",
}
