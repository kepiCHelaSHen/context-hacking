"""
Grover's Search Algorithm — state-vector quantum simulation.
Frozen spec: frozen/grover_rules.md

State vector: 2^n complex amplitudes. NOT classical search.
Oracle: PHASE FLIP (amplitudes[target] *= -1). NOT boolean return.
Diffusion: inversion about mean. G = D * O (oracle first, then diffusion).
k_opt = floor(pi/4 * sqrt(N)). For N=1024: k=25.
"""

from __future__ import annotations

import logging
import math

import numpy as np

_log = logging.getLogger(__name__)

N_QUBITS = 10
N_ITEMS = 2 ** N_QUBITS  # 1024
K_OPTIMAL = int(math.floor(math.pi / 4 * math.sqrt(N_ITEMS)))  # 25


class GroverSimulator:
    """State-vector Grover's algorithm simulation."""

    def __init__(self, n_qubits: int = N_QUBITS, seed: int = 42) -> None:
        self.n_qubits = n_qubits
        self.n_items = 2 ** n_qubits
        self.rng = np.random.default_rng(seed)
        self.target = int(self.rng.integers(0, self.n_items))
        self.amplitudes = np.zeros(self.n_items, dtype=np.float64)

    def initialize(self) -> None:
        """Equal superposition: all amplitudes = 1/sqrt(N)."""
        self.amplitudes[:] = 1.0 / math.sqrt(self.n_items)

    def apply_oracle(self) -> None:
        """Phase flip on target: amplitudes[target] *= -1."""
        self.amplitudes[self.target] *= -1

    def apply_diffusion(self) -> None:
        """Inversion about the mean: D = 2|psi0><psi0| - I."""
        mean_amp = np.mean(self.amplitudes)
        self.amplitudes = 2.0 * mean_amp - self.amplitudes

    def grover_iteration(self) -> None:
        """One Grover iteration: G = D * O (oracle then diffusion)."""
        self.apply_oracle()
        self.apply_diffusion()

    def success_probability(self) -> float:
        """P(measuring target) = |amplitude[target]|^2."""
        return float(self.amplitudes[self.target] ** 2)

    def target_amplitude(self) -> float:
        return float(abs(self.amplitudes[self.target]))


def run_simulation(
    seed: int = 42,
    n_qubits: int = N_QUBITS,
    iterations: int = K_OPTIMAL,
) -> dict:
    sim = GroverSimulator(n_qubits=n_qubits, seed=seed)
    sim.initialize()

    for _ in range(iterations):
        sim.grover_iteration()

    return {
        "success_probability": sim.success_probability(),
        "target_amplitude": sim.target_amplitude(),
        "target": sim.target,
        "iterations": iterations,
        "n_items": sim.n_items,
    }
