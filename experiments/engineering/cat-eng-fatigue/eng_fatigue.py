"""S-N Curve / Fatigue Life / Miner's Rule — CHP Engineering Sprint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from eng_fatigue_constants import *


def endurance_limit_steel(Su):
    """Endurance limit for steel: Se ≈ 0.5*Su when Su < 1400 MPa.

    Returns Se in the same units as Su (Pa).
    For Su >= 1400 MPa the approximation breaks down; clamp at 700 MPa.
    """
    if Su < SU_THRESHOLD:
        return 0.5 * Su
    return 0.5 * SU_THRESHOLD  # 700 MPa cap


def has_endurance_limit(material):
    """Return True if the material has a true endurance limit, False otherwise.

    Steel and titanium exhibit a distinct endurance limit (knee in S-N curve).
    Aluminum, copper, and magnesium do NOT — fatigue life is always finite!
    """
    mat = material.strip().lower()
    if mat in MATERIALS_WITH_ENDURANCE:
        return True
    if mat in MATERIALS_WITHOUT_ENDURANCE:
        return False
    raise ValueError(f"Unknown material: {material}")


def miner_damage(cycles_list, life_list):
    """Miner's rule cumulative damage: D = Σ(nᵢ / Nᵢ).

    Parameters
    ----------
    cycles_list : list of float  — actual cycles at each stress level (nᵢ)
    life_list   : list of float  — cycles to failure at each stress level (Nᵢ)

    Returns
    -------
    float — cumulative damage fraction (failure when D >= 1.0)
    """
    if len(cycles_list) != len(life_list):
        raise ValueError("cycles_list and life_list must have the same length")
    return sum(n / N for n, N in zip(cycles_list, life_list))


def remaining_life(damage, N_remaining):
    """Remaining cycles at a new stress level given accumulated damage.

    Parameters
    ----------
    damage      : float — cumulative damage so far (0 <= damage < 1)
    N_remaining : float — total cycles to failure at the new stress level

    Returns
    -------
    float — remaining allowable cycles: N_remaining * (1 - damage)
    """
    if not (0.0 <= damage < 1.0):
        raise ValueError(f"Damage must be in [0, 1), got {damage}")
    return N_remaining * (1.0 - damage)


if __name__ == "__main__":
    # Steel endurance limit
    Su = 800e6  # 800 MPa
    Se = endurance_limit_steel(Su)
    print(f"Steel Su = {Su/1e6:.0f} MPa -> Se = {Se/1e6:.0f} MPa  (Se ~ 0.5*Su)")

    # Aluminum check
    print(f"Aluminum has endurance limit? {has_endurance_limit('aluminum')}")
    print(f"Steel has endurance limit?    {has_endurance_limit('steel')}")

    # Miner's rule example
    # 50,000 cycles at S=500 MPa (N=100,000) then remaining at S=450 MPa (N=500,000)
    d1 = miner_damage([50_000], [100_000])
    print(f"\nDamage after 50k cycles at 500 MPa: {d1:.2f}")

    n2 = remaining_life(d1, 500_000)
    print(f"Remaining life at 450 MPa: {n2:.0f} cycles")

    d_total = miner_damage([50_000, n2], [100_000, 500_000])
    print(f"Total Miner damage at failure: {d_total:.2f}")
