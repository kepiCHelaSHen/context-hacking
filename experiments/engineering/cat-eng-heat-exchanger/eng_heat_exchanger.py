"""LMTD Method — Heat Exchanger Design — CHP Engineering Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from eng_heat_exchanger_constants import TH_IN, TH_OUT, TC_IN, TC_OUT, U_TEST, A_TEST

def lmtd(dT1, dT2):
    """Log-Mean Temperature Difference: (ΔT₁ - ΔT₂) / ln(ΔT₁ / ΔT₂)."""
    if abs(dT1 - dT2) < 1e-12:
        return dT1  # degenerate case: both equal
    return (dT1 - dT2) / math.log(dT1 / dT2)

def counter_flow_deltas(Th_in, Th_out, Tc_in, Tc_out):
    """Counter-flow ΔT endpoints are CROSSED: hot-in↔cold-out, hot-out↔cold-in."""
    dT1 = Th_in - Tc_out
    dT2 = Th_out - Tc_in
    return dT1, dT2

def parallel_flow_deltas(Th_in, Th_out, Tc_in, Tc_out):
    """Parallel-flow ΔT endpoints are SAME-SIDE: hot-in↔cold-in, hot-out↔cold-out."""
    dT1 = Th_in - Tc_in
    dT2 = Th_out - Tc_out
    return dT1, dT2

def heat_transfer(U, A, lmtd_val):
    """Q = U * A * LMTD."""
    return U * A * lmtd_val

if __name__ == "__main__":
    dT1_c, dT2_c = counter_flow_deltas(TH_IN, TH_OUT, TC_IN, TC_OUT)
    lmtd_c = lmtd(dT1_c, dT2_c)
    Q_c = heat_transfer(U_TEST, A_TEST, lmtd_c)
    print(f"Counter-flow:  dT1={dT1_c:.0f}C, dT2={dT2_c:.0f}C, LMTD={lmtd_c:.2f}C, Q={Q_c:.1f} W")

    dT1_p, dT2_p = parallel_flow_deltas(TH_IN, TH_OUT, TC_IN, TC_OUT)
    lmtd_p = lmtd(dT1_p, dT2_p)
    Q_p = heat_transfer(U_TEST, A_TEST, lmtd_p)
    print(f"Parallel-flow: dT1={dT1_p:.0f}C, dT2={dT2_p}C, LMTD={lmtd_p:.2f}C, Q={Q_p:.1f} W")
