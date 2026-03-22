"""
Crystal Packing — Frozen Constants
Source: Ashcroft & Mermin Solid State Physics (1976), CRC Handbook 103rd Ed
Packing efficiencies are exact mathematical results.
DO NOT MODIFY.
"""
import math

PACKING = {
    "SC":      math.pi / 6,
    "BCC":     math.pi * math.sqrt(3) / 8,
    "FCC":     math.pi / (3*math.sqrt(2)),   # = 0.7405 — maximum possible
    "HCP":     math.pi / (3*math.sqrt(2)),
    "diamond": math.pi * math.sqrt(3) / 16,
}

ATOMS_PER_CELL = {"SC": 1, "BCC": 2, "FCC": 4, "diamond": 8}
# LLM prior for FCC: says 8 (counts corners only, forgets face atoms)

COORD_NUMBER = {"SC": 6, "BCC": 8, "FCC": 12, "diamond": 4}

RADIUS = {"Cu": 128, "Al": 143, "Fe": 126, "Na": 186}  # pm
STRUCTURE = {"Cu": "FCC", "Al": "FCC", "Fe": "BCC", "Na": "BCC"}

AVOGADRO = 6.02214076e23

PRIOR_ERRORS = {
    "fcc_8_atoms":   "Says FCC has 8 atoms — forgets face-center (4 atoms)",
    "formula_swap":  "Uses FCC formula for BCC or vice versa",
    "kepler_unknown":"Doesn't know FCC = maximum possible packing",
}
