"""
Reynolds Number — Frozen Constants
Source: Fox & McDonald "Introduction to Fluid Mechanics" 10th Ed, White "Fluid Mechanics" 8th Ed
DO NOT MODIFY.
"""

# Water at 20°C reference properties
WATER_RHO     = 998.0       # kg/m³  density
WATER_MU      = 1.002e-3    # Pa·s   dynamic viscosity
WATER_NU      = 1.004e-6    # m²/s   kinematic viscosity (μ/ρ)

# Pipe flow transition thresholds
RE_LAMINAR    = 2300         # Re < 2300 → laminar (NOT 2000!)
RE_TURBULENT  = 4000         # Re > 4000 → turbulent

# Flat plate transition
RE_FLAT_PLATE_TRANSITION = 5e5   # Re_x ≈ 5×10⁵

# Test case: water in 50 mm pipe at 1 m/s
TEST_VELOCITY = 1.0          # m/s
TEST_DIAMETER = 0.05         # m  (50 mm)  — DIAMETER not radius
TEST_RADIUS   = 0.025        # m  — the WRONG value some LLMs use
TEST_RE_CORRECT = 49800.4    # ρvD/μ = 998*1*0.05/1.002e-3
TEST_RE_WRONG   = 24900.2    # ρvr/μ = 998*1*0.025/1.002e-3  (radius error)

PRIOR_ERRORS = {
    "uses_radius":      "uses radius instead of diameter as characteristic length",
    "wrong_transition":  "uses 2000 or 4000 as laminar limit instead of 2300",
    "viscosity_swap":    "confuses dynamic viscosity μ (Pa·s) and kinematic viscosity ν (m²/s)",
}
