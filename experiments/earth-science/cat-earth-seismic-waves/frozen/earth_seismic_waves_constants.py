"""Seismic Waves — Frozen Constants. Source: Shearer, Intro to Seismology 2nd Ed. DO NOT MODIFY."""
import math

# P-wave (compressional): Vp = sqrt((K + 4G/3) / rho)
# S-wave (shear):         Vs = sqrt(G / rho)
# S-waves CANNOT travel through fluids — G=0 in liquids => Vs=0

# Upper mantle approximate elastic moduli (PREM reference model)
K_UPPER_MANTLE = 130e9    # Pa  bulk modulus
G_UPPER_MANTLE = 80e9     # Pa  shear modulus
RHO_UPPER_MANTLE = 3300.0 # kg/m^3  density

# Computed reference velocities for upper mantle
#   Vp = sqrt((130e9 + 4*80e9/3) / 3300)
#      = sqrt((130e9 + 106.667e9) / 3300)
#      = sqrt(236.667e9 / 3300)
#      = sqrt(71717171.7...)
#      = 8468.6 m/s  ~ 8.5 km/s
VP_UPPER_MANTLE = math.sqrt((K_UPPER_MANTLE + 4 * G_UPPER_MANTLE / 3) / RHO_UPPER_MANTLE)

#   Vs = sqrt(80e9 / 3300) = sqrt(24242424.2...) = 4923.7 m/s  ~ 4.9 km/s
VS_UPPER_MANTLE = math.sqrt(G_UPPER_MANTLE / RHO_UPPER_MANTLE)

# Vp/Vs ratio for a Poisson solid (nu=0.25): Vp/Vs = sqrt(3) ~ 1.732
VP_VS_RATIO_POISSON = math.sqrt(3)
VP_VS_RATIO_UPPER_MANTLE = VP_UPPER_MANTLE / VS_UPPER_MANTLE

# Liquid outer core: G = 0 => S-waves CANNOT propagate
G_LIQUID = 0.0
K_OUTER_CORE = 650e9     # Pa  approximate bulk modulus outer core
RHO_OUTER_CORE = 10000.0 # kg/m^3  approximate density
VP_OUTER_CORE = math.sqrt(K_OUTER_CORE / RHO_OUTER_CORE)  # P-wave still works
VS_OUTER_CORE = 0.0      # ZERO — no S-waves in liquid!

# S-wave shadow zone: 104 to 140 degrees from epicenter
SHADOW_ZONE_MIN_DEG = 104.0
SHADOW_ZONE_MAX_DEG = 140.0

# Test scenario: upper mantle parameters
TEST_K = K_UPPER_MANTLE
TEST_G = G_UPPER_MANTLE
TEST_RHO = RHO_UPPER_MANTLE
TEST_VP = VP_UPPER_MANTLE
TEST_VS = VS_UPPER_MANTLE

PRIOR_ERRORS = {
    "s_through_liquid": "Claims S-waves can travel through liquid (WRONG — G=0 in fluids, Vs=0)",
    "vp_vs_equal":      "Claims P-wave and S-wave travel at the same speed (P always faster)",
    "shadow_zone_wrong": "Gives wrong angular range for S-wave shadow zone (should be 104-140 deg)",
}
