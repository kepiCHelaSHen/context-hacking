"""PCR Amplification — CHP Biology Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from bio_pcr_amplification_constants import *


def pcr_yield(N0, efficiency, cycles):
    """Return PCR yield: N₀ * (1 + E)^c.

    Parameters
    ----------
    N0 : float  — initial template copy number (must be > 0)
    efficiency : float — amplification efficiency (0 < E ≤ 1)
    cycles : int — number of thermal cycles (must be ≥ 0)
    """
    if N0 <= 0:
        raise ValueError("Initial template count N0 must be positive")
    if not (0 < efficiency <= 1.0):
        raise ValueError("Efficiency must be in (0, 1]")
    if cycles < 0:
        raise ValueError("Cycle count must be non-negative")
    return N0 * (1 + efficiency) ** cycles


def ideal_yield(N0, cycles):
    """Return ideal PCR yield assuming 100% efficiency: N₀ * 2^c."""
    if N0 <= 0:
        raise ValueError("Initial template count N0 must be positive")
    if cycles < 0:
        raise ValueError("Cycle count must be non-negative")
    return N0 * 2 ** cycles


def fold_amplification(efficiency, cycles):
    """Return fold-amplification: (1 + E)^c."""
    if not (0 < efficiency <= 1.0):
        raise ValueError("Efficiency must be in (0, 1]")
    if cycles < 0:
        raise ValueError("Cycle count must be non-negative")
    return (1 + efficiency) ** cycles


def cycles_needed(target_fold, efficiency):
    """Return minimum integer cycles to reach target fold-amplification.

    Solves (1+E)^c ≥ target_fold  →  c = ceil(log(target_fold) / log(1+E)).
    """
    if target_fold <= 1:
        raise ValueError("Target fold must be > 1")
    if not (0 < efficiency <= 1.0):
        raise ValueError("Efficiency must be in (0, 1]")
    return math.ceil(math.log(target_fold) / math.log(1 + efficiency))


if __name__ == "__main__":
    print(f"PCR Amplification — E_typical={E_TYPICAL}, cycles={CYCLES}")
    print(f"  Ideal yield (E=1.0):   {ideal_yield(N0, CYCLES):,.0f}")
    print(f"  Real yield  (E={E_TYPICAL}): {pcr_yield(N0, E_TYPICAL, CYCLES):,.0f}")
    print(f"  Ratio (real/ideal):    {RATIO:.4f}")
    print(f"  Fold at E={E_TYPICAL}, c={CYCLES}: {fold_amplification(E_TYPICAL, CYCLES):,.0f}")
    print(f"  Cycles for 1M-fold (E={E_TYPICAL}): {cycles_needed(1e6, E_TYPICAL)}")
