"""Milankovitch Cycles (Orbital Parameter Periodicity) — CHP Earth Science Sprint. All constants from frozen spec."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from earth_milankovitch_constants import (
    ECCENTRICITY_PERIOD, ECCENTRICITY_PERIOD_LONG,
    OBLIQUITY_PERIOD, CURRENT_OBLIQUITY,
    CLIMATIC_PRECESSION_PERIOD, AXIAL_PRECESSION_PERIOD,
)


def eccentricity_period():
    """Dominant eccentricity cycle period in years. Returns ~100,000."""
    return ECCENTRICITY_PERIOD


def obliquity_period():
    """Obliquity (axial tilt) cycle period in years. Returns ~41,000."""
    return OBLIQUITY_PERIOD


def climatic_precession_period():
    """Climatic precession dominant period in years. Returns ~23,000 (NOT 26,000)."""
    return CLIMATIC_PRECESSION_PERIOD


def axial_precession_period():
    """Axial precession (gyroscopic wobble) period in years. Returns ~26,000."""
    return AXIAL_PRECESSION_PERIOD


def current_obliquity():
    """Current Earth obliquity in degrees. Returns 23.44°."""
    return CURRENT_OBLIQUITY


if __name__ == "__main__":
    print(f"Eccentricity period:          {eccentricity_period():>10,} yr")
    print(f"Obliquity period:             {obliquity_period():>10,} yr")
    print(f"Climatic precession period:   {climatic_precession_period():>10,} yr")
    print(f"Axial precession period:      {axial_precession_period():>10,} yr")
    print(f"Current obliquity:            {current_obliquity():>10.2f}°")
