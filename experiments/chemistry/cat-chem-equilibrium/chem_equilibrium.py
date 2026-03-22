"""
Chemical Equilibrium — CHP Chemistry Sprint
Kp↔Kc conversion, van't Hoff equation, pH from Kw.
All constants from frozen spec.
"""
import sys
import math
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from chem_equilibrium_constants import (
    R_J, R_ATM, HABER_Kp_298, HABER_Kp_700, HABER_dH, HABER_delta_n,
    Kw_298, Kw_310, Kw_373,
)


def kp_to_kc(Kp, delta_n, T_K):
    """Convert Kp to Kc: Kc = Kp / (R_ATM * T)^delta_n."""
    return Kp / (R_ATM * T_K) ** delta_n


def kc_to_kp(Kc, delta_n, T_K):
    """Convert Kc to Kp: Kp = Kc * (R_ATM * T)^delta_n."""
    return Kc * (R_ATM * T_K) ** delta_n


def van_t_hoff(K1, T1_K, T2_K, dH_J):
    """Van't Hoff equation: K2 = K1 * exp(-(dH/R)*(1/T2 - 1/T1))."""
    exponent = -(dH_J / R_J) * (1.0 / T2_K - 1.0 / T1_K)
    return K1 * math.exp(exponent)


def pH_from_Kw(T_K):
    """Calculate pH of pure water at temperature T_K using interpolation of Kw."""
    # Known data points: (T, Kw)
    data = [(298.15, Kw_298), (310.0, Kw_310), (373.15, Kw_373)]
    # Log-linear interpolation in 1/T vs ln(Kw)
    inv_T = 1.0 / T_K
    # Find bracketing points
    inv_temps = [1.0 / t for t, _ in data]
    ln_kws = [math.log(kw) for _, kw in data]

    # Linear interpolation in 1/T vs ln(Kw) space
    if inv_T >= inv_temps[0]:
        # Below or at 298K — extrapolate from first two points
        slope = (ln_kws[1] - ln_kws[0]) / (inv_temps[1] - inv_temps[0])
        ln_kw = ln_kws[0] + slope * (inv_T - inv_temps[0])
    elif inv_T >= inv_temps[1]:
        # Between 298K and 310K
        slope = (ln_kws[1] - ln_kws[0]) / (inv_temps[1] - inv_temps[0])
        ln_kw = ln_kws[0] + slope * (inv_T - inv_temps[0])
    elif inv_T >= inv_temps[2]:
        # Between 310K and 373K
        slope = (ln_kws[2] - ln_kws[1]) / (inv_temps[2] - inv_temps[1])
        ln_kw = ln_kws[1] + slope * (inv_T - inv_temps[1])
    else:
        # Above 373K — extrapolate from last two points
        slope = (ln_kws[2] - ln_kws[1]) / (inv_temps[2] - inv_temps[1])
        ln_kw = ln_kws[1] + slope * (inv_T - inv_temps[1])

    kw = math.exp(ln_kw)
    # pH = -log10(sqrt(Kw)) = 0.5 * pKw
    pKw = -math.log10(kw)
    return pKw / 2.0


if __name__ == "__main__":
    print("=== Chemical Equilibrium ===\n")

    # Kp vs Kc for Haber-Bosch at 298K
    Kc_298 = kp_to_kc(HABER_Kp_298, HABER_delta_n, 298.15)
    print(f"Haber-Bosch at 298K:")
    print(f"  Kp = {HABER_Kp_298:.2e}")
    print(f"  Kc = {Kc_298:.2e}")
    print(f"  Ratio Kc/Kp = {Kc_298/HABER_Kp_298:.4f}")
    print(f"  (They DIFFER because delta_n = {HABER_delta_n})\n")

    # Van't Hoff: predict Kp at 700K
    Kp_700_pred = van_t_hoff(HABER_Kp_298, 298.15, 700, HABER_dH)
    print(f"Haber-Bosch Kp at 700K:")
    print(f"  Van't Hoff prediction: {Kp_700_pred:.2e}")
    print(f"  Frozen value:          {HABER_Kp_700:.2e}")
    print(f"  (Exothermic: K decreases with T)\n")

    # pH of water at different temperatures
    print(f"pH of pure water:")
    print(f"  25°C (298K): {pH_from_Kw(298.15):.2f}  (NOT always 7.00)")
    print(f"  37°C (310K): {pH_from_Kw(310):.2f}  (body temperature)")
    print(f"  100°C (373K): {pH_from_Kw(373.15):.2f}  (boiling point)")
