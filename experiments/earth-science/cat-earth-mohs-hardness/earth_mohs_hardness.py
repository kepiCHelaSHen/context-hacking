"""Mohs Hardness Scale — CHP Earth Science Sprint. All constants from frozen spec."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from earth_mohs_hardness_constants import MOHS_SCALE, VICKERS_APPROX


def mohs_number(mineral):
    """Return the Mohs hardness (1-10) for a mineral name (case-insensitive).
    Raises KeyError if mineral not in the standard 10-mineral scale."""
    key = mineral.strip().lower()
    if key not in MOHS_SCALE:
        raise KeyError(f"Unknown mineral: {mineral!r}")
    return MOHS_SCALE[key]


def can_scratch(hardness_a, hardness_b):
    """Return True if mineral A (hardness_a) can scratch mineral B (hardness_b).
    A scratches B iff A's Mohs number is strictly greater than B's."""
    return hardness_a > hardness_b


def absolute_hardness_vickers(mohs):
    """Return approximate Vickers hardness for a Mohs number (1-10).
    Demonstrates that Mohs scale is ordinal, NOT linear in absolute hardness.
    Raises KeyError if mohs not in 1-10."""
    if mohs not in VICKERS_APPROX:
        raise KeyError(f"Mohs number must be 1-10, got {mohs!r}")
    return VICKERS_APPROX[mohs]


def is_linear():
    """Return False. The Mohs scale is ORDINAL (rank-order), not linear.
    Diamond (10) is NOT 10x harder than talc (1) — it is ~1500x harder in Vickers.
    The largest gap is between corundum (9) and diamond (10)."""
    return False


if __name__ == "__main__":
    print("=== Mohs Hardness Scale ===\n")
    print("Mineral          Mohs   Vickers (approx)")
    print("-" * 45)
    for mineral, mohs in sorted(MOHS_SCALE.items(), key=lambda x: x[1]):
        vickers = VICKERS_APPROX[mohs]
        print(f"{mineral:<16} {mohs:>4}   {vickers:>6}")

    print(f"\nCan quartz (7) scratch glass (5.5)? {can_scratch(7, 5.5)}")
    print(f"Can fingernail (2.5) scratch gypsum (2)? {can_scratch(2.5, 2)}")
    print(f"Is Mohs scale linear? {is_linear()}")
    print(f"\nVickers gap 9->10: {VICKERS_APPROX[10] - VICKERS_APPROX[9]}")
    print(f"Vickers gap 1->2:  {VICKERS_APPROX[2] - VICKERS_APPROX[1]}")
    print(f"Diamond/Talc Vickers ratio: {VICKERS_APPROX[10]/VICKERS_APPROX[1]:.0f}x (NOT 10x!)")
