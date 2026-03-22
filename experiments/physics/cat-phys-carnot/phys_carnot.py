"""Carnot Cycle — CHP Physics Sprint. All constants from frozen spec."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from phys_carnot_constants import *

def carnot_efficiency(T_hot_K, T_cold_K):
    """η = 1 - Tc/Th. Temperatures MUST be in Kelvin."""
    if T_hot_K <= T_cold_K:
        raise ValueError("T_hot must exceed T_cold")
    return 1.0 - T_cold_K / T_hot_K

def cop_heat_pump(T_hot_K, T_cold_K):
    """COP_hp = Th/(Th-Tc). Can be > 1."""
    return T_hot_K / (T_hot_K - T_cold_K)

def cop_refrigerator(T_hot_K, T_cold_K):
    """COP_ref = Tc/(Th-Tc). Note: COP_hp = COP_ref + 1."""
    return T_cold_K / (T_hot_K - T_cold_K)

def work_from_heat(Q_hot, efficiency):
    """W = η·Q_hot."""
    return efficiency * Q_hot

if __name__ == "__main__":
    eta = carnot_efficiency(TH_TEST, TC_TEST)
    print(f"Carnot efficiency (500K/300K): {eta:.1%}")
    print(f"COP heat pump: {cop_heat_pump(TH_TEST, TC_TEST):.1f}")
    print(f"COP refrigerator: {cop_refrigerator(TH_TEST, TC_TEST):.1f}")
    print(f"COP_hp = COP_ref + 1: {cop_heat_pump(TH_TEST, TC_TEST) == cop_refrigerator(TH_TEST, TC_TEST) + 1}")
