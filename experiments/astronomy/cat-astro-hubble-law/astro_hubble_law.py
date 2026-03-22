"""Hubble's Law — CHP Astronomy Sprint. All constants from frozen spec."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from astro_hubble_law_constants import H0_DEFAULT, MPC_TO_M, MPC_TO_LY, GYR_TO_S


def hubble_distance(v_km_s, H0=H0_DEFAULT):
    """Distance from recession velocity via Hubble's law: d = v / H₀.
    v_km_s : recession velocity in km/s
    H0     : Hubble constant in km/s/Mpc (default 70)
    Returns distance in Mpc.
    KEY: H₀ ≈ 70 km/s/Mpc (modern). NOT 50 or 100."""
    return v_km_s / H0


def hubble_velocity(d_Mpc, H0=H0_DEFAULT):
    """Recession velocity from distance: v = H₀ · d.
    d_Mpc : distance in Mpc
    H0    : Hubble constant in km/s/Mpc (default 70)
    Returns velocity in km/s."""
    return H0 * d_Mpc


def hubble_time_gyr(H0=H0_DEFAULT):
    """Hubble time t_H = 1/H₀, converted to Gyr.
    H0 : Hubble constant in km/s/Mpc (default 70)
    Returns t_H in Gyr.
    Conversion: H₀ [km/s/Mpc] → [s⁻¹] = H₀ × 1e3 / MPC_TO_M, then t_H = 1/H₀_SI."""
    H0_si = H0 * 1e3 / MPC_TO_M   # convert to s⁻¹
    return 1.0 / H0_si / GYR_TO_S  # convert s → Gyr


def mpc_to_ly(mpc):
    """Convert Megaparsecs to light-years.
    1 Mpc ≈ 3.262 × 10⁶ light-years."""
    return mpc * MPC_TO_LY


if __name__ == "__main__":
    from astro_hubble_law_constants import (
        V_TEST, D_TEST_MPC, D_TEST_LY,
        V_TEST2, D_TEST2_MPC,
        HUBBLE_TIME_GYR, H0_PLANCK, H0_SHOES,
    )
    # Basic distance calculation
    d = hubble_distance(V_TEST)
    print(f"v = {V_TEST} km/s -> d = {d:.1f} Mpc (expect {D_TEST_MPC})")
    print(f"  = {mpc_to_ly(d):.3e} light-years")

    # Round-trip check
    v_back = hubble_velocity(d)
    print(f"Round-trip: d = {d} Mpc -> v = {v_back:.1f} km/s (expect {V_TEST})")

    # Second test vector
    d2 = hubble_distance(V_TEST2)
    print(f"v = {V_TEST2} km/s -> d = {d2:.1f} Mpc (expect {D_TEST2_MPC})")

    # Hubble time
    t = hubble_time_gyr()
    print(f"Hubble time (H0=70): {t:.2f} Gyr (expect ~{HUBBLE_TIME_GYR:.2f})")
    t_planck = hubble_time_gyr(H0_PLANCK)
    t_shoes = hubble_time_gyr(H0_SHOES)
    print(f"Hubble time (Planck 67.4): {t_planck:.2f} Gyr")
    print(f"Hubble time (SH0ES 73.04): {t_shoes:.2f} Gyr")
    print(f"Hubble tension: {t_planck - t_shoes:.2f} Gyr difference in t_H")
