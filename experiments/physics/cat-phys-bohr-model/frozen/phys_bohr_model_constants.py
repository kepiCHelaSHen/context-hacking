"""
Bohr Model of Hydrogen — Frozen Constants
Source: CODATA 2018, Bohr (1913)
DO NOT MODIFY.
"""

# Rydberg constant
R_INF = 1.0973731568160e7  # m⁻¹ (CODATA 2018)
# LLM prior: 1.097e7 (4 sig figs)

# Rydberg energy
RY_EV = 13.605693122994    # eV (ionization energy of hydrogen)
# LLM prior: 13.6 eV (3 sig figs)

# Bohr radius
A0 = 5.29177210903e-11    # m (CODATA 2018)
# = 0.529 Å
# LLM prior: 0.53 Å

# Energy levels: E_n = -13.6/n² eV
# LLM prior: wrong sign (positive) or wrong n dependence

# Balmer series: 1/λ = R_inf * (1/2² - 1/n²), n = 3,4,5,...
# First line (Hα): n=3→2, λ = 656.3 nm (red)
LAMBDA_H_ALPHA = 1.0 / (R_INF * (1.0/4 - 1.0/9))   # = 656.3 nm

# Lyman series: n→1, UV
# Lyman alpha: n=2→1
LAMBDA_LYMAN_ALPHA = 1.0 / (R_INF * (1.0 - 1.0/4))  # = 121.6 nm

# Paschen series: n→3, IR
LAMBDA_PASCHEN_ALPHA = 1.0 / (R_INF * (1.0/9 - 1.0/16))  # = 1875 nm

PRIOR_ERRORS = {
    "energy_positive":     "Uses E_n = +13.6/n² (should be NEGATIVE)",
    "n_not_squared":       "Uses E_n = -13.6/n instead of -13.6/n²",
    "rydberg_rounded":     "Uses R∞ = 1.097e7 instead of full precision",
    "wrong_n_assignment":  "Confuses n_upper and n_lower in spectral series",
}
