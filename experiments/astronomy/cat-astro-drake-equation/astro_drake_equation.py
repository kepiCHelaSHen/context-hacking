"""Drake Equation — CHP Astronomy Sprint. All constants from frozen spec."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from astro_drake_equation_constants import (
    R_STAR_DEFAULT, F_P_MODERN, N_E_DEFAULT,
    F_L_DEFAULT, F_I_DEFAULT, F_C_DEFAULT, L_DEFAULT,
    OPTIMISTIC_R_STAR, OPTIMISTIC_F_P, OPTIMISTIC_N_E,
    OPTIMISTIC_F_L, OPTIMISTIC_F_I, OPTIMISTIC_F_C, OPTIMISTIC_L,
    PESSIMISTIC_R_STAR, PESSIMISTIC_F_P, PESSIMISTIC_N_E,
    PESSIMISTIC_F_L, PESSIMISTIC_F_I, PESSIMISTIC_F_C, PESSIMISTIC_L,
)


def drake_equation(R_star=R_STAR_DEFAULT, f_p=F_P_MODERN, n_e=N_E_DEFAULT,
                   f_l=F_L_DEFAULT, f_i=F_I_DEFAULT, f_c=F_C_DEFAULT,
                   L=L_DEFAULT):
    """Compute N — estimated number of communicating civilizations in the Milky Way.

    N = R* x f_p x n_e x f_l x f_i x f_c x L

    Parameters
    ----------
    R_star : float  — star formation rate (stars/year), default ~2
    f_p    : float  — fraction of stars with planets, default ~1.0 (Kepler!)
    n_e    : float  — habitable planets per system, default ~0.2
    f_l    : float  — fraction developing life, default 0.5
    f_i    : float  — fraction developing intelligence, default 0.5
    f_c    : float  — fraction communicating, default 0.1
    L      : float  — years of detectable signals, default 10000

    KEY: f_p ~ 1.0 is now well-established. Do NOT use old values of 0.1-0.5.
    """
    return R_star * f_p * n_e * f_l * f_i * f_c * L


def modern_f_p():
    """Return the modern estimate of f_p from Kepler mission data.

    Returns ~1.0 — nearly all stars have planets.
    Old pre-Kepler estimates of 0.1-0.5 are WRONG."""
    return F_P_MODERN


def optimistic_estimate():
    """Return the optimistic Drake Equation parameter set and result.

    Uses: R*=2, f_p=1.0, n_e=0.2, f_l=1.0, f_i=0.5, f_c=0.1, L=10000
    Result: N = 200
    """
    params = {
        "R_star": OPTIMISTIC_R_STAR,
        "f_p": OPTIMISTIC_F_P,
        "n_e": OPTIMISTIC_N_E,
        "f_l": OPTIMISTIC_F_L,
        "f_i": OPTIMISTIC_F_I,
        "f_c": OPTIMISTIC_F_C,
        "L": OPTIMISTIC_L,
    }
    params["N"] = drake_equation(**{k: v for k, v in params.items() if k != "N"})
    return params


def pessimistic_estimate():
    """Return the pessimistic Drake Equation parameter set and result.

    Uses: R*=1.5, f_p=1.0, n_e=0.1, f_l=0.01, f_i=0.01, f_c=0.01, L=1000
    Result: N = 0.00015 (essentially zero — we may be alone)
    """
    params = {
        "R_star": PESSIMISTIC_R_STAR,
        "f_p": PESSIMISTIC_F_P,
        "n_e": PESSIMISTIC_N_E,
        "f_l": PESSIMISTIC_F_L,
        "f_i": PESSIMISTIC_F_I,
        "f_c": PESSIMISTIC_F_C,
        "L": PESSIMISTIC_L,
    }
    params["N"] = drake_equation(**{k: v for k, v in params.items() if k != "N"})
    return params


if __name__ == "__main__":
    from astro_drake_equation_constants import OPTIMISTIC_N, PESSIMISTIC_N

    # Default estimate
    N_default = drake_equation()
    print(f"Default N = {N_default:.2f}")

    # Modern f_p
    print(f"Modern f_p = {modern_f_p()} (Kepler: nearly all stars have planets)")

    # Optimistic
    opt = optimistic_estimate()
    print(f"Optimistic N = {opt['N']:.1f} (expect {OPTIMISTIC_N})")

    # Pessimistic
    pess = pessimistic_estimate()
    print(f"Pessimistic N = {pess['N']:.6f} (expect {PESSIMISTIC_N})")

    # Show the orders-of-magnitude range
    import math
    ratio = opt["N"] / pess["N"]
    print(f"Range: {math.log10(ratio):.1f} orders of magnitude between optimistic and pessimistic")
