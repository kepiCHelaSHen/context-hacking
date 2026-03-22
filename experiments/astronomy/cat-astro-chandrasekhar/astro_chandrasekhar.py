"""Chandrasekhar Limit — CHP Astronomy Sprint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from astro_chandrasekhar_constants import *


def chandrasekhar_mass(mu_e=2.0):
    """M_Ch = 5.83 / μ_e² in solar masses — returns M_sun units.

    For C/O white dwarf (μ_e=2): M_Ch ≈ 1.4575 ≈ 1.44 M_sun (NOT 1.4!).
    """
    return OMEGA_CH / mu_e ** 2


def chandrasekhar_mass_kg(mu_e=2.0):
    """M_Ch in kilograms — returns kg.

    For C/O white dwarf (μ_e=2): M_Ch ≈ 2.899e30 kg.
    """
    return chandrasekhar_mass(mu_e) * M_SUN


def wd_radius_relative(M_ratio):
    """White dwarf radius scaling: R ∝ M^(-1/3).

    More massive = SMALLER! (inverse cube root relation)
    M_ratio is mass in units of some reference mass (dimensionless).
    Returns relative radius (dimensionless).
    """
    if M_ratio <= 0:
        raise ValueError("Mass ratio must be positive")
    return M_ratio ** WD_RADIUS_EXPONENT


def is_above_limit(M_Msun, limit=1.44):
    """True if mass M (in solar masses) exceeds the Chandrasekhar limit.

    Above this limit: electron degeneracy pressure cannot support the star
    → collapse to neutron star or Type Ia supernova.
    """
    return M_Msun > limit


if __name__ == "__main__":
    m_ch = chandrasekhar_mass()
    m_ch_kg = chandrasekhar_mass_kg()
    print(f"Chandrasekhar limit (mu_e=2): {m_ch:.4f} M_sun = {m_ch_kg:.3e} kg")
    m_ch_fe = chandrasekhar_mass(mu_e=MU_E_FE)
    print(f"Chandrasekhar limit (Fe, mu_e={MU_E_FE}): {m_ch_fe:.4f} M_sun")
    print(f"WD radius scaling: 1.0 M -> R={wd_radius_relative(1.0):.4f}")
    print(f"WD radius scaling: 1.2 M -> R={wd_radius_relative(1.2):.4f} (SMALLER!)")
    print(f"Is 1.5 M_sun above limit? {is_above_limit(1.5)}")
    print(f"Is 1.0 M_sun above limit? {is_above_limit(1.0)}")
    print(f"WRONG (rounded): {M_CH_WRONG_ROUNDED} M_sun (loses 0.04 M_sun)")
