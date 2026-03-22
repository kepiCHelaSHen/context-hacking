"""
Tidal Locking Timescale — Frozen Constants
Source: Murray & Dermott (Solar System Dynamics), Goldreich (1966),
        NASA Planetary Fact Sheets, Gladman et al. (1996)
DO NOT MODIFY.
"""
import math

# === Fundamental constants ===
G_NEWTON = 6.67430e-11     # N·m²/kg² (CODATA 2018)

# === Tidal locking timescale (simplified) ===
# t_lock = (ω * a⁶ * I * Q) / (3 * G * M_p² * k₂ * R⁵)
#
# ω   = initial spin angular velocity (rad/s)
# a   = orbital semi-major axis (m)
# I   = moment of inertia (kg·m²)
# Q   = tidal quality factor (dissipation)
# G   = gravitational constant
# M_p = mass of the primary (the body being orbited) (kg)
# k₂  = Love number (tidal deformability)
# R   = radius of the satellite (m)
#
# KEY INSIGHT: t_lock ∝ a⁶ — SIXTH power of orbital distance!
# Doubling the distance → 2⁶ = 64× longer to tidally lock.
# NOT a³ (common LLM mistake — confuses with Kepler's law).

# === Tidal quality factors Q ===
# Higher Q = less dissipation = longer locking time
Q_EARTH = 12              # Earth tidal Q (ocean + solid body)
Q_MOON = 27               # Moon tidal Q
Q_JUPITER = 1.0e5         # Jupiter Q (lower bound, gas giant — very little dissipation)
Q_JUPITER_HIGH = 1.0e6    # Jupiter Q (upper bound)
Q_MARS = 80               # Mars tidal Q estimate
Q_IO = 100                # Io tidal Q estimate

# === Love numbers k₂ ===
K2_EARTH = 0.30            # Earth Love number
K2_MOON = 0.024            # Moon Love number
K2_MARS = 0.17             # Mars Love number

# === Masses ===
M_EARTH = 5.972e24         # kg
M_MOON = 7.342e22          # kg
M_SUN = 1.98892e30         # kg
M_JUPITER = 1.898e27       # kg

# === Radii ===
R_MOON = 1.737e6           # m (mean radius)
R_EARTH = 6.371e6          # m (mean radius)

# === Orbital parameters ===
A_MOON = 3.844e8           # m (Moon semi-major axis, current)
A_MOON_HALF = A_MOON / 2   # m (hypothetical: Moon at half distance)

# === Spin-orbit states ===
# Moon: tidally locked (1:1 resonance)
T_ORBIT_MOON = 27.322 * 86400      # s (sidereal orbital period, days → s)
T_SPIN_MOON = 27.322 * 86400       # s (spin period = orbital period, locked!)

# Mercury: 3:2 spin-orbit resonance (NOT 1:1 locked!)
# Spins 3 times for every 2 orbits
T_ORBIT_MERCURY = 87.969 * 86400   # s (sidereal orbital period)
T_SPIN_MERCURY = 58.646 * 86400    # s (sidereal rotation period)
# Ratio: T_orbit / T_spin = 87.969 / 58.646 ≈ 1.5 = 3/2

# Pluto-Charon: mutually tidally locked (both bodies locked to each other)
T_ORBIT_PLUTO_CHARON = 6.387 * 86400   # s
T_SPIN_PLUTO = 6.387 * 86400           # s (locked)
T_SPIN_CHARON = 6.387 * 86400          # s (locked)

# === Distance dependence verification ===
# t_lock ∝ a⁶
# Moon at current distance vs half distance:
# t_ratio = (a / a_half)⁶ = (2)⁶ = 64
DISTANCE_RATIO_TEST = (A_MOON / A_MOON_HALF) ** 6  # = 64.0
assert abs(DISTANCE_RATIO_TEST - 64.0) < 1e-10, "a⁶ ratio check failed"

# === Spin-orbit resonance verification ===
MERCURY_RESONANCE_RATIO = T_ORBIT_MERCURY / T_SPIN_MERCURY
# Should be ≈ 1.5 (i.e., 3:2)
assert abs(MERCURY_RESONANCE_RATIO - 1.5) < 0.01, (
    f"Mercury resonance check: {MERCURY_RESONANCE_RATIO:.4f}, expected ~1.5"
)

# === Known LLM errors ===
PRIOR_ERRORS = {
    "a_cubed_not_sixth":  "Uses a³ instead of a⁶ in tidal locking timescale — "
                          "confuses Kepler's 3rd law (T² ∝ a³) with tidal locking "
                          "(t_lock ∝ a⁶). Doubling distance should give 64×, not 8×.",
    "q_wrong_order":      "Uses wrong tidal Q for a body — e.g., uses Earth's Q≈12 "
                          "for Jupiter (Q≈10⁵-10⁶) or vice versa. Off by 4+ orders "
                          "of magnitude.",
    "mercury_is_locked":  "Claims Mercury is tidally locked 1:1 to the Sun — it is "
                          "actually in a 3:2 spin-orbit resonance (spins 3× per 2 orbits). "
                          "Ratio T_orb/T_spin ≈ 1.5, not 1.0.",
}
