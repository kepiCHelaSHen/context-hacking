"""One-Compartment Pharmacokinetics — CHP Biology Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from bio_pharmacokinetics_1c_constants import *


def concentration(C0, ke, t):
    """Return drug concentration at time t: C(t) = C₀ * e^(-ke*t)."""
    return C0 * math.exp(-ke * t)


def half_life(ke):
    """Return elimination half-life: t½ = ln(2)/ke."""
    return math.log(2) / ke


def volume_of_distribution(dose, C0):
    """Return volume of distribution: Vd = Dose / C₀."""
    return dose / C0


def clearance(ke, Vd):
    """Return clearance: CL = ke * Vd."""
    return ke * Vd


def time_to_fraction(ke, fraction):
    """Return time for concentration to fall to a given fraction of C₀: t = -ln(fraction)/ke."""
    return -math.log(fraction) / ke


if __name__ == "__main__":
    print(f"C0 = {C0} mg/L, ke = {KE} /hr, Dose = {DOSE} mg")
    t_half = half_life(KE)
    print(f"t1/2 = ln(2)/ke = {t_half:.4f} hr")
    print(f"WRONG t1/2 = 1/ke = {1/KE:.4f} hr")
    print(f"C(t1/2) = {concentration(C0, KE, t_half):.4f} mg/L  (should be {C0/2})")
    print(f"C(10) = {concentration(C0, KE, 10):.4f} mg/L  (NOT 50)")
    vd = volume_of_distribution(DOSE, C0)
    cl = clearance(KE, vd)
    print(f"Vd = {vd:.2f} L, CL = {cl:.2f} L/hr")
    print(f"Time to 25% of C0 = {time_to_fraction(KE, 0.25):.4f} hr  (2 half-lives)")
