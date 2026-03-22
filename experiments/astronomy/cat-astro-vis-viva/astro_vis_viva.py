"""Vis-Viva Equation — CHP Astronomy Sprint. All constants from frozen spec."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from astro_vis_viva_constants import MU_SUN, AU

def vis_viva(GM, r, a):
    """v = sqrt(GM * (2/r - 1/a)). Core orbital mechanics equation.
    GM: gravitational parameter (m^3/s^2)
    r:  current distance from central body (m)
    a:  semi-major axis of orbit (m); use float('inf') for escape trajectory
    """
    return math.sqrt(GM * (2 / r - 1 / a))

def circular_velocity(GM, r):
    """v_c = sqrt(GM/r). Special case of vis-viva where r=a."""
    return math.sqrt(GM / r)

def escape_velocity(GM, r):
    """v_esc = sqrt(2GM/r). Special case of vis-viva where a->inf (1/a->0).
    Note: v_esc = v_c * sqrt(2), NOT just GM/r.
    """
    return math.sqrt(2 * GM / r)

def is_bound(v, GM, r):
    """Returns True if orbit is bound (elliptical), False if escape (hyperbolic).
    Bound iff v < v_esc = sqrt(2GM/r).
    """
    v_esc = escape_velocity(GM, r)
    return v < v_esc

if __name__ == "__main__":
    vc = circular_velocity(MU_SUN, AU)
    ve = escape_velocity(MU_SUN, AU)
    print(f"Circular velocity at 1 AU: {vc:.0f} m/s ({vc/1000:.1f} km/s)")
    print(f"Escape velocity at 1 AU:   {ve:.0f} m/s ({ve/1000:.1f} km/s)")
    print(f"Ratio v_esc/v_circ: {ve/vc:.6f} (should be sqrt2={math.sqrt(2):.6f})")
    # Elliptical orbit: a=1.5 AU, at perihelion r=1 AU
    a_ell = 1.5 * AU
    vp = vis_viva(MU_SUN, AU, a_ell)
    print(f"Vis-viva at perihelion (a=1.5AU, r=1AU): {vp:.0f} m/s ({vp/1000:.1f} km/s)")
    print(f"Bound orbit? {is_bound(vp, MU_SUN, AU)}")
