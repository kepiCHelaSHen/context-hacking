"""
Stoichiometry — CHP Chemistry Sprint
Formula parsing, molecular weight, moles/grams, limiting reagent.
All constants from frozen spec.
"""
import sys
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from chem_stoichiometry_constants import AW, AVOGADRO


def parse_formula(formula):
    """Parse chemical formula into element counts.
    Handles multi-letter elements, digits, and parentheses.
    'H2O' -> {'H': 2, 'O': 1}
    'Ca(OH)2' -> {'Ca': 1, 'O': 2, 'H': 2}
    'C6H12O6' -> {'C': 6, 'H': 12, 'O': 6}
    """
    def _parse(s, i):
        counts = {}
        while i < len(s):
            if s[i] == '(':
                inner, i = _parse(s, i + 1)
                # Get multiplier after ')'
                num_str = ''
                while i < len(s) and s[i].isdigit():
                    num_str += s[i]
                    i += 1
                multiplier = int(num_str) if num_str else 1
                for elem, cnt in inner.items():
                    counts[elem] = counts.get(elem, 0) + cnt * multiplier
            elif s[i] == ')':
                return counts, i + 1
            elif s[i].isupper():
                elem = s[i]
                i += 1
                while i < len(s) and s[i].islower():
                    elem += s[i]
                    i += 1
                num_str = ''
                while i < len(s) and s[i].isdigit():
                    num_str += s[i]
                    i += 1
                count = int(num_str) if num_str else 1
                counts[elem] = counts.get(elem, 0) + count
            else:
                i += 1
        return counts, i

    result, _ = _parse(formula, 0)
    return result


def molecular_weight(formula):
    """MW = sum(AW[element] * count). Uses IUPAC 2021 weights, NOT integers."""
    elements = parse_formula(formula)
    return sum(AW[elem] * count for elem, count in elements.items())


def moles(mass_g, formula):
    """moles = mass / MW."""
    return mass_g / molecular_weight(formula)


def grams(moles_val, formula):
    """grams = moles * MW."""
    return moles_val * molecular_weight(formula)


def limiting_reagent(reagents):
    """Find limiting reagent from dict {formula: {'grams': x, 'stoich': n}}.
    Returns (formula, moles_available/stoich) for the limiting reagent.
    """
    ratios = {}
    for formula, info in reagents.items():
        mol = moles(info["grams"], formula)
        ratios[formula] = mol / info["stoich"]
    limiting = min(ratios, key=ratios.get)
    return limiting, ratios[limiting]


def percent_yield(actual_g, theoretical_g):
    """Percent yield = 100 * actual / theoretical."""
    return 100.0 * actual_g / theoretical_g


if __name__ == "__main__":
    print("=== Stoichiometry ===\n")

    mw_h2o = molecular_weight("H2O")
    print(f"H2O:     MW = {mw_h2o:.3f} g/mol (NOT 18.000)")

    mw_glucose = molecular_weight("C6H12O6")
    print(f"Glucose: MW = {mw_glucose:.3f} g/mol")

    mw_aspirin = molecular_weight("C9H8O4")
    print(f"Aspirin: MW = {mw_aspirin:.3f} g/mol\n")

    # Limiting reagent: 2H2 + O2 -> 2H2O
    reagents = {
        "H2": {"grams": 4.0, "stoich": 2},
        "O2": {"grams": 16.0, "stoich": 1},
    }
    lim, ratio = limiting_reagent(reagents)
    print(f"Limiting reagent (2H2 + O2 -> 2H2O):")
    print(f"  4g H2 + 16g O2 -> limiting = {lim}")
