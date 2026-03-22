"""Diffraction — Frozen Constants. Source: Hecht Optics 5th Ed. DO NOT MODIFY."""
import math
# Single slit: minima at a·sin(θ) = mλ, m = ±1, ±2, ...
# Double slit: maxima at d·sin(θ) = mλ, m = 0, ±1, ±2, ...
# LLM prior: confuses minima/maxima conditions between single and double slit
# Single slit central maximum angular width: 2θ where sin(θ) = λ/a
# Test: λ=632.8nm (HeNe laser), slit width a=0.1mm
LAMBDA_HENE = 632.8e-9  # m
A_SLIT = 1e-4           # m (0.1 mm)
THETA_FIRST_MIN = math.asin(LAMBDA_HENE / A_SLIT)  # = 0.006328 rad = 0.3626°
# Double slit: d=0.5mm
D_SLITS = 5e-4          # m
THETA_FIRST_MAX = math.asin(LAMBDA_HENE / D_SLITS)  # = 0.001266 rad
# Rayleigh criterion: θ_min = 1.22 λ/D (circular aperture)
D_APERTURE = 0.01       # m (1cm lens)
THETA_RAYLEIGH = 1.22 * LAMBDA_HENE / D_APERTURE  # = 7.72e-5 rad
PRIOR_ERRORS = {
    "min_max_swap":      "Uses maxima condition for single-slit minima (or vice versa)",
    "missing_1_22":      "Forgets 1.22 factor in Rayleigh criterion for circular aperture",
    "order_zero":        "Includes m=0 as minimum in single slit (it's the central max)",
}
