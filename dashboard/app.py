"""
CHP Dashboard — Clinical Scientific Instrument Panel
=====================================================
Real-time monitoring of the Context Hacking Protocol loop.
Displays live figures, gate scores, telemetry, and experiment data.

READ-ONLY: this dashboard never writes to any CHP file.
Safe to run alongside `chp run`.

Launch: chp dashboard  (or: streamlit run dashboard/app.py)
"""

from __future__ import annotations

import json
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st

# ── Page config (must be first Streamlit call) ───────────────────────────────

st.set_page_config(
    page_title="CHP Instrument Panel",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Figure caption descriptions ──────────────────────────────────────────────

FIGURE_DESCRIPTIONS: dict[str, str] = {
    "grid_final": "Final agent grid — segregation index measured from this state",
    "schelling_comparison": "Baseline vs CHP dynamic tolerance — segregation comparison",
    "segregation_over_time": "Segregation index over simulation steps",
    "cluster_map": "Cluster labels — spatially contiguous same-type groups",
    "lattice_final": "Final cooperator/defector lattice (blue=cooperate, red=defect)",
    "spatial_pd_lattice": "Nowak & May spatial PD — cooperator/defector pattern",
    "cooperation_rate": "Cooperation rate per generation",
    "pattern_evolution": "Spatial pattern development across generations",
    "population_timeseries": "Prey and predator population dynamics",
    "lotka_volterra_dynamics": "Agent-based predator-prey time series + phase portrait",
    "phase_portrait": "Phase space — prey vs predator trajectory",
    "epidemic_curve": "Stochastic SIR epidemic curve — one representative run",
    "sir_epidemic_curve": "SIR epidemic — I(t) is integer, not float (stochastic)",
    "r0_distribution": "R0 estimate distribution across seeds",
    "convergence": "Bayesian optimization convergence — best validation accuracy",
    "search_space": "2D hyperparameter search space heatmap",
    "attractor_3d": "Lorenz strange attractor — 3D phase space trajectory",
    "lorenz_attractor": "Lorenz butterfly — RK45 adaptive, sigma=10 rho=28 beta=8/3",
    "lyapunov_convergence": "Lyapunov exponent convergence across time",
    "amplitude_bars": "Grover amplitude per basis state at optimal iterations",
    "grover_amplitude": "Grover success probability vs iteration count (sinusoidal)",
    "grover_states": "Grover state amplitudes at k=25 — target state highlighted",
    "success_probability": "Grover success probability vs iteration count",
    "voltage_raster": "Izhikevich neuron membrane voltage traces",
    "izhikevich_patterns": "5 firing patterns: RS, IB, FS, CH, LTS (NOT Hodgkin-Huxley)",
    "isi_histogram": "Inter-spike interval distribution by firing pattern",
    "consensus_rounds": "PBFT consensus per round with Byzantine faults",
    "blockchain_safety": "Safety vs f Byzantine nodes — threshold f < N/3",
    "byzantine_threshold": "Safety boundary — PBFT vs Raft under equivocation",
    "metal_vs_classical": "Classical flags 6-9 errors per Pantera riff. Metal: zero.",
}

# ── CSS Design System ────────────────────────────────────────────────────────

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;500;600;700&family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Source+Sans+3:wght@300;400;500;600&display=swap');

    :root {
        --bg: #09090E;
        --surface: #0D0F16;
        --surface-2: #111420;
        --surface-3: #171B28;
        --line: #191E2E;
        --line-2: #222840;
        --line-3: #2C3450;
        --text-1: #D6DAE8;
        --text-2: #8A90A8;
        --text-3: #525870;
        --text-4: #333A50;
        --amber: #C8902A;
        --amber-dim: #7A5518;
        --amber-glow: rgba(200,144,42,0.10);
        --amber-glow2: rgba(200,144,42,0.05);
        --pass: #2E9E6A;
        --pass-dim: #1A5C3E;
        --pass-glow: rgba(46,158,106,0.08);
        --fail: #C84848;
        --fail-dim: #7A2C2C;
        --fail-glow: rgba(200,72,72,0.08);
        --info: #4A7AB8;
        --warn: #C87830;
        --mono: 'IBM Plex Mono', 'Courier New', monospace;
        --serif: 'Libre Baskerville', Georgia, serif;
        --sans: 'Source Sans 3', 'Helvetica Neue', Arial, sans-serif;
    }

    html, body, .main, .stApp {
        background-color: var(--bg) !important;
        font-family: var(--sans);
        color: var(--text-1);
    }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 0 !important; max-width: 100% !important; }

    /* Scanline texture */
    .stApp::before {
        content: '';
        position: fixed; inset: 0;
        pointer-events: none; z-index: 0;
        background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.06) 2px, rgba(0,0,0,0.06) 3px);
    }

    /* Scrollbars */
    ::-webkit-scrollbar { width: 4px; height: 4px; }
    ::-webkit-scrollbar-thumb { background: var(--line-2); }
    ::-webkit-scrollbar-thumb:hover { background: var(--amber-dim); }

    h1, h2, h3 { font-family: var(--sans); color: var(--text-1); }

    div[data-testid="stMetricValue"] {
        font-family: var(--mono) !important;
        font-size: 1.55rem !important;
        font-weight: 500;
        color: var(--text-1);
    }
    div[data-testid="stMetricLabel"] {
        font-family: var(--sans) !important;
        font-size: 0.60rem !important;
        color: var(--text-3);
        text-transform: uppercase;
        letter-spacing: 0.12em;
    }

    /* Tabs */
    button[data-baseweb="tab"] {
        font-family: var(--mono) !important;
        font-size: 0.70rem !important;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: var(--text-3) !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: var(--amber) !important;
        border-bottom: 2px solid var(--amber) !important;
    }
    div[data-baseweb="tab-list"] {
        border-bottom: 1px solid var(--line-2);
        background: var(--surface);
    }

    /* Expanders */
    details { background: var(--surface) !important; border: 1px solid var(--line) !important; border-radius: 0 !important; }
    details summary { font-family: var(--mono); font-size: 0.72rem; color: var(--text-2); }

    /* Buttons */
    .stButton > button {
        border-radius: 0 !important;
        border: 1px solid var(--line-2) !important;
        background: var(--surface-2) !important;
        font-family: var(--mono) !important;
        font-size: 0.70rem !important;
        text-transform: uppercase;
        letter-spacing: 0.10em;
        color: var(--text-2) !important;
    }
    .stButton > button:hover {
        border-color: var(--amber) !important;
        color: var(--amber) !important;
        background: var(--amber-glow2) !important;
    }

    /* Custom components */
    .chp-header {
        background: var(--surface);
        border-bottom: 1px solid var(--amber-dim);
        padding: 12px 28px;
        font-family: var(--mono);
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: nowrap;
        margin-bottom: 8px;
    }
    .chp-header .left { display: flex; align-items: center; gap: 8px; }
    .chp-header .center { display: flex; align-items: center; gap: 8px; font-size: 0.72rem; }
    .chp-header .right { font-size: 0.62rem; color: var(--text-4); }

    .sec-head {
        display: flex; align-items: center; gap: 12px;
        margin: 22px 0 10px;
    }
    .sec-head-label { font-family: var(--serif); font-style: italic; font-size: 0.82rem; color: var(--text-2); white-space: nowrap; }
    .sec-head-line { flex-grow: 1; height: 1px; background: var(--line-2); }
    .sec-head-index { font-family: var(--mono); font-size: 0.56rem; color: var(--text-4); letter-spacing: 0.10em; }

    .gate-meter {
        padding: 10px 14px;
        background: var(--surface);
        margin: 5px 0;
        position: relative;
    }
    .gate-meter-pass { border-left: 3px solid var(--pass); }
    .gate-meter-fail { border-left: 3px solid var(--fail); }
    .gate-meter-warn { border-left: 3px solid var(--warn); }
    .gate-meter .track { height: 3px; background: var(--surface-3); position: relative; margin: 6px 0 4px; }
    .gate-meter .fill { height: 3px; position: absolute; top: 0; left: 0; }
    .gate-meter .tick { position: absolute; width: 1px; height: 9px; top: -3px; background: var(--amber); }

    .sigma-reading {
        display: flex; align-items: center; gap: 10px;
        padding: 7px 14px;
        border-bottom: 1px solid var(--line);
        font-family: var(--mono); font-size: 0.68rem;
    }
    .sigma-reading:nth-child(odd) { background: var(--surface); }
    .sigma-reading:nth-child(even) { background: var(--surface-2); }

    .contra-row {
        display: flex; align-items: center; gap: 10px;
        padding: 8px 14px;
        border-bottom: 1px solid var(--line);
        background: var(--fail-glow);
    }

    .stat-cell {
        background: var(--surface);
        border: 1px solid var(--line);
        border-top: 2px solid var(--amber-dim);
        padding: 12px 16px;
    }
    .stat-cell .label { font-family: var(--sans); font-size: 0.58rem; color: var(--text-3); text-transform: uppercase; letter-spacing: 0.14em; }
    .stat-cell .value { font-family: var(--mono); font-size: 1.50rem; color: var(--text-1); font-weight: 500; }
    .stat-cell .sub { font-family: var(--sans); font-size: 0.62rem; color: var(--text-3); margin-top: 3px; }

    .fig-thumb {
        border: 1px solid var(--line-2);
        background: var(--surface-2);
        padding: 4px;
    }

    .protocol-table { width: 100%; border-collapse: collapse; font-family: var(--mono); font-size: 0.70rem; }
    .protocol-table th { border-bottom: 1px solid var(--amber-dim); color: var(--text-3); text-transform: uppercase; letter-spacing: 0.10em; padding: 9px 14px; text-align: left; font-weight: 400; }
    .protocol-table td { border-bottom: 1px solid var(--line); color: var(--text-2); padding: 9px 14px; }
    .protocol-table tr:hover td { background: var(--surface-2); }

    @keyframes lamp-pulse { 0%,100% { opacity:1 } 50% { opacity:0.35 } }
    .lamp { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
    .lamp-active { animation: lamp-pulse 2s ease-in-out infinite; }
</style>
""", unsafe_allow_html=True)

# ── Constants ────────────────────────────────────────────────────────────────

REFRESH_SECONDS = 5
CONFIG_PATH = Path("config.yaml")
STATE_VECTOR_PATH = Path("state_vector.md")
INNOVATION_LOG_PATH = Path("innovation_log.md")
DEAD_ENDS_PATH = Path("dead_ends.md")

EXPERIMENT_CATALOG = {
    "schelling-segregation":       {"domain": "Social Science",      "icon": "🏘", "catches": "tolerance drift, sequential update"},
    "spatial-prisoners-dilemma":    {"domain": "Game Theory",         "icon": "🎲", "catches": "T/R/P/S payoff, missing self"},
    "lotka-volterra":              {"domain": "Ecology",             "icon": "🐺", "catches": "ODE equations, zero extinction"},
    "sir-epidemic":                {"domain": "Epidemiology",        "icon": "🦠", "catches": "rate equations, zero fadeout"},
    "ml-hyperparam-search":        {"domain": "Machine Learning",    "icon": "🤖", "catches": "grid search, data leakage"},
    "lorenz-attractor":            {"domain": "Chaos Theory",        "icon": "🦋", "catches": "Euler integration, rounded beta"},
    "quantum-grover":              {"domain": "Quantum Computing",   "icon": "⚛",  "catches": "classical search, boolean oracle"},
    "izhikevich-neurons":          {"domain": "Neuroscience",        "icon": "🧠", "catches": "Hodgkin-Huxley, wrong model"},
    "blockchain-consensus":        {"domain": "Distributed Systems", "icon": "🔗", "catches": "Raft/Paxos, f+1 quorum"},
}

GATE_NAMES = {
    "Gate 1": ("G1", "FROZEN COMPLIANCE", 1.0),
    "Gate 2": ("G2", "ARCHITECTURE", 0.85),
    "Gate 3": ("G3", "SCIENTIFIC VALIDITY", 0.85),
    "Gate 4": ("G4", "DRIFT CHECK", 0.85),
}


# ── File readers (READ-ONLY) ────────────────────────────────────────────────

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

def _find_figures(experiment_dir: Path) -> list[Path]:
    """Return sorted list of PNG/SVG figures from experiment's figures/ dir."""
    figures_dir = experiment_dir / "figures"
    if not figures_dir.exists():
        return []
    return sorted(
        [p for p in figures_dir.iterdir()
         if p.suffix.lower() in (".png", ".svg", ".jpg", ".jpeg")],
        key=lambda p: p.stat().st_mtime, reverse=True,
    )

def _detect_experiment(cfg: dict) -> str | None:
    name = cfg.get("project", {}).get("name", "")
    for k in EXPERIMENT_CATALOG:
        if k in name or name in k: return k
    return None

def _time_ago(mtime: float) -> str:
    diff = time.time() - mtime
    if diff < 10: return "just now"
    if diff < 60: return f"{int(diff)}s ago"
    if diff < 3600: return f"{int(diff/60)}m ago"
    return f"{int(diff/3600)}h ago"


# ── Component builders ───────────────────────────────────────────────────────

def _sec_head(label: str, index: str) -> str:
    return (f'<div class="sec-head">'
            f'<span class="sec-head-label">{label}</span>'
            f'<div class="sec-head-line"></div>'
            f'<span class="sec-head-index">{index}</span></div>')


def _gate_meter(gate_key: str, score: float) -> str:
    short, full_name, threshold = GATE_NAMES.get(gate_key, ("G?", "UNKNOWN", 0.85))
    if score >= threshold:
        cls, color = "gate-meter-pass", "var(--pass)"
    elif score >= threshold - 0.05:
        cls, color = "gate-meter-warn", "var(--warn)"
    else:
        cls, color = "gate-meter-fail", "var(--fail)"
    pct = min(score * 100, 100)
    tick_pct = threshold * 100
    return (
        f'<div class="gate-meter {cls}">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;">'
        f'<span style="font-family:var(--mono);font-size:0.65rem;color:var(--text-2);text-transform:uppercase;letter-spacing:0.10em;">{short} · {full_name}</span>'
        f'<span style="font-family:var(--mono);font-size:0.90rem;font-weight:600;color:{color};">{score:.2f}</span>'
        f'</div>'
        f'<div class="track"><div class="fill" style="width:{pct}%;background:{color};"></div>'
        f'<div class="tick" style="left:{tick_pct}%;"></div></div>'
        f'<div style="font-family:var(--sans);font-size:0.63rem;color:var(--text-3);">threshold: {threshold}</div>'
        f'</div>'
    )


def _mode_lamp(mode: str, turn: str) -> str:
    m = mode.upper()
    lamps = {"LOOP": False, "VALIDATION": False, "EXPLORATION": False, "ANOMALY": False, "COUNCIL": False}
    if "DONE" in m or "COMPLETE" in m:
        text = f"COMPLETE — ALL MILESTONES DELIVERED"
        text_color = "var(--pass)"
    elif "EXIT" in m:
        lamps["LOOP"] = True
        text = f"EXIT — {mode}"
        text_color = "var(--fail)"
    elif "EXPLORATION" in m:
        lamps["LOOP"] = True
        lamps["EXPLORATION"] = True
        text = f"EXPLORATION · TURN {turn}"
        text_color = "var(--warn)"
    else:
        lamps["LOOP"] = True
        lamps["VALIDATION"] = True
        text = f"VALIDATION · TURN {turn}"
        text_color = "var(--info)"

    lamp_html = ""
    colors = {"LOOP": "var(--info)", "VALIDATION": "var(--info)", "EXPLORATION": "var(--warn)", "ANOMALY": "var(--fail)", "COUNCIL": "var(--text-3)"}
    for name, active in lamps.items():
        c = colors.get(name, "var(--text-3)")
        if active:
            glow = f"box-shadow:0 0 8px 2px {c};"
            lamp_html += f'<div style="text-align:center;"><div class="lamp lamp-active" style="background:{c};{glow}margin:0 auto;"></div><div style="font-size:0.55rem;color:{c};margin-top:3px;">{name}</div></div>'
        else:
            lamp_html += f'<div style="text-align:center;"><div class="lamp" style="background:var(--line-2);margin:0 auto;"></div><div style="font-size:0.55rem;color:var(--text-4);margin-top:3px;">{name}</div></div>'

    return (
        f'<div style="display:flex;gap:16px;justify-content:center;margin:12px 0;">{lamp_html}</div>'
        f'<div style="text-align:center;font-family:var(--mono);font-size:1.0rem;color:{text_color};margin:8px 0;">{text}</div>'
    )


# ── MAIN ─────────────────────────────────────────────────────────────────────

def main() -> None:
    config = _yaml(CONFIG_PATH)
    sv = _sv(_read(STATE_VECTOR_PATH))
    log_text = _read(INNOVATION_LOG_PATH)
    dead_text = _read(DEAD_ENDS_PATH)
    report_text = _find_report()
    experiment = _detect_experiment(config)
    project = config.get("project", {}).get("name", "CHP Project")
    turn = sv.get("TURN", "0")
    mode = sv.get("MODE", "VALIDATION")
    de_count = len(_dead_ends(dead_text))
    flags = sv.get("OPEN_FLAGS", "none")
    flag_count = 0 if flags.lower() == "none" else len(flags.split(","))

    # Figure count for active experiment
    fig_count = 0
    if experiment:
        exp_dir = Path("experiments") / experiment
        if exp_dir.exists():
            fig_count = len(_find_figures(exp_dir))

    # ── FIXED HEADER (Component 1) ───────────────────────────────────
    mode_dot_color = "var(--info)"
    mode_label = "VALIDATION"
    if "EXPLORATION" in mode.upper():
        mode_dot_color = "var(--warn)"
        mode_label = "EXPLORATION"
    elif "DONE" in mode.upper() or "COMPLETE" in mode.upper():
        mode_dot_color = "var(--pass)"
        mode_label = "COMPLETE"
    elif "EXIT" in mode.upper():
        mode_dot_color = "var(--fail)"
        mode_label = "EXIT"

    fig_color = "var(--info)" if fig_count > 0 else "var(--text-4)"
    de_color = "var(--text-3)" if de_count > 0 else "var(--text-4)"

    st.markdown(
        f'<div class="chp-header">'
        f'<div class="left">'
        f'<span style="color:var(--amber);font-size:0.90rem;">&#x2B21;</span>'
        f'<span style="color:var(--text-4);">·</span>'
        f'<span style="color:var(--text-3);font-size:0.68rem;letter-spacing:0.15em;">CHP</span>'
        f'<span style="color:var(--text-4);">·</span>'
        f'<span style="color:var(--amber);font-weight:500;">{project}</span>'
        f'</div>'
        f'<div class="center">'
        f'<span style="color:var(--text-1);font-weight:600;">T:{turn}</span>'
        f'<span style="color:var(--text-4);">·</span>'
        f'<span class="lamp" style="background:{mode_dot_color};width:6px;height:6px;"></span>'
        f'<span style="color:{mode_dot_color};font-size:0.68rem;">{mode_label}</span>'
        f'<span style="color:var(--text-4);">·</span>'
        f'<span style="color:{de_color};font-size:0.68rem;">{de_count} DEAD ENDS</span>'
        f'<span style="color:var(--text-4);">·</span>'
        f'<span style="color:{fig_color};font-size:0.68rem;">{fig_count} FIGS</span>'
        f'</div>'
        f'<div class="right">'
        f'AUTO-REFRESH {REFRESH_SECONDS}s · {time.strftime("%H:%M:%S")}'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ── TABS ─────────────────────────────────────────────────────────
    tab_monitor, tab_health, tab_report, tab_gallery = st.tabs([
        "📊 LIVE MONITOR", "🏥 PROTOCOL HEALTH", "📄 EXPERIMENT REPORT", "🧪 EXPERIMENT GALLERY"
    ])

    # ── TAB 1: LIVE MONITOR ──────────────────────────────────────────
    with tab_monitor:
        left, right = st.columns([1, 1])

        with left:
            # Mode lamp
            st.markdown(_mode_lamp(mode, turn), unsafe_allow_html=True)

            # Critic Scorecard
            st.markdown(_sec_head("Critic Scorecard", "§ 01"), unsafe_allow_html=True)
            scores = _critic_scores(log_text)
            if scores:
                for gate_key, score in scores.items():
                    st.markdown(_gate_meter(gate_key, score), unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="font-family:var(--mono);font-size:0.68rem;color:var(--text-4);padding:14px;">awaiting build · run chp run</div>', unsafe_allow_html=True)

            # sigma-Gates
            st.markdown(_sec_head("sigma-Gate Readings", "§ 02"), unsafe_allow_html=True)
            checks = config.get("gates", {}).get("anomaly_checks", [])
            if checks:
                html = '<div style="border:1px solid var(--line-2);">'
                for ch in checks:
                    name = ch.get("metric", "?")
                    op = ch.get("operator", ">")
                    thresh = ch.get("threshold", 0)
                    html += (f'<div class="sigma-reading">'
                             f'<div class="lamp" style="background:var(--text-4);width:5px;height:5px;"></div>'
                             f'<span style="flex-grow:1;color:var(--text-2);overflow:hidden;text-overflow:ellipsis;">{name}</span>'
                             f'<span style="color:var(--text-4);min-width:18px;">{op}</span>'
                             f'<span style="color:var(--amber);font-weight:500;min-width:45px;">{thresh}</span>'
                             f'</div>')
                html += '</div>'
                st.markdown(html, unsafe_allow_html=True)

            # Council Status
            st.markdown(_sec_head("Council Status", "§ 03"), unsafe_allow_html=True)
            recent = log_text[-3000:].upper()
            drift = ("DRIFT:" in recent and ("YES" in recent or "CONCERN" in recent)) or "BOTH FLAG DRIFT" in recent
            if drift:
                st.error("DRIFT flagged by council")
            else:
                st.success("No drift detected")

        with right:
            # Innovation Log (timeline)
            st.markdown(_sec_head("Innovation Log", "§ 04"), unsafe_allow_html=True)
            entries = _log_entries(log_text)
            if entries:
                for entry in reversed(entries):
                    turn_m = re.match(r"## Turn (\d+)", entry)
                    label = f"TURN {turn_m.group(1)}" if turn_m else "ENTRY"
                    has_fp = "FALSE POSITIVE" in entry.upper()
                    icon = "◆" if has_fp else "○"
                    fp_badge = ' <span style="color:var(--amber);font-family:var(--mono);font-size:0.60rem;">◆ FALSE POSITIVE CAUGHT</span>' if has_fp else ""
                    with st.expander(f"{icon} {label}{fp_badge}", expanded=(has_fp or entry == entries[-1])):
                        st.markdown(entry[:2000])
            else:
                st.markdown(f'<div style="color:var(--text-4);font-family:var(--mono);font-size:0.68rem;padding:14px;">no turns recorded · run chp run to start the protocol</div>', unsafe_allow_html=True)

            # Contraindications (Dead Ends)
            st.markdown(_sec_head("Contraindications", "§ 05"), unsafe_allow_html=True)
            des = _dead_ends(dead_text)
            if des:
                st.markdown(f'<div style="background:var(--fail-glow);border:1px solid var(--fail-dim);padding:6px 14px;font-family:var(--mono);font-size:0.60rem;color:var(--fail);text-transform:uppercase;">CONTRAINDICATIONS — DO NOT REPEAT THESE APPROACHES</div>', unsafe_allow_html=True)
                for idx, de in enumerate(des):
                    rule = f'<br/><span style="font-style:italic;color:var(--fail-dim);font-size:0.65rem;">Do NOT repeat: {de["rule"]}</span>' if de["rule"] else ""
                    st.markdown(
                        f'<div class="contra-row">'
                        f'<span style="font-family:var(--mono);font-size:0.65rem;color:var(--fail-dim);">C{idx+1:02d}</span>'
                        f'<span style="font-family:var(--mono);font-size:0.72rem;color:var(--text-2);flex-grow:1;">{de["title"]}</span>'
                        f'<span style="color:var(--fail);">&#x2717;</span>'
                        f'{rule}</div>',
                        unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="text-align:center;color:var(--text-4);font-family:var(--mono);font-size:0.68rem;padding:20px;">— NO CONTRAINDICATIONS LOGGED —</div>', unsafe_allow_html=True)

            # Live Figure Strip (Component 12A)
            if experiment:
                exp_dir = Path("experiments") / experiment
                figs = _find_figures(exp_dir) if exp_dir.exists() else []
                if figs:
                    latest_time = _time_ago(figs[0].stat().st_mtime)
                    st.markdown(_sec_head(f"Live Figures · {len(figs)} figures · last updated {latest_time}", "§ 06"), unsafe_allow_html=True)
                    cols = st.columns(min(len(figs), 4))
                    for i, fig in enumerate(figs[:4]):
                        with cols[i]:
                            st.image(str(fig), use_container_width=True)
                            st.markdown(f'<div style="text-align:center;font-family:var(--mono);font-size:0.55rem;color:var(--text-3);">{fig.stem}</div>', unsafe_allow_html=True)

    # ── TAB 2: PROTOCOL HEALTH ───────────────────────────────────────
    with tab_health:
        _render_protocol_health()

    # ── TAB 3: EXPERIMENT REPORT ─────────────────────────────────────
    with tab_report:
        if report_text:
            st.markdown(_sec_head("Experiment Report", "§ 01"), unsafe_allow_html=True)
            st.markdown(report_text)

            # Figures gallery (Component 12B)
            if experiment:
                exp_dir = Path("experiments") / experiment
                figs = _find_figures(exp_dir) if exp_dir.exists() else []
                if figs:
                    st.markdown(_sec_head("Publication Figures", "§ 05"), unsafe_allow_html=True)
                    fig_cols = st.columns(2)
                    for i, fig in enumerate(figs):
                        with fig_cols[i % 2]:
                            st.image(str(fig), use_container_width=True)
                            desc = FIGURE_DESCRIPTIONS.get(fig.stem, fig.stem.replace("_", " ").title())
                            st.markdown(f'<div style="font-family:var(--mono);font-size:0.68rem;color:var(--text-2);">{i+1}. {desc}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div style="font-family:var(--mono);font-size:0.62rem;color:var(--text-4);margin-top:8px;">Source: {exp_dir}/figures/</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="color:var(--text-4);font-family:var(--mono);font-size:0.68rem;padding:40px;text-align:center;">no report generated yet · complete the experiment to see results</div>', unsafe_allow_html=True)

        st.markdown("")
        if st.button("EXPORT PAPER APPENDIX", use_container_width=True):
            _export(config, log_text, dead_text, sv, report_text)
            st.success("Exported to paper_appendix.md")

    # ── TAB 4: EXPERIMENT GALLERY ────────────────────────────────────
    with tab_gallery:
        st.markdown(_sec_head("Experiment Registry — 9 Protocols", "§ 01"), unsafe_allow_html=True)

        if "selected_experiment" not in st.session_state:
            st.session_state.selected_experiment = None

        # Protocol index table (Component 9)
        rows_html = ""
        for key, meta in EXPERIMENT_CATALOG.items():
            active = key == experiment
            exp_dir = Path("experiments") / key
            figs = _find_figures(exp_dir) if exp_dir.exists() else []
            fig_text = f'<span style="color:var(--info);">{len(figs)} figs</span>' if figs else '<span style="color:var(--text-4);">—</span>'

            if active:
                status = f'<span class="lamp" style="background:var(--pass);width:6px;height:6px;"></span> <span style="color:var(--pass);">ACTIVE</span>'
                row_style = "background:var(--amber-glow2);border-left:2px solid var(--amber);"
            else:
                status = f'<span style="color:var(--text-4);">—</span>'
                row_style = ""

            rows_html += (
                f'<tr style="{row_style}">'
                f'<td>{meta["icon"]}</td>'
                f'<td><b>{key}</b></td>'
                f'<td>{meta["domain"]}</td>'
                f'<td style="font-size:0.62rem;">{meta["catches"]}</td>'
                f'<td>{fig_text}</td>'
                f'<td>{status}</td>'
                f'</tr>'
            )

        st.markdown(
            f'<table class="protocol-table">'
            f'<thead><tr><th>#</th><th>EXPERIMENT</th><th>DOMAIN</th><th>PRIOR DRIFT CATCHES</th><th>FIGS</th><th>STATUS</th></tr></thead>'
            f'<tbody>{rows_html}</tbody></table>',
            unsafe_allow_html=True,
        )

        # View buttons
        cols = st.columns(3)
        for idx, key in enumerate(EXPERIMENT_CATALOG):
            with cols[idx % 3]:
                if st.button(f"View {key}", key=f"btn_{key}", use_container_width=True):
                    st.session_state.selected_experiment = key

        # Detail panel
        selected = st.session_state.selected_experiment
        if selected:
            st.markdown(f'<div style="border-top:1px solid var(--line-2);margin:16px 0;"></div>', unsafe_allow_html=True)
            st.markdown(_sec_head(f"{EXPERIMENT_CATALOG[selected]['icon']}  {selected}", "DETAIL"), unsafe_allow_html=True)

            exp_dirs = [Path("experiments") / selected, Path("..") / "experiments" / selected, Path(__file__).parent.parent / "experiments" / selected]
            exp_dir = None
            for d in exp_dirs:
                if d.exists() and (d / "frozen").exists():
                    exp_dir = d
                    break

            if exp_dir:
                detail_tabs = st.tabs(["SPEC", "FROZEN RULES", "DEAD ENDS", "REPORT", "FIGURES"])

                with detail_tabs[0]:
                    spec = exp_dir / "spec.md"
                    if spec.exists(): st.markdown(spec.read_text(encoding="utf-8"))
                    else: st.caption("No spec.md found.")

                with detail_tabs[1]:
                    frozen = exp_dir / "frozen"
                    if frozen.exists():
                        for fp in sorted(frozen.glob("*.md")):
                            with st.expander(fp.name, expanded=True):
                                st.markdown(fp.read_text(encoding="utf-8")[:5000])

                with detail_tabs[2]:
                    de_file = exp_dir / "dead_ends.md"
                    if de_file.exists():
                        des2 = _dead_ends(de_file.read_text(encoding="utf-8"))
                        for de in des2:
                            rule = f'<br/><span style="font-style:italic;color:var(--fail-dim);">→ {de["rule"]}</span>' if de["rule"] else ""
                            st.markdown(f'<div class="contra-row"><b style="color:var(--fail);">&#x2717;</b> <span style="color:var(--text-2);">{de["title"]}</span>{rule}</div>', unsafe_allow_html=True)

                with detail_tabs[3]:
                    rpt = exp_dir / "REPORT.md"
                    if rpt.exists(): st.markdown(rpt.read_text(encoding="utf-8"))
                    else: st.markdown(f'<div style="color:var(--text-4);text-align:center;padding:40px;">experiment not yet completed</div>', unsafe_allow_html=True)

                with detail_tabs[4]:
                    figs = _find_figures(exp_dir)
                    if figs:
                        st.markdown(f'<div style="font-family:var(--mono);font-size:0.68rem;color:var(--text-3);margin-bottom:8px;">{len(figs)} figures · most recent: {_time_ago(figs[0].stat().st_mtime)}</div>', unsafe_allow_html=True)
                        fig_cols = st.columns(2)
                        for i, fig in enumerate(figs):
                            with fig_cols[i % 2]:
                                st.image(str(fig), use_container_width=True)
                                desc = FIGURE_DESCRIPTIONS.get(fig.stem, fig.stem.replace("_", " ").title())
                                sz = fig.stat().st_size / 1024
                                mod = datetime.fromtimestamp(fig.stat().st_mtime).strftime("%H:%M:%S")
                                st.markdown(f'<div style="font-family:var(--mono);font-size:0.62rem;color:var(--text-2);">{desc}</div><div style="font-family:var(--mono);font-size:0.58rem;color:var(--text-4);">{sz:.0f} KB · {mod}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div style="color:var(--text-4);text-align:center;padding:40px;font-family:var(--mono);font-size:0.68rem;">— NO FIGURES GENERATED YET —<br/><span style="font-size:0.62rem;">run chp run --experiment {selected}</span></div>', unsafe_allow_html=True)

    # ── FOOTER ───────────────────────────────────────────────────────
    st.markdown(
        f'<div style="border-top:1px solid var(--line);margin:24px 0 8px;padding:8px 0;text-align:center;font-family:var(--mono);font-size:0.58rem;color:var(--text-4);">'
        f'Context Hacking Protocol v0.2 · 9-Layer Anti-Drift Framework · '
        f'<a href="https://github.com/kepiCHelaSHen/context-hacking" style="color:var(--info);">GitHub</a></div>',
        unsafe_allow_html=True,
    )

    # ── Auto-refresh ─────────────────────────────────────────────────
    time.sleep(REFRESH_SECONDS)
    st.rerun()


# ── Protocol Health tab ──────────────────────────────────────────────────────

def _render_protocol_health() -> None:
    import plotly.graph_objects as go

    telemetry_path = Path(".chp") / "telemetry.json"

    st.markdown(_sec_head("Protocol Health — Is the loop learning?", "§ 01"), unsafe_allow_html=True)

    plotly_theme = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#0D0F16",
        font=dict(family="IBM Plex Mono, monospace", color="#525870", size=10),
        margin=dict(l=40, r=20, t=36, b=36),
        height=240,
    )
    axis_style = dict(gridcolor="#191E2E", tickfont=dict(family="IBM Plex Mono", size=9, color="#525870"))

    if not telemetry_path.exists():
        for label, desc in [
            ("Tokens per Turn", "How efficient is the loop getting?"),
            ("Drift Rate", "Is the Builder matching the spec?"),
            ("First-Try Pass Rate", "How often do tests pass without fixes?"),
            ("Gate Score Trend", "Is code quality improving?"),
            ("Dead Ends Avoided", "Is the memory system working?"),
            ("Time per Turn", "Is it getting faster?"),
        ]:
            st.markdown(f'<div class="stat-cell"><div class="label">{label}</div><div class="value" style="color:var(--text-4);">—</div><div class="sub">{desc}</div></div>', unsafe_allow_html=True)
        return

    try:
        data = json.loads(telemetry_path.read_text(encoding="utf-8"))
        turns_data = data.get("turns", [])
    except Exception:
        st.error("Failed to load telemetry.")
        return

    if not turns_data:
        return

    # Summary stat cells
    total_tokens = sum(t.get("tokens_total", 0) for t in turns_data)
    total_lines = sum(t.get("lines_written", 0) for t in turns_data)
    total_time = sum(t.get("duration_seconds", 0) for t in turns_data)
    n_fp = sum(1 for t in turns_data if t.get("false_positive_caught"))
    n_de = sum(t.get("dead_ends_avoided", 0) for t in turns_data)
    tested = [t for t in turns_data if t.get("tests_passed", 0) + t.get("tests_failed", 0) > 0]
    ftr = sum(1 for t in tested if t.get("tests_passed_first_try")) / max(len(tested), 1)
    tpl = round(total_tokens / max(total_lines, 1), 1)

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Tokens/Line", f"{tpl}")
    with c2: st.metric("False Positives Caught", str(n_fp))
    with c3: st.metric("Dead Ends Avoided", str(n_de))
    with c4: st.metric("First-Try Pass", f"{ftr:.0%}")

    c5, c6, c7, c8 = st.columns(4)
    with c5: st.metric("Total Tokens", f"{total_tokens:,}")
    with c6: st.metric("Lines Built", f"{total_lines:,}")
    with c7: st.metric("Total Time", f"{total_time/60:.1f} min")
    with c8: st.metric("Turns", str(len(turns_data)))

    # Charts
    turn_nums = [t.get("turn", i+1) for i, t in enumerate(turns_data)]

    tokens = [t.get("tokens_total", 0) for t in turns_data]
    if any(t > 0 for t in tokens):
        fig = go.Figure(data=go.Scatter(x=turn_nums, y=tokens, mode="lines+markers",
                                         line=dict(color="#4A7AB8")))
        fig.update_layout(title="Tokens per Turn", xaxis_title="Turn", yaxis_title="Tokens",
                          xaxis=axis_style, yaxis=axis_style, **plotly_theme)
        st.plotly_chart(fig, use_container_width=True)

    g1 = [t.get("gate_1_frozen", 0) for t in turns_data]
    g3 = [t.get("gate_3_scientific", 0) for t in turns_data]
    if any(g > 0 for g in g1):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=turn_nums, y=g1, name="G1 Frozen", mode="lines+markers", line=dict(color="#2E9E6A")))
        fig.add_trace(go.Scatter(x=turn_nums, y=g3, name="G3 Scientific", mode="lines+markers", line=dict(color="#C87830")))
        fig.add_hline(y=0.85, line_dash="dot", line_color="#C8902A", annotation_text="threshold")
        fig.update_layout(title="Gate Scores", xaxis=axis_style, yaxis=axis_style, **plotly_theme)
        st.plotly_chart(fig, use_container_width=True)

    # Events
    st.markdown(_sec_head("Key Events", "§ 02"), unsafe_allow_html=True)
    for t in turns_data:
        n = t.get("turn", "?")
        if t.get("false_positive_caught"):
            st.markdown(f'<div style="background:var(--amber-glow);border-left:3px solid var(--amber);padding:8px 12px;margin:4px 0;font-family:var(--mono);font-size:0.72rem;">Turn {n}: <span style="color:var(--amber);">◆ FALSE POSITIVE CAUGHT</span> — {t.get("false_positive_description", "see log")}</div>', unsafe_allow_html=True)
        if t.get("anomaly"):
            st.markdown(f'<div style="background:var(--fail-glow);border-left:3px solid var(--fail);padding:8px 12px;margin:4px 0;font-family:var(--mono);font-size:0.72rem;">Turn {n}: <span style="color:var(--fail);">ANOMALY</span></div>', unsafe_allow_html=True)


# ── Export ───────────────────────────────────────────────────────────────────

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
