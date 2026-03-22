"""
Regenerate Lorenz attractor figure with GPT-suggested improvements:
  1. Paper-style annotation (Greek letters, separate lines)
  2. Highlighted start point
  3. Reduced grid opacity so attractor pops
  4. 3-panel figure: Wrong (Euler) → Detected (divergence) → Corrected (RK45)
"""

from __future__ import annotations
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from scipy.integrate import solve_ivp

FIGURES_DIR = Path(__file__).parent / "figures"
FIGURES_DIR.mkdir(exist_ok=True)

SIGMA, RHO, BETA = 10.0, 28.0, 8.0 / 3.0
X0, Y0, Z0 = 1.0, 1.0, 1.0
T_END, N = 50.0, 10000

# ── Solve with RK45 ──────────────────────────────────────────────────────────

def lorenz_deriv(t, s):
    x, y, z = s
    return [SIGMA*(y-x), x*(RHO-z)-y, x*y - BETA*z]

t_eval = np.linspace(0, T_END, N)
sol = solve_ivp(lorenz_deriv, [0, T_END], [X0, Y0, Z0],
                method="RK45", t_eval=t_eval, rtol=1e-9, atol=1e-9)
x, y, z = sol.y

# Lyapunov (simplified)
eps = 1e-7
sol2 = solve_ivp(lorenz_deriv, [0, T_END], [X0, Y0, Z0+eps],
                 method="RK45", t_eval=t_eval, rtol=1e-9, atol=1e-9)
