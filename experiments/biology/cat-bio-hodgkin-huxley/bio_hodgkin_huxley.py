"""Hodgkin-Huxley Ionic Currents — CHP Biology Sprint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from bio_hodgkin_huxley_constants import *


def i_na(g_na, m, h, V, E_na):
    """Sodium current: I_Na = g_Na * m^3 * h * (V - E_Na).

    m = activation gate (rises during depolarization, fast)
    h = inactivation gate (falls during depolarization, slow)
    """
    return g_na * m**3 * h * (V - E_na)


def i_k(g_k, n, V, E_k):
    """Potassium current: I_K = g_K * n^4 * (V - E_K).

    n = activation gate (rises during depolarization, slow)
    """
    return g_k * n**4 * (V - E_k)


def i_leak(g_l, V, E_l):
    """Leak current: I_L = g_L * (V - E_L)."""
    return g_l * (V - E_l)


def total_ionic_current(g_na, m, h, V_m, E_na, g_k, n, E_k, g_l, E_l):
    """Total membrane ionic current: I_ion = I_Na + I_K + I_L."""
    return (i_na(g_na, m, h, V_m, E_na)
            + i_k(g_k, n, V_m, E_k)
            + i_leak(g_l, V_m, E_l))


if __name__ == "__main__":
    print(f"Hodgkin-Huxley ionic currents at V_rest={V_REST} mV")
    print(f"  g_Na={G_NA}, g_K={G_K}, g_L={G_L} mS/cm^2")
    print(f"  E_Na={E_NA}, E_K={E_K}, E_L={E_L} mV")
    print(f"  m={M_REST}, h={H_REST}, n={N_REST}")
    print(f"  I_Na  = {i_na(G_NA, M_REST, H_REST, V_REST, E_NA):.6f} uA/cm^2")
    print(f"  I_K   = {i_k(G_K, N_REST, V_REST, E_K):.6f} uA/cm^2")
    print(f"  I_L   = {i_leak(G_L, V_REST, E_L):.6f} uA/cm^2")
    print(f"  I_tot = {total_ionic_current(G_NA, M_REST, H_REST, V_REST, E_NA, G_K, N_REST, E_K, G_L, E_L):.6f} uA/cm^2")
