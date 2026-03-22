"""USDA Soil Texture Triangle — CHP Earth Science Sprint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from earth_soil_classification_constants import *


def validate_composition(clay, silt, sand):
    """Return True iff clay + silt + sand is approximately 100."""
    return abs((clay + silt + sand) - COMPOSITION_SUM) <= TOLERANCE


def is_clay_dominated(clay):
    """Return True if clay >= 40% (clay texture class threshold)."""
    return clay >= CLAY_MIN_FOR_CLAY_CLASS


def is_sandy(sand, clay):
    """Return True if sand >= 85% and clay < 10% (sand texture class)."""
    return sand >= SAND_MIN_FOR_SAND_CLASS and clay < CLAY_MAX_FOR_SAND_CLASS


def classify_simple(clay, silt, sand):
    """Classify soil texture using simplified USDA texture triangle rules.

    Returns texture class name as a string.
    Raises ValueError if percentages do not sum to ~100.
    """
    if not validate_composition(clay, silt, sand):
        raise ValueError(
            f"Composition must sum to 100 (got {clay + silt + sand:.1f})"
        )

    # Clay class: clay >= 40%
    if is_clay_dominated(clay):
        return "clay"

    # Sand class: sand >= 85% and clay < 10%
    if is_sandy(sand, clay):
        return "sand"

    # Loamy sand: sand 70-90%, clay < 15%
    if (LOAMY_SAND_SAND_MIN <= sand <= LOAMY_SAND_SAND_MAX
            and clay < LOAMY_SAND_CLAY_MAX):
        return "loamy sand"

    # Silt loam: silt >= 50% and clay <= 27%
    if silt >= SILT_LOAM_SILT_MIN and clay <= SILT_LOAM_CLAY_MAX:
        return "silt loam"

    # Sandy loam: sand 43-85% and clay < 20%
    if (SANDY_LOAM_SAND_MIN <= sand <= SANDY_LOAM_SAND_MAX
            and clay < SANDY_LOAM_CLAY_MAX):
        return "sandy loam"

    # Loam: clay 7-27%, silt 28-50%, sand <= 52%
    if (LOAM_CLAY_MIN <= clay <= LOAM_CLAY_MAX
            and LOAM_SILT_MIN <= silt <= LOAM_SILT_MAX
            and sand <= LOAM_SAND_MAX):
        return "loam"

    # Fallback for other classes (silty clay, sandy clay, clay loam, etc.)
    if clay >= 27 and clay < 40:
        return "clay loam"

    return "other"


if __name__ == "__main__":
    for tv in [TEST_LOAM, TEST_CLAY, TEST_LOAMY_SAND, TEST_SAND]:
        result = classify_simple(tv["clay"], tv["silt"], tv["sand"])
        status = "PASS" if result == tv["expected"] else "FAIL"
        print(f"[{status}] {tv['clay']}c/{tv['silt']}si/{tv['sand']}sa "
              f"=> {result} (expected {tv['expected']})")
