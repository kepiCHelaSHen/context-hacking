"""Island Biogeography — Species-Area Relationship — CHP Biology Sprint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from bio_island_biogeography_constants import *


def species_area(c, A, z):
    """Number of species on an island/area using the species-area relationship.

    S = c * A^z

    Parameters
    ----------
    c : float  — taxon/region-specific constant
    A : float  — area in km^2 (must be > 0)
    z : float  — species-area exponent (~0.30 for oceanic islands, ~0.15 for mainland)

    Returns
    -------
    float — predicted number of species S
    """
    if A <= 0:
        raise ValueError(f"Area must be positive, got {A}")
    return c * A ** z


def doubling_ratio(z):
    """Species ratio when island area doubles.

    When area doubles: S_new / S_old = 2^z
    For z=0.30 (islands): 2^0.30 ≈ 1.23 → ~23% more species, NOT double.
    For z=0.15 (mainland): 2^0.15 ≈ 1.11 → ~11% more species.

    Parameters
    ----------
    z : float — species-area exponent

    Returns
    -------
    float — multiplicative factor for species count when area doubles
    """
    return 2 ** z


def z_island():
    """Canonical species-area exponent for oceanic islands.

    Returns z ≈ 0.30 (range 0.25-0.35).
    NOT 0.5 or 1.0 — those are common errors.
    """
    return 0.30


def z_mainland():
    """Canonical species-area exponent for mainland/continental areas.

    Returns z ≈ 0.15 (range 0.12-0.17).
    Lower than islands because mainland areas have more immigration corridors.
    """
    return 0.15


if __name__ == "__main__":
    print("=== Island Biogeography: Species-Area Relationship ===")
    print(f"z (island)   = {z_island()}")
    print(f"z (mainland) = {z_mainland()}")
    print()
    print(f"S(c={C_TEST}, A={A_TEST}, z={Z_ISLAND}) = {species_area(C_TEST, A_TEST, Z_ISLAND):.4f}")
    print(f"S(c={C_TEST}, A=200,  z={Z_ISLAND}) = {species_area(C_TEST, 200, Z_ISLAND):.4f}")
    print(f"S(c={C_TEST}, A=1000, z={Z_ISLAND}) = {species_area(C_TEST, 1000, Z_ISLAND):.4f}")
    print()
    dr = doubling_ratio(Z_ISLAND)
    print(f"Doubling ratio (island, z={Z_ISLAND}): {dr:.6f} → {(dr-1)*100:.2f}% increase")
    dr_m = doubling_ratio(Z_MAINLAND)
    print(f"Doubling ratio (mainland, z={Z_MAINLAND}): {dr_m:.6f} → {(dr_m-1)*100:.2f}% increase")
