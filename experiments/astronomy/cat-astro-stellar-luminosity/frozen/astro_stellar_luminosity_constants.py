"""Stellar Luminosity (Stefan-Boltzmann) — Frozen Constants. Source: IAU 2015 Nominal Values. DO NOT MODIFY."""
import math

# Stefan-Boltzmann Law: L = 4*pi*R^2 * sigma * T^4
# KEY: R must be in METERS for SI formula. Common error: using km or solar radii directly.
SIGMA = 5.670e-8  # Stefan-Boltzmann constant, W/(m^2 K^4)

# Solar reference values (IAU 2015 nominal)
L_SUN = 3.828e26   # W (solar luminosity)
R_SUN = 6.957e8    # m (solar radius)
T_SUN = 5778       # K (solar effective temperature)

# Verification: L = 4*pi*R_sun^2 * sigma * T_sun^4
# = 4*pi*(6.957e8)^2 * 5.670e-8 * (5778)^4
# = 4*pi*4.840e17 * 5.670e-8 * 1.115e15
# = 3.844e26 W  (within 0.4% of L_SUN — rounding of constants)
L_SUN_CALC = 4 * math.pi * R_SUN**2 * SIGMA * T_SUN**4

# Solar-units formula: L/L_sun = (R/R_sun)^2 * (T/T_sun)^4
# This avoids unit issues entirely — no meters needed.

# Test star: Sirius A — T=9940 K, R=1.711 R_sun
T_SIRIUS = 9940       # K
R_SIRIUS_RSUN = 1.711  # solar radii
R_SIRIUS_M = R_SIRIUS_RSUN * R_SUN  # = 1.190e9 m

# SI calculation
L_SIRIUS = 4 * math.pi * R_SIRIUS_M**2 * SIGMA * T_SIRIUS**4
# = 9.856e27 W

# Solar-units calculation
L_SIRIUS_SOLAR = R_SIRIUS_RSUN**2 * (T_SIRIUS / T_SUN)**4
# = 2.928 * 8.759 = 25.64 L_sun

# Wrong-unit traps (for testing LLM errors)
R_SUN_KM = 6.957e5     # km — WRONG unit for SI formula
R_SUN_AU = 4.6505e-3   # AU — WRONG unit for SI formula

PRIOR_ERRORS = {
    "r_not_meters":          "Uses R in km or solar radii directly in SI formula L=4piR^2*sigma*T^4",
    "sigma_wrong":           "Uses wrong Stefan-Boltzmann constant (e.g. 5.67e-9 or confuses with Boltzmann k)",
    "t_squared_not_fourth":  "Uses T^2 instead of T^4 in Stefan-Boltzmann law",
}
