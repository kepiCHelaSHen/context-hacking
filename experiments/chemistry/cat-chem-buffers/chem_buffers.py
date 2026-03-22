"""
Buffer Chemistry — CHP Chemistry Sprint
Henderson-Hasselbalch, buffer capacity, titration curves, blood pH.
All constants from frozen spec.
"""
import sys
import math
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from chem_buffers_constants import (
    ACETIC_pKa, CARBONIC_pKa1, BUFFER_LN10,
)


def henderson_hasselbalch(pKa, conc_acid, conc_base):
    """pH = pKa + log10([A-]/[HA]). NOT inverted."""
    return pKa + math.log10(conc_base / conc_acid)


def buffer_capacity(C_total, pKa, pH):
    """Buffer capacity: beta = C * ln(10) * Ka*[H+] / (Ka + [H+])^2."""
    Ka = 10.0 ** (-pKa)
    H = 10.0 ** (-pH)
    return C_total * BUFFER_LN10 * Ka * H / (Ka + H) ** 2


def titration_curve(C_acid, V_acid, C_base, V_base_range, pKa):
    """Calculate pH at each volume of base added during titration."""
    Ka = 10.0 ** (-pKa)
    results = []
    for V_base in V_base_range:
        mol_acid = C_acid * V_acid / 1000.0
        mol_base = C_base * V_base / 1000.0
        V_total = (V_acid + V_base) / 1000.0

        if mol_base >= mol_acid:
            # Past equivalence: excess OH-
            excess_base = mol_base - mol_acid
            OH = excess_base / V_total
            if OH > 0:
                pOH = -math.log10(OH)
                pH = 14.0 - pOH
            else:
                pH = 7.0
        elif mol_base <= 0:
            # Pure weak acid
            C_acid_eff = mol_acid / V_total
            H = (-Ka + math.sqrt(Ka**2 + 4*Ka*C_acid_eff)) / 2.0
            pH = -math.log10(H)
        else:
            # Buffer region
            acid_remaining = mol_acid - mol_base
            base_formed = mol_base
            pH = pKa + math.log10(base_formed / acid_remaining)

        results.append(pH)
    return results


def blood_pH(pCO2_mmHg, HCO3_mM):
    """Blood pH via Henderson-Hasselbalch for bicarbonate buffer.
    Clinical standard: pKa' = 6.1 at 37°C, alpha = 0.03 mM/mmHg.
    (CARBONIC_pKa1 = 6.352 is the thermodynamic value for CO2+H2O;
     the clinical apparent pKa at body temperature is 6.1.)
    NOT using pKa = 3.6 (true H2CO3).
    Normal: pCO2=40, HCO3=24 -> pH ~7.40
    """
    pKa_clinical = 6.1    # clinical apparent pKa at 37°C
    alpha = 0.03           # CO2 solubility mM/mmHg at 37°C
    CO2_conc = alpha * pCO2_mmHg  # mM
    return pKa_clinical + math.log10(HCO3_mM / CO2_conc)


if __name__ == "__main__":
    print("=== Buffer Chemistry ===\n")

    pH_equal = henderson_hasselbalch(ACETIC_pKa, 0.1, 0.1)
    print(f"Acetic acid buffer (equal conc): pH = {pH_equal:.3f} (should = pKa = {ACETIC_pKa})")

    pH_blood = blood_pH(40, 24)
    print(f"Blood pH (pCO2=40, HCO3=24): {pH_blood:.2f} (normal ~7.40)")
    print(f"  Using apparent pKa = {CARBONIC_pKa1} (NOT 3.6)")

    beta = buffer_capacity(0.1, ACETIC_pKa, ACETIC_pKa)
    print(f"\nBuffer capacity at pH=pKa: {beta:.4f} (includes ln10={BUFFER_LN10})")
