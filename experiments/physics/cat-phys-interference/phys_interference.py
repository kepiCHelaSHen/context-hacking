"""Thin Film Interference — CHP Physics Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from phys_interference_constants import N_OIL, N_WATER

def constructive_wavelengths(n_film, thickness, m_max=3, one_phase_change=True):
    """Wavelengths showing constructive interference."""
    results = []
    for m in range(0, m_max+1):
        if one_phase_change:
            lam = 2 * n_film * thickness / (m + 0.5)
        else:
            lam = 2 * n_film * thickness / (m + 1) if m >= 0 else None
        if lam and 380e-9 < lam < 750e-9:
            results.append((m, lam))
    return results

def phase_change_at_reflection(n_incident, n_transmitted):
    """Phase change of π when reflecting from higher-n surface."""
    return n_transmitted > n_incident

def path_difference(n_film, thickness): return 2 * n_film * thickness

if __name__ == "__main__":
    visible = constructive_wavelengths(N_OIL, 300e-9)
    for m, lam in visible:
        print(f"m={m}: λ={lam*1e9:.0f} nm")
    print(f"Phase change air→oil: {phase_change_at_reflection(1.0, N_OIL)}")
