"""
Crystal Packing — CHP Chemistry Sprint
Packing efficiency, atoms per cell, unit cell edge, density.
All constants from frozen spec.
"""
import sys
import math
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from chem_crystal_packing_constants import (
    PACKING, ATOMS_PER_CELL, COORD_NUMBER, RADIUS, STRUCTURE, AVOGADRO,
)


def packing_efficiency(structure):
    """Packing efficiency from frozen constants."""
    return PACKING[structure]


def atoms_per_cell(structure):
    """Atoms per unit cell: FCC=4 (NOT 8), BCC=2, SC=1."""
    return ATOMS_PER_CELL[structure]


def unit_cell_edge(element):
    """Unit cell edge length in pm.
    FCC: a = 2*sqrt(2)*r
    BCC: a = 4*r/sqrt(3)
    """
    r = RADIUS[element]
    struct = STRUCTURE[element]
    if struct == "FCC":
        return 2.0 * math.sqrt(2) * r
    elif struct == "BCC":
        return 4.0 * r / math.sqrt(3)
    else:
        raise ValueError(f"Unknown structure for {element}: {struct}")


def density(element, molar_mass):
    """Density in g/cm^3.
    d = (atoms_per_cell * molar_mass) / (AVOGADRO * a^3)
    a in cm (convert from pm: a_cm = a_pm * 1e-10)
    """
    struct = STRUCTURE[element]
    n_atoms = atoms_per_cell(struct)
    a_pm = unit_cell_edge(element)
    a_cm = a_pm * 1e-10  # pm to cm
    return (n_atoms * molar_mass) / (AVOGADRO * a_cm**3)


if __name__ == "__main__":
    print("=== Crystal Packing ===\n")

    print("Packing efficiencies:")
    for struct in ["SC", "BCC", "FCC", "HCP", "diamond"]:
        print(f"  {struct:8s}: {packing_efficiency(struct):.4f} ({packing_efficiency(struct)*100:.1f}%)")
    print(f"  FCC is the MAXIMUM possible (Kepler conjecture)\n")

    print("Atoms per unit cell:")
    for struct in ["SC", "BCC", "FCC", "diamond"]:
        print(f"  {struct:8s}: {atoms_per_cell(struct)}")
    print(f"  FCC = 4 (NOT 8 — LLM prior error)\n")

    rho_Cu = density("Cu", 63.546)
    print(f"Copper density: {rho_Cu:.2f} g/cm^3 (literature: 8.96)")
