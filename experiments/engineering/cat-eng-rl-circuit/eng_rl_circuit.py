"""RL Circuit — CHP Engineering Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from eng_rl_circuit_constants import R_TEST, L_TEST

def time_constant(L, R):
    """τ = L/R  (NOT R/L!)"""
    return L / R

def current_rise(V, R, L, t):
    """Step response: i(t) = (V/R)(1 - e^(-t/τ)), τ = L/R."""
    tau = time_constant(L, R)
    return (V / R) * (1.0 - math.exp(-t / tau))

def current_decay(I0, R, L, t):
    """Natural response: i(t) = I₀·e^(-t/τ), τ = L/R."""
    tau = time_constant(L, R)
    return I0 * math.exp(-t / tau)

def cutoff_freq(R, L):
    """Cutoff frequency: f_c = R/(2πL)."""
    return R / (2.0 * math.pi * L)

if __name__ == "__main__":
    tau = time_constant(L_TEST, R_TEST)
    print(f"τ = L/R = {L_TEST}/{R_TEST} = {tau*1000:.1f} ms")
    i_rise = current_rise(10.0, R_TEST, L_TEST, tau)
    print(f"i(τ) step = {i_rise:.5f} A  (63.2% of {10.0/R_TEST:.1f} A)")
    i_decay = current_decay(0.1, R_TEST, L_TEST, tau)
    print(f"i(τ) decay = {i_decay:.5f} A  (36.8% of 0.1 A)")
    fc = cutoff_freq(R_TEST, L_TEST)
    print(f"f_c = {fc:.3f} Hz")
