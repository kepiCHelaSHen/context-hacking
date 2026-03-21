"""
CHP Live Dashboard — Scientific Control Panel
===============================================
Real-time monitoring of the Context Hacking Protocol loop.

Launch: chp dashboard  (or: streamlit run dashboard/app.py)

READ-ONLY: this dashboard never writes to any CHP file.
Safe to run alongside `chp run`.
"""

from __future__ import annotations

import re
import time
from pathlib import Path
from typing import Any

import streamlit as st

# ── Page config (must be first Streamlit call) ───────────────────────────────

st.set_page_config(
    page_title="CHP Dashboard",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Constants ────────────────────────────────────────────────────────────────

REFRESH_SECONDS = 5
CONFIG_PATH = Path("config.yaml")
STATE_VECTOR_PATH = Path("state_vector.md")
INNOVATION_LOG_PATH = Path("innovation_log.md")
DEAD_ENDS_PATH = Path("dead_ends.md")

EXPERIMENT_CATALOG = {
    "schelling-segregation":       {"domain": "Social Science",      "icon": "🏘️", "plot": "grid"},
    "spatial-prisoners-dilemma":    {"domain": "Game Theory",        "icon": "🎲", "plot": "lattice"},
    "lotka-volterra":              {"domain": "Ecology",            "icon": "🐺", "plot": "timeseries"},
    "sir-epidemic":                {"domain": "Epidemiology",       "icon": "🦠", "plot": "area"},
    "ml-hyperparam-search":        {"domain": "Machine Learning",   "icon": "🤖", "plot": "convergence"},
    "lorenz-attractor":            {"domain": "Chaos Theory",       "icon": "🦋", "plot": "attractor3d"},
    "quantum-grover":              {"domain": "Quantum Computing",  "icon": "⚛️", "plot": "bars"},
    "izhikevich-neurons":          {"domain": "Neuroscience",       "icon": "🧠", "plot": "raster"},
    "blockchain-consensus":        {"domain": "Distributed Systems","icon": "🔗", "plot": "network"},
}


# ── File readers (read-only, graceful fallback) ─────────────────────────────

def _read_file(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def _read_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    import yaml
    with open(path) as f:
        return yaml.safe_load(f) or {}


def _parse_state_vector(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in text.splitlines():
        if ":" in line and not line.startswith("#"):
            key, _, val = line.partition(":")
            result[key.strip()] = val.strip()
    return result


def _parse_dead_ends(text: str) -> list[str]:
    return re.findall(r"^## DEAD END \d+ — (.+)$", text, re.MULTILINE)


def _parse_innovation_entries(text: str, max_entries: int = 15) -> list[str]:
    entries = re.split(r"\n---\n", text)
    entries = [e.strip() for e in entries if e.strip() and "## Turn" in e]
    return entries[-max_entries:]


def _parse_critic_scores(text: str) -> dict[str, float]:
    scores: dict[str, float] = {}
    for gate_n in range(1, 5):
        m = re.search(rf"gate_{gate_n}[^:]*:\s*([0-9.]+)", text, re.IGNORECASE)
        if m:
            scores[f"Gate {gate_n}"] = float(m.group(1))
    return scores


def _detect_experiment(config: dict) -> str | None:
    name = config.get("project", {}).get("name", "")
    for exp_key in EXPERIMENT_CATALOG:
        if exp_key in name or name in exp_key:
            return exp_key
    return None


# ── Mode colors ──────────────────────────────────────────────────────────────

def _mode_color(mode: str) -> str:
    m = mode.upper()
    if "EXPLORATION" in m:
        return "#FFA500"  # amber
    if "EXIT" in m or "STOP" in m or "DONE" in m:
        return "#FF4444"  # red
    return "#00CC66"  # green (VALIDATION)


def _mode_badge(mode: str) -> str:
    color = _mode_color(mode)
    label = mode.split("—")[0].strip() if "—" in mode else mode
    return (
        f'<div style="background:{color};color:white;padding:12px 24px;'
        f'border-radius:8px;font-size:28px;font-weight:bold;text-align:center;'
        f'margin-bottom:12px;">{label}</div>'
    )


# ── Sigma gauge ──────────────────────────────────────────────────────────────

def _gauge_html(name: str, value: float | None, threshold: float, op: str) -> str:
    if value is None:
        return f'<div style="padding:8px;background:#333;border-radius:6px;margin:4px 0;color:#888;">{name}: no data</div>'

    if op in (">", ">="):
        passed = value >= threshold
    elif op in ("<", "<="):
        passed = value <= threshold
    else:
        passed = abs(value - threshold) < 1e-6

    color = "#00CC66" if passed else "#FF4444"
    icon = "✓" if passed else "✗"
    return (
        f'<div style="padding:8px 12px;background:#1a1a2e;border-left:4px solid {color};'
        f'border-radius:4px;margin:4px 0;font-family:monospace;">'
        f'<span style="color:{color};font-weight:bold;">{icon}</span> '
        f'{name}: <b>{value:.4f}</b> '
        f'<span style="color:#888;">({op} {threshold})</span></div>'
    )


# ── Main dashboard ───────────────────────────────────────────────────────────

def main() -> None:
    config = _read_yaml(CONFIG_PATH)
    sv_text = _read_file(STATE_VECTOR_PATH)
    sv = _parse_state_vector(sv_text)
    log_text = _read_file(INNOVATION_LOG_PATH)
    dead_text = _read_file(DEAD_ENDS_PATH)

    project_name = config.get("project", {}).get("name", "CHP Project")
    experiment = _detect_experiment(config)

    # ── Header ───────────────────────────────────────────────────────────
    st.title(f"🔬 CHP Dashboard — {project_name}")

    mode = sv.get("MODE", "VALIDATION")
    turn = sv.get("TURN", "0")
    milestone = sv.get("MILESTONE", "—")

    col_mode, col_turn, col_milestone = st.columns([2, 1, 2])
    with col_mode:
        st.markdown(_mode_badge(mode), unsafe_allow_html=True)
    with col_turn:
        st.metric("Turn", turn)
    with col_milestone:
        st.markdown(f"**Milestone:** {milestone}")

    # ── Main layout: left (metrics + critic) | right (log + dead ends) ───
    left, right = st.columns([1, 1])

    # ── LEFT: Sigma Gauges + Critic ──────────────────────────────────────
    with left:
        st.subheader("σ-Gate Status")
        gates_cfg = config.get("gates", {})
        checks = gates_cfg.get("anomaly_checks", [])

        if checks:
            gauge_html = ""
            for check in checks:
                metric_name = check.get("metric", "unknown")
                op = check.get("operator", ">")
                threshold = check.get("threshold", 0)
                desc = check.get("description", "")
                # Try to read value from state vector (metric_status field)
                metric_status = sv.get("METRIC_STATUS", "")
                # For now, show the gate definition; live values come from experiment output
                gauge_html += _gauge_html(
                    f"{metric_name} — {desc}", None, threshold, op
                )
            st.markdown(gauge_html, unsafe_allow_html=True)
        else:
            st.info("No anomaly checks defined in config.yaml")

        # ── Critic Scorecard ─────────────────────────────────────────────
        st.subheader("Critic Scorecard")
        critic_scores = _parse_critic_scores(log_text)
        if critic_scores:
            critic_cfg = config.get("critic", {})
            gate_thresholds = {g["name"]: g["threshold"]
                               for g in critic_cfg.get("gates", [])}
            for gate_name, score in critic_scores.items():
                gate_num = gate_name.split()[-1]
                threshold_map = {"1": 1.0, "2": 0.85, "3": 0.85, "4": 0.85}
                threshold = threshold_map.get(gate_num, 0.85)
                passed = score >= threshold
                color = "#00CC66" if passed else "#FF4444"
                st.markdown(
                    f'<span style="color:{color};font-size:18px;">{"●" if passed else "○"}</span> '
                    f'**{gate_name}**: {score:.2f} / {threshold}',
                    unsafe_allow_html=True,
                )
        else:
            st.caption("No critic review found in innovation log yet.")

        # ── Council Status ───────────────────────────────────────────────
        st.subheader("Council Votes")
        if "DRIFT" in log_text.upper()[-3000:]:
            st.warning("⚠️ DRIFT flagged in recent council review")
        else:
            st.success("No drift detected")

        # ── Open Flags ───────────────────────────────────────────────────
        flags = sv.get("OPEN_FLAGS", "none")
        if flags and flags.lower() != "none":
            st.error(f"⚠️ Open flags: {flags}")

    # ── RIGHT: Innovation Log + Dead Ends ────────────────────────────────
    with right:
        st.subheader("Innovation Log (last 15)")
        entries = _parse_innovation_entries(log_text)
        if entries:
            for entry in reversed(entries):
                # Extract turn number for styling
                turn_match = re.match(r"## Turn (\d+)", entry)
                turn_label = f"Turn {turn_match.group(1)}" if turn_match else "Turn ?"
                with st.expander(turn_label, expanded=False):
                    st.markdown(entry[:1000])  # truncate for performance
        else:
            st.caption("No turns recorded yet. Run `chp run` to start.")

        st.subheader("Dead Ends")
        dead_ends = _parse_dead_ends(dead_text)
        if dead_ends:
            for de in dead_ends:
                st.markdown(f"🚫 **{de}**")
        else:
            st.caption("No dead ends logged yet.")

    # ── Experiment Gallery ────────────────────────────────────────────────
    st.divider()
    st.subheader("Experiment Gallery")

    cols = st.columns(3)
    for idx, (exp_key, meta) in enumerate(EXPERIMENT_CATALOG.items()):
        with cols[idx % 3]:
            is_active = (exp_key == experiment)
            border = "2px solid #00CC66" if is_active else "1px solid #333"
            badge = " ✅ ACTIVE" if is_active else ""
            st.markdown(
                f'<div style="border:{border};border-radius:8px;padding:12px;'
                f'margin:6px 0;background:#1a1a2e;">'
                f'<span style="font-size:24px;">{meta["icon"]}</span> '
                f'<b>{exp_key}</b>{badge}<br/>'
                f'<span style="color:#888;font-size:13px;">{meta["domain"]}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # ── Experiment-specific plot area ─────────────────────────────────────
    if experiment:
        st.divider()
        st.subheader(f"Live Plot — {experiment}")
        plot_type = EXPERIMENT_CATALOG.get(experiment, {}).get("plot", "none")
        _render_experiment_plot(experiment, plot_type)

    # ── Export button ─────────────────────────────────────────────────────
    st.divider()
    col_export, col_refresh = st.columns([1, 3])
    with col_export:
        if st.button("📄 Export Paper Appendix", use_container_width=True):
            _export_appendix(config, log_text, dead_text, sv)
            st.success("Exported to paper_appendix.md")
    with col_refresh:
        st.caption(f"Auto-refreshes every {REFRESH_SECONDS}s. Last update: {time.strftime('%H:%M:%S')}")

    # ── Auto-refresh ─────────────────────────────────────────────────────
    time.sleep(REFRESH_SECONDS)
    st.rerun()


# ── Experiment-specific plots ────────────────────────────────────────────────

def _render_experiment_plot(experiment: str, plot_type: str) -> None:
    """Render a domain-appropriate plot for the active experiment.

    Reads from experiment output files if they exist. Shows placeholder
    instructions otherwise.
    """
    import plotly.graph_objects as go

    # Look for output CSVs in common locations
    csv_candidates = list(Path(".").glob("*.csv")) + list(Path("outputs").glob("*.csv"))

    if plot_type == "grid":
        _plot_schelling(csv_candidates)
    elif plot_type == "lattice":
        _plot_spatial_pd()
    elif plot_type == "timeseries":
        _plot_lotka_volterra(csv_candidates)
    elif plot_type == "area":
        _plot_sir(csv_candidates)
    elif plot_type == "convergence":
        _plot_ml_convergence(csv_candidates)
    elif plot_type == "attractor3d":
        _plot_lorenz()
    elif plot_type == "bars":
        _plot_grover()
    elif plot_type == "raster":
        _plot_izhikevich()
    elif plot_type == "network":
        _plot_blockchain()
    else:
        st.info(f"No live plot configured for plot type: {plot_type}")


def _plot_schelling(csvs: list[Path]) -> None:
    import plotly.graph_objects as go
    st.markdown("**Segregation Grid** — agent types shown as colored cells, "
                "segregation index gauge below.")
    # Look for a grid state file
    grid_file = _find_csv(csvs, "grid", "schelling")
    if grid_file:
        import pandas as pd
        df = pd.read_csv(grid_file)
        st.dataframe(df.tail(5))
    else:
        fig = go.Figure(data=go.Heatmap(
            z=[[0.5] * 10 for _ in range(10)],
            colorscale="RdBu", showscale=False,
        ))
        fig.update_layout(title="Waiting for simulation data...",
                          height=300, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)


def _plot_spatial_pd() -> None:
    import plotly.graph_objects as go
    st.markdown("**Cooperator/Defector Lattice** — blue = cooperate, red = defect.")
    fig = go.Figure(data=go.Heatmap(
        z=[[1, 0, 1, 1, 0], [0, 1, 1, 0, 1], [1, 1, 0, 1, 1],
           [0, 1, 1, 1, 0], [1, 0, 1, 0, 1]],
        colorscale=[[0, "red"], [1, "blue"]], showscale=False,
    ))
    fig.update_layout(title="Waiting for simulation data...",
                      height=300, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)


def _plot_lotka_volterra(csvs: list[Path]) -> None:
    import plotly.graph_objects as go
    st.markdown("**Prey vs Predator** — population time series + phase portrait.")
    csv = _find_csv(csvs, "lotka", "prey", "predator")
    if csv:
        import pandas as pd
        df = pd.read_csv(csv)
        fig = go.Figure()
        if "prey_count" in df.columns:
            fig.add_trace(go.Scatter(y=df["prey_count"], name="Prey", line=dict(color="green")))
        if "predator_count" in df.columns:
            fig.add_trace(go.Scatter(y=df["predator_count"], name="Predator", line=dict(color="red")))
        fig.update_layout(title="Population Dynamics", height=350,
                          xaxis_title="Tick", yaxis_title="Count")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Run the Lotka-Volterra experiment to see live population curves.")


def _plot_sir(csvs: list[Path]) -> None:
    import plotly.graph_objects as go
    st.markdown("**SIR Epidemic Curve** — S (blue), I (red), R (green) stacked area.")
    csv = _find_csv(csvs, "sir", "epidemic")
    if csv:
        import pandas as pd
        df = pd.read_csv(csv)
        fig = go.Figure()
        for col, color in [("S", "blue"), ("I", "red"), ("R", "green")]:
            if col in df.columns:
                fig.add_trace(go.Scatter(y=df[col], name=col, fill="tonexty",
                                         line=dict(color=color)))
        fig.update_layout(title="Epidemic Curve", height=350)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Run the SIR experiment to see the epidemic curve.")


def _plot_ml_convergence(csvs: list[Path]) -> None:
    import plotly.graph_objects as go
    st.markdown("**Best-so-far Validation Accuracy** — convergence curve of Bayesian optimization.")
    csv = _find_csv(csvs, "hyperparam", "convergence", "accuracy")
    if csv:
        import pandas as pd
        df = pd.read_csv(csv)
        if "best_val_accuracy" in df.columns:
            fig = go.Figure(data=go.Scatter(
                y=df["best_val_accuracy"], mode="lines+markers",
                line=dict(color="#00CC66"),
            ))
            fig.update_layout(title="BO Convergence", height=350,
                              xaxis_title="Evaluation", yaxis_title="Best Val Accuracy")
            st.plotly_chart(fig, use_container_width=True)
            return
    st.info("Run the ML Hyperparameter experiment to see the convergence curve.")


def _plot_lorenz() -> None:
    import plotly.graph_objects as go
    st.markdown("**Lorenz Attractor** — 3D butterfly (rotatable).")
    # Check for trajectory output
    traj_file = Path("trajectory.csv")
    if traj_file.exists():
        import pandas as pd
        df = pd.read_csv(traj_file)
        if all(c in df.columns for c in ["x", "y", "z"]):
            fig = go.Figure(data=go.Scatter3d(
                x=df["x"], y=df["y"], z=df["z"],
                mode="lines", line=dict(color=df.index, colorscale="Viridis", width=1.5),
            ))
            fig.update_layout(title="Lorenz Attractor", height=500,
                              scene=dict(xaxis_title="x", yaxis_title="y", zaxis_title="z"))
            st.plotly_chart(fig, use_container_width=True)
            return
    st.info("Run the Lorenz experiment to see the 3D butterfly attractor.")


def _plot_grover() -> None:
    import plotly.graph_objects as go
    st.markdown("**Grover Amplitudes** — probability per basis state after k iterations.")
    st.info("Run the Grover experiment to see amplitude bar charts.")


def _plot_izhikevich() -> None:
    import plotly.graph_objects as go
    st.markdown("**Membrane Voltage** — spike raster plot for each firing pattern.")
    st.info("Run the Izhikevich experiment to see voltage traces.")


def _plot_blockchain() -> None:
    import plotly.graph_objects as go
    st.markdown("**Consensus Network** — node communication graph with safety/liveness indicators.")
    st.info("Run the Blockchain experiment to see the consensus network.")


def _find_csv(candidates: list[Path], *keywords: str) -> Path | None:
    """Find a CSV whose name contains any of the keywords."""
    for csv in candidates:
        name_lower = csv.name.lower()
        if any(kw in name_lower for kw in keywords):
            return csv
    return None


# ── Export ───────────────────────────────────────────────────────────────────

def _export_appendix(
    config: dict, log_text: str, dead_text: str, sv: dict[str, str]
) -> None:
    sections = [
        "# CHP Paper Appendix — Automated Build Log\n",
        f"Project: {config.get('project', {}).get('name', 'unknown')}\n",
        f"Generated: {time.strftime('%Y-%m-%d %H:%M')}\n",
        "\n## Final State Vector\n",
    ]
    for k, v in sv.items():
        sections.append(f"- **{k}**: {v}")

    sections.append("\n\n## Full Innovation Log\n")
    sections.append(log_text)

    sections.append("\n\n## Dead Ends\n")
    sections.append(dead_text)

    Path("paper_appendix.md").write_text("\n".join(sections), encoding="utf-8")


# ── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    main()
