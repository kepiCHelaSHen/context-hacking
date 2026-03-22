"""Entropy — CHP Physics Sprint. All constants from frozen spec."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from phys_entropy_constants import R, K_B

def entropy_isothermal_expansion(n, V1, V2):
    """ΔS = nR·ln(V2/V1) for isothermal ideal gas expansion."""
    return n * R * math.log(V2 / V1)

def entropy_ideal_gas(n, Cv, T1, T2, V1, V2):
    """ΔS = nCv·ln(T2/T1) + nR·ln(V2/V1)."""
    return n * Cv * math.log(T2 / T1) + n * R * math.log(V2 / V1)

def entropy_mixing_ideal(n_total, mole_fractions):
    """ΔS_mix = -nR·Σ(xi·ln(xi)). Always positive."""
    return -n_total * R * sum(x * math.log(x) for x in mole_fractions if x > 0)

def entropy_phase_transition(delta_H, T_K):
    """ΔS = ΔH/T. T must be in Kelvin."""
    return delta_H / T_K

def boltzmann_entropy(W):
    """S = k_B · ln(W)."""
    return K_B * math.log(W)

if __name__ == "__main__":
    ds = entropy_isothermal_expansion(1.0, 1.0, 2.0)
    print(f"Isothermal V doubles: dS = {ds:.3f} J/(mol·K)")
    ds_mix = entropy_mixing_ideal(1.0, [0.5, 0.5])
    print(f"50/50 mixing: dS = {ds_mix:.3f} J/(mol·K)")
    ds_ice = entropy_phase_transition(6010, 273.15)
    print(f"Ice melting: dS = {ds_ice:.2f} J/(mol·K)")
