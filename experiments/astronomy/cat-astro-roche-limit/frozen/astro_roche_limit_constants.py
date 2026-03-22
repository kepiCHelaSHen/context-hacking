"""Roche Limit — Frozen Constants. Source: classical celestial mechanics (Roche 1849). DO NOT MODIFY."""
import math

# Roche limit: tidal disruption distance
# Rigid body:  d = R_M * (2 * rho_M / rho_m)^(1/3)
# Fluid body:  d = 2.456 * R_M * (rho_M / rho_m)^(1/3)   (Roche's original result)
# KEY: Density ratio exponent is 1/3 (CUBE ROOT), NOT linear!

COEFF_RIGID = 2.0    # factor inside cube root for rigid body
COEFF_FLUID = 2.456  # Roche's coefficient for fluid body

# Earth-Moon system test case
R_EARTH = 6.371e6    # m (mean radius of Earth)
RHO_EARTH = 5515.0   # kg/m^3 (mean density of Earth)
RHO_MOON = 3344.0    # kg/m^3 (mean density of Moon)
D_MOON_ACTUAL = 3.844e8  # m (384400 km — actual Moon distance)

# Density ratio cube root: (rho_Earth / rho_Moon)^(1/3)
DENSITY_RATIO_CUBEROOT = (RHO_EARTH / RHO_MOON) ** (1/3)  # ≈ 1.1817

# Roche limits for Earth-Moon system
D_ROCHE_RIGID_EARTH_MOON = R_EARTH * (COEFF_RIGID * RHO_EARTH / RHO_MOON) ** (1/3)
# = 6.371e6 * (2 * 5515/3344)^(1/3) = 6.371e6 * 1.4889 ≈ 9,484,000 m ≈ 9484 km

D_ROCHE_FLUID_EARTH_MOON = COEFF_FLUID * R_EARTH * (RHO_EARTH / RHO_MOON) ** (1/3)
# = 2.456 * 6.371e6 * 1.1817 ≈ 18,483,000 m ≈ 18483 km

# Saturn system — rings are INSIDE Roche limit (that's why they can't coalesce)
R_SATURN = 5.8232e7   # m (mean radius of Saturn)
RHO_SATURN = 687.0    # kg/m^3 (mean density of Saturn)
RHO_ICE = 500.0       # kg/m^3 (porous ice — ring particles are porous, NOT solid 917 kg/m^3)
D_SATURN_RING_OUTER = 1.367e8  # m (outer edge of B ring, ~136700 km)

D_ROCHE_FLUID_SATURN_ICE = COEFF_FLUID * R_SATURN * (RHO_SATURN / RHO_ICE) ** (1/3)
# Saturn's Roche limit for ice particles

# Verify Moon is well outside Roche limit
assert D_MOON_ACTUAL > D_ROCHE_FLUID_EARTH_MOON * 10, "Moon must be far outside Roche limit"

# Verify Saturn rings are inside Roche limit
assert D_SATURN_RING_OUTER < D_ROCHE_FLUID_SATURN_ICE, "Saturn B ring must be inside Roche limit"

PRIOR_ERRORS = {
    "density_ratio_linear":    "Uses rho_M/rho_m without cube root — must be (rho_M/rho_m)^(1/3)",
    "rigid_fluid_confused":    "Uses rigid coefficient (2^(1/3)≈1.26) when fluid (2.456) is needed or vice versa",
    "roche_inside_means_stable": "Claims object inside Roche limit is stable — inside means tidal disruption",
}
