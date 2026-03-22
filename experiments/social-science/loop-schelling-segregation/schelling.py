"""
Schelling Segregation Model — CHP Implementation
Frozen spec: frozen/schelling_rules.md (Schelling 1971 + dynamic tolerance)

All coefficients match the frozen spec exactly:
  GRID_SIZE=50, DENSITY=0.90, TOLERANCE_DEFAULT=0.375
  UPDATE_ORDER=simultaneous, NEIGHBORHOOD=moore (8 cells)
  Dynamic tolerance: update_rate=0.005, comfort_margin=0.1, range [0.1, 0.9]
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

import numpy as np

_log = logging.getLogger(__name__)

# ── Frozen coefficients (must match frozen/schelling_rules.md) ────────────────
GRID_SIZE = 50
DENSITY = 0.90
TYPE_RATIO = 0.50
TOLERANCE_DEFAULT = 0.375
MAX_STEPS = 500
TOLERANCE_UPDATE_RATE = 0.005
TOLERANCE_COMFORT_MARGIN = 0.1
TOLERANCE_MIN = 0.1
TOLERANCE_MAX = 0.9


@dataclass
class Agent:
    agent_type: int   # 1 = A, 2 = B
    tolerance: float  # satisfaction threshold


class SchellingGrid:
    """50x50 toroidal Schelling segregation grid."""

    def __init__(
        self,
        seed: int = 42,
        grid_size: int = GRID_SIZE,
        density: float = DENSITY,
        tolerance: float = TOLERANCE_DEFAULT,
    ) -> None:
        self.grid_size = grid_size
        self.rng = np.random.default_rng(seed)

        # Grid: 0 = empty, 1 = type A, 2 = type B
        self.grid = np.zeros((grid_size, grid_size), dtype=int)

        # Agents stored by position for tolerance tracking
        self.agents: dict[tuple[int, int], Agent] = {}

        # Place agents
        n_cells = grid_size * grid_size
        n_occupied = int(n_cells * density)
        n_a = int(n_occupied * TYPE_RATIO)
        n_b = n_occupied - n_a

        positions = list(range(n_cells))
        self.rng.shuffle(positions)

        for i, pos in enumerate(positions[:n_occupied]):
            r, c = divmod(pos, grid_size)
            agent_type = 1 if i < n_a else 2
            self.grid[r, c] = agent_type
            self.agents[(r, c)] = Agent(agent_type=agent_type, tolerance=tolerance)

        self.update_order = "simultaneous"
        _log.info("SchellingGrid created: %dx%d, density=%.2f, tolerance=%.3f",
                  grid_size, grid_size, density, tolerance)

    def _neighbors(self, r: int, c: int) -> list[tuple[int, int]]:
        """Moore neighborhood (8 cells) with toroidal wrapping."""
        result = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr = (r + dr) % self.grid_size
                nc = (c + dc) % self.grid_size
                result.append((nr, nc))
        return result

    def _is_satisfied(self, r: int, c: int) -> bool:
        """Check if the agent at (r,c) is satisfied per its tolerance."""
        agent = self.agents.get((r, c))
        if agent is None:
            return True  # empty cell

        neighbors = self._neighbors(r, c)
        occupied = [(nr, nc) for nr, nc in neighbors if self.grid[nr, nc] != 0]
        if not occupied:
            return True  # no neighbors = satisfied

        same = sum(1 for nr, nc in occupied if self.grid[nr, nc] == agent.agent_type)
        fraction = same / len(occupied)
        return fraction >= agent.tolerance

    def _same_type_fraction(self, r: int, c: int) -> float:
        """Fraction of occupied neighbors that are same type."""
        agent = self.agents.get((r, c))
        if agent is None:
            return 0.0
        neighbors = self._neighbors(r, c)
        occupied = [(nr, nc) for nr, nc in neighbors if self.grid[nr, nc] != 0]
        if not occupied:
            return 1.0
        same = sum(1 for nr, nc in occupied if self.grid[nr, nc] == agent.agent_type)
        return same / len(occupied)

    def step(self, dynamic_tolerance: bool = False) -> int:
        """Run one step. Returns number of agents that moved.

        SIMULTANEOUS update: all moves computed from the same pre-move state,
        then applied together. This matches the frozen spec.
        """
        # Find all dissatisfied agents
        dissatisfied: list[tuple[int, int]] = []
        for (r, c), agent in self.agents.items():
            if not self._is_satisfied(r, c):
                dissatisfied.append((r, c))

        # Find all empty cells
        empty: list[tuple[int, int]] = []
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if self.grid[r, c] == 0:
                    empty.append((r, c))

        # Shuffle empty cells for random placement
        self.rng.shuffle(empty)

        # Move dissatisfied agents (SIMULTANEOUS: compute all, then apply)
        moves: list[tuple[tuple[int, int], tuple[int, int]]] = []
        empty_idx = 0
        for old_pos in dissatisfied:
            if empty_idx >= len(empty):
                break
            new_pos = empty[empty_idx]
            empty_idx += 1
            moves.append((old_pos, new_pos))

        # Apply all moves at once
        for old_pos, new_pos in moves:
            agent = self.agents.pop(old_pos)
            self.grid[old_pos[0], old_pos[1]] = 0
            self.grid[new_pos[0], new_pos[1]] = agent.agent_type
            self.agents[new_pos] = agent

        # Dynamic tolerance update (applied AFTER move step, per frozen spec)
        if dynamic_tolerance:
            for (r, c), agent in self.agents.items():
                frac = self._same_type_fraction(r, c)
                if frac > agent.tolerance + TOLERANCE_COMFORT_MARGIN:
                    agent.tolerance = min(TOLERANCE_MAX,
                                          agent.tolerance + TOLERANCE_UPDATE_RATE)
                elif frac < agent.tolerance - TOLERANCE_COMFORT_MARGIN:
                    agent.tolerance = max(TOLERANCE_MIN,
                                          agent.tolerance - TOLERANCE_UPDATE_RATE)

        return len(moves)

    def segregation_index(self) -> float:
        """Mean same-type neighbor fraction across all occupied cells."""
        fracs = []
        for (r, c) in self.agents:
            fracs.append(self._same_type_fraction(r, c))
        return float(np.mean(fracs)) if fracs else 0.0

    def cluster_count(self) -> int:
        """Count connected components of same-type agents (BFS)."""
        visited = set()
        clusters = 0
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if self.grid[r, c] == 0 or (r, c) in visited:
                    continue
                # BFS from this cell
                clusters += 1
                queue = [(r, c)]
                visited.add((r, c))
                agent_type = self.grid[r, c]
                while queue:
                    cr, cc = queue.pop(0)
                    for nr, nc in self._neighbors(cr, cc):
                        if (nr, nc) not in visited and self.grid[nr, nc] == agent_type:
                            visited.add((nr, nc))
                            queue.append((nr, nc))
        return clusters

    @property
    def population(self) -> int:
        return len(self.agents)


def run_simulation(
    seed: int = 42,
    grid_size: int = GRID_SIZE,
    density: float = DENSITY,
    type_ratio: float = TYPE_RATIO,
    tolerance: float = TOLERANCE_DEFAULT,
    dynamic_tolerance: bool = False,
    tolerance_update_rate: float = TOLERANCE_UPDATE_RATE,
    tolerance_comfort_margin: float = TOLERANCE_COMFORT_MARGIN,
    tolerance_min: float = TOLERANCE_MIN,
    tolerance_max: float = TOLERANCE_MAX,
    max_steps: int = MAX_STEPS,
) -> dict:
    """Run a full Schelling simulation and return metrics."""
    grid = SchellingGrid(seed=seed, grid_size=grid_size, density=density,
                         tolerance=tolerance)

    n_moved = -1
    for step in range(max_steps):
        n_moved = grid.step(dynamic_tolerance=dynamic_tolerance)
        # With dynamic tolerance, don't stop at convergence — tolerances
        # keep evolving even when no agents move, which can CREATE new
        # dissatisfaction and trigger further movement. Only stop when
        # no movement for 10 consecutive steps (true equilibrium).
        if not dynamic_tolerance and n_moved == 0:
            _log.info("Converged at step %d (fixed tolerance)", step)
            break
    # Dynamic tolerance runs for all max_steps

    seg = grid.segregation_index()
    clusters = grid.cluster_count()

    return {
        "segregation_index": seg,
        "cluster_count": clusters,
        "population": grid.population,
        "steps_to_converge": step + 1,
        "converged": n_moved == 0,
    }
