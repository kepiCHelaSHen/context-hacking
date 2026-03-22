"""
Stochastic SIR Epidemic — Individual-based model.
Frozen spec: frozen/sir_rules.md

NOT deterministic rate equations. Each agent has discrete S/I/R state.
Infection via complement method: p = 1 - (1-beta)^k_infected.
I(t) is always an INTEGER, never a float.
"""

from __future__ import annotations

import logging

import numpy as np

_log = logging.getLogger(__name__)

N_DEFAULT = 500
INITIAL_INFECTED = 5
BETA = 0.03
GAMMA = 0.10
CONTACTS_PER_TICK = 10
MAX_TICKS = 300


class SIRModel:
    """Stochastic individual-based SIR."""

    def __init__(
        self, seed: int = 42, n: int = N_DEFAULT,
        initial_infected: int = INITIAL_INFECTED,
        beta: float = BETA, gamma: float = GAMMA,
        contacts_per_tick: int = CONTACTS_PER_TICK,
    ) -> None:
        self.n = n
        self.beta = beta
        self.gamma = gamma
        self.contacts_per_tick = contacts_per_tick
        self.rng = np.random.default_rng(seed)

        # States: 0=S, 1=I, 2=R (integers, not floats)
        self.states = np.zeros(n, dtype=int)
        infected_idx = self.rng.choice(n, size=initial_infected, replace=False)
        self.states[infected_idx] = 1

    def count_susceptible(self) -> int:
        return int(np.sum(self.states == 0))

    def count_infected(self) -> int:
        return int(np.sum(self.states == 1))

    def count_recovered(self) -> int:
        return int(np.sum(self.states == 2))

    def step(self) -> None:
        new_states = self.states.copy()
        n = self.n
        infected_mask = self.states == 1

        for i in range(n):
            if self.states[i] == 0:  # Susceptible
                # Draw K contacts uniformly
                contacts = self.rng.choice(n, size=self.contacts_per_tick, replace=True)
                k_infected = int(np.sum(infected_mask[contacts]))
                # Complement method: p_infect = 1 - (1-beta)^k_infected
                if k_infected > 0:
                    p_escape = (1.0 - self.beta) ** k_infected
                    p_infect = 1.0 - p_escape
                    if self.rng.random() < p_infect:
                        new_states[i] = 1

            elif self.states[i] == 1:  # Infected
                if self.rng.random() < self.gamma:
                    new_states[i] = 2

        self.states = new_states


def run_simulation(
    seed: int = 42, n: int = N_DEFAULT,
    initial_infected: int = INITIAL_INFECTED,
    beta: float = BETA, gamma: float = GAMMA,
    contacts_per_tick: int = CONTACTS_PER_TICK,
    max_ticks: int = MAX_TICKS,
) -> dict:
    model = SIRModel(seed=seed, n=n, initial_infected=initial_infected,
                     beta=beta, gamma=gamma, contacts_per_tick=contacts_per_tick)

    epidemic_curve = [model.count_infected()]
    peak_infected = epidemic_curve[0]
    peak_tick = 0

    for tick in range(max_ticks):
        model.step()
        i_count = model.count_infected()
        epidemic_curve.append(i_count)
        if i_count > peak_infected:
            peak_infected = i_count
            peak_tick = tick + 1
        if i_count == 0:
            break

    final_recovered = model.count_recovered()
    final_size_fraction = final_recovered / n
    fadeout = final_recovered < int(0.20 * n)

    # R0 recovery from early growth
    r0_recovered = 0.0
    if len(epidemic_curve) > 5 and epidemic_curve[1] > 0:
        early = np.array(epidemic_curve[1:6], dtype=float)
        if np.all(early > 0):
            growth_rates = np.diff(np.log(early))
            if len(growth_rates) > 0:
                mean_growth = float(np.mean(growth_rates))
                r0_recovered = 1.0 + mean_growth / gamma if gamma > 0 else 0.0

    return {
        "peak_infected": peak_infected,
        "peak_tick": peak_tick,
        "final_recovered": final_recovered,
        "final_size_fraction": final_size_fraction,
        "fadeout": fadeout,
        "epidemic_curve": epidemic_curve,
        "r0_recovered": r0_recovered,
    }
