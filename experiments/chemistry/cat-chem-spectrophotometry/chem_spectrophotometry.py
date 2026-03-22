"""
Beer-Lambert Spectrophotometry — CHP Chemistry Sprint
Absorbance, transmittance, concentration, DNA quantification.
All constants from frozen spec.
"""
import sys
import math
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from chem_spectrophotometry_constants import EPSILON, DNA_A260_FACTORS


def absorbance_from_T(T_fractional):
    """A = -log10(T). Uses log10 NOT ln. T is fractional (0-1)."""
    return -math.log10(T_fractional)


def T_from_absorbance(A):
    """T = 10^(-A)."""
    return 10.0 ** (-A)


def concentration(A, epsilon, path_cm):
    """c = A / (epsilon * l). Path length MUST be included."""
    return A / (epsilon * path_cm)


def absorbance(c, epsilon, path_cm):
    """A = epsilon * c * l. Beer-Lambert law."""
    return epsilon * c * path_cm


def dna_conc(A260, molecule_type="dsDNA"):
    """DNA/RNA concentration: conc = A260 * factor. dsDNA=50, NOT 40 (that's RNA)."""
    return A260 * DNA_A260_FACTORS[molecule_type]


def percent_T_to_A(percent_T):
    """A = 2 - log10(%T)."""
    return 2.0 - math.log10(percent_T)


if __name__ == "__main__":
    print("=== Beer-Lambert Spectrophotometry ===\n")

    A = absorbance_from_T(0.01)
    print(f"Absorbance at T=0.01: A = {A:.3f} (should be 2.000)")
    print(f"  Uses log10, NOT ln (ln would give {-math.log(0.01):.3f})\n")

    A_1cm = absorbance(0.001, EPSILON["KMnO4_525"], 1.0)
    A_2cm = absorbance(0.001, EPSILON["KMnO4_525"], 2.0)
    print(f"KMnO4 at 0.001 M:")
    print(f"  A(1cm) = {A_1cm:.3f}")
    print(f"  A(2cm) = {A_2cm:.3f} (doubles with path length)\n")

    conc_ds = dna_conc(1.0, "dsDNA")
    conc_rna = dna_conc(1.0, "RNA")
    print(f"DNA at A260=1.0:")
    print(f"  dsDNA: {conc_ds:.0f} ug/mL (NOT {conc_rna:.0f})")
    print(f"  RNA:   {conc_rna:.0f} ug/mL")
