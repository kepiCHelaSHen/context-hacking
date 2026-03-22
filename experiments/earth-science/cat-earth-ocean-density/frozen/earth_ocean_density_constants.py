"""Ocean Water Density — Frozen Constants. Source: Pond & Pickard 'Introductory Dynamical Oceanography' 3rd Ed. DO NOT MODIFY."""
import math

# Seawater density depends on Temperature, Salinity, AND Pressure (all three!)
# Simplified empirical approximation near surface (P ≈ 0):
#   ρ ≈ 1000 + 0.8*S - 0.0065*(T - 4)²
#   S in psu (practical salinity units), T in °C

# Coefficients
SALT_COEFF = 0.8       # kg/m³ per psu
TEMP_COEFF = 0.0065    # kg/m³ per °C²  (quadratic around 4°C)
RHO_BASE = 1000.0      # kg/m³ base density (pure water at 4°C)
T_MAX_DENSITY = 4.0    # °C — freshwater max density temperature (anomaly!)

# Typical ocean ranges
T_OCEAN_MIN = 2.0      # °C (deep ocean)
T_OCEAN_MAX = 30.0     # °C (tropical surface)
S_OCEAN_MIN = 33.0     # psu
S_OCEAN_MAX = 37.0     # psu
RHO_OCEAN_MIN = 1020.0 # kg/m³ (approximate lower bound)
RHO_OCEAN_MAX = 1028.0 # kg/m³ (approximate upper bound)

# σ_t (sigma-t) notation: σ_t = ρ - 1000
# e.g., σ_t = 25 means ρ = 1025 kg/m³
SIGMA_T_OFFSET = 1000.0

# Test case: T=10°C, S=35 psu
TEST_T = 10.0          # °C
TEST_S = 35.0          # psu
# ρ = 1000 + 0.8*35 - 0.0065*(10-4)² = 1000 + 28 - 0.0065*36 = 1028 - 0.234 = 1027.766
TEST_RHO = RHO_BASE + SALT_COEFF * TEST_S - TEMP_COEFF * (TEST_T - T_MAX_DENSITY)**2
# = 1027.766 kg/m³
TEST_SIGMA_T = TEST_RHO - SIGMA_T_OFFSET  # = 27.766

# Second test: T=25°C, S=36 psu (warm tropical water)
TEST2_T = 25.0
TEST2_S = 36.0
TEST2_RHO = RHO_BASE + SALT_COEFF * TEST2_S - TEMP_COEFF * (TEST2_T - T_MAX_DENSITY)**2
# = 1000 + 28.8 - 0.0065*441 = 1028.8 - 2.8665 = 1025.9335
TEST2_SIGMA_T = TEST2_RHO - SIGMA_T_OFFSET  # = 25.9335

# Freshwater (S=0) at 4°C — maximum density
FRESHWATER_MAX_RHO = RHO_BASE + SALT_COEFF * 0 - TEMP_COEFF * (T_MAX_DENSITY - T_MAX_DENSITY)**2
# = 1000.0 kg/m³ exactly (by construction of the approximation)

# Density change with temperature: higher T → lower density above 4°C
# (because the quadratic term -(T-4)² increases with |T-4|)

PRIOR_ERRORS = {
    "density_only_salinity": "Uses only salinity to compute density — ignores temperature effect entirely",
    "freshwater_max_0C":     "Claims freshwater maximum density occurs at 0°C, not 4°C",
    "sigma_t_wrong":         "Confuses σ_t with full density (e.g., reports 25 instead of 1025 kg/m³)",
}
