"""Isoelectric Point (pI) — CHP Biology Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from bio_protein_pI_constants import *


def pI_simple(pKa1, pKa2):
    """Return pI for a simple amino acid (no ionizable side chain).

    pI = (pKa1 + pKa2) / 2
    where pKa1 = α-COOH, pKa2 = α-NH₃⁺.
    """
    return (pKa1 + pKa2) / 2


def pI_acidic(pKa1, pKaR):
    """Return pI for an acidic amino acid (Asp, Glu).

    pI = (pKa1 + pKaR) / 2
    Uses the TWO LOWEST pKa values that flank the zwitterion.
    pKa1 = α-COOH, pKaR = side-chain COOH.
    """
    return (pKa1 + pKaR) / 2


def pI_basic(pKa2, pKaR):
    """Return pI for a basic amino acid (Lys, Arg, His).

    pI = (pKa2 + pKaR) / 2
    Uses the TWO HIGHEST pKa values that flank the zwitterion.
    pKa2 = α-NH₃⁺, pKaR = side-chain NH₃⁺ or guanidinium.
    """
    return (pKa2 + pKaR) / 2


def classify_amino_acid(pKaR, pKa1, pKa2):
    """Classify amino acid as 'acidic', 'basic', or 'neutral' based on side-chain pKaR.

    Parameters
    ----------
    pKaR : float or None
        Side-chain pKa. None means no ionizable side chain (neutral).
    pKa1 : float
        α-COOH pKa.
    pKa2 : float
        α-NH₃⁺ pKa.

    Returns
    -------
    str : 'acidic', 'basic', or 'neutral'
    """
    if pKaR is None:
        return "neutral"
    if pKaR < pKa2:
        # Side-chain pKa sits below α-NH₃⁺ → acidic side chain (e.g. Asp, Glu)
        return "acidic"
    else:
        # Side-chain pKa sits above α-NH₃⁺ → basic side chain (e.g. Lys, Arg)
        return "basic"


if __name__ == "__main__":
    print(f"Glycine:    pKa1={GLY_PKA1}, pKa2={GLY_PKA2} -> pI = {pI_simple(GLY_PKA1, GLY_PKA2):.3f}")
    print(f"Aspartate:  pKa1={ASP_PKA1}, pKaR={ASP_PKAR}, pKa2={ASP_PKA2} -> pI = {pI_acidic(ASP_PKA1, ASP_PKAR):.3f}")
    print(f"Lysine:     pKa1={LYS_PKA1}, pKa2={LYS_PKA2}, pKaR={LYS_PKAR} -> pI = {pI_basic(LYS_PKA2, LYS_PKAR):.3f}")
    print(f"Asp class:  {classify_amino_acid(ASP_PKAR, ASP_PKA1, ASP_PKA2)}")
    print(f"Lys class:  {classify_amino_acid(LYS_PKAR, LYS_PKA1, LYS_PKA2)}")
    print(f"Gly class:  {classify_amino_acid(None, GLY_PKA1, GLY_PKA2)}")
