"""
Lorenz Attractor — adaptive RK45 integration.
Frozen spec: frozen/lorenz_rules.md

sigma=10, rho=28, beta=8/3 (EXACT, not 2.667).
IC=(1,1,1) (NOT (0,1,0) from paper).
Integration: scipy.integrate.solve_ivp RK45, rtol=atol=1e-9.
NOT Euler. NOT fixed-step RK4.
"""

from __future__ import annotations

import logging

import numpy as np
from scipy.integrate import solve_ivp

_log = logging.getLogger(__name__)

SIGMA = 10.0
RHO = 28.0
BETA = 8.0 / 3.0  # exact fraction, NOT 2.667
X0, Y0, Z0 = 1.0, 1.0, 1.0
T_END = 50.0
N_POINTS = 10000
RTOL = 1e-9
ATOL = 1e-9


class LorenzSystem:
    def __init__(self, sigma: float = SIGMA, rho: float = RHO, beta: float = BETA) -> None:
        self.sigma = sigma
        self.rho = rho
        self.beta = beta

    def derivatives(self, t: float, state: np.ndarray) -> list[float]:
        x, y, z = state
        return [
            self.sigma * (y - x),
            x * (self.rho - z) - y,
            x * y - self.beta * z,
        ]


def run_simulation(
    sigma: float = SIGMA, rho: float = RHO, beta: float = BETA,
    x0: float = X0, y0: float = Y0, z0: float = Z0,
    t_end: float = T_END, n_points: int = N_POINTS,
    rtol: float = RTOL, atol: float = ATOL,
) -> dict:
    sys = LorenzSystem(sigma=sigma, rho=rho, beta=beta)
    t_eval = np.linspace(0, t_end, n_points)

    sol = solve_ivp(
        sys.derivatives, [0, t_end], [x0, y0, z0],
        method="RK45", t_eval=t_eval, rtol=rtol, atol=atol,
    )

    x, y, z = sol.y

    # Attractor bounds
    bounded = bool(np.all(np.abs(x) < 25) and np.all(np.abs(y) < 30) and np.all(np.abs(z) < 55))

    # Not fixed point (check last 1000 points)
    not_fp = bool(np.std(x[-1000:]) > 1.0)

    # Lyapunov exponent (simplified: from divergence of perturbed trajectory)
    eps = 1e-7
    sol2 = solve_ivp(
        sys.derivatives, [0, t_end], [x0, y0, z0 + eps],
        method="RK45", t_eval=t_eval, rtol=rtol, atol=atol,
    )
    x2 = sol2.y[0]
    div = np.abs(x - x2)
    div = np.where(div > 0, div, 1e-20)
    log_div = np.log(div / eps)
    lyapunov = float(np.mean(log_div[n_points // 2:])) / t_end

    return {
        "x": x.tolist(), "y": y.tolist(), "z": z.tolist(),
        "attractor_bounded": bounded,
        "not_fixed_point": not_fp,
        "lyapunov_exponent": lyapunov,
    }
