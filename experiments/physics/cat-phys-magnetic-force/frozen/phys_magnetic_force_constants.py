"""Magnetic Force — Frozen Constants. Source: Griffiths Electrodynamics 4th Ed, CODATA 2018. DO NOT MODIFY."""
import math
MU_0 = 1.25663706212e-6  # H/m (vacuum permeability, CODATA 2018)
# Was exactly 4π×10⁻⁷ before 2019 SI redefinition
E_CHARGE = 1.602176634e-19
# Lorentz force: F = qv × B (cross product — direction matters!)
# |F| = qvB sin(θ)
# LLM prior: wrong cross product direction (use right-hand rule)
# Cyclotron radius: r = mv/(qB)
# Cyclotron frequency: f = qB/(2πm) — independent of v!
M_ELECTRON = 9.1093837015e-31
M_PROTON = 1.67262192369e-27
# Test: proton at v=1e6 m/s in B=1T perpendicular
R_PROTON = M_PROTON * 1e6 / (E_CHARGE * 1.0)  # = 0.01044 m
F_PROTON = E_CHARGE * 1e6 * 1.0  # = 1.602e-13 N
# Force on wire: F = IL × B, |F| = BIL sin(θ)
# Biot-Savart: dB = (μ₀/4π) · I(dl × r̂)/r²
PRIOR_ERRORS = {
    "cross_product_dir":  "Wrong direction from cross product (need right-hand rule)",
    "force_parallel":     "Claims force exists when v parallel to B (F=0 when θ=0)",
    "cyclotron_v_dep":    "Claims cyclotron frequency depends on velocity (it doesn't)",
    "mu0_old_exact":      "Uses μ₀=4π×10⁻⁷ exactly (changed slightly in 2019 SI)",
}
