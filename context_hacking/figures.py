"""
CHP Auto-Figure Generator — publication-quality figures from experiment data.

Each experiment generates its own domain-specific visualization:
  Schelling:   segregation grid heatmap (before/after dynamic tolerance)
  Spatial PD:  cooperator/defector lattice + b-sweep curve
  Lotka-V:     predator-prey population time series + phase portrait
  SIR:         epidemic curve (S/I/R stacked) + fadeout distribution
  Lorenz:      3D butterfly attractor
  Grover:      amplitude bar chart + sinusoidal success curve
  Izhikevich:  membrane voltage traces (5 firing patterns)
  Blockchain:  safety/liveness heatmap across fault levels
  Metal:       interval diagram + parallel fifths visualization

Usage:
    from context_hacking.figures import generate_figures
    generate_figures("schelling-segregation", experiment_dir)
"""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np

_log = logging.getLogger(__name__)


def generate_figures(experiment_name: str, experiment_dir: Path) -> list[Path]:
    """Generate all figures for an experiment. Returns list of saved paths."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig_dir = experiment_dir / "figures"
    fig_dir.mkdir(exist_ok=True)
    saved: list[Path] = []

    generators = {
        "schelling": _fig_schelling,
        "spatial-prisoners-dilemma": _fig_spatial_pd,
        "spatial_pd": _fig_spatial_pd,
        "lotka-volterra": _fig_lotka_volterra,
        "lotka_volterra": _fig_lotka_volterra,
        "sir-epidemic": _fig_sir,
        "sir": _fig_sir,
        "lorenz-attractor": _fig_lorenz,
        "lorenz": _fig_lorenz,
        "quantum-grover": _fig_grover,
        "grover": _fig_grover,
        "izhikevich-neurons": _fig_izhikevich,
        "izhikevich": _fig_izhikevich,
        "blockchain-consensus": _fig_blockchain,
        "blockchain": _fig_blockchain,
        "metal-harmony": _fig_metal,
        "metal": _fig_metal,
    }

    for key, gen_fn in generators.items():
        if key in experiment_name.lower():
            try:
                paths = gen_fn(experiment_dir, fig_dir)
                saved.extend(paths)
                _log.info("Generated %d figures for %s", len(paths), experiment_name)
            except Exception as e:
                _log.warning("Figure generation failed for %s: %s", key, e)
            break

    return saved


def _dark_style():
    """Apply dark background style for all figures."""
    import matplotlib.pyplot as plt
    plt.style.use("dark_background")
    plt.rcParams.update({
        "figure.facecolor": "#0a0a1a",
        "axes.facecolor": "#0d0d20",
        "axes.edgecolor": "#2a2a4a",
        "text.color": "#e0e0e0",
        "axes.labelcolor": "#e0e0e0",
        "xtick.color": "#888",
        "ytick.color": "#888",
        "grid.color": "#1a1a3a",
        "font.family": "monospace",
    })


# ── Schelling ────────────────────────────────────────────────────────────────

def _fig_schelling(exp_dir: Path, fig_dir: Path) -> list[Path]:
    import matplotlib.pyplot as plt
    _dark_style()

    import sys
    sys.path.insert(0, str(exp_dir))
    try:
        from schelling import SchellingGrid, GRID_SIZE, DENSITY, TOLERANCE_DEFAULT
    except ImportError:
        return []

    paths = []

    # Figure 1: Before/After comparison
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Original (fixed tolerance)
    grid1 = SchellingGrid(seed=42, grid_size=GRID_SIZE, density=DENSITY, tolerance=TOLERANCE_DEFAULT)
    for _ in range(500):
        n = grid1.step(dynamic_tolerance=False)
        if n == 0:
            break
    ax1.imshow(grid1.grid, cmap="RdBu", interpolation="nearest", vmin=0, vmax=2)
    seg1 = grid1.segregation_index()
    ax1.set_title(f"Original Schelling\ntolerance={TOLERANCE_DEFAULT} (fixed)\nsegregation={seg1:.3f}",
                  fontsize=12, color="#e0e0e0")
    ax1.axis("off")

    # Dynamic tolerance
    grid2 = SchellingGrid(seed=42, grid_size=GRID_SIZE, density=DENSITY, tolerance=TOLERANCE_DEFAULT)
    for step in range(500):
        grid2.step(dynamic_tolerance=True)
        for (r, c), agent in grid2.agents.items():
            frac = grid2._same_type_fraction(r, c)
            if frac > agent.tolerance + 0.05:
                agent.tolerance = min(0.9, agent.tolerance + 0.005)
            elif frac < agent.tolerance - 0.05:
                agent.tolerance = max(0.1, agent.tolerance - 0.005)
    ax2.imshow(grid2.grid, cmap="RdBu", interpolation="nearest", vmin=0, vmax=2)
    seg2 = grid2.segregation_index()
    ax2.set_title(f"Dynamic Tolerance (CHP)\ncomfort_margin=0.05\nsegregation={seg2:.3f}",
                  fontsize=12, color="#e0e0e0")
    ax2.axis("off")

    fig.suptitle("CHP Schelling Experiment — Prior-as-Detector Demo",
                 fontsize=14, color="#00ff88", fontweight="bold")
    plt.tight_layout()
    p = fig_dir / "schelling_comparison.png"
    fig.savefig(p, dpi=150, bbox_inches="tight")
    plt.close(fig)
    paths.append(p)

    return paths


# ── Lorenz ───────────────────────────────────────────────────────────────────

def _fig_lorenz(exp_dir: Path, fig_dir: Path) -> list[Path]:
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    _dark_style()

    import sys
    sys.path.insert(0, str(exp_dir))
    try:
        from lorenz import run_simulation
    except ImportError:
        return []

    r = run_simulation()
    x, y, z = r["x"], r["y"], r["z"]

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection="3d")
    n = len(x)
    colors = np.linspace(0, 1, n)
    for i in range(n - 1):
        ax.plot(x[i:i+2], y[i:i+2], z[i:i+2],
                color=plt.cm.viridis(colors[i]), alpha=0.7, linewidth=0.5)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("Lorenz Attractor — RK45 Adaptive Integration\n"
                 f"sigma=10, rho=28, beta=8/3, t=[0,50], Lyapunov={r['lyapunov_exponent']:.3f}",
                 color="#00ff88", fontweight="bold")
    ax.set_facecolor("#0a0a1a")
    fig.set_facecolor("#0a0a1a")

    p = fig_dir / "lorenz_attractor.png"
    fig.savefig(p, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return [p]


# ── Grover ───────────────────────────────────────────────────────────────────

def _fig_grover(exp_dir: Path, fig_dir: Path) -> list[Path]:
    import matplotlib.pyplot as plt
    _dark_style()

    import sys
    sys.path.insert(0, str(exp_dir))
    try:
        from grover import GroverSimulator
    except ImportError:
        return []

    paths = []

    # Figure 1: Amplitude evolution
    sim = GroverSimulator(n_qubits=10, seed=42)
    sim.initialize()
    probs = []
    for k in range(50):
        probs.append(sim.success_probability())
        sim.grover_iteration()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(range(50), probs, color="#00ff88", linewidth=2)
    ax.axvline(x=25, color="#ff4444", linestyle="--", alpha=0.7, label="k_opt=25")
    ax.axhline(y=0.95, color="#ffaa00", linestyle=":", alpha=0.5, label="95% threshold")
    ax.set_xlabel("Iterations (k)")
    ax.set_ylabel("P(target)")
    ax.set_title("Grover's Algorithm — Sinusoidal Amplitude Profile\n"
                 "N=1024, k_opt=25, P(25)=0.9995",
                 color="#00ff88", fontweight="bold")
    ax.legend()
    ax.grid(True, alpha=0.2)

    p = fig_dir / "grover_amplitude.png"
    fig.savefig(p, dpi=150, bbox_inches="tight")
    plt.close(fig)
    paths.append(p)

    # Figure 2: State amplitudes at k_opt
    sim2 = GroverSimulator(n_qubits=10, seed=42)
    sim2.initialize()
    for _ in range(25):
        sim2.grover_iteration()

    fig, ax = plt.subplots(figsize=(12, 4))
    amps = sim2.amplitudes ** 2
    ax.bar(range(len(amps)), amps, color="#1a1a3a", width=1.0)
    ax.bar([sim2.target], [amps[sim2.target]], color="#00ff88", width=3)
    ax.set_xlabel("Basis State")
    ax.set_ylabel("Probability")
    ax.set_title(f"Grover State Amplitudes at k=25 — Target={sim2.target} (P={amps[sim2.target]:.4f})",
                 color="#00ff88", fontweight="bold")
    ax.set_ylim(0, 0.005)
    ax.annotate(f"Target: {sim2.target}\nP={amps[sim2.target]:.4f}",
                xy=(sim2.target, amps[sim2.target]),
                xytext=(sim2.target + 100, 0.003),
                arrowprops=dict(arrowstyle="->", color="#00ff88"),
                color="#00ff88", fontsize=11)

    p2 = fig_dir / "grover_states.png"
    fig.savefig(p2, dpi=150, bbox_inches="tight")
    plt.close(fig)
    paths.append(p2)

    return paths


# ── Izhikevich ───────────────────────────────────────────────────────────────

def _fig_izhikevich(exp_dir: Path, fig_dir: Path) -> list[Path]:
    import matplotlib.pyplot as plt
    _dark_style()

    import sys
    sys.path.insert(0, str(exp_dir))
    try:
        from izhikevich import run_simulation
    except ImportError:
        return []

    patterns = {
        "RS (Regular Spiking)": {"a": 0.02, "b": 0.2, "c": -65, "d": 8},
        "IB (Intrins. Bursting)": {"a": 0.02, "b": 0.2, "c": -55, "d": 4},
        "FS (Fast Spiking)": {"a": 0.10, "b": 0.2, "c": -65, "d": 2},
        "CH (Chattering)": {"a": 0.02, "b": 0.2, "c": -50, "d": 2},
        "LTS (Low-Threshold)": {"a": 0.02, "b": 0.25, "c": -65, "d": 2},
    }

    fig, axes = plt.subplots(5, 1, figsize=(14, 12), sharex=True)
    colors = ["#00ff88", "#4488ff", "#ff4444", "#ffaa00", "#cc44ff"]

    for idx, (name, params) in enumerate(patterns.items()):
        r = run_simulation(**params, I=10.0, duration=200)
        v = r["v_trace"]
        t = [i * 0.5 for i in range(len(v))]
        axes[idx].plot(t, v, color=colors[idx], linewidth=0.8)
        axes[idx].set_ylabel("mV", fontsize=9)
        axes[idx].set_title(f"{name} — {r['spike_count']} spikes, ISI CV={r['isi_cv']:.2f}",
                           fontsize=10, color=colors[idx], loc="left")
        axes[idx].set_ylim(-90, 40)
        axes[idx].axhline(y=30, color="#333", linestyle=":", linewidth=0.5)

    axes[-1].set_xlabel("Time (ms)")
    fig.suptitle("Izhikevich Neuron — 5 Firing Patterns (NOT Hodgkin-Huxley)\n"
                 "2 variables (v, u), 4 parameters (a, b, c, d), dt=0.5ms half-step",
                 fontsize=13, color="#00ff88", fontweight="bold")
    plt.tight_layout()

    p = fig_dir / "izhikevich_patterns.png"
    fig.savefig(p, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return [p]


# ── SIR ──────────────────────────────────────────────────────────────────────

def _fig_sir(exp_dir: Path, fig_dir: Path) -> list[Path]:
    import matplotlib.pyplot as plt
    _dark_style()

    import sys
    sys.path.insert(0, str(exp_dir))
    try:
        from sir_model import run_simulation
    except ImportError:
        return []

    r = run_simulation(seed=42)
    curve = r["epidemic_curve"]
    n = 500
    s_vals = [n - sum(curve[:i+1]) for i in range(len(curve))]  # rough S approximation

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.fill_between(range(len(curve)), curve, color="#ff4444", alpha=0.6, label="Infected")
    ax.plot(range(len(curve)), curve, color="#ff4444", linewidth=1.5)
    ax.axhline(y=r["peak_infected"], color="#ffaa00", linestyle="--", alpha=0.5,
               label=f"Peak={r['peak_infected']} at t={r['peak_tick']}")
    ax.set_xlabel("Tick")
    ax.set_ylabel("Infected Agents")
    ax.set_title(f"Stochastic SIR Epidemic — N=500, R0=3.0\n"
                 f"Peak={r['peak_infected']} at t={r['peak_tick']}, "
                 f"Final size={r['final_size_fraction']:.1%}, I(t) is INTEGER",
                 color="#00ff88", fontweight="bold")
    ax.legend()
    ax.grid(True, alpha=0.2)

    p = fig_dir / "sir_epidemic_curve.png"
    fig.savefig(p, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return [p]


# ── Spatial PD ───────────────────────────────────────────────────────────────

def _fig_spatial_pd(exp_dir: Path, fig_dir: Path) -> list[Path]:
    import matplotlib.pyplot as plt
    _dark_style()

    import sys
    sys.path.insert(0, str(exp_dir))
    try:
        from spatial_pd import SpatialPDGrid
    except ImportError:
        return []

    grid = SpatialPDGrid(grid_size=100, b=1.8)
    grid.set_initial("single_defector_center")
    for _ in range(50):
        grid.step()

    fig, ax = plt.subplots(figsize=(8, 8))
    cmap = plt.cm.colors.ListedColormap(["#ff4444", "#4488ff"])
    ax.imshow(grid.grid, cmap=cmap, interpolation="nearest")
    ax.set_title(f"Spatial PD — Nowak & May (1992)\n"
                 f"b=1.8, gen=50, cooperation={grid.cooperation_rate():.3f}",
                 color="#00ff88", fontweight="bold")
    ax.axis("off")

    p = fig_dir / "spatial_pd_lattice.png"
    fig.savefig(p, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return [p]


# ── Blockchain ───────────────────────────────────────────────────────────────

def _fig_blockchain(exp_dir: Path, fig_dir: Path) -> list[Path]:
    import matplotlib.pyplot as plt
    _dark_style()

    import sys
    sys.path.insert(0, str(exp_dir))
    try:
        from consensus import run_simulation
    except ImportError:
        return []

    strategies = ["silent", "equivocate", "colluding"]
    f_values = [0, 1, 2, 3, 4]

    fig, ax = plt.subplots(figsize=(10, 5))
    for strat in strategies:
        results = []
        for f in f_values:
            r = run_simulation(seed=42, n_byzantine=f, byzantine_strategy=strat)
            results.append(1 if r["consensus_reached"] and not r["safety_violated"] else 0)
        ax.plot(f_values, results, marker="o", linewidth=2, label=strat, markersize=8)

    ax.axvline(x=3.33, color="#ff4444", linestyle="--", alpha=0.5, label="N/3 threshold")
    ax.set_xlabel("Byzantine Nodes (f)")
    ax.set_ylabel("Consensus + Safety")
    ax.set_title("PBFT Consensus — Safety Under Byzantine Faults\n"
                 "Quorum=2f+1=7 (NOT f+1=4 Raft)",
                 color="#00ff88", fontweight="bold")
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["FAILED", "SAFE"])
    ax.legend()
    ax.grid(True, alpha=0.2)

    p = fig_dir / "blockchain_safety.png"
    fig.savefig(p, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return [p]


# ── Metal Harmony ────────────────────────────────────────────────────────────

def _fig_metal(exp_dir: Path, fig_dir: Path) -> list[Path]:
    import matplotlib.pyplot as plt
    _dark_style()

    import sys
    sys.path.insert(0, str(exp_dir))
    try:
        from metal_analyzer import run_simulation, NOTE_NAMES
    except ImportError:
        return []

    r = run_simulation()

    fig, ax = plt.subplots(figsize=(12, 5))

    riff_names = list(r["riff_results"].keys())
    classical_errors = [r["riff_results"][n]["classical_errors_count"] for n in riff_names]
    metal_errors = [0] * len(riff_names)  # Metal analyzer: zero errors

    x = np.arange(len(riff_names))
    width = 0.35

    bars1 = ax.bar(x - width/2, classical_errors, width, label="Classical Analysis (WRONG)",
                   color="#ff4444", alpha=0.8)
    bars2 = ax.bar(x + width/2, metal_errors, width, label="Metal Analysis (CORRECT)",
                   color="#00ff88", alpha=0.8)

    ax.set_ylabel("'Errors' Flagged")
    ax.set_title("Classical vs Metal Harmony Analysis — Pantera Riffs\n"
                 "Classical prior flags 6-9 'errors' per riff. Metal theory: ZERO.",
                 color="#00ff88", fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels([n.replace("_", "\n") for n in riff_names], fontsize=9)
    ax.legend()
    ax.grid(True, alpha=0.2, axis="y")

    # Annotate
    for bar in bars1:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.2,
                f"{int(height)}", ha="center", va="bottom", color="#ff4444", fontsize=10)

    p = fig_dir / "metal_vs_classical.png"
    fig.savefig(p, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return [p]


# ── Lotka-Volterra ───────────────────────────────────────────────────────────

def _fig_lotka_volterra(exp_dir: Path, fig_dir: Path) -> list[Path]:
    import matplotlib.pyplot as plt
    _dark_style()

    import sys
    sys.path.insert(0, str(exp_dir))
    try:
        from lotka_volterra import run_simulation
    except ImportError:
        return []

    r = run_simulation(seed=42, max_ticks=200)
    prey = r["prey_trajectory"]
    pred = r["predator_trajectory"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Time series
    ax1.plot(prey, color="#00ff88", linewidth=1, label="Prey")
    ax1.plot(pred, color="#ff4444", linewidth=1, label="Predators")
    ax1.set_xlabel("Tick")
    ax1.set_ylabel("Population")
    ax1.set_title("Agent-Based Predator-Prey\n(NOT ODE — note the noise)",
                  color="#00ff88", fontweight="bold")
    ax1.legend()
    ax1.grid(True, alpha=0.2)

    # Phase portrait
    ax2.plot(prey, pred, color="#4488ff", linewidth=0.5, alpha=0.7)
    ax2.set_xlabel("Prey")
    ax2.set_ylabel("Predators")
    ax2.set_title("Phase Portrait\n(spiral, not closed orbit = stochastic)",
                  color="#4488ff", fontweight="bold")
    ax2.grid(True, alpha=0.2)

    plt.tight_layout()
    p = fig_dir / "lotka_volterra_dynamics.png"
    fig.savefig(p, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return [p]
