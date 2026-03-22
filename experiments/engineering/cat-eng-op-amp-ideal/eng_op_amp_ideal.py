"""Ideal Op-Amp — CHP Engineering Sprint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from eng_op_amp_ideal_constants import *


def inverting_gain(Rf, Rin):
    """Inverting amplifier gain: Av = -Rf/Rin (NEGATIVE)."""
    return -(Rf / Rin)


def noninverting_gain(Rf, Rin):
    """Non-inverting amplifier gain: Av = 1 + Rf/Rin (always >= 1)."""
    return 1 + (Rf / Rin)


def inverting_output(Vin, Rf, Rin):
    """Inverting amplifier output voltage."""
    return inverting_gain(Rf, Rin) * Vin


def noninverting_output(Vin, Rf, Rin):
    """Non-inverting amplifier output voltage."""
    return noninverting_gain(Rf, Rin) * Vin


def difference_output(V1, V2, Rf, Rin):
    """Difference amplifier (equal-resistor config): Vout = (Rf/Rin)*(V2 - V1)."""
    return (Rf / Rin) * (V2 - V1)


if __name__ == "__main__":
    print(f"Rf={RF}, Rin={RIN}, Vin={VIN}")
    print(f"Inverting:     gain={inverting_gain(RF, RIN):.1f}, Vout={inverting_output(VIN, RF, RIN):.1f} V")
    print(f"Non-inverting: gain={noninverting_gain(RF, RIN):.1f}, Vout={noninverting_output(VIN, RF, RIN):.1f} V")
    print(f"Difference:    V1={V1_DIFF}, V2={V2_DIFF}, Vout={difference_output(V1_DIFF, V2_DIFF, RF, RIN):.1f} V")
