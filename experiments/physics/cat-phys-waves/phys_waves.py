"""Waves & Harmonics — CHP Physics Sprint. All constants from frozen spec."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from phys_waves_constants import V_SOUND

def open_pipe_harmonics(L, n_max=5):
    """Open pipe: f_n = n·v/(2L) for n=1,2,3,... (ALL harmonics)."""
    return [n * V_SOUND / (2 * L) for n in range(1, n_max + 1)]

def closed_pipe_harmonics(L, n_max=5):
    """Closed pipe: f_n = n·v/(4L) for n=1,3,5,... (ODD harmonics only)."""
    return [n * V_SOUND / (4 * L) for n in range(1, 2 * n_max, 2)]

def string_harmonics(L, v_string, n_max=5):
    """String fixed at both ends: f_n = n·v/(2L)."""
    return [n * v_string / (2 * L) for n in range(1, n_max + 1)]

def beat_frequency(f1, f2):
    """f_beat = |f1 - f2|."""
    return abs(f1 - f2)

def wavelength(f, v=V_SOUND):
    """λ = v/f."""
    return v / f

if __name__ == "__main__":
    print(f"Open pipe (1m): {open_pipe_harmonics(1.0, 4)} Hz")
    print(f"Closed pipe (1m): {closed_pipe_harmonics(1.0, 4)} Hz")
    print(f"Closed pipe has NO even harmonics!")
    print(f"Beat freq (440, 442): {beat_frequency(440, 442)} Hz")
