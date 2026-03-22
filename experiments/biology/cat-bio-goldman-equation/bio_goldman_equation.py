"""Goldman-Hodgkin-Katz Equation — CHP Biology Sprint."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from bio_goldman_equation_constants import *


def ghk_numerator(P_K, K_o, P_Na, Na_o, P_Cl, Cl_i):
    """GHK numerator: cation [outside] + anion [inside].

    Cations (K⁺, Na⁺) use extracellular concentrations.
    Anions (Cl⁻) use INTRACELLULAR concentration — reversed vs cations!
    """
    return P_K * K_o + P_Na * Na_o + P_Cl * Cl_i


def ghk_denominator(P_K, K_i, P_Na, Na_i, P_Cl, Cl_o):
    """GHK denominator: cation [inside] + anion [outside].

    Cations (K⁺, Na⁺) use intracellular concentrations.
    Anions (Cl⁻) use EXTRACELLULAR concentration — reversed vs cations!
    """
    return P_K * K_i + P_Na * Na_i + P_Cl * Cl_o


def goldman_potential(P_K, K_o, K_i, P_Na, Na_o, Na_i, P_Cl, Cl_o, Cl_i, T=310.15):
    """Goldman-Hodgkin-Katz voltage equation → V_m in mV.

    V_m = (RT/F) * ln( (P_K[K]_o + P_Na[Na]_o + P_Cl[Cl]_i)
                      / (P_K[K]_i + P_Na[Na]_i + P_Cl[Cl]_o) )

    KEY: Anions (Cl⁻) appear reversed — [Cl]_i in numerator, [Cl]_o in denominator.
    This is because anions carry negative charge, so their electrochemical
    driving force is opposite to that of cations.
    """
    rt_f_mv = (R * T / F) * 1000.0
    num = ghk_numerator(P_K, K_o, P_Na, Na_o, P_Cl, Cl_i)
    den = ghk_denominator(P_K, K_i, P_Na, Na_i, P_Cl, Cl_o)
    return rt_f_mv * math.log(num / den)


if __name__ == "__main__":
    print(f"Goldman-Hodgkin-Katz Equation at T={T} K")
    print(f"  Permeabilities: P_K={P_K}, P_Na={P_NA}, P_Cl={P_CL}")
    print(f"  [K]_o={K_O}, [K]_i={K_I}, [Na]_o={NA_O}, [Na]_i={NA_I}, [Cl]_o={CL_O}, [Cl]_i={CL_I}")
    num = ghk_numerator(P_K, K_O, P_NA, NA_O, P_CL, CL_I)
    den = ghk_denominator(P_K, K_I, P_NA, NA_I, P_CL, CL_O)
    V_m = goldman_potential(P_K, K_O, K_I, P_NA, NA_O, NA_I, P_CL, CL_O, CL_I, T)
    print(f"  Numerator  = {num:.4f}")
    print(f"  Denominator = {den:.4f}")
    print(f"  V_m = {V_m:.4f} mV")
