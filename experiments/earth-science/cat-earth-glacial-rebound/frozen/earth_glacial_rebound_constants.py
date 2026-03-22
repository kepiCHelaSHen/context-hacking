"""Glacial Rebound (Isostatic Adjustment) — Frozen Constants. Source: Turcotte & Schubert, Geodynamics 3rd Ed. DO NOT MODIFY."""
import math

# Isostasy: rho_ice * h_ice = rho_mantle * d  =>  d = h_ice * rho_ice / rho_mantle
RHO_ICE = 917        # kg/m^3
RHO_MANTLE = 3300    # kg/m^3
DENSITY_RATIO = RHO_ICE / RHO_MANTLE  # 0.27788...  (NOT inverted!)

# Post-glacial rebound: exponential recovery
# d(t) = d0 * exp(-t / tau)
# Relaxation time: tau ~ 4*pi*eta / (rho_mantle * g * lambda) for wavelength lambda
# Typical tau ~ 3000-5000 years for Fennoscandia

# Mantle viscosity — THE critical value
# eta ~ 10^21 Pa·s  (NOT 10^18 which is asthenosphere, NOT 10^24 which is lower mantle)
MANTLE_VISCOSITY_ORDER = 21  # log10(eta / Pa·s)
MANTLE_VISCOSITY = 1e21      # Pa·s

# Test scenario: 3 km ice sheet over Fennoscandia
TEST_H_ICE = 3000.0        # m
TEST_D0 = TEST_H_ICE * DENSITY_RATIO  # 833.636... m depression
TEST_TAU = 4000.0           # years (relaxation time)
TEST_T = 10000.0            # years after ice removal

# Expected results
TEST_REBOUND_REMAINING = TEST_D0 * math.exp(-TEST_T / TEST_TAU)  # d0*exp(-2.5) ~ 68.4 m
TEST_UPLIFT_RATE_T0 = TEST_D0 / TEST_TAU  # m/yr at t=0 ~ 0.2084 m/yr = 208.4 mm/yr
TEST_UPLIFT_RATE_T = (TEST_D0 / TEST_TAU) * math.exp(-TEST_T / TEST_TAU)  # at t=10000yr

# Current Scandinavian uplift rate: ~10 mm/yr (still rising after ~10000 years)
CURRENT_SCANDINAVIA_RATE_MM = 10.0  # mm/yr (approximate)

PRIOR_ERRORS = {
    "viscosity_wrong_order":   "Uses mantle viscosity 10^18 or 10^24 instead of correct 10^21 Pa·s",
    "linear_not_exponential":  "Models rebound as linear d(t)=d0-rate*t instead of exponential d0*exp(-t/tau)",
    "density_ratio_inverted":  "Uses rho_mantle/rho_ice instead of rho_ice/rho_mantle for depression depth",
}
