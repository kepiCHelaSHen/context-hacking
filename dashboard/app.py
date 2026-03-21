"""
CHP Live Dashboard — Scientific Control Panel
===============================================
Real-time monitoring of the Context Hacking Protocol loop.

Launch: chp dashboard  (or: streamlit run dashboard/app.py)

READ-ONLY: this dashboard never writes to any CHP file.
Safe to run alongside `chp run`.
"""

from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Any

import streamlit as st

# ── Page config ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="CHP Scientific Dashboard",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS for scientific look ───────────────────────────────────────────

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;600;700&display=swap');

    .main { background-color: #0a0a1a; }
    .stApp { background-color: #0a0a1a; }

    h1, h2, h3 { font-family: 'Inter', sans-serif; color: #e0e0e0; }
    p, li, td, th { font-family: 'Inter', sans-serif; }

    .metric-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 1px solid #2a2a4a;
        border-radius: 12px;
        padding: 20px;
        margin: 8px 0;
    }
    .metric-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 32px;
        font-weight: 700;
        color: #00ff88;
    }
    .metric-label {
        font-size: 13px;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .mode-badge {
        padding: 16px 32px;
        border-radius: 12px;
        font-size: 24px;
        font-weight: 700;
        text-align: center;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 2px;
    }
    .gate-row {
        padding: 10px 16px;
        margin: 4px 0;
        border-radius: 6px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 14px;
        background: #12122a;
    }
    .gate-pass { border-left: 4px solid #00ff88; }
    .gate-fail { border-left: 4px solid #ff4444; }
    .gate-warn { border-left: 4px solid #ffaa00; }
    .sigma-gauge {
        padding: 8px 14px;
        margin: 3px 0;
        border-radius: 6px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 13px;
        background: #0d0d20;
    }
    .dead-end-card {
        background: #1a0a0a;
        border: 1px solid #441111;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 6px 0;
        color: #ff6666;
    }
    .log-entry {
        background: #0d0d20;
        border: 1px solid #1a1a3a;
        border-radius: 8px;
        padding: 14px;
        margin: 8px 0;
        font-size: 13px;
    }
    .experiment-card {
        border: 1px solid #2a2a4a;
        border-radius: 10px;
        padding: 14px;
        margin: 6px 0;
        background: #12122a;
        transition: border-color 0.3s;
    }
    .experiment-card-active {
        border: 2px solid #00ff88;
        background: #0a1a0a;
    }
    .report-section {
        background: #0d0d20;
        border: 1px solid #1a1a3a;
        border-radius: 12px;
        padding: 24px;
        margin: 12px 0;
        font-size: 14px;
        line-height: 1.7;
    }
    .section-divider {
        border-top: 1px solid #2a2a4a;
        margin: 24px 0;
    }
    div[data-testid="stMetricValue"] { font-family: 'JetBrains Mono', monospace; }
    .health-gauge {
        padding: 10px 16px;
        margin: 6px 0;
        border-radius: 8px;
        font-family: 'JetBrains Mono', monospace;
        position: relative;
        overflow: hidden;
    }
    .health-gauge .bar {
        position: absolute;
        top: 0; left: 0; bottom: 0;
        border-radius: 8px;
        opacity: 0.15;
    }
    .health-gauge .content {
        position: relative;
        z-index: 1;
    }
</style>
""", unsafe_allow_html=True)

# ── Constants ────────────────────────────────────────────────────────────────

REFRESH_SECONDS = 5
CONFIG_PATH = Path("config.yaml")
STATE_VECTOR_PATH = Path("state_vector.md")
INNOVATION_LOG_PATH = Path("innovation_log.md")
DEAD_ENDS_PATH = Path("dead_ends.md")

EXPERIMENT_CATALOG = {
    "schelling-segregation":       {"domain": "Social Science",      "icon": "🏘️", "plot": "grid"},
    "spatial-prisoners-dilemma":    {"domain": "Game Theory",         "icon": "🎲", "plot": "lattice"},
    "lotka-volterra":              {"domain": "Ecology",             "icon": "🐺", "plot": "timeseries"},
    "sir-epidemic":                {"domain": "Epidemiology",        "icon": "🦠", "plot": "area"},
    "ml-hyperparam-search":        {"domain": "Machine Learning",    "icon": "🤖", "plot": "convergence"},
    "lorenz-attractor":            {"domain": "Chaos Theory",        "icon": "🦋", "plot": "attractor3d"},
    "quantum-grover":              {"domain": "Quantum Computing",   "icon": "⚛️",  "plot": "bars"},
    "izhikevich-neurons":          {"domain": "Neuroscience",        "icon": "🧠", "plot": "raster"},
    "blockchain-consensus":        {"domain": "Distributed Systems", "icon": "🔗", "plot": "network"},
}


# ── File readers ─────────────────────────────────────────────────────────────

def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""

def _yaml(path: Path) -> dict[str, Any]:
    if not path.exists(): return {}
    import yaml
    with open(path) as f: return yaml.safe_load(f) or {}

def _sv(text: str) -> dict[str, str]:
    r: dict[str, str] = {}
    for line in text.splitlines():
        if ":" in line and not line.startswith("#"):
            k, _, v = line.partition(":")
            r[k.strip()] = v.strip()
    return r

def _dead_ends(text: str) -> list[dict[str, str]]:
    entries = []
    blocks = re.split(r"\n## DEAD END", text)
    for b in blocks[1:]:
        title_m = re.match(r"\s*\d+\s*[—–-]\s*(.+)", b)
        title = title_m.group(1).strip() if title_m else "Unknown"
        repeat_m = re.search(r"\*\*Do NOT repeat\*\*:\s*(.+)", b)
        repeat = repeat_m.group(1).strip() if repeat_m else ""
        entries.append({"title": title, "rule": repeat})
    return entries

def _log_entries(text: str, max_n: int = 15) -> list[str]:
    parts = re.split(r"\n---\n", text)
    entries = [p.strip() for p in parts if p.strip() and "## Turn" in p]
    return entries[-max_n:]

def _critic_scores(text: str) -> dict[str, float]:
    scores: dict[str, float] = {}
    for i in range(1, 5):
        m = re.search(rf"gate_{i}[^:]*:\s*([0-9.]+)", text, re.IGNORECASE)
        if m: scores[f"Gate {i}"] = float(m.group(1))
    return scores

def _find_report() -> str:
    for p in Path(".").rglob("REPORT.md"):
        return p.read_text(encoding="utf-8")
    return ""

def _detect_experiment(cfg: dict) -> str | None:
    name = cfg.get("project", {}).get("name", "")
    for k in EXPERIMENT_CATALOG:
        if k in name or name in k: return k
    return None

def _health_gauge(label: str, value: float, target: float, direction: str = "higher_better") -> str:
    """Render a green-yellow-red gradient health gauge.

    direction: "higher_better" (green=high, red=low) or "lower_better" (green=low, red=high)
    value and target are used to compute the score (0-1).
    """
    if direction == "higher_better":
        score = min(value / max(target, 0.001), 1.0) if target > 0 else 0.5
    else:
        score = min(target / max(value, 0.001), 1.0) if value > 0 else 1.0
    score = max(0.0, min(1.0, score))

    # Green-yellow-red gradient
    if score >= 0.8:
        color = "#00ff88"  # green
    elif score >= 0.5:
        color = "#ffcc00"  # yellow
    elif score >= 0.3:
        color = "#ff8800"  # orange
    else:
        color = "#ff4444"  # red

    pct = int(score * 100)
    return (
        f'<div class="health-gauge" style="background:#0d0d20;border-left:4px solid {color};">'
        f'<div class="bar" style="width:{pct}%;background:{color};"></div>'
        f'<div class="content">'
        f'<b style="color:{color};">{label}</b><br/>'
        f'<span style="font-size:22px;color:{color};">{value:.2f}</span>'
        f' <span style="color:#666;">/ {target:.2f} target</span>'
        f' <span style="float:right;color:{color};font-size:18px;">{pct}%</span>'
        f'</div></div>'
    )


def _mode_html(mode: str) -> str:
    m = mode.upper()
    if "DONE" in m or "COMPLETE" in m:
        color, label = "#00ff88", "✓ COMPLETE"
    elif "EXPLORATION" in m:
        color, label = "#ffaa00", "◆ EXPLORATION"
    elif "EXIT" in m or "STOP" in m:
        color, label = "#ff4444", "✕ EXIT"
    else:
        color, label = "#4488ff", "● VALIDATION"
    return (f'<div class="mode-badge" style="background:{color}22;color:{color};'
            f'border:2px solid {color};">{label}</div>')


# ── MAIN ─────────────────────────────────────────────────────────────────────

def main() -> None:
    config = _yaml(CONFIG_PATH)
    sv = _sv(_read(STATE_VECTOR_PATH))
    log_text = _read(INNOVATION_LOG_PATH)
    dead_text = _read(DEAD_ENDS_PATH)
    report_text = _find_report()
    experiment = _detect_experiment(config)
    project = config.get("project", {}).get("name", "CHP Project")

    # ── HEADER ───────────────────────────────────────────────────────────
    st.markdown(f"# 🔬 Context Hacking Protocol — `{project}`")
    st.markdown(f"<p style='color:#666;margin-top:-10px;'>Scientific Control Panel "
                f"· Auto-refresh {REFRESH_SECONDS}s · {time.strftime('%H:%M:%S')}</p>",
                unsafe_allow_html=True)

    # ── TOP ROW: Mode + Key Metrics ──────────────────────────────────────
    c1, c2, c3, c4, c5 = st.columns([2, 1, 1, 1, 2])
    with c1:
        st.markdown(_mode_html(sv.get("MODE", "VALIDATION")), unsafe_allow_html=True)
    with c2:
        st.metric("Turn", sv.get("TURN", "0"))
    with c3:
        de_count = len(_dead_ends(dead_text))
        st.metric("Dead Ends", str(de_count))
    with c4:
        flags = sv.get("OPEN_FLAGS", "none")
        st.metric("Flags", "0" if flags.lower() == "none" else flags)
    with c5:
        milestone = sv.get("MILESTONE", "—")
        st.markdown(f'<div class="metric-card"><div class="metric-label">Milestone</div>'
                    f'<div style="color:#e0e0e0;font-size:16px;">{milestone}</div></div>',
                    unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # ── MAIN GRID ────────────────────────────────────────────────────────
    tab_monitor, tab_health, tab_report, tab_gallery = st.tabs([
        "📊 Live Monitor", "🏥 Protocol Health", "📄 Experiment Report", "🧪 Experiment Gallery"
    ])

    # ── TAB 1: LIVE MONITOR ──────────────────────────────────────────────
    with tab_monitor:
        left, right = st.columns([1, 1])

        with left:
            # ── Critic Scorecard ─────────────────────────────────────
            st.markdown("### Critic Scorecard")
            scores = _critic_scores(log_text)
            thresholds = {"Gate 1": 1.0, "Gate 2": 0.85, "Gate 3": 0.85, "Gate 4": 0.85}
            gate_names = {
                "Gate 1": "Frozen Compliance",
                "Gate 2": "Architecture",
                "Gate 3": "Scientific Validity",
                "Gate 4": "Drift Check"
            }
            if scores:
                for gate, score in scores.items():
                    thresh = thresholds.get(gate, 0.85)
                    passed = score >= thresh
                    cls = "gate-pass" if passed else ("gate-fail" if score < thresh - 0.1 else "gate-warn")
                    icon = "✓" if passed else "✗"
                    color = "#00ff88" if passed else "#ff4444"
                    st.markdown(
                        f'<div class="gate-row {cls}">'
                        f'<span style="color:{color};font-weight:bold;">{icon}</span> '
                        f'{gate_names.get(gate, gate)}: '
                        f'<b style="color:{color};">{score:.2f}</b> / {thresh}</div>',
                        unsafe_allow_html=True)
            else:
                st.caption("No critic review yet. Run `chp run` to start.")

            # ── sigma-Gates ──────────────────────────────────────────
            st.markdown("### σ-Gate Status")
            checks = config.get("gates", {}).get("anomaly_checks", [])
            if checks:
                for ch in checks:
                    name = ch.get("metric", "?")
                    op = ch.get("operator", ">")
                    thresh = ch.get("threshold", 0)
                    desc = ch.get("description", "")
                    st.markdown(
                        f'<div class="sigma-gauge">'
                        f'<span style="color:#666;">◇</span> '
                        f'<b>{name}</b> {op} {thresh}'
                        f'<br/><span style="color:#555;font-size:11px;">{desc}</span>'
                        f'</div>', unsafe_allow_html=True)
            else:
                st.caption("No gates defined.")

            # ── Council ──────────────────────────────────────────────
            st.markdown("### Council Status")
            recent = log_text[-3000:].upper()
            drift = ("DRIFT:" in recent and ("YES" in recent or "CONCERN" in recent)) or "BOTH FLAG DRIFT" in recent
            if drift:
                st.error("⚠ DRIFT flagged by council")
            else:
                st.success("No drift detected")

        with right:
            # ── Innovation Log ───────────────────────────────────────
            st.markdown("### Innovation Log")
            entries = _log_entries(log_text)
            if entries:
                for entry in reversed(entries):
                    turn_m = re.match(r"## Turn (\d+)", entry)
                    label = f"Turn {turn_m.group(1)}" if turn_m else "Entry"
                    # Detect false positive
                    has_fp = "FALSE POSITIVE" in entry.upper()
                    icon = "🚨" if has_fp else "📝"
                    with st.expander(f"{icon} {label}", expanded=(has_fp or entry == entries[-1])):
                        st.markdown(entry[:2000])
            else:
                st.caption("No turns recorded. Run `chp run` to start the loop.")

            # ── Dead Ends ────────────────────────────────────────────
            st.markdown("### Dead Ends")
            des = _dead_ends(dead_text)
            if des:
                for de in des:
                    rule_html = ""
                    if de["rule"]:
                        rule_html = (
                            '<br/><span style="font-size:12px;color:#aa4444;">'
                            f'→ {de["rule"]}</span>'
                        )
                    st.markdown(
                        f'<div class="dead-end-card">'
                        f'<b>🚫 {de["title"]}</b>'
                        f'{rule_html}'
                        f'</div>', unsafe_allow_html=True)
            else:
                st.caption("No dead ends logged.")

    # ── TAB 2: PROTOCOL HEALTH ──────────────────────────────────────────
    with tab_health:
        _render_protocol_health()

    # ── TAB 3: EXPERIMENT REPORT ─────────────────────────────────────────
    with tab_report:
        if report_text:
            st.markdown("### Experiment Report")
            st.markdown(f'<div class="report-section">', unsafe_allow_html=True)
            st.markdown(report_text)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No REPORT.md found yet. The report is generated when the experiment completes.")

        # Export button
        st.markdown("")
        if st.button("📄 Export Paper Appendix", use_container_width=True):
            _export(config, log_text, dead_text, sv, report_text)
            st.success("Exported to paper_appendix.md")

    # ── TAB 3: EXPERIMENT GALLERY ────────────────────────────────────────
    with tab_gallery:
        st.markdown("### 9 Built-in Showcase Experiments")
        st.markdown("Each experiment demonstrates the Context Hacking Protocol "
                     "on a different scientific domain with domain-specific "
                     "σ-gates and pre-loaded false-positive stories.")

        cols = st.columns(3)
        for idx, (key, meta) in enumerate(EXPERIMENT_CATALOG.items()):
            with cols[idx % 3]:
                active = key == experiment
                cls = "experiment-card-active" if active else "experiment-card"
                badge = '<span style="color:#00ff88;font-weight:bold;"> ✓ ACTIVE</span>' if active else ""
                st.markdown(
                    f'<div class="{cls}">'
                    f'<span style="font-size:28px;">{meta["icon"]}</span> '
                    f'<b>{key}</b>{badge}<br/>'
                    f'<span style="color:#666;font-size:12px;">{meta["domain"]}</span>'
                    f'</div>', unsafe_allow_html=True)

    # ── FOOTER ───────────────────────────────────────────────────────────
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        f'<p style="text-align:center;color:#444;font-size:12px;">'
        f'Context Hacking Protocol v0.2 · 9-Layer Anti-Drift Framework · '
        f'<a href="https://github.com/kepiCHelaSHen/context-hacking" style="color:#4488ff;">GitHub</a>'
        f'</p>', unsafe_allow_html=True)

    # ── Auto-refresh ─────────────────────────────────────────────────────
    time.sleep(REFRESH_SECONDS)
    st.rerun()


def _render_protocol_health() -> None:
    """Render the Protocol Health tab with telemetry data."""
    import plotly.graph_objects as go

    telemetry_path = Path(".chp") / "telemetry.json"

    st.markdown("### Protocol Health — Is the loop learning?")
    st.markdown(
        "These metrics track whether the CHP protocol is getting more efficient "
        "over time. A healthy loop shows: declining drift rate, improving gate "
        "scores, faster turns, and fewer fix cycles."
    )

    if not telemetry_path.exists():
        st.info(
            "No telemetry data yet. Telemetry is recorded automatically when "
            "the loop runs via `chp run --method api`. "
            "The metrics below will populate as turns complete."
        )
        # Show empty metric cards with explanations
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(
                '<div class="metric-card">'
                '<div class="metric-label">Tokens per Turn</div>'
                '<div style="color:#888;font-size:14px;">How efficient is the loop getting?<br/>'
                'Fewer tokens per turn = Builder learns to be concise.</div>'
                '</div>', unsafe_allow_html=True)
        with col2:
            st.markdown(
                '<div class="metric-card">'
                '<div class="metric-label">Drift Rate</div>'
                '<div style="color:#888;font-size:14px;">Is the Builder matching the spec?<br/>'
                'Declining drift = fewer coefficients wrong per turn.</div>'
                '</div>', unsafe_allow_html=True)
        with col3:
            st.markdown(
                '<div class="metric-card">'
                '<div class="metric-label">First-Try Pass Rate</div>'
                '<div style="color:#888;font-size:14px;">How often do tests pass without fixes?<br/>'
                'Rising rate = Builder producing cleaner code.</div>'
                '</div>', unsafe_allow_html=True)

        col4, col5, col6 = st.columns(3)
        with col4:
            st.markdown(
                '<div class="metric-card">'
                '<div class="metric-label">Gate Score Trend</div>'
                '<div style="color:#888;font-size:14px;">Is code quality improving?<br/>'
                'Rising scores = Critic finding fewer issues.</div>'
                '</div>', unsafe_allow_html=True)
        with col5:
            st.markdown(
                '<div class="metric-card">'
                '<div class="metric-label">Dead Ends Avoided</div>'
                '<div style="color:#888;font-size:14px;">Is the memory system working?<br/>'
                'Each avoided dead end = a mistake NOT repeated.</div>'
                '</div>', unsafe_allow_html=True)
        with col6:
            st.markdown(
                '<div class="metric-card">'
                '<div class="metric-label">Time per Turn</div>'
                '<div style="color:#888;font-size:14px;">Is it getting faster?<br/>'
                'Declining time = more efficient builds.</div>'
                '</div>', unsafe_allow_html=True)
        return

    # Load telemetry data
    try:
        data = json.loads(telemetry_path.read_text(encoding="utf-8"))
        turns_data = data.get("turns", [])
    except Exception:
        st.error("Failed to load telemetry data.")
        return

    if not turns_data:
        st.info("No turns recorded yet.")
        return

    # ── Summary cards ────────────────────────────────────────────────
    total_tokens = sum(t.get("tokens_total", 0) for t in turns_data)
    total_lines = sum(t.get("lines_written", 0) for t in turns_data)
    total_time = sum(t.get("duration_seconds", 0) for t in turns_data)
    n_fp = sum(1 for t in turns_data if t.get("false_positive_caught"))
    n_de = sum(t.get("dead_ends_avoided", 0) for t in turns_data)
    tested = [t for t in turns_data if t.get("tests_passed", 0) + t.get("tests_failed", 0) > 0]
    first_try = sum(1 for t in tested if t.get("tests_passed_first_try"))
    ftr = first_try / len(tested) if tested else 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        tpl = round(total_tokens / total_lines, 1) if total_lines > 0 else 0
        st.metric("Tokens/Line", f"{tpl}", help="Lower = more token-efficient")
    with col2:
        st.metric("Total Tokens", f"{total_tokens:,}")
    with col3:
        st.metric("False Positives Caught", str(n_fp))
    with col4:
        st.metric("Dead Ends Avoided", str(n_de))

    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.metric("First-Try Pass", f"{ftr:.0%}", help="Tests pass without fix cycle")
    with col6:
        st.metric("Total Lines Built", f"{total_lines:,}")
    with col7:
        st.metric("Total Time", f"{total_time/60:.1f} min")
    with col8:
        st.metric("Turns", str(len(turns_data)))

    # ── Trend charts ─────────────────────────────────────────────────
    st.markdown("### Trends Over Time")

    turn_nums = [t.get("turn", i+1) for i, t in enumerate(turns_data)]

    # Token consumption per turn
    tokens = [t.get("tokens_total", 0) for t in turns_data]
    if any(t > 0 for t in tokens):
        fig_tokens = go.Figure(data=go.Scatter(
            x=turn_nums, y=tokens, mode="lines+markers",
            line=dict(color="#4488ff"), name="Tokens",
        ))
        fig_tokens.update_layout(
            title="Tokens per Turn — is the loop getting more efficient?",
            xaxis_title="Turn", yaxis_title="Tokens",
            height=300, template="plotly_dark",
            paper_bgcolor="#0a0a1a", plot_bgcolor="#0d0d20",
        )
        st.plotly_chart(fig_tokens, use_container_width=True)

    # Gate scores over time
    g1 = [t.get("gate_1_frozen", 0) for t in turns_data]
    g3 = [t.get("gate_3_scientific", 0) for t in turns_data]
    if any(g > 0 for g in g1):
        fig_gates = go.Figure()
        fig_gates.add_trace(go.Scatter(
            x=turn_nums, y=g1, name="Gate 1 (Frozen)", mode="lines+markers",
            line=dict(color="#00ff88"),
        ))
        fig_gates.add_trace(go.Scatter(
            x=turn_nums, y=g3, name="Gate 3 (Scientific)", mode="lines+markers",
            line=dict(color="#ffaa00"),
        ))
        fig_gates.add_hline(y=0.85, line_dash="dash", line_color="#ff4444",
                            annotation_text="Threshold (0.85)")
        fig_gates.update_layout(
            title="Critic Gate Scores — is code quality improving?",
            xaxis_title="Turn", yaxis_title="Score",
            height=300, template="plotly_dark",
            paper_bgcolor="#0a0a1a", plot_bgcolor="#0d0d20",
        )
        st.plotly_chart(fig_gates, use_container_width=True)

    # Drift rate over time
    drifts = [t.get("drift_rate", 0) for t in turns_data]
    if any(d > 0 for d in drifts):
        fig_drift = go.Figure(data=go.Scatter(
            x=turn_nums, y=drifts, mode="lines+markers",
            line=dict(color="#ff4444"), fill="tozeroy",
            fillcolor="rgba(255,68,68,0.1)",
        ))
        fig_drift.update_layout(
            title="Drift Rate — is the Builder matching the spec better?",
            xaxis_title="Turn", yaxis_title="Drift Rate (lower = better)",
            height=300, template="plotly_dark",
            paper_bgcolor="#0a0a1a", plot_bgcolor="#0d0d20",
        )
        st.plotly_chart(fig_drift, use_container_width=True)

    # Time per turn
    times = [t.get("duration_seconds", 0) for t in turns_data]
    if any(t > 0 for t in times):
        fig_time = go.Figure(data=go.Bar(
            x=turn_nums, y=[t/60 for t in times],
            marker_color=["#00ff88" if t < 300 else "#ffaa00" if t < 600 else "#ff4444"
                          for t in times],
        ))
        fig_time.update_layout(
            title="Time per Turn — is it getting faster?",
            xaxis_title="Turn", yaxis_title="Minutes",
            height=300, template="plotly_dark",
            paper_bgcolor="#0a0a1a", plot_bgcolor="#0d0d20",
        )
        st.plotly_chart(fig_time, use_container_width=True)

    # ── Event log ────────────────────────────────────────────────────
    st.markdown("### Key Events")
    for t in turns_data:
        turn_n = t.get("turn", "?")
        if t.get("false_positive_caught"):
            st.markdown(
                f'<div style="background:#1a1a0a;border-left:4px solid #ffaa00;'
                f'padding:8px 12px;margin:4px 0;border-radius:4px;">'
                f'Turn {turn_n}: FALSE POSITIVE CAUGHT — '
                f'{t.get("false_positive_description", "see innovation log")}'
                f'</div>', unsafe_allow_html=True)
        if t.get("anomaly"):
            st.markdown(
                f'<div style="background:#1a0a0a;border-left:4px solid #ff4444;'
                f'padding:8px 12px;margin:4px 0;border-radius:4px;">'
                f'Turn {turn_n}: ANOMALY — sigma-gate failed'
                f'</div>', unsafe_allow_html=True)
        if t.get("new_dead_ends_logged", 0) > 0:
            st.markdown(
                f'<div style="background:#0a0a1a;border-left:4px solid #4488ff;'
                f'padding:8px 12px;margin:4px 0;border-radius:4px;">'
                f'Turn {turn_n}: New dead end logged'
                f'</div>', unsafe_allow_html=True)


def _export(cfg: dict, log: str, dead: str, sv: dict, report: str) -> None:
    sections = [
        "# CHP Paper Appendix\n",
        f"Project: {cfg.get('project', {}).get('name', '?')}\n",
        f"Generated: {time.strftime('%Y-%m-%d %H:%M')}\n",
        "\n## State Vector\n",
        *[f"- **{k}**: {v}\n" for k, v in sv.items()],
        "\n## Innovation Log\n", log,
        "\n## Dead Ends\n", dead,
    ]
    if report:
        sections.extend(["\n## Experiment Report\n", report])
    Path("paper_appendix.md").write_text("\n".join(sections), encoding="utf-8")


if __name__ == "__main__":
    main()
