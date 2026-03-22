"""Tidal Locking Timescale — CHP Astronomy Sprint. All constants from frozen spec."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from astro_tidal_locking_constants import (
    Q_EARTH, Q_MOON, Q_JUPITER, Q_JUPITER_HIGH, Q_MARS, Q_IO,
)

# === Body Q-factor lookup ===
_Q_TABLE = {
    "earth":        Q_EARTH,
    "moon":         Q_MOON,
    "jupiter":      Q_JUPITER,
    "jupiter_high": Q_JUPITER_HIGH,
    "mars":         Q_MARS,
    "io":           Q_IO,
}


def locking_timescale_ratio(a1, a2):
    """Ratio of tidal locking timescales for two orbital distances.
    t_lock ∝ a⁶, so ratio = (a1/a2)⁶.
    KEY: This is the SIXTH power — NOT third."""
    return (a1 / a2) ** 6


def is_tidally_locked(spin_period, orbital_period, tol=0.01):
    """Check if a body is tidally locked (1:1 spin-orbit resonance).
    Returns True if |spin_period/orbital_period - 1| < tol.
    NOTE: Mercury is NOT tidally locked (3:2 resonance)."""
    ratio = spin_period / orbital_period
    return abs(ratio - 1.0) < tol


def spin_orbit_resonance(spin, orbital):
    """Determine approximate spin-orbit resonance as a string ratio.
    spin   : spin (rotation) period in any consistent unit
    orbital: orbital period in the same unit
    Returns a string like '1:1', '3:2', etc."""
    ratio = orbital / spin  # how many spins per orbit
    # Check common resonances
    common = [
        (1.0, "1:1"),
        (1.5, "3:2"),
        (2.0, "2:1"),
        (2.5, "5:2"),
        (3.0, "3:1"),
        (0.5, "1:2"),
    ]
    for val, label in common:
        if abs(ratio - val) < 0.05:
            return label
    # Fall back to approximate ratio
    return f"{ratio:.2f}:1"


def q_factor(body):
    """Return tidal quality factor Q for a known body.
    body: string name (case-insensitive), e.g. 'Earth', 'Moon', 'Jupiter'.
    KEY: Q varies enormously — Earth Q≈12, Jupiter Q≈10⁵."""
    key = body.strip().lower()
    if key not in _Q_TABLE:
        raise ValueError(
            f"Unknown body '{body}'. Known: {', '.join(sorted(_Q_TABLE))}"
        )
    return _Q_TABLE[key]


if __name__ == "__main__":
    from astro_tidal_locking_constants import (
        A_MOON, A_MOON_HALF,
        T_SPIN_MOON, T_ORBIT_MOON,
        T_SPIN_MERCURY, T_ORBIT_MERCURY,
    )

    # Distance dependence: Moon at current vs half distance
    ratio = locking_timescale_ratio(A_MOON, A_MOON_HALF)
    print(f"Locking time ratio (current/half distance): {ratio:.1f}× (expect 64)")

    # Moon: tidally locked
    locked = is_tidally_locked(T_SPIN_MOON, T_ORBIT_MOON)
    print(f"Moon tidally locked: {locked} (expect True)")

    # Mercury: 3:2 resonance, NOT locked
    locked_merc = is_tidally_locked(T_SPIN_MERCURY, T_ORBIT_MERCURY)
    res = spin_orbit_resonance(T_SPIN_MERCURY, T_ORBIT_MERCURY)
    print(f"Mercury tidally locked: {locked_merc} (expect False)")
    print(f"Mercury resonance: {res} (expect 3:2)")

    # Q factors
    for body in ["Earth", "Moon", "Jupiter"]:
        print(f"Q({body}) = {q_factor(body)}")
