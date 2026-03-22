"""RC Circuit — CHP Engineering Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from eng_rc_circuit_constants import *


def time_constant(R, C):
    """Return tau = R * C in seconds."""
    return R * C


def cutoff_freq_hz(R, C):
    """Return cutoff frequency f_c = 1/(2*pi*R*C) in Hz.  The 2*pi is critical!"""
    return 1.0 / (2.0 * math.pi * R * C)


def cutoff_freq_rad(R, C):
    """Return angular cutoff frequency omega_c = 1/(R*C) in rad/s."""
    return 1.0 / (R * C)


def charging_voltage(V0, R, C, t):
    """Capacitor charging: V(t) = V0 * (1 - exp(-t / tau))."""
    tau = R * C
    return V0 * (1.0 - math.exp(-t / tau))


def discharging_voltage(V0, R, C, t):
    """Capacitor discharging: V(t) = V0 * exp(-t / tau)."""
    tau = R * C
    return V0 * math.exp(-t / tau)


def gain_at_cutoff():
    """At the -3 dB cutoff frequency, gain = 1/sqrt(2)."""
    return 1.0 / math.sqrt(2.0)


if __name__ == "__main__":
    R, C = 1000.0, 1e-6  # 1 kOhm, 1 uF
    tau = time_constant(R, C)
    fc = cutoff_freq_hz(R, C)
    wc = cutoff_freq_rad(R, C)
    print(f"tau = {tau*1e3:.3f} ms")
    print(f"f_c = {fc:.2f} Hz  (NOT {1/(R*C):.0f} Hz — 2*pi matters!)")
    print(f"omega_c = {wc:.0f} rad/s")
    print(f"Gain @ cutoff = {gain_at_cutoff():.6f} (-3 dB)")
    V0 = 5.0
    print(f"Charging  V(tau) = {charging_voltage(V0, R, C, tau):.4f} V")
    print(f"Discharging V(tau) = {discharging_voltage(V0, R, C, tau):.4f} V")
