"""PID Controller — CHP Engineering Sprint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from eng_pid_controller_constants import *


def proportional(Kp, error):
    """P term: Kp * e(t)."""
    return Kp * error


def integral_term(Ki, error_sum, dt):
    """I term: Ki * cumulative_error_sum.  error_sum already includes dt."""
    return Ki * error_sum


def derivative_term(Kd, error_current, error_prev, dt):
    """D term: Kd * (e[n] - e[n-1]) / dt.  Sign: current minus previous."""
    return Kd * (error_current - error_prev) / dt


def pid_output(Kp, Ki, Kd, error, integral, derivative):
    """Full PID output: u = P + I + D (pre-computed terms supplied)."""
    return Kp * error + integral + derivative


def simulate_step_response(Kp, Ki, Kd, errors, dt):
    """Run discrete PID over an error sequence, return list of outputs."""
    outputs = []
    error_sum = 0.0
    for n, e in enumerate(errors):
        error_sum += e * dt
        p = proportional(Kp, e)
        i = integral_term(Ki, error_sum, dt)
        if n == 0:
            d = 0.0
        else:
            d = derivative_term(Kd, e, errors[n - 1], dt)
        outputs.append(p + i + d)
    return outputs


if __name__ == "__main__":
    results = simulate_step_response(KP, KI, KD, ERRORS, DT)
    for n, (u, u_exp) in enumerate(zip(results, U_EXPECTED)):
        status = "OK" if abs(u - u_exp) < 1e-9 else "MISMATCH"
        print(f"Step {n}: u={u:.4f}  expected={u_exp:.4f}  [{status}]")
