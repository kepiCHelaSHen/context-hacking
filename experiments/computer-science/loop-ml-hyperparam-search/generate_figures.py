"""Generate publication-quality figures for ML Hyperparameter Search experiment."""

from __future__ import annotations

import sys
import os

# Ensure we can import the experiment module
sys.path.insert(0, os.path.dirname(__file__))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from hyperparam_search import run_simulation


def main() -> None:
    out_dir = os.path.join(os.path.dirname(__file__), "figures")
    os.makedirs(out_dir, exist_ok=True)

    # Run BO search
    result = run_simulation(seed=42, method="bayesian", budget=50)
    convergence = result["convergence_curve"]
    points = result["evaluated_points"]
    # Reconstruct per-iteration val accuracies from convergence curve
    # convergence[i] = max(val_accs[:i+1]), so val_accs[i] = convergence[i] if convergence[i] > convergence[i-1] else something <= convergence[i]
    # But we need the raw val_accs for scatter color; re-derive from the result data.
    # The simplest approach: re-run and capture val_accs directly.
    # Actually, let's just re-import and re-run to get val_accs.
    from hyperparam_search import BayesianOptPipeline, BO_INIT_RANDOM
    pipe = BayesianOptPipeline(seed=42)

    val_accs = []
    for p in points:
        va, _ = pipe.evaluate(p)
        val_accs.append(va)

    # ---- Figure 1: Convergence curve ----
    fig1, ax1 = plt.subplots(figsize=(8, 5), facecolor="white")
    iterations = np.arange(1, len(convergence) + 1)
    ax1.plot(iterations, convergence, color="#1f77b4", linewidth=1.8, label="Best val accuracy")
    ax1.axhline(y=0.98, color="red", linestyle="--", linewidth=1.2, label="Leakage threshold (0.98)")
    ax1.axvline(x=BO_INIT_RANDOM, color="gray", linestyle=":", linewidth=1.0, alpha=0.7,
                label=f"Random -> GP transition (iter {BO_INIT_RANDOM})")
    ax1.set_xlabel("BO Iteration", fontsize=11)
    ax1.set_ylabel("Validation Accuracy", fontsize=11)
    ax1.set_title("Bayesian Optimization Convergence", fontsize=13, fontweight="bold")
    ax1.legend(frameon=True, fontsize=9, loc="lower right")
    ax1.set_xlim(1, len(convergence))
    ax1.grid(True, alpha=0.3)
    fig1.tight_layout()

    path1 = os.path.join(out_dir, "convergence.png")
    fig1.savefig(path1, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig1)

    size1 = os.path.getsize(path1) / 1024
    print(f"Saved: {path1}  ({size1:.1f} KB)")
    assert size1 > 10, f"File too small: {size1:.1f} KB"

    # ---- Figure 2: Search space scatter ----
    # Extract hyperparameter values for the scatter
    lrs = [p["lr"] for p in points]
    alphas = [p["alpha"] for p in points]
    layer1s = [p["layer_1"] for p in points]

    fig2, axes = plt.subplots(1, 2, figsize=(13, 5), facecolor="white")

    # Left: lr vs alpha, color = val accuracy
    sc1 = axes[0].scatter(lrs, alphas, c=val_accs, cmap="viridis", s=50, alpha=0.85,
                          edgecolors="k", linewidths=0.3)
    axes[0].set_xscale("log")
    axes[0].set_yscale("log")
    axes[0].set_xlabel("Learning Rate", fontsize=11)
    axes[0].set_ylabel("L2 Regularization (alpha)", fontsize=11)
    axes[0].set_title("LR vs Alpha", fontsize=12)
    axes[0].grid(True, alpha=0.3, which="both")
    cb1 = fig2.colorbar(sc1, ax=axes[0], shrink=0.85)
    cb1.set_label("Val Accuracy", fontsize=10)

    # Right: layer_1 vs lr, color = val accuracy
    sc2 = axes[1].scatter(layer1s, lrs, c=val_accs, cmap="viridis", s=50, alpha=0.85,
                          edgecolors="k", linewidths=0.3)
    axes[1].set_yscale("log")
    axes[1].set_xlabel("Hidden Layer 1 Size", fontsize=11)
    axes[1].set_ylabel("Learning Rate", fontsize=11)
    axes[1].set_title("Layer Size vs LR", fontsize=12)
    axes[1].grid(True, alpha=0.3, which="both")
    cb2 = fig2.colorbar(sc2, ax=axes[1], shrink=0.85)
    cb2.set_label("Val Accuracy", fontsize=10)

    fig2.suptitle("Bayesian Optimization Search Space (non-regular sampling)",
                  fontsize=13, fontweight="bold", y=1.02)
    fig2.tight_layout()

    path2 = os.path.join(out_dir, "search_space.png")
    fig2.savefig(path2, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig2)

    size2 = os.path.getsize(path2) / 1024
    print(f"Saved: {path2}  ({size2:.1f} KB)")
    assert size2 > 10, f"File too small: {size2:.1f} KB"

    print("OK — all figures generated.")


if __name__ == "__main__":
    main()
