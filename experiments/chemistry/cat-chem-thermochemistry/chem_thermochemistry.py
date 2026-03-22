"""
Thermochemistry — CHP Chemistry Sprint
Hess's law, bond enthalpy calculations.
All constants from frozen spec.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from chem_thermochemistry_constants import DHF, BOND_ENTHALPY


def hess_law(products, reactants):
    """Hess's law: dH = sum(n*DHF[products]) - sum(n*DHF[reactants]).
    PRODUCTS minus REACTANTS — not reversed.
    products/reactants: list of (species, stoich_coeff) tuples.
    """
    prod_sum = sum(n * DHF[species] for species, n in products)
    react_sum = sum(n * DHF[species] for species, n in reactants)
    return prod_sum - react_sum


def bond_enthalpy_dH(bonds_broken, bonds_formed):
    """dH = sum(broken) - sum(formed).
    Breaking bonds is endothermic (positive), forming is exothermic.
    bonds_broken/formed: list of (bond_type, count) tuples.
    """
    broken_sum = sum(count * BOND_ENTHALPY[bond] for bond, count in bonds_broken)
    formed_sum = sum(count * BOND_ENTHALPY[bond] for bond, count in bonds_formed)
    return broken_sum - formed_sum


if __name__ == "__main__":
    print("=== Thermochemistry ===\n")

    # Water formation
    dH_water = hess_law(
        [("H2O(l)", 1)],
        [("H2(g)", 1), ("O2(g)", 0.5)]
    )
    print(f"Water formation: dH = {dH_water:.3f} kJ/mol")

    # Methane combustion
    dH_methane = hess_law(
        [("CO2(g)", 1), ("H2O(l)", 2)],
        [("CH4(g)", 1), ("O2(g)", 2)]
    )
    print(f"Methane combustion: dH = {dH_methane:.3f} kJ/mol\n")

    # Positive DHf species
    print(f"Species with POSITIVE dHf:")
    print(f"  C2H4(g): {DHF['C2H4(g)']:+.2f} kJ/mol (LLM often gives negative!)")
    print(f"  NO(g):   {DHF['NO(g)']:+.2f} kJ/mol (LLM often gives negative!)")
    print(f"  NO2(g):  {DHF['NO2(g)']:+.2f} kJ/mol\n")

    print(f"H2O(g) vs H2O(l):")
    print(f"  H2O(g): {DHF['H2O(g)']:.3f} kJ/mol")
    print(f"  H2O(l): {DHF['H2O(l)']:.3f} kJ/mol")
    print(f"  Difference: {DHF['H2O(g)']-DHF['H2O(l)']:.3f} kJ/mol")
