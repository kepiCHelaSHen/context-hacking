"""
Reaction Kinetics — CHP Chemistry Sprint
Arrhenius equation, Ea recovery, integrated rate laws.
All constants from frozen spec.
"""
import sys
import math
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from chem_kinetics_constants import R, H2I2_Ea, H2I2_A, H2I2_k700


def arrhenius_k(A, Ea_J_per_mol, T_K):
    """Arrhenius rate constant: k = A * exp(-Ea/(RT)). Ea must be in J/mol."""
    if Ea_J_per_mol < 1000:
        raise ValueError("Ea looks like kJ — must be J/mol")
    return A * math.exp(-Ea_J_per_mol / (R * T_K))


def ea_from_two_temps(k1, T1, k2, T2):
    """Recover Ea from rate constants at two temperatures."""
    # Ea = -R * ln(k2/k1) / (1/T2 - 1/T1)
    return -R * math.log(k2 / k1) / (1.0 / T2 - 1.0 / T1)


def half_life_first_order(k):
    """First-order half-life: t½ = ln(2)/k."""
    return math.log(2) / k


def integrated_rate_law(C0, k, t, order):
    """Integrated rate law for order 0, 1, or 2."""
    if order == 0:
        return max(C0 - k * t, 0.0)
    elif order == 1:
        return C0 * math.exp(-k * t)
    elif order == 2:
        return C0 / (1.0 + C0 * k * t)
    else:
        raise ValueError(f"Unsupported order: {order}")


if __name__ == "__main__":
    print("=== Arrhenius Kinetics ===\n")

    k700 = arrhenius_k(H2I2_A, H2I2_Ea, 700)
    print(f"H2+I2 at 700K:")
    print(f"  k(calc)  = {k700:.4e} L mol-1 s-1")
    print(f"  k(pub)   = {H2I2_k700:.4e} L mol-1 s-1")
    print(f"  Ea = {H2I2_Ea:.0f} J/mol (NOT 165 kJ!)\n")

    k600 = arrhenius_k(H2I2_A, H2I2_Ea, 600)
    k800 = arrhenius_k(H2I2_A, H2I2_Ea, 800)
    Ea_recovered = ea_from_two_temps(k600, 600, k800, 800)
    print(f"Ea recovery from 600K & 800K: {Ea_recovered:.0f} J/mol\n")

    t_half = half_life_first_order(0.05)
    print(f"First-order half-life (k=0.05): {t_half:.2f} s")

    print(f"\nConcentration at t=10 (C0=1.0, k=0.1):")
    for order in [0, 1, 2]:
        C = integrated_rate_law(1.0, 0.1, 10, order)
        print(f"  Order {order}: C = {C:.4f}")
