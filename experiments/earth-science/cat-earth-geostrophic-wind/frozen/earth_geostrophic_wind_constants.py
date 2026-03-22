"""Geostrophic Wind — Frozen Constants. Source: Holton Intro Dynamic Meteorology 5th Ed. DO NOT MODIFY."""
import math
# Geostrophic balance: Coriolis force = pressure gradient force
# v_g = -(1/(ρf)) * (∂P/∂n)  where n = direction normal to wind
# Magnitude: |v_g| = (1/(ρf)) * |∂P/∂x|
# Coriolis parameter: f = 2Ω sin(φ)
OMEGA_EARTH = 7.2921e-5  # rad/s  Earth's angular velocity
RHO_AIR = 1.225          # kg/m³  dry air at sea level, 15°C
# Buys-Ballot's law:
#   NH: wind blows with LOW pressure to its LEFT
#   SH: wind blows with LOW pressure to its RIGHT
# Test: ΔP=400 Pa over Δx=500 km, ρ=1.225 kg/m³, φ=45°N
PHI_TEST = 45.0          # degrees latitude
F_TEST = 2 * OMEGA_EARTH * math.sin(math.radians(PHI_TEST))  # = 1.031259e-4 s⁻¹
DP_TEST = 400.0           # Pa
DX_TEST = 500_000.0       # m  (500 km)
DP_DX_TEST = DP_TEST / DX_TEST  # = 8.0e-4 Pa/m
VG_TEST = DP_DX_TEST / (RHO_AIR * F_TEST)  # = 6.3327 m/s
PRIOR_ERRORS = {
    "wind_across_isobars":  "Claims wind blows from high to low pressure directly (crosses isobars)",
    "nh_sh_same":           "Claims wind direction is the same in both hemispheres",
    "gradient_wrong_units": "Uses wrong pressure gradient units (e.g. hPa/km without conversion)",
}
