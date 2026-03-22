"""Belt Drives — Tension Ratio (Euler Belt Equation) — CHP Engineering Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from eng_power_transmission_constants import *


def wrap_angle_rad(degrees):
    """Convert wrap angle from degrees to radians: theta_rad = degrees * pi / 180."""
    return degrees * math.pi / 180.0


def tension_ratio(mu, theta_rad):
    """Euler belt friction: T1/T2 = e^(mu * theta) where theta is in RADIANS."""
    return math.exp(mu * theta_rad)


def tight_side_tension(T_slack, mu, theta_rad):
    """Tight-side tension: T1 = T2 * e^(mu * theta). T_slack = T2 (the smaller tension)."""
    return T_slack * math.exp(mu * theta_rad)


def belt_power(T1, T2, v):
    """Power transmitted by belt: P = (T1 - T2) * v. Uses the DIFFERENCE, not T1 alone."""
    return (T1 - T2) * v


if __name__ == "__main__":
    mu, theta_deg, T2, v = 0.3, 180, 500.0, 10.0
    theta_rad = wrap_angle_rad(theta_deg)
    ratio = tension_ratio(mu, theta_rad)
    T1 = tight_side_tension(T2, mu, theta_rad)
    P = belt_power(T1, T2, v)

    print(f"Wrap angle: {theta_deg} deg = {theta_rad:.4f} rad")
    print(f"Tension ratio T1/T2 = e^({mu}*{theta_rad:.4f}) = {ratio:.4f}")
    print(f"T1 = {T1:.2f} N, T2 = {T2:.2f} N")
    print(f"Power P = ({T1:.2f} - {T2:.2f}) * {v} = {P:.2f} W")
    print()
    print("--- Common LLM errors ---")
    ratio_wrong = math.exp(mu * theta_deg)
    print(f"WRONG (degrees): e^({mu}*{theta_deg}) = {ratio_wrong:.4e}  (absurd!)")
    P_wrong = T1 * v
    print(f"WRONG (P=T1*v): {P_wrong:.2f} W  (correct: {P:.2f} W)")
