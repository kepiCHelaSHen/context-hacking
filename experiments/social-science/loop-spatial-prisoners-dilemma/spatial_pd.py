"""
Spatial Prisoner's Dilemma — Nowak & May (1992) Nature 359:826-829
Frozen spec: frozen/spatial_pd_rules.md

All coefficients match exactly:
  GRID_SIZE=100, b=1.8, NEIGHBORHOOD=moore_plus_self (9 cells)
  UPDATE=synchronous_deterministic_imitation
  INITIAL=single_defector_center
"""

from __future__ import annotations

import logging

import numpy as np

_log = logging.getLogger(__name__)

GRID_SIZE = 100
B_DEFAULT = 1.8
GENERATIONS = 200


class SpatialPDGrid:
    """Nowak & May (1992) spatial PD on a toroidal lattice."""

    def __init__(self, grid_size: int = GRID_SIZE, b: float = B_DEFAULT) -> None:
        self.grid_size = grid_size
        self.b = b
        # 1 = cooperate, 0 = defect
        self.grid = np.ones((grid_size, grid_size), dtype=int)
        self._payoffs = np.zeros((grid_size, grid_size), dtype=float)

    def set_initial(self, condition: str = "single_defector_center") -> None:
        if condition == "single_defector_center":
            self.grid[:] = 1
            c = self.grid_size // 2
            self.grid[c, c] = 0
        elif condition == "random_half":
            rng = np.random.default_rng(42)
            self.grid = rng.integers(0, 2, size=(self.grid_size, self.grid_size))

    def get_neighborhood(self, r: int, c: int) -> list[tuple[int, int]]:
        """Moore + SELF = 9 cells (frozen spec)."""
        result = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr = (r + dr) % self.grid_size
                nc = (c + dc) % self.grid_size
                result.append((nr, nc))
        return result

    def payoff(self, strategy_a: int, strategy_b: int) -> float:
        """Simplified Nowak & May payoff. CC=1, CD=0, DC=b, DD=0."""
        if strategy_a == 1 and strategy_b == 1:
            return 1.0
        elif strategy_a == 0 and strategy_b == 1:
            return self.b
        return 0.0

    def _compute_payoffs(self) -> None:
        """Compute total payoff for every cell (plays all 9 neighbors)."""
        self._payoffs[:] = 0.0
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                total = 0.0
                for nr, nc in self.get_neighborhood(r, c):
                    total += self.payoff(self.grid[r, c], self.grid[nr, nc])
                self._payoffs[r, c] = total

    def step(self) -> None:
        """SYNCHRONOUS DETERMINISTIC imitation: copy best neighbor."""
        self._compute_payoffs()
        new_grid = self.grid.copy()

        for r in range(self.grid_size):
            for c in range(self.grid_size):
                best_payoff = self._payoffs[r, c]
                best_strategy = self.grid[r, c]
                for nr, nc in self.get_neighborhood(r, c):
                    if self._payoffs[nr, nc] > best_payoff:
                        best_payoff = self._payoffs[nr, nc]
                        best_strategy = self.grid[nr, nc]
                new_grid[r, c] = best_strategy

        self.grid = new_grid

    def cooperation_rate(self) -> float:
        return float(np.mean(self.grid))

    def spatial_clustering(self) -> float:
        """Fraction of C-C neighbor pairs among all C neighbors."""
        cc_pairs = 0
        c_total = 0
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if self.grid[r, c] == 1:
                    for nr, nc in self.get_neighborhood(r, c):
                        if (nr, nc) != (r, c):
                            c_total += 1
                            if self.grid[nr, nc] == 1:
                                cc_pairs += 1
        return cc_pairs / max(c_total, 1)

    def pattern_stability(self, old_grid: np.ndarray) -> float:
        """Hamming distance between current and previous grid."""
        return float(np.mean(self.grid != old_grid))


def run_simulation(
    seed: int = 42,
    grid_size: int = GRID_SIZE,
    b: float = B_DEFAULT,
    initial_condition: str = "single_defector_center",
    generations: int = GENERATIONS,
) -> dict:
    rng = np.random.default_rng(seed)
    grid = SpatialPDGrid(grid_size=grid_size, b=b)

    if initial_condition == "random_half":
        grid.grid = rng.integers(0, 2, size=(grid_size, grid_size))
    else:
        grid.set_initial(initial_condition)

    stability = 0.0
    for gen in range(generations):
        old = grid.grid.copy()
        grid.step()
        stability = grid.pattern_stability(old)
        if stability == 0.0 and gen > 5:
            break

    return {
        "cooperation_rate": grid.cooperation_rate(),
        "spatial_clustering": grid.spatial_clustering(),
        "pattern_stability": stability,
        "generations_run": gen + 1,
    }
