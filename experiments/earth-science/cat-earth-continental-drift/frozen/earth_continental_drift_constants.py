"""Plate Velocity from Hotspot Tracks — Frozen Constants. Source: Clague & Dalrymple 1987; Torsvik et al. 2017. DO NOT MODIFY."""
# Hawaiian-Emperor chain: hotspot track with major bend at ~43 Ma
# Ages increase AWAY from hotspot (youngest island closest to hotspot)
# Before bend (~43 Ma): Pacific plate moved NNW at ~65 mm/yr
# After bend (recent): Pacific plate moved WNW at ~81 mm/yr
# KEY: velocity changes at major bends — must use segment-by-segment calculation

# Test chain: island A (0 Ma, at hotspot), island B (15 Ma, 1000 km), island C (43 Ma, 2500 km)
# Bend occurs at island B (direction change)
ISLAND_A_AGE_MA = 0.0
ISLAND_A_DIST_KM = 0.0

ISLAND_B_AGE_MA = 15.0
ISLAND_B_DIST_KM = 1000.0

ISLAND_C_AGE_MA = 43.0
ISLAND_C_DIST_KM = 2500.0

# Segment AB: 1000 km / 15 Ma = 66.667 km/Ma = 66.7 mm/yr (post-bend, WNW)
SEGMENT_AB_DIST_KM = ISLAND_B_DIST_KM - ISLAND_A_DIST_KM  # 1000 km
SEGMENT_AB_AGE_DIFF_MA = ISLAND_B_AGE_MA - ISLAND_A_AGE_MA  # 15 Ma
SEGMENT_AB_VELOCITY_MMYR = SEGMENT_AB_DIST_KM / SEGMENT_AB_AGE_DIFF_MA  # 66.667 mm/yr

# Segment BC: 1500 km / 28 Ma = 53.571 km/Ma = 53.6 mm/yr (pre-bend, NNW)
SEGMENT_BC_DIST_KM = ISLAND_C_DIST_KM - ISLAND_B_DIST_KM  # 1500 km
SEGMENT_BC_AGE_DIFF_MA = ISLAND_C_AGE_MA - ISLAND_B_AGE_MA  # 28 Ma
SEGMENT_BC_VELOCITY_MMYR = SEGMENT_BC_DIST_KM / SEGMENT_BC_AGE_DIFF_MA  # 53.571 mm/yr

# WRONG total average: 2500 km / 43 Ma = 58.14 mm/yr — meaningless across a direction change
WRONG_TOTAL_AVG_MMYR = ISLAND_C_DIST_KM / ISLAND_C_AGE_MA  # 58.14 mm/yr

# Velocities clearly differ across the bend (66.7 vs 53.6 mm/yr)
VELOCITY_DIFFER_THRESHOLD_MMYR = 5.0

PRIOR_ERRORS = {
    "total_average":       "Uses total distance/total time ignoring bends — averages across direction change",
    "constant_velocity":   "Assumes plate speed never changed — ignores bend evidence",
    "wrong_age_direction": "Ages increase away from hotspot, not toward — reverses age gradient",
}
