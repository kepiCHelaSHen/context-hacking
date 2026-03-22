"""Plate Velocity from Hotspot Tracks — CHP Earth Science Sprint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from earth_continental_drift_constants import *


def segment_velocity(distance_km, age_diff_Ma):
    """Velocity for one segment: v = d / Δt.  Returns mm/yr (1 km/Ma = 1 mm/yr)."""
    if age_diff_Ma <= 0:
        raise ValueError("age_diff_Ma must be positive")
    return distance_km / age_diff_Ma


def total_average_velocity(total_dist_km, total_age_Ma):
    """WRONG approach: total distance / total time — ignores direction changes at bends."""
    if total_age_Ma <= 0:
        raise ValueError("total_age_Ma must be positive")
    return total_dist_km / total_age_Ma


def velocities_differ(v1, v2, threshold=5.0):
    """True if two segment velocities differ by more than threshold (mm/yr)."""
    return abs(v1 - v2) > threshold


def age_increases_away_from_hotspot():
    """Ages along a hotspot track increase with distance from the hotspot. Always True."""
    return True


if __name__ == "__main__":
    v_ab = segment_velocity(SEGMENT_AB_DIST_KM, SEGMENT_AB_AGE_DIFF_MA)
    v_bc = segment_velocity(SEGMENT_BC_DIST_KM, SEGMENT_BC_AGE_DIFF_MA)
    v_wrong = total_average_velocity(ISLAND_C_DIST_KM, ISLAND_C_AGE_MA)
    print(f"Segment AB (post-bend): {v_ab:.1f} mm/yr")
    print(f"Segment BC (pre-bend):  {v_bc:.1f} mm/yr")
    print(f"Wrong total average:    {v_wrong:.1f} mm/yr (WRONG — averages across direction change)")
    print(f"Velocities differ? {velocities_differ(v_ab, v_bc)} (threshold {VELOCITY_DIFFER_THRESHOLD_MMYR} mm/yr)")
    print(f"Ages increase away from hotspot? {age_increases_away_from_hotspot()}")
