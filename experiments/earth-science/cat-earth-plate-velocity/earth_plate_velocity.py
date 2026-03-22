"""Plate Motion — Velocity from Hotspot Tracks — CHP Earth Science Sprint. All constants from frozen spec."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from earth_plate_velocity_constants import R_EARTH

def plate_velocity_mmyr(distance_km, age_Ma):
    """v = distance / time. Returns velocity in mm/yr (= km/Ma)."""
    if age_Ma <= 0:
        raise ValueError("Age must be positive")
    return distance_km / age_Ma

def plate_velocity_cmyr(distance_km, age_Ma):
    """v = distance / time. Returns velocity in cm/yr."""
    return plate_velocity_mmyr(distance_km, age_Ma) / 10.0

def great_circle_distance(lat1, lon1, lat2, lon2, R=R_EARTH):
    """Haversine formula. Inputs in degrees, returns distance in km."""
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def euler_velocity(omega_deg_Myr, R_earth, angular_dist_deg):
    """v = omega * R * sin(theta). Returns velocity in mm/yr (= km/Ma)."""
    omega_rad = math.radians(omega_deg_Myr)
    return omega_rad * R_earth * math.sin(math.radians(angular_dist_deg))

if __name__ == "__main__":
    from earth_plate_velocity_constants import (
        HAWAII_DIST_KM, HAWAII_AGE_MA, HAWAII_V_CMYR,
        LAT1_HON, LON1_HON, LAT2_MID, LON2_MID,
        OMEGA_PACIFIC_DEG_MYR, TEST_THETA_DEG
    )
    v = plate_velocity_cmyr(HAWAII_DIST_KM, HAWAII_AGE_MA)
    print(f"Hawaiian chain: {HAWAII_DIST_KM} km / {HAWAII_AGE_MA} Ma = {v:.2f} cm/yr")
    gc = great_circle_distance(LAT1_HON, LON1_HON, LAT2_MID, LON2_MID)
    print(f"Great circle Honolulu-Midway: {gc:.1f} km")
    ev = euler_velocity(OMEGA_PACIFIC_DEG_MYR, R_EARTH, TEST_THETA_DEG)
    print(f"Euler velocity at {TEST_THETA_DEG}° from pole: {ev:.1f} mm/yr = {ev/10:.1f} cm/yr")
