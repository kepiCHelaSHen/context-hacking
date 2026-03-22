"""Price Elasticity of Demand — CHP Economics Sprint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from econ_elasticity_constants import (
    P1, Q1, P2, Q2, PED_TEST, PED_CLASSIFICATION,
    Y1, Y2, QY1, QY2, YED_TEST,
    PB1, PB2, QA1, QA2, XED_TEST,
)


def price_elasticity_midpoint(P1, Q1, P2, Q2):
    """PED using midpoint (arc) method. Returns NEGATIVE value for normal goods."""
    pct_delta_p = (P2 - P1) / ((P1 + P2) / 2)
    pct_delta_q = (Q2 - Q1) / ((Q1 + Q2) / 2)
    return pct_delta_q / pct_delta_p


def classify_elasticity(ped):
    """Classify by |PED|: >1 elastic, <1 inelastic, =1 unit elastic."""
    abs_ped = abs(ped)
    if abs(abs_ped - 1.0) < 1e-9:
        return "unit elastic"
    elif abs_ped > 1.0:
        return "elastic"
    else:
        return "inelastic"


def income_elasticity(Q1, Q2, Y1, Y2):
    """Income elasticity of demand (midpoint method). Positive=normal, negative=inferior."""
    pct_delta_y = (Y2 - Y1) / ((Y1 + Y2) / 2)
    pct_delta_q = (Q2 - Q1) / ((Q1 + Q2) / 2)
    return pct_delta_q / pct_delta_y


def cross_elasticity(Qa1, Qa2, Pb1, Pb2):
    """Cross-price elasticity (midpoint method). Positive=substitutes, negative=complements."""
    pct_delta_pb = (Pb2 - Pb1) / ((Pb1 + Pb2) / 2)
    pct_delta_qa = (Qa2 - Qa1) / ((Qa1 + Qa2) / 2)
    return pct_delta_qa / pct_delta_pb


if __name__ == "__main__":
    ped = price_elasticity_midpoint(P1, Q1, P2, Q2)
    print(f"PED (midpoint): {ped:.4f}  <-- NEGATIVE for normal goods")
    print(f"|PED| = {abs(ped):.4f} -> {classify_elasticity(ped)}")
    print()
    yed = income_elasticity(QY1, QY2, Y1, Y2)
    print(f"Income elasticity: {yed:.4f} -> {'normal' if yed > 0 else 'inferior'} good")
    print()
    xed = cross_elasticity(QA1, QA2, PB1, PB2)
    print(f"Cross-price elasticity: {xed:.4f} -> {'substitutes' if xed > 0 else 'complements'}")
