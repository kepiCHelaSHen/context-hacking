"""
Izhikevich (2003) Spiking Neuron Model.
Frozen spec: frozen/izhikevich_rules.md

TWO variables: v, u. NOT four (Hodgkin-Huxley: V,m,h,n).
Parameters: a, b, c, d. NOT gNa, gK, gL.
v' = 0.04*v^2 + 5*v + 140 - u + I
Two half-steps at dt=0.5 ms (per Izhikevich 2003).
"""

from __future__ import annotations

import logging

import numpy as np

_log = logging.getLogger(__name__)

DT = 0.5
DURATION = 1000
STEPS = int(DURATION / DT)
SPIKE_THRESHOLD = 30


class IzhikevichNeuron:
    """Izhikevich spiking neuron — 2 variables (v, u), 4 parameters (a, b, c, d)."""

    def __init__(self, a: float, b: float, c: float, d: float) -> None:
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.v: float = -65.0  # mV, resting potential
        self.u: float = b * (-65.0)

    def step(self, I: float, dt: float = DT) -> bool:
        """Advance one time step. Returns True if spike occurred.

        Uses TWO half-steps for v (per Izhikevich 2003, Section II):
          v += 0.5*(0.04*v^2 + 5*v + 140 - u + I)
          v += 0.5*(0.04*v^2 + 5*v + 140 - u + I)
          u += a*(b*v - u)
        """
        # Two half-steps for v (numerical stability)
        self.v += 0.5 * (0.04 * self.v ** 2 + 5 * self.v + 140 - self.u + I)
        self.v += 0.5 * (0.04 * self.v ** 2 + 5 * self.v + 140 - self.u + I)
        self.u += self.a * (self.b * self.v - self.u)

        if self.v >= 30:
            spike = True
            self.v = self.c
            self.u += self.d
        else:
            spike = False

        return spike


def run_simulation(
    a: float = 0.02, b: float = 0.2, c: float = -65.0, d: float = 8.0,
    I: float = 10.0, dt: float = DT, duration: float = DURATION,
    seed: int = 42,
) -> dict:
    neuron = IzhikevichNeuron(a=a, b=b, c=c, d=d)
    rng = np.random.default_rng(seed)

    steps = int(duration / dt)
    v_trace: list[float] = []
    spike_times: list[float] = []

    for step_i in range(steps):
        t = step_i * dt
        spike = neuron.step(I, dt)
        v_trace.append(neuron.v)
        if spike:
            spike_times.append(t)

    # ISI statistics
    isis = np.diff(spike_times) if len(spike_times) > 1 else []
    mean_isi = float(np.mean(isis)) if len(isis) > 0 else 0.0
    isi_cv = float(np.std(isis) / np.mean(isis)) if len(isis) > 1 and np.mean(isis) > 0 else 0.0

    return {
        "spike_count": len(spike_times),
        "spike_times": spike_times,
        "mean_isi": mean_isi,
        "isi_cv": isi_cv,
        "v_trace": v_trace,
        "v_bounded": all(-90 <= v <= 40 for v in v_trace),
    }
