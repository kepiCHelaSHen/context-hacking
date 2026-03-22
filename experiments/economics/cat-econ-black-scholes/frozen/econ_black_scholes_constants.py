"""Black-Scholes Option Pricing — Frozen Constants. Source: Hull, Options Futures & Other Derivatives 11th Ed. DO NOT MODIFY."""
import math

# Standard normal CDF via erf
def N(x):
    """Standard normal cumulative distribution function."""
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))

# --- Test case: at-the-money European option ---
S_TEST = 100.0       # Spot price
K_TEST = 100.0       # Strike price
R_TEST = 0.05        # Risk-free rate (annual)
SIGMA_TEST = 0.20    # Annualized volatility (20%)
T_TEST = 1.0         # Time to expiry (years)

# KEY: sigma is ANNUALIZED volatility.
# If given monthly sigma, must multiply by sqrt(12)!
# If given daily sigma, must multiply by sqrt(252)!

# d1 = [ln(S/K) + (r + sigma^2/2)*T] / (sigma*sqrt(T))
D1_TEST = (math.log(S_TEST / K_TEST) + (R_TEST + SIGMA_TEST**2 / 2) * T_TEST) / (SIGMA_TEST * math.sqrt(T_TEST))
# d2 = d1 - sigma*sqrt(T)  (NOT d1 + sigma*sqrt(T)!)
D2_TEST = D1_TEST - SIGMA_TEST * math.sqrt(T_TEST)

# N(d1), N(d2)
ND1_TEST = N(D1_TEST)
ND2_TEST = N(D2_TEST)

# Call: C = S*N(d1) - K*e^(-rT)*N(d2)
CALL_TEST = S_TEST * ND1_TEST - K_TEST * math.exp(-R_TEST * T_TEST) * ND2_TEST
# Put:  P = K*e^(-rT)*N(-d2) - S*N(-d1)
PUT_TEST = K_TEST * math.exp(-R_TEST * T_TEST) * N(-D2_TEST) - S_TEST * N(-D1_TEST)

# Put-call parity: C - P = S - K*e^(-rT)
PARITY_RHS = S_TEST - K_TEST * math.exp(-R_TEST * T_TEST)

# Monthly sigma error example: if someone gives sigma_monthly = 0.20 but it's really monthly
# They should annualize: sigma_annual = 0.20 * sqrt(12) ≈ 0.6928
SIGMA_MONTHLY_EXAMPLE = 0.20
SIGMA_ANNUALIZED_FROM_MONTHLY = SIGMA_MONTHLY_EXAMPLE * math.sqrt(12)

PRIOR_ERRORS = {
    "sigma_not_annualized":    "Uses monthly sigma without sqrt(12) scaling — volatility must be annualized",
    "d2_wrong_sign":           "Computes d2 = d1 + sigma*sqrt(T) instead of d1 - sigma*sqrt(T)",
    "put_call_parity_wrong":   "Uses wrong parity formula (e.g., C + P = S - Ke^(-rT) instead of C - P)",
}
