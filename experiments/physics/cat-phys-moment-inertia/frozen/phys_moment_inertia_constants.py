"""Moment of Inertia — Frozen Constants. Source: Halliday 12th Ed Table 10-2. DO NOT MODIFY."""
import math
# Standard shapes about center of mass
I_SOLID_SPHERE = lambda m, r: 2/5 * m * r**2
I_HOLLOW_SPHERE = lambda m, r: 2/3 * m * r**2  # LLM prior: uses 2/5 (solid)
I_SOLID_CYLINDER = lambda m, r: 1/2 * m * r**2
I_HOLLOW_CYLINDER = lambda m, r1, r2: 1/2 * m * (r1**2 + r2**2)
I_ROD_CENTER = lambda m, L: 1/12 * m * L**2
I_ROD_END = lambda m, L: 1/3 * m * L**2
I_DISK = lambda m, r: 1/2 * m * r**2
# Parallel axis theorem: I = I_cm + m*d^2
# Test: solid sphere m=2kg, r=0.1m
I_TEST_SOLID = 2/5 * 2.0 * 0.1**2   # = 0.008 kg·m²
I_TEST_HOLLOW = 2/3 * 2.0 * 0.1**2  # = 0.01333 kg·m²
PRIOR_ERRORS = {
    "hollow_solid_swap": "Uses 2/5 for hollow sphere (should be 2/3)",
    "rod_center_vs_end": "Uses 1/3 for rod about center (should be 1/12)",
    "parallel_axis":     "Forgets md² term in parallel axis theorem",
}