div = np.abs(x - sol2.y[0])
div = np.where(div > 0, div, 1e-20)
lyap = float(np.mean(np.log(div/eps)[N//2:])) / T_END

# ── Euler (wrong) ────────────────────────────────────────────────────────────

def euler_lorenz(dt=0.01):
    xs, ys, zs = [X0], [Y0], [Z0]
    cx, cy, cz = X0, Y0, Z0
    steps = int(T_END / dt)
    for _ in range(steps):
        dx, dy, dz = lorenz_deriv(0, [cx, cy, cz])
        cx += dx * dt
        cy += dy * dt
        cz += dz * dt
        xs.append(cx)
        ys.append(cy)
        zs.append(cz)
    return np.array(xs), np.array(ys), np.array(zs)

ex, ey, ez = euler_lorenz(dt=0.01)

# ── Figure 1: Improved single attractor ──────────────────────────────────────

fig = plt.figure(figsize=(12, 9), facecolor="#0a0a14")
ax  = fig.add_subplot(111, projection="3d")
ax.set_facecolor("#0a0a14")

# Color by time
t_norm = np.linspace(0, 1, N)
from matplotlib.colors import LinearSegmentedColormap
cmap = LinearSegmentedColormap.from_list("lorenz", ["#6B21A8","#06B6D4","#84CC16","#FBBF24"])
colors = cmap(t_norm)

# Draw trajectory in segments for color
seg = 200
for i in range(0, N-seg, seg):
    c = colors[i + seg//2]
    ax.plot(x[i:i+seg+1], y[i:i+seg+1], z[i:i+seg+1],
            color=c, linewidth=0.6, alpha=0.85)

# Start point — bright white dot
ax.scatter([x[0]], [y[0]], [z[0]], color="white", s=60, zorder=5,
           label="t=0", depthshade=False)
ax.scatter([x[0]], [y[0]], [z[0]], color="white", s=200, zorder=4,
           alpha=0.25, depthshade=False)

# Grid: very subtle
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
ax.xaxis.pane.set_edgecolor("#1a1a2e")
ax.yaxis.pane.set_edgecolor("#1a1a2e")
ax.zaxis.pane.set_edgecolor("#1a1a2e")
ax.grid(True, color="#1a1a2e", linewidth=0.4, alpha=0.4)   # reduced opacity
ax.xaxis._axinfo["grid"]["linewidth"] = 0.3
ax.yaxis._axinfo["grid"]["linewidth"] = 0.3
ax.zaxis._axinfo["grid"]["linewidth"] = 0.3

# Tick labels minimal
for axis in [ax.xaxis, ax.yaxis, ax.zaxis]:
    axis.label.set_color("#4a5568")
    [t.set_color("#4a5568") for t in axis.get_ticklabels()]

# Paper-style annotation (top-left, 3 lines)
fig.text(0.13, 0.93,
         r"Lorenz ($\sigma=10,\ \rho=28,\ \beta=\frac{8}{3}$)",
         color="#e2e8f0", fontsize=13, fontweight="bold",
         fontfamily="DejaVu Serif")
fig.text(0.13, 0.89,
         rf"Lyapunov $\lambda \approx {lyap:.3f}$",
         color="#94a3b8", fontsize=11, fontfamily="DejaVu Serif")
fig.text(0.13, 0.86,
         "Integrator: RK45 (adaptive,  $\\varepsilon$=1e-9)",
         color="#64748b", fontsize=10, fontfamily="DejaVu Serif")

# White dot legend
ax.legend(handles=[
    plt.Line2D([0],[0], marker="o", color="w", markerfacecolor="white",
               markersize=6, label="Start  t=0", linestyle="None")
], loc="upper right", framealpha=0, labelcolor="white", fontsize=9)

ax.view_init(elev=22, azim=-55)
plt.tight_layout(rect=[0, 0, 1, 0.85])
out = FIGURES_DIR / "lorenz_attractor.png"
plt.savefig(out, dpi=150, bbox_inches="tight",
            facecolor=fig.get_facecolor())
plt.close()
print(f"Saved: {out}")

# ── Figure 2: 3-panel Wrong → Detected → Corrected ───────────────────────────

fig2 = plt.figure(figsize=(18, 6), facecolor="#0a0a14")
gs   = gridspec.GridSpec(1, 3, figure=fig2, wspace=0.05)

panel_cfg = [
    ("Wrong",     "Euler (dt=0.01)",      "#EF4444",
     ex, ey, ez,  "LLM prior: fixed-step Euler\nDiverges from true attractor"),
    ("Detected",  "Critic flags divergence", "#F59E0B",
     None, None, None,  "Gate 3 FAIL: trajectory diverges\nfrom RK45 reference at t≈15"),
    ("Corrected", "RK45 Adaptive",         "#10B981",
     x, y, z,    "CHP fix: scipy RK45, rtol=1e-9\nLyapunov λ≈{:.3f}".format(lyap)),
]

for col, (title, subtitle, color, px, py, pz, note) in enumerate(panel_cfg):
    ax = fig2.add_subplot(gs[col], projection="3d")
    ax.set_facecolor("#0a0a14")

    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor("#111827")
    ax.yaxis.pane.set_edgecolor("#111827")
    ax.zaxis.pane.set_edgecolor("#111827")
    ax.grid(True, color="#111827", linewidth=0.3, alpha=0.3)
    for axis in [ax.xaxis, ax.yaxis, ax.zaxis]:
        [t.set_color("#374151") for t in axis.get_ticklabels()]
        axis.label.set_color("#374151")

    if col == 0:
        # Euler — show it going wrong: first half plausible, second half diverging
        split = len(ex) // 3
        ax.plot(ex[:split], ey[:split], ez[:split],
                color="#F87171", linewidth=0.5, alpha=0.7)
        ax.plot(ex[split:], ey[split:], ez[split:],
                color="#991B1B", linewidth=0.5, alpha=0.4)
        # Overlay ghost of correct attractor
        ax.plot(x[::3], y[::3], z[::3],
                color="#374151", linewidth=0.3, alpha=0.3, linestyle="--")
        ax.text2D(0.5, 0.02, "✗  Euler diverges", transform=ax.transAxes,
                  ha="center", color="#EF4444", fontsize=8)

    elif col == 1:
        # Detected panel: show divergence chart instead of attractor
        # Use 2D inset showing |x_euler - x_rk45| over time
        ax.set_visible(False)
        ax2d = fig2.add_subplot(gs[col])
        ax2d.set_facecolor("#0a0a14")
        t_short = t_eval[:min(len(ex)-1, N)]
        ex_short = ex[1:len(t_short)+1]
        diff = np.abs(ex_short - x[:len(t_short)])
        ax2d.semilogy(t_short, diff + 1e-10,
                      color="#F59E0B", linewidth=1.2)
        ax2d.axvline(x=15, color="#EF4444", linewidth=1, linestyle="--", alpha=0.8)
        ax2d.text(15.5, diff.max()*0.3, "Critic flag", color="#EF4444",
                  fontsize=8, va="top")
        ax2d.set_xlabel("t", color="#6B7280", fontsize=9)
        ax2d.set_ylabel("|x_euler − x_rk45|", color="#6B7280", fontsize=9)
        ax2d.tick_params(colors="#4B5563")
        ax2d.spines["bottom"].set_color("#1F2937")
        ax2d.spines["left"].set_color("#1F2937")
        ax2d.spines["top"].set_visible(False)
        ax2d.spines["right"].set_visible(False)
        ax2d.set_facecolor("#0a0a14")
        ax2d.yaxis.label.set_color("#6B7280")
        ax2d.xaxis.label.set_color("#6B7280")
        for spine in ax2d.spines.values():
            spine.set_color("#1F2937")
        ax2d.text(0.5, 1.04, "Detected",
                  transform=ax2d.transAxes, ha="center",
                  color="#F59E0B", fontsize=12, fontweight="bold")
        ax2d.text(0.5, 0.98, "Critic flags divergence",
                  transform=ax2d.transAxes, ha="center",
                  color="#92400E", fontsize=9)
        ax2d.text(0.5, 0.03, "Gate 3 FAIL → Exploration mode",
                  transform=ax2d.transAxes, ha="center",
                  color="#F59E0B", fontsize=8)
        continue

    elif col == 2:
        # Corrected RK45
        for i in range(0, N-seg, seg):
            c = cmap(t_norm[i + seg//2])
            ax.plot(x[i:i+seg+1], y[i:i+seg+1], z[i:i+seg+1],
                    color=c, linewidth=0.6, alpha=0.9)
        ax.scatter([x[0]], [y[0]], [z[0]], color="white", s=40,
                   zorder=5, depthshade=False)
        ax.text2D(0.5, 0.02, "✓  RK45 converged", transform=ax.transAxes,
                  ha="center", color="#10B981", fontsize=8)

    ax.view_init(elev=22, azim=-55)

    # Panel title
    ax.set_title(f"{title}\n{subtitle}",
                 color=color, fontsize=11, fontweight="bold", pad=10)
    ax.text2D(0.5, -0.04, note, transform=ax.transAxes,
              ha="center", color="#6B7280", fontsize=8, va="top")

# Super title
fig2.suptitle(
    "CHP Prior-as-Detector: Lorenz Attractor  ·  Wrong → Detected → Corrected",
    color="#E2E8F0", fontsize=13, fontweight="bold", y=1.01,
    fontfamily="DejaVu Serif",
)

out2 = FIGURES_DIR / "lorenz_chp_story.png"
fig2.savefig(out2, dpi=150, bbox_inches="tight",
             facecolor=fig2.get_facecolor())
plt.close()
print(f"Saved: {out2}")
print("Done.")
