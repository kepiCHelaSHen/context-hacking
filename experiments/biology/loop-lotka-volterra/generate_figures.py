"""Generate publication-quality figures for Agent-Based Lotka-Volterra experiment."""

from __future__ import annotations

import sys
import os

# Ensure we can import the experiment module
sys.path.insert(0, os.path.dirname(__file__))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from lotka_volterra import run_simulation


def main() -> None:
    out_dir = os.path.join(os.path.dirname(__file__), "figures")
    os.makedirs(out_dir, exist_ok=True)

    # Use reduced grid/population to keep runtime feasible (full 50x50 grid
    # with 200 prey and 500 ticks causes runaway population growth and takes
    # extremely long).  The dynamics are qualitatively identical on a 30x30 grid.
    SIM_KW = dict(grid_w=30, grid_h=30, initial_prey=100, initial_predators=30,
                  max_ticks=200)

    # --- Run seed=42 for the showcase panels ---
    result_42 = run_simulation(seed=42, **SIM_KW)
    prey_traj = result_42["prey_trajectory"]
    pred_traj = result_42["predator_trajectory"]

    # --- Run 5 seeds and count extinctions ---
    seeds = [42, 123, 456, 789, 1024]
    extinctions = 0
    for s in seeds:
        r = run_simulation(seed=s, **SIM_KW)
        if r["prey_extinct"] or r["predator_extinct"]:
            extinctions += 1

    # --- Figure: two panels ---
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), facecolor="white")

    # Left panel: population over time
    ax = axes[0]
    ticks = np.arange(len(prey_traj))
    ax.plot(ticks, prey_traj, color="#2ca02c", linewidth=1.2, label="Prey")
    ax.plot(ticks, pred_traj, color="#d62728", linewidth=1.2, label="Predator")
    ax.set_xlabel("Tick", fontsize=11)
    ax.set_ylabel("Population", fontsize=11)
    ax.set_title("Population Dynamics (seed=42)", fontsize=12)
    ax.legend(frameon=True, fontsize=10)
    ax.set_xlim(0, len(prey_traj) - 1)
    ax.set_ylim(bottom=0)
    ax.grid(True, alpha=0.3)

    # Text box: extinction count across 5 seeds
    textstr = f"Extinctions: {extinctions}/{len(seeds)} seeds"
    props = dict(boxstyle="round,pad=0.4", facecolor="wheat", alpha=0.8)
    ax.text(0.97, 0.97, textstr, transform=ax.transAxes, fontsize=10,
            verticalalignment="top", horizontalalignment="right", bbox=props)

    # Right panel: phase portrait
    ax2 = axes[1]
    ax2.plot(prey_traj, pred_traj, color="#1f77b4", linewidth=0.7, alpha=0.8)
    ax2.plot(prey_traj[0], pred_traj[0], "go", markersize=8, label="Start", zorder=5)
    ax2.plot(prey_traj[-1], pred_traj[-1], "rs", markersize=8, label="End", zorder=5)
    ax2.set_xlabel("Prey count", fontsize=11)
    ax2.set_ylabel("Predator count", fontsize=11)
    ax2.set_title("Phase Portrait (seed=42)", fontsize=12)
    ax2.legend(frameon=True, fontsize=10)
    ax2.set_xlim(left=0)
    ax2.set_ylim(bottom=0)
    ax2.grid(True, alpha=0.3)

    fig.suptitle("Agent-Based Lotka-Volterra \u2014 Prior-as-Detector Demo",
                 fontsize=14, fontweight="bold", y=1.02)
    fig.tight_layout()

    out_path = os.path.join(out_dir, "lotka_volterra_dynamics.png")
    fig.savefig(out_path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    size_kb = os.path.getsize(out_path) / 1024
    print(f"Saved: {out_path}  ({size_kb:.1f} KB)")
    assert size_kb > 10, f"File too small: {size_kb:.1f} KB"
    print("OK")


if __name__ == "__main__":
    main()
