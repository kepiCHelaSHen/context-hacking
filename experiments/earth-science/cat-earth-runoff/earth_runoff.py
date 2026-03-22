"""
Rational Method & SCS Curve Number — CHP Earth Science Sprint
Peak runoff estimation: Q = C*i*A (Rational), Q = (P-Ia)²/(P-Ia+S) (SCS).
C is dimensionless [0,1], NOT a flow rate. All constants from frozen spec.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from earth_runoff_constants import (
    SCS_NUMERATOR, SCS_SUBTRAHEND, SCS_IA_COEFF, SCS_DENOM_COEFF,
    C_PAVEMENT_MIN, C_PAVEMENT_MAX,
    C_GRASS_MIN, C_GRASS_MAX,
    C_FOREST_MIN, C_FOREST_MAX,
    C_ROOFTOP_MIN, C_ROOFTOP_MAX,
    C_GRAVEL_MIN, C_GRAVEL_MAX,
)


def rational_method(C, i_m_per_s, A_m2):
    """Peak runoff via the Rational Method: Q = C * i * A.

    Args:
        C:         runoff coefficient, dimensionless, must be in [0, 1]
        i_m_per_s: rainfall intensity in m/s
        A_m2:      catchment area in m²

    Returns:
        Q in m³/s
    """
    if not (0.0 <= C <= 1.0):
        raise ValueError(f"C must be in [0, 1], got {C}")
    if i_m_per_s < 0:
        raise ValueError(f"Rainfall intensity must be non-negative, got {i_m_per_s}")
    if A_m2 < 0:
        raise ValueError(f"Area must be non-negative, got {A_m2}")
    return C * i_m_per_s * A_m2


def scs_storage(CN):
    """SCS potential maximum retention: S = (25400 / CN) - 254.

    Args:
        CN: curve number, must be in (0, 100]

    Returns:
        S in mm
    """
    if not (0.0 < CN <= 100.0):
        raise ValueError(f"CN must be in (0, 100], got {CN}")
    return SCS_NUMERATOR / CN - SCS_SUBTRAHEND


def scs_runoff(P_mm, CN):
    """SCS curve number runoff depth.

    Q = (P - 0.2*S)² / (P + 0.8*S)  when P > 0.2*S, else 0.

    Args:
        P_mm: precipitation depth in mm (must be >= 0)
        CN:   curve number in (0, 100]

    Returns:
        Runoff depth Q in mm
    """
    if P_mm < 0:
        raise ValueError(f"Precipitation must be non-negative, got {P_mm}")
    S = scs_storage(CN)
    Ia = SCS_IA_COEFF * S
    if P_mm <= Ia:
        return 0.0
    return (P_mm - Ia) ** 2 / (P_mm + SCS_DENOM_COEFF * S)


def runoff_coefficient_range(surface_type):
    """Return (C_min, C_max) for a given surface type.

    Args:
        surface_type: one of 'pavement', 'grass', 'forest', 'rooftop', 'gravel'

    Returns:
        Tuple (C_min, C_max), both in [0, 1]
    """
    table = {
        "pavement": (C_PAVEMENT_MIN, C_PAVEMENT_MAX),
        "grass":    (C_GRASS_MIN,    C_GRASS_MAX),
        "forest":   (C_FOREST_MIN,   C_FOREST_MAX),
        "rooftop":  (C_ROOFTOP_MIN,  C_ROOFTOP_MAX),
        "gravel":   (C_GRAVEL_MIN,   C_GRAVEL_MAX),
    }
    key = surface_type.lower().strip()
    if key not in table:
        raise ValueError(f"Unknown surface type '{surface_type}'. "
                         f"Valid: {sorted(table.keys())}")
    return table[key]


if __name__ == "__main__":
    print("=== Rational Method & SCS Curve Number ===\n")

    # Rational method reference
    C, i, A = 0.5, 1.38889e-5, 10000.0
    Q = rational_method(C, i, A)
    print(f"Rational: C={C}, i={i:.5e} m/s, A={A:.0f} m²")
    print(f"  Q = {Q:.6f} m³/s = {Q*1000:.1f} L/s")
    print(f"  Expected: 0.069444 m³/s = 69.4 L/s\n")

    # SCS reference
    CN = 75.0
    S = scs_storage(CN)
    print(f"SCS: CN={CN}, S = {S:.3f} mm")
    print(f"  Expected S = 84.667 mm\n")

    P = 100.0
    Q_scs = scs_runoff(P, CN)
    print(f"SCS runoff: P={P} mm, CN={CN}")
    print(f"  Q = {Q_scs:.3f} mm")
    print(f"  Expected: ~41.1 mm\n")

    # Coefficient ranges
    for surf in ["pavement", "grass", "forest"]:
        lo, hi = runoff_coefficient_range(surf)
        print(f"  {surf:10s}: C = {lo:.2f} – {hi:.2f}")
