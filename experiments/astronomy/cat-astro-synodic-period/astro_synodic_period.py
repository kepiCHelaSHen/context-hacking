"""Synodic Period — CHP Astronomy Sprint. All constants from frozen spec."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from astro_synodic_period_constants import P_EARTH


def synodic_superior(P_earth, P_planet):
    """Synodic period for a SUPERIOR planet (farther than Earth).
    Formula: 1/S = 1/P_earth - 1/P_planet
    Requires P_planet > P_earth; raises ValueError otherwise."""
    if P_earth <= 0 or P_planet <= 0:
        raise ValueError("Periods must be positive")
    if P_planet <= P_earth:
        raise ValueError(
            f"Superior planet must have P_planet > P_earth, "
            f"got P_planet={P_planet}, P_earth={P_earth}"
        )
    return 1.0 / (1.0 / P_earth - 1.0 / P_planet)


def synodic_inferior(P_earth, P_planet):
    """Synodic period for an INFERIOR planet (closer than Earth).
    Formula: 1/S = 1/P_planet - 1/P_earth
    Requires P_planet < P_earth; raises ValueError otherwise."""
    if P_earth <= 0 or P_planet <= 0:
        raise ValueError("Periods must be positive")
    if P_planet >= P_earth:
        raise ValueError(
            f"Inferior planet must have P_planet < P_earth, "
            f"got P_planet={P_planet}, P_earth={P_earth}"
        )
    return 1.0 / (1.0 / P_planet - 1.0 / P_earth)


def is_superior(P_planet, P_earth):
    """Return True if planet is superior (farther than Earth), i.e. P_planet > P_earth."""
    return P_planet > P_earth


def synodic_auto(P_earth, P_planet):
    """Compute synodic period, automatically selecting the correct formula.
    Superior (P_planet > P_earth): 1/S = 1/P_earth - 1/P_planet
    Inferior (P_planet < P_earth): 1/S = 1/P_planet - 1/P_earth
    KEY: These are DIFFERENT formulas — using the wrong one gives negative S."""
    if P_earth <= 0 or P_planet <= 0:
        raise ValueError("Periods must be positive")
    if P_planet == P_earth:
        raise ValueError("Planet cannot have same period as Earth (S would be infinite)")
    if is_superior(P_planet, P_earth):
        return synodic_superior(P_earth, P_planet)
    else:
        return synodic_inferior(P_earth, P_planet)


if __name__ == "__main__":
    from astro_synodic_period_constants import (
        P_MARS, P_VENUS, P_MERCURY, P_JUPITER, P_SATURN,
        S_MARS, S_VENUS, S_MERCURY, S_JUPITER, S_SATURN,
    )
    planets = [
        ("Mars",    P_MARS,    S_MARS,    True),
        ("Jupiter", P_JUPITER, S_JUPITER, True),
        ("Saturn",  P_SATURN,  S_SATURN,  True),
        ("Venus",   P_VENUS,   S_VENUS,   False),
        ("Mercury", P_MERCURY, S_MERCURY, False),
    ]
    for name, P, S_expected, sup in planets:
        S = synodic_auto(P_EARTH, P)
        tag = "superior" if sup else "inferior"
        print(f"{name:8s} ({tag:8s}): P={P:9.2f} d  S={S:8.2f} d = {S/365.25:.4f} yr  "
              f"(expected {S_expected:.2f} d)")
