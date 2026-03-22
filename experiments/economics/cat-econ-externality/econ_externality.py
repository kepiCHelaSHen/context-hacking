"""Externalities — CHP Economics Sprint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from econ_externality_constants import A_MPC, B_MPC, B_MEC, A_MB, B_MB

def msc(mpc, mec):
    """Marginal social cost = marginal private cost + marginal external cost."""
    return mpc + mec

def market_equilibrium(a_mpc, b_mpc, a_mb, b_mb):
    """Market equilibrium: MPC = MB (ignores external cost).
    MPC = a_mpc + b_mpc*Q, MB = a_mb - b_mb*Q
    → Q = (a_mb - a_mpc) / (b_mpc + b_mb)
    """
    Q = (a_mb - a_mpc) / (b_mpc + b_mb)
    P = a_mb - b_mb * Q
    return (Q, P)

def social_optimum(a_mpc, b_mpc, b_mec, a_mb, b_mb):
    """Social optimum: MSC = MB (includes external cost).
    MSC = a_mpc + (b_mpc + b_mec)*Q, MB = a_mb - b_mb*Q
    → Q = (a_mb - a_mpc) / (b_mpc + b_mec + b_mb)
    """
    Q = (a_mb - a_mpc) / (b_mpc + b_mec + b_mb)
    P = a_mb - b_mb * Q
    return (Q, P)

def pigouvian_tax(b_mec, Q_soc):
    """Pigouvian tax = MEC evaluated at social optimum quantity."""
    return b_mec * Q_soc

def deadweight_loss(a_mpc, b_mpc, b_mec, a_mb, b_mb):
    """DWL from negative externality = 0.5 * (Q_mkt - Q_soc) * (MSC(Q_mkt) - MB(Q_mkt))."""
    Q_mkt, _ = market_equilibrium(a_mpc, b_mpc, a_mb, b_mb)
    Q_soc, _ = social_optimum(a_mpc, b_mpc, b_mec, a_mb, b_mb)
    msc_at_mkt = a_mpc + (b_mpc + b_mec) * Q_mkt
    mb_at_mkt = a_mb - b_mb * Q_mkt
    return 0.5 * (Q_mkt - Q_soc) * (msc_at_mkt - mb_at_mkt)

if __name__ == "__main__":
    Q_m, P_m = market_equilibrium(A_MPC, B_MPC, A_MB, B_MB)
    Q_s, P_s = social_optimum(A_MPC, B_MPC, B_MEC, A_MB, B_MB)
    tax = pigouvian_tax(B_MEC, Q_s)
    dwl = deadweight_loss(A_MPC, B_MPC, B_MEC, A_MB, B_MB)
    print(f"Market:   Q={Q_m:.2f}, P={P_m:.2f}")
    print(f"Social:   Q={Q_s:.2f}, P={P_s:.2f}")
    print(f"Tax:      {tax:.3f}")
    print(f"DWL:      {dwl:.3f}")
    print(f"Market OVERPRODUCES by {Q_m - Q_s:.2f} units")
