"""Cosmological Redshift — CHP Astronomy Sprint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from astro_redshift_constants import C_KMS


def redshift(lambda_obs, lambda_emit):
    """Compute redshift z from observed and emitted wavelengths."""
    return lambda_obs / lambda_emit - 1


def velocity_low_z(z, c=C_KMS):
    """Low-z recession velocity: v = cz (km/s). Only valid for z << 1."""
    return c * z


def velocity_sr_doppler(z):
    """Special-relativistic Doppler velocity as v/c ratio.
    v/c = ((1+z)^2 - 1) / ((1+z)^2 + 1)
    Always gives v < c for finite z.
    NOTE: cosmological redshift is not actually a Doppler shift —
    this formula applies to motion in flat spacetime only.
    """
    zp1_sq = (1 + z) ** 2
    return (zp1_sq - 1) / (zp1_sq + 1)


def is_low_z_valid(z, threshold=0.1):
    """Check whether the low-z approximation v=cz is valid."""
    return z < threshold


if __name__ == "__main__":
    # Lyman-alpha at z = 1
    z = redshift(243.134, 121.567)
    print(f"Redshift z = {z:.4f}")
    print(f"Low-z v = cz: {velocity_low_z(z):.0f} km/s  (= {velocity_low_z(z)/C_KMS:.2f}c — WRONG, equals c!)")
    print(f"SR Doppler v/c: {velocity_sr_doppler(z):.4f}  (= {velocity_sr_doppler(z)*C_KMS:.0f} km/s)")
    print(f"Low-z valid? {is_low_z_valid(z)}")
    print()
    for zv in [0.05, 0.1, 0.5, 1.0, 2.0, 3.0]:
        vsr = velocity_sr_doppler(zv)
        vcz = velocity_low_z(zv) / C_KMS
        print(f"z={zv:<5}  v_cz/c={vcz:.3f}  v_SR/c={vsr:.4f}  low_z_ok={is_low_z_valid(zv)}")
