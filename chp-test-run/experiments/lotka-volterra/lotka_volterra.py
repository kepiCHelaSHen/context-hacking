"""
Agent-Based Lotka-Volterra — individual predator-prey on spatial grid.
Frozen spec: frozen/lotka_volterra_rules.md

NOT ODE difference equations. Each agent is a discrete object with energy.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

import numpy as np

_log = logging.getLogger(__name__)

GRID_W = 50
GRID_H = 50
INITIAL_PREY = 200
INITIAL_PREDATORS = 50
PREY_ENERGY_GAIN = 0.05
PREY_REPRODUCE_THRESHOLD = 1.5
PREDATOR_ENERGY_COST = 0.10
PREDATOR_ENERGY_GAIN = 0.80
PREDATOR_REPRODUCE_THRESHOLD = 1.5
MAX_TICKS = 500


@dataclass
class Agent:
    species: str  # "prey" or "predator"
    energy: float = 1.0
    x: int = 0
    y: int = 0
    alive: bool = True


class LotkaVolterraGrid:
    """Agent-based predator-prey on toroidal grid."""

    def __init__(self, seed: int = 42, grid_w: int = GRID_W, grid_h: int = GRID_H) -> None:
        self.grid_w = grid_w
        self.grid_h = grid_h
        self.rng = np.random.default_rng(seed)
        self.prey_energy_gain = PREY_ENERGY_GAIN
        self.predator_energy_cost = PREDATOR_ENERGY_COST
        self.predator_energy_gain = PREDATOR_ENERGY_GAIN
        self.agents: list[Agent] = []

    def populate(self, n_prey: int = INITIAL_PREY, n_pred: int = INITIAL_PREDATORS) -> None:
        for _ in range(n_prey):
            a = Agent(species="prey", energy=1.0,
                      x=int(self.rng.integers(0, self.grid_w)),
                      y=int(self.rng.integers(0, self.grid_h)))
            self.agents.append(a)
        for _ in range(n_pred):
            a = Agent(species="predator", energy=1.0,
                      x=int(self.rng.integers(0, self.grid_w)),
                      y=int(self.rng.integers(0, self.grid_h)))
            self.agents.append(a)

    def step(self) -> None:
        self.rng.shuffle(self.agents)
        new_agents: list[Agent] = []

        # Build spatial index for prey
        prey_at: dict[tuple[int, int], list[Agent]] = {}
        for a in self.agents:
            if a.alive and a.species == "prey":
                key = (a.x, a.y)
                prey_at.setdefault(key, []).append(a)

        for a in self.agents:
            if not a.alive:
                continue

            # Move randomly (4-connected)
            direction = int(self.rng.integers(0, 4))
            if direction == 0: a.x = (a.x + 1) % self.grid_w
            elif direction == 1: a.x = (a.x - 1) % self.grid_w
            elif direction == 2: a.y = (a.y + 1) % self.grid_h
            else: a.y = (a.y - 1) % self.grid_h

            if a.species == "prey":
                a.energy += PREY_ENERGY_GAIN
                if a.energy >= PREY_REPRODUCE_THRESHOLD:
                    a.energy /= 2
                    child = Agent(species="prey", energy=a.energy, x=a.x, y=a.y)
                    new_agents.append(child)

            elif a.species == "predator":
                a.energy -= PREDATOR_ENERGY_COST
                # Try to eat prey at same cell
                key = (a.x, a.y)
                if key in prey_at and prey_at[key]:
                    victim = prey_at[key].pop(0)
                    victim.alive = False
                    a.energy += PREDATOR_ENERGY_GAIN
                # Reproduce
                if a.energy >= PREDATOR_REPRODUCE_THRESHOLD:
                    a.energy /= 2
                    child = Agent(species="predator", energy=a.energy, x=a.x, y=a.y)
                    new_agents.append(child)
                # Starve
                if a.energy <= 0:
                    a.alive = False

        self.agents = [a for a in self.agents if a.alive] + new_agents

    def count_prey(self) -> int:
        return sum(1 for a in self.agents if a.alive and a.species == "prey")

    def count_predators(self) -> int:
        return sum(1 for a in self.agents if a.alive and a.species == "predator")


def run_simulation(
    seed: int = 42, grid_w: int = GRID_W, grid_h: int = GRID_H,
    initial_prey: int = INITIAL_PREY, initial_predators: int = INITIAL_PREDATORS,
    prey_energy_gain: float = PREY_ENERGY_GAIN,
    prey_reproduce_threshold: float = PREY_REPRODUCE_THRESHOLD,
    predator_energy_cost: float = PREDATOR_ENERGY_COST,
    predator_energy_gain: float = PREDATOR_ENERGY_GAIN,
    predator_reproduce_threshold: float = PREDATOR_REPRODUCE_THRESHOLD,
    max_ticks: int = MAX_TICKS,
) -> dict:
    grid = LotkaVolterraGrid(seed=seed, grid_w=grid_w, grid_h=grid_h)
    grid.populate(initial_prey, initial_predators)

    prey_traj = [grid.count_prey()]
    pred_traj = [grid.count_predators()]

    for tick in range(max_ticks):
        grid.step()
        prey_traj.append(grid.count_prey())
        pred_traj.append(grid.count_predators())
        if grid.count_prey() == 0 and grid.count_predators() == 0:
            break

    # Oscillation detection
    prey_arr = np.array(prey_traj[50:]) if len(prey_traj) > 100 else np.array(prey_traj)
    osc_period = 0.0
    if len(prey_arr) > 20:
        from scipy.signal import find_peaks
        peaks, _ = find_peaks(prey_arr, distance=10)
        if len(peaks) >= 2:
            osc_period = float(np.mean(np.diff(peaks)))

    return {
        "prey_count": grid.count_prey(),
        "predator_count": grid.count_predators(),
        "prey_extinct": grid.count_prey() == 0,
        "predator_extinct": grid.count_predators() == 0,
        "oscillation_period": osc_period,
        "prey_trajectory": prey_traj,
        "predator_trajectory": pred_traj,
    }
