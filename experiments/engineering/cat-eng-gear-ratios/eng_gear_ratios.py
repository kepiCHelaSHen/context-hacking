"""Gear Train Analysis — CHP Engineering Sprint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from eng_gear_ratios_constants import *


def gear_ratio(N_driver, N_driven):
    """Gear ratio GR = N_driven / N_driver (NOT N_driver/N_driven!)."""
    return N_driven / N_driver


def output_speed(input_speed, N_driver, N_driven):
    """Output speed: omega_driven = omega_driver * (N_driver / N_driven)."""
    return input_speed * (N_driver / N_driven)


def output_torque(input_torque, GR):
    """Output torque: tau_driven = tau_driver * GR (torque INCREASES with speed reduction)."""
    return input_torque * GR


def rotation_reversed(n_meshes):
    """Each external mesh reverses direction. Odd meshes -> reversed, even -> same."""
    return n_meshes % 2 == 1


def compound_ratio(gear_pairs):
    """Compound gear train: total GR = product of individual (N_driven/N_driver) ratios.
    gear_pairs is a list of (N_driver, N_driven) tuples."""
    total = 1.0
    for N_driver, N_driven in gear_pairs:
        total *= N_driven / N_driver
    return total


if __name__ == "__main__":
    # Simple gear pair
    GR = gear_ratio(N1, N2)
    w_out = output_speed(OMEGA_IN, N1, N2)
    t_out = output_torque(TAU_IN_REF, GR)
    rev = rotation_reversed(N_MESHES_SIMPLE)
    print(f"Simple pair: N1={N1}, N2={N2}")
    print(f"  GR = {GR:.1f}  (NOT {GR_INVERTED:.4f})")
    print(f"  Speed: {OMEGA_IN:.0f} -> {w_out:.2f} RPM  (NOT {OMEGA_OUT_WRONG:.0f})")
    print(f"  Torque: {TAU_IN_REF:.1f} -> {t_out:.1f} N*m  (NOT {TAU_OUT_WRONG:.4f})")
    print(f"  Direction reversed: {rev}  (1 mesh = odd -> reversed)")

    # Compound gear train
    pairs = [(NC1_DRIVER, NC1_DRIVEN), (NC2_DRIVER, NC2_DRIVEN)]
    GR_c = compound_ratio(pairs)
    w_c = output_speed(OMEGA_IN, 1, GR_c)  # equivalent: input / total GR
    rev_c = rotation_reversed(N_MESHES_COMPOUND)
    print(f"\nCompound: {pairs}")
    print(f"  Total GR = {GR_c:.1f}")
    print(f"  Speed: {OMEGA_IN:.0f} -> {w_c:.2f} RPM")
    print(f"  Direction reversed: {rev_c}  (2 meshes = even -> same)")
