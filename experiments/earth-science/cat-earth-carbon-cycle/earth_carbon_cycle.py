"""Carbon Cycle — Reservoir Sizes & Fluxes — CHP Earth Science Sprint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from earth_carbon_cycle_constants import (
    RESERVOIRS, RESERVOIR_OCEAN, RESERVOIR_ATMOSPHERE,
    AIRBORNE_FRACTION, GTC_PER_PPM, OCEAN_IS_NET_SINK,
)


def reservoir_size(name):
    """Return reservoir size in GtC for a named carbon reservoir.

    Args:
        name: one of 'atmosphere', 'ocean', 'land_biosphere',
              'fossil_fuels', 'sediments'

    Returns:
        Size in GtC.

    Raises:
        KeyError: if name is not a recognised reservoir.
    """
    key = name.lower().replace(" ", "_")
    if key not in RESERVOIRS:
        raise KeyError(f"Unknown reservoir '{name}'. Valid: {list(RESERVOIRS.keys())}")
    return RESERVOIRS[key]


def airborne_fraction_increase(emissions, af=AIRBORNE_FRACTION):
    """Compute annual atmospheric CO₂ increase from total emissions.

    Args:
        emissions: total annual emissions in GtC/yr
        af: airborne fraction (default 0.45)

    Returns:
        Atmospheric increase in GtC/yr.
    """
    return emissions * af


def gtc_to_ppm(gtc):
    """Convert gigatonnes carbon to atmospheric ppm CO₂.

    1 ppm ≈ 2.12 GtC.

    Args:
        gtc: mass in GtC

    Returns:
        Equivalent ppm.
    """
    return gtc / GTC_PER_PPM


def ppm_to_gtc(ppm):
    """Convert atmospheric ppm CO₂ to gigatonnes carbon.

    Args:
        ppm: concentration in ppm

    Returns:
        Equivalent GtC.
    """
    return ppm * GTC_PER_PPM


def ocean_is_net_sink():
    """Return True — the modern ocean is a net sink of atmospheric CO₂.

    The ocean absorbs approximately 2.5 GtC/yr more than it emits.

    Returns:
        True
    """
    return OCEAN_IS_NET_SINK


if __name__ == "__main__":
    print("=== Carbon Cycle — Reservoir Sizes & Fluxes ===")
    for name, gtc in RESERVOIRS.items():
        print(f"  {name:20s}: {gtc:>15,.0f} GtC")
    print()
    inc_gtc = airborne_fraction_increase(11.5)
    inc_ppm = gtc_to_ppm(inc_gtc)
    print(f"Total emissions: 11.5 GtC/yr")
    print(f"  Airborne fraction increase: {inc_gtc:.3f} GtC/yr")
    print(f"  ppm equivalent: {inc_ppm:.2f} ppm/yr  (observed ~2.5 ppm/yr)")
    print(f"Ocean is net sink: {ocean_is_net_sink()}")
    print(f"Ocean reservoir ({reservoir_size('ocean'):.0f} GtC) >> "
          f"Atmosphere ({reservoir_size('atmosphere'):.0f} GtC)")
