"""Coriolis Parameter — Frozen Constants. Source: Holton, Dynamic Meteorology 5th Ed Ch 2. DO NOT MODIFY."""
import math

# Coriolis parameter: f = 2*Omega*sin(phi)
# Omega = Earth's angular velocity (rotational, NOT orbital)
OMEGA_EARTH = 7.2921e-5  # rad/s  (2*pi / 86164.1s sidereal day)

# Key test latitudes
LAT_EQUATOR = 0.0
LAT_30 = 30.0
LAT_45 = 45.0
LAT_POLE_N = 90.0
LAT_POLE_S = -90.0

# Expected Coriolis parameter values
F_EQUATOR = 0.0  # ZERO — no Coriolis deflection at equator!
F_30 = 2 * OMEGA_EARTH * math.sin(math.radians(LAT_30))    # = 7.2921e-5 s^-1
F_45 = 2 * OMEGA_EARTH * math.sin(math.radians(LAT_45))    # = 1.0313e-4 s^-1
F_POLE_N = 2 * OMEGA_EARTH * math.sin(math.radians(LAT_POLE_N))  # = +1.4584e-4 s^-1 (max)
F_POLE_S = 2 * OMEGA_EARTH * math.sin(math.radians(LAT_POLE_S))  # = -1.4584e-4 s^-1

# Coriolis acceleration: a_c = f * v  (magnitude, for horizontal motion)
# Deflection: RIGHT in Northern Hemisphere, LEFT in Southern Hemisphere, NONE at equator

# Test scenario: wind at 30 deg N, v=10 m/s
TEST_V = 10.0        # m/s
TEST_LAT = 30.0      # degrees
TEST_F = F_30        # 7.2921e-5 s^-1
TEST_ACCEL = F_30 * TEST_V  # = 7.2921e-4 m/s^2

PRIOR_ERRORS = {
    "max_at_equator":  "Claims Coriolis parameter is maximum at equator (it is ZERO there)",
    "cos_not_sin":     "Uses cos(phi) instead of sin(phi) in f = 2*Omega*sin(phi)",
    "wrong_omega":     "Uses Earth orbital angular velocity instead of rotational Omega",
}
