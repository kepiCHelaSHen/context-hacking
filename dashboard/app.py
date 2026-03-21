"""
CHP Dashboard - Clinical White Scientific Instrument Panel
READ-ONLY: never writes to any CHP file.
Launch: python -m streamlit run dashboard/app.py --server.port 8502
"""
from __future__ import annotations
import io, json, re, subprocess, sys, time, zipfile
from datetime import datetime
from pathlib import Path
from typing import Any
import streamlit as st

st.set_page_config(page_title="CHP - Context Hacking Protocol", page_icon="O",
                   layout="wide", initial_sidebar_state="collapsed")

FIGURE_DESCRIPTIONS: dict[str, str] = {
    "schelling_comparison": "Baseline vs CHP dynamic tolerance - segregation comparison",
    "grid_final": "Final agent grid - segregation index measured from this state",
    "segregation_over_time": "Segregation index over simulation steps",
    "cluster_map": "Cluster labels - spatially contiguous groups",
    "spatial_pd_lattice": "Nowak & May spatial PD - cooperator/defector pattern",
    "cooperation_rate": "Cooperation rate per generation",
    "population_timeseries": "Prey and predator population dynamics",
    "phase_portrait": "Phase space - prey vs predator trajectory",
    "sir_epidemic_curve": "Stochastic SIR - I(t) integer, not float",
    "r0_distribution": "R0 estimate distribution across seeds",
    "convergence": "Bayesian optimization convergence",
    "search_space": "2D hyperparameter search space heatmap",
    "lorenz_attractor": "Lorenz butterfly - RK45 adaptive, sigma=10 rho=28 beta=8/3",
    "lorenz_chp_story": "CHP Prior-as-Detector: Wrong -> Detected -> Corrected",
    "lyapunov_convergence": "Lyapunov exponent convergence across time",
    "grover_amplitude": "Grover success probability vs iteration count",
    "grover_states": "State amplitudes at k=25 - target state highlighted",
    "izhikevich_patterns": "5 firing patterns: RS IB FS CH LTS (not Hodgkin-Huxley)",
    "isi_histogram": "Inter-spike interval distribution by firing pattern",
    "blockchain_safety": "Safety vs f Byzantine nodes - PBFT threshold f < N/3",
    "consensus_rounds": "PBFT consensus per round with Byzantine faults",
    "metal_vs_classical": "Classical harmony flags 6-9 errors per Pantera riff. Metal: zero.",
}

EXPERIMENT_CATALOG = {
    "schelling-segregation":     {"domain": "Social Science",      "icon": "H", "catches": "tolerance drift, sequential update"},
    "spatial-prisoners-dilemma": {"domain": "Game Theory",         "icon": "D", "catches": "async update, T/R/P/S payoff"},
    "lotka-volterra":            {"domain": "Ecology",             "icon": "W", "catches": "ODE params, zero extinction"},
    "sir-epidemic":              {"domain": "Epidemiology",        "icon": "V", "catches": "deterministic vs stochastic"},
    "ml-hyperparam-search":      {"domain": "Machine Learning",    "icon": "R", "catches": "grid search, data leakage"},
    "lorenz-attractor":          {"domain": "Chaos Theory",        "icon": "B", "catches": "Euler integration, wrong beta"},
    "quantum-grover":            {"domain": "Quantum Computing",   "icon": "Q", "catches": "classical search, boolean oracle"},
    "izhikevich-neurons":        {"domain": "Neuroscience",        "icon": "N", "catches": "Hodgkin-Huxley contamination"},
    "blockchain-consensus":      {"domain": "Distributed Systems", "icon": "C", "catches": "Raft/Paxos, f+1 quorum"},
}

REFRESH_SECONDS = 5

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;500;600&family=Inter:wght@300;400;500;600&display=swap');
:root {
    --bg:#F8F9FC; --sur:#FFFFFF; --sur2:#F3F4F8; --sur3:#E9EBF2;
    --ln:#E2E5EF; --ln2:#C8CCDB;
    --t1:#0F1117; --t2:#374151; --t3:#6B7280; --t4:#9CA3AF; --t5:#D1D5DB;
    --blue:#1D4ED8; --bluebg:#EFF6FF; --bluebd:#93C5FD;
    --pass:#065F46; --passbg:#ECFDF5; --passbd:#34D399;
    --fail:#991B1B; --failbg:#FEF2F2; --failbd:#FCA5A5;
    --warn:#92400E; --warnbg:#FFFBEB; --warnbd:#FCD34D;
    --amber:#D97706;
    --mono:'IBM Plex Mono',monospace; --sans:'Inter',system-ui,sans-serif;
}
html,body,.main,.stApp{background-color:var(--bg)!important;font-family:var(--sans)!important;color:var(--t1)!important;}
#MainMenu,footer,header{visibility:hidden;}
.block-container{padding:0!important;max-width:100%!important;}
section[data-testid="stMain"]>div{padding:0!important;}
::-webkit-scrollbar{width:5px;height:5px;}
::-webkit-scrollbar-track{background:var(--bg);}
::-webkit-scrollbar-thumb{background:var(--ln2);border-radius:3px;}
div[data-testid="stTabs"]>div:first-child{background:var(--sur)!important;border-bottom:2px solid var(--ln)!important;padding:0 20px!important;}
button[role="tab"]{font-family:var(--mono)!important;font-size:0.68rem!important;font-weight:500!important;color:var(--t3)!important;text-transform:uppercase!important;letter-spacing:0.10em!important;padding:11px 14px!important;border-bottom:2px solid transparent!important;background:transparent!important;margin-bottom:-2px!important;}
button[role="tab"][aria-selected="true"]{color:var(--blue)!important;border-bottom-color:var(--blue)!important;font-weight:600!important;}
div[data-testid="stExpander"]{background:var(--sur)!important;border:1px solid var(--ln)!important;border-radius:4px!important;}
div[data-testid="stExpander"] summary{font-family:var(--mono)!important;font-size:0.72rem!important;color:var(--t2)!important;}
.stButton button{font-family:var(--mono)!important;font-size:0.68rem!important;letter-spacing:0.08em!important;text-transform:uppercase!important;border-radius:4px!important;border:1.5px solid var(--ln2)!important;background:var(--sur)!important;color:var(--t2)!important;padding:6px 14px!important;transition:all 0.15s!important;}
.stButton button:hover{border-color:var(--blue)!important;color:var(--blue)!important;background:var(--bluebg)!important;}
div[data-testid="stMetricValue"]{font-family:var(--mono)!important;color:var(--t1)!important;font-size:1.5rem!important;font-weight:600!important;}
div[data-testid="stMetricLabel"]{font-family:var(--sans)!important;font-size:0.58rem!important;color:var(--t3)!important;text-transform:uppercase!important;letter-spacing:0.12em!important;}
div[data-testid="stAlert"]{border-radius:4px!important;font-family:var(--mono)!important;font-size:0.72rem!important;}
.ctrl{background:var(--sur);border-bottom:2px solid var(--ln);padding:10px 24px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px;}
.ctrl-id{display:flex;align-items:center;gap:10px;flex-wrap:wrap;}
.ctrl-logo{font-family:var(--mono);font-size:0.88rem;font-weight:600;color:var(--t1);}
.ctrl-proj{font-family:var(--mono);font-size:0.70rem;color:var(--blue);background:var(--bluebg);border:1px solid var(--bluebd);border-radius:4px;padding:3px 10px;}
.ctrl-stats{font-family:var(--mono);font-size:0.65rem;color:var(--t3);display:flex;align-items:center;gap:8px;}
.sh{display:flex;align-items:center;gap:10px;margin:16px 0 8px;}
.sh-lbl{font-family:var(--sans);font-size:0.68rem;font-weight:600;color:var(--t2);text-transform:uppercase;letter-spacing:0.10em;white-space:nowrap;}
.sh-line{flex:1;height:1px;background:var(--ln);}
.sc{background:var(--sur);border:1px solid var(--ln);border-top:3px solid var(--blue);border-radius:6px;padding:12px 16px;}
.sc.g{border-top-color:var(--passbd);} .sc.r{border-top-color:var(--failbd);} .sc.a{border-top-color:var(--warnbd);}
.sc-lbl{font-family:var(--mono);font-size:0.58rem;color:var(--t3);text-transform:uppercase;letter-spacing:0.12em;margin-bottom:4px;}
.sc-val{font-family:var(--mono);font-size:1.35rem;color:var(--t1);font-weight:600;line-height:1.1;}
.sc-sub{font-family:var(--sans);font-size:0.60rem;color:var(--t4);margin-top:3px;}
.gm{background:var(--sur);border:1px solid var(--ln);border-left:3px solid var(--ln2);border-radius:0 4px 4px 0;padding:9px 12px;margin:4px 0;}
.gm.p{border-left-color:var(--passbd);} .gm.f{border-left-color:var(--failbd);} .gm.w{border-left-color:var(--warnbd);}
.gm-hdr{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:5px;}
.gm-name{font-family:var(--mono);font-size:0.63rem;color:var(--t3);text-transform:uppercase;letter-spacing:0.10em;}
.gm-score{font-family:var(--mono);font-size:0.88rem;font-weight:600;}
.gm-score.p{color:var(--pass);} .gm-score.f{color:var(--fail);} .gm-score.w{color:var(--warn);}
.gm-track{height:3px;background:var(--sur3);border-radius:2px;position:relative;}
.gm-fill{height:100%;border-radius:2px;}
.gm-fill.p{background:var(--passbd);} .gm-fill.f{background:var(--failbd);} .gm-fill.w{background:var(--warnbd);}
.gm-tick{position:absolute;top:-3px;width:1.5px;height:9px;background:var(--amber);}
.gm-foot{font-size:0.60rem;color:var(--t4);margin-top:3px;font-family:var(--mono);}
.sr{display:flex;align-items:center;gap:10px;padding:7px 12px;border-bottom:1px solid var(--ln);font-family:var(--mono);font-size:0.68rem;}
.sr:last-child{border-bottom:none;} .sr:nth-child(even){background:var(--sur2);}
.sr-dot{width:5px;height:5px;border-radius:50%;background:var(--t5);flex-shrink:0;}
.cw{border:1px solid var(--failbd);border-radius:4px;overflow:hidden;}
.ch{background:var(--failbg);padding:7px 12px;font-family:var(--mono);font-size:0.60rem;color:var(--fail);text-transform:uppercase;letter-spacing:0.12em;font-weight:600;}
.cr{display:flex;align-items:flex-start;gap:10px;padding:8px 12px;border-top:1px solid var(--ln);background:var(--sur);}
.cr:nth-child(even){background:var(--sur2);}
.cr-idx{font-family:var(--mono);font-size:0.62rem;color:var(--failbd);min-width:28px;font-weight:600;}
.cr-title{font-family:var(--mono);font-size:0.70rem;color:var(--t2);}
.cr-rule{font-family:var(--sans);font-size:0.63rem;color:var(--t4);font-style:italic;margin-top:2px;}
.fp-box{background:var(--warnbg);border:1px solid var(--warnbd);border-left:4px solid var(--amber);border-radius:4px;padding:12px 16px;margin:8px 0;}
.fp-hdr{font-family:var(--mono);font-size:0.60rem;color:var(--amber);text-transform:uppercase;letter-spacing:0.14em;font-weight:600;margin-bottom:6px;}
.fp-body{font-family:var(--sans);font-size:0.78rem;color:var(--t2);line-height:1.6;}
.fc{background:var(--sur);border:1px solid var(--ln);border-radius:6px;overflow:hidden;margin-bottom:10px;}
.fc-cap{font-family:var(--mono);font-size:0.60rem;color:var(--t3);padding:6px 10px;background:var(--sur2);border-top:1px solid var(--ln);}
.pt{width:100%;border-collapse:collapse;font-family:var(--mono);font-size:0.68rem;}
.pt th{text-align:left;padding:8px 12px;border-bottom:2px solid var(--ln2);color:var(--t3);font-size:0.60rem;text-transform:uppercase;letter-spacing:0.10em;background:var(--sur2);}
.pt td{padding:8px 12px;border-bottom:1px solid var(--ln);color:var(--t2);vertical-align:middle;}
.pt tr:hover td{background:var(--bluebg);} .pt tr.act td{background:var(--bluebg);} .pt tr.act td:first-child{border-left:3px solid var(--blue);}
.badge{display:inline-block;font-family:var(--mono);font-size:0.58rem;font-weight:600;padding:2px 7px;border-radius:3px;text-transform:uppercase;letter-spacing:0.06em;}
.b-bl{background:var(--bluebg);color:var(--blue);border:1px solid var(--bluebd);}
.b-gn{background:var(--passbg);color:var(--pass);border:1px solid var(--passbd);}
.b-am{background:var(--warnbg);color:var(--warn);border:1px solid var(--warnbd);}
.b-rd{background:var(--failbg);color:var(--fail);border:1px solid var(--failbd);}
.b-gy{background:var(--sur2);color:var(--t3);border:1px solid var(--ln2);}
.dot{display:inline-block;border-radius:50%;}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.35}}
.pulsing{animation:pulse 2s ease-in-out infinite;}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

# ── File readers ──────────────────────────────────────────────────────────────

def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""

def _yaml(p: Path) -> dict[str, Any]:
    if not p.exists(): return {}
    import yaml
    with open(p) as f: return yaml.safe_load(f) or {}

def _sv(text: str) -> dict[str, str]:
    r: dict[str, str] = {}
    for line in text.splitlines():
        if ":" in line and not line.startswith("#"):
            k, _, v = line.partition(":")
            r[k.strip()] = v.strip()
    return r

def _dead_ends(text: str) -> list[dict[str, str]]:
    out = []
    for b in re.split(r"\n## DEAD END", text)[1:]:
        t = re.match(r"\s*\d+\s*[—–-]\s*(.+)", b)
        r = re.search(r"\*\*Do NOT repeat\*\*:\s*(.+)", b)
        out.append({"title": t.group(1).strip() if t else "Unknown",
                    "rule": r.group(1).strip() if r else ""})
    return out

def _log_entries(text: str, max_n: int = 15) -> list[str]:
    return [p.strip() for p in re.split(r"\n---\n", text)
            if p.strip() and "## Turn" in p][-max_n:]

def _critic_scores(text: str) -> dict[str, float]:
    s: dict[str, float] = {}
    for i in range(1, 5):
        m = re.search(rf"gate_{i}[^:]*:\s*([0-9.]+)", text, re.IGNORECASE)
        if m: s[f"Gate {i}"] = float(m.group(1))
    return s

def _find_report(base: Path) -> str:
    for p in base.rglob("REPORT.md"):
        return p.read_text(encoding="utf-8")
    return ""

def _find_figures(exp_dir: Path) -> list[Path]:
    d = exp_dir / "figures"
    if not d.exists(): return []
    return sorted([p for p in d.iterdir()
                   if p.suffix.lower() in (".png", ".svg", ".jpg", ".jpeg")],
                  key=lambda p: p.stat().st_mtime, reverse=True)

def _detect_experiment(cfg: dict) -> str | None:
    name = cfg.get("project", {}).get("name", "")
    for k in EXPERIMENT_CATALOG:
        if k in name or name in k: return k
    return None

def _time_ago(mtime: float) -> str:
    d = time.time() - mtime
    if d < 10: return "just now"
    if d < 60: return f"{int(d)}s ago"
    if d < 3600: return f"{int(d/60)}m ago"
    return f"{int(d/3600)}h ago"

def _detect_project_dir() -> Path:
    for p in [Path.cwd(), Path.cwd().parent,
              Path(__file__).parent.parent,
              Path(__file__).parent.parent / "chp-test-run"]:
        if (p / "config.yaml").exists(): return p
    return Path.cwd()

# ── HTML helpers ──────────────────────────────────────────────────────────────

def _sh(label: str) -> str:
    return (f'<div class="sh"><span class="sh-lbl">{label}</span>'
            f'<div class="sh-line"></div></div>')

def _gate_html(key: str, score: float) -> str:
    names = {"Gate 1": ("G1 - FROZEN COMPLIANCE", 1.0),
             "Gate 2": ("G2 - ARCHITECTURE", 0.85),
             "Gate 3": ("G3 - SCIENTIFIC VALIDITY", 0.85),
             "Gate 4": ("G4 - DRIFT CHECK", 0.85)}
    name, thresh = names.get(key, (key, 0.85))
    cls = "p" if score >= thresh else ("w" if score >= thresh - 0.05 else "f")
    pct = min(score * 100, 100)
    return (f'<div class="gm {cls}"><div class="gm-hdr">'
            f'<span class="gm-name">{name}</span>'
            f'<span class="gm-score {cls}">{score:.2f}</span></div>'
            f'<div class="gm-track"><div class="gm-fill {cls}" style="width:{pct}%"></div>'
            f'<div class="gm-tick" style="left:{thresh*100:.0f}%"></div></div>'
            f'<div class="gm-foot">threshold {thresh}</div></div>')

def _mode_badge(mode: str) -> str:
    m = mode.upper()
    if "DONE" in m or "COMPLETE" in m: return '<span class="badge b-gn">Complete</span>'
    if "EXPLORATION" in m: return '<span class="badge b-am">Exploration</span>'
    if "EXIT" in m: return '<span class="badge b-rd">Exit</span>'
    return '<span class="badge b-bl">Validation</span>'

def _empty_box(msg: str, sub: str = "") -> str:
    s = f'<br><span style="font-size:0.60rem;">{sub}</span>' if sub else ""
    return (f'<div style="font-family:var(--mono);font-size:0.68rem;color:var(--t4);'
            f'text-align:center;padding:24px;border:1px dashed var(--ln2);'
            f'border-radius:4px;">{msg}{s}</div>')

# ── MAIN ──────────────────────────────────────────────────────────────────────

def main() -> None:
    project_dir = _detect_project_dir()
    config      = _yaml(project_dir / "config.yaml")
    sv          = _sv(_read(project_dir / "state_vector.md"))
    log_text    = _read(project_dir / "innovation_log.md")
    dead_text   = _read(project_dir / "dead_ends.md")
    report_text = _find_report(project_dir)
    experiment  = _detect_experiment(config)
    project     = config.get("project", {}).get("name", "CHP Project")
    turn        = sv.get("TURN", "0")
    mode        = sv.get("MODE", "VALIDATION")
    flags       = sv.get("OPEN_FLAGS", "none")
    de_count    = len(_dead_ends(dead_text))
    flag_count  = 0 if flags.lower() == "none" else len(flags.split(","))
    fig_count   = 0
    if experiment:
        ed = project_dir / "experiments" / experiment
        if ed.exists(): fig_count = len(_find_figures(ed))

    # Control panel header
    de_col  = "color:var(--fail)" if de_count  > 0 else "color:var(--t4)"
    fig_col = "color:var(--blue)" if fig_count > 0 else "color:var(--t4)"
    st.markdown(
        f'<div class="ctrl"><div class="ctrl-id">'
        f'<span class="ctrl-logo">CHP</span>'
        f'<span class="ctrl-proj">{project}</span>'
        f'<div class="ctrl-stats">T:<strong style="color:var(--t1)">{turn}</strong>'
        f'&nbsp;·&nbsp;{_mode_badge(mode)}'
        f'&nbsp;·&nbsp;<span style="{de_col}"><strong>{de_count}</strong> dead ends</span>'
        f'&nbsp;·&nbsp;<span style="{fig_col}"><strong>{fig_count}</strong> figs</span>'
        f'</div></div>'
        f'<span style="font-family:var(--mono);font-size:0.60rem;color:var(--t4);">'
        f'auto-refresh {REFRESH_SECONDS}s &nbsp;·&nbsp; {time.strftime("%H:%M:%S")}'
        f'</span></div>', unsafe_allow_html=True)

    # Action buttons
    b1, b2, b3, b4, b5, b6, b7 = st.columns([1, 1, 1.8, 1, 1, 1.6, 1])
    with b1:
        if st.button("Run Loop", use_container_width=True, key="btn_run"):
            try:
                kw = {"creationflags": subprocess.CREATE_NEW_CONSOLE} if sys.platform == "win32" else {}
                subprocess.Popen(["chp", "run"], cwd=str(project_dir), **kw)
                st.toast("Loop started")
            except FileNotFoundError:
                st.error("chp not found - activate your venv")
    with b2:
        if st.button("Stop Loop", use_container_width=True, key="btn_stop"):
            (project_dir / "STOP").touch()
            st.toast("STOP file created")
    with b3:
        sel = st.selectbox("exp", ["-- run experiment --"] + list(EXPERIMENT_CATALOG.keys()),
                           key="ctrl_exp", label_visibility="collapsed")
        if sel != "-- run experiment --":
            if st.button("Run This Experiment", use_container_width=True, key="btn_exp"):
                try:
                    kw = {"creationflags": subprocess.CREATE_NEW_CONSOLE} if sys.platform == "win32" else {}
                    subprocess.Popen(["chp", "run", "--experiment", sel], cwd=str(project_dir), **kw)
                    st.toast(f"Started: {sel}")
                except FileNotFoundError:
                    st.error("chp not found")
    with b4:
        if st.button("Export Paper", use_container_width=True, key="btn_export"):
            _export(config, log_text, dead_text, sv, report_text)
            st.toast("Saved: paper_appendix.md")
    with b5:
        if st.button("Refresh", use_container_width=True, key="btn_refresh"):
            st.rerun()
    with b6:
        if st.button("Download All Figures", use_container_width=True, key="btn_dl"):
            buf = io.BytesIO()
            count = total = 0
            with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
                for exp_name in EXPERIMENT_CATALOG:
                    fd = project_dir / "experiments" / exp_name / "figures"
                    if fd.exists():
                        for fig in fd.glob("*"):
                            if fig.suffix.lower() in (".png", ".svg", ".jpg", ".jpeg"):
                                zf.write(fig, f"{exp_name}/{fig.name}")
                                count += 1
                                total += fig.stat().st_size
            buf.seek(0)
            if count > 0:
                st.download_button(f"Save ZIP ({count} figs, {total//1024} KB)",
                                   data=buf, file_name="chp_figures.zip",
                                   mime="application/zip", key="btn_dl2",
                                   use_container_width=True)
            else:
                st.warning("No figures found yet")
    with b7:
        if st.button("Clear Stop", use_container_width=True, key="btn_clr"):
            stop = project_dir / "STOP"
            if stop.exists(): stop.unlink(); st.toast("STOP removed")

    st.markdown('<div style="height:1px;background:var(--ln);margin:0 0 8px;"></div>',
                unsafe_allow_html=True)

    # Tabs
    tab_mon, tab_health, tab_report, tab_gallery = st.tabs([
        "Live Monitor", "Protocol Health", "Experiment Report", "Experiment Gallery"])

    # TAB 1 - LIVE MONITOR
    with tab_mon:
        m = mode.upper()
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            cls = "g" if ("DONE" in m or "COMPLETE" in m) else ("a" if "EXPLORATION" in m else "")
            st.markdown(f'<div class="sc {cls}"><div class="sc-lbl">Mode</div>'
                        f'<div class="sc-val" style="font-size:0.9rem;">{_mode_badge(mode)}</div>'
                        f'<div class="sc-sub">{mode.split("--")[0].strip()}</div></div>',
                        unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="sc"><div class="sc-lbl">Turn</div>'
                        f'<div class="sc-val">{turn}</div><div class="sc-sub">of 50 max</div></div>',
                        unsafe_allow_html=True)
        with c3:
            cls = "r" if de_count > 0 else ""
            st.markdown(f'<div class="sc {cls}"><div class="sc-lbl">Dead Ends</div>'
                        f'<div class="sc-val">{de_count}</div>'
                        f'<div class="sc-sub">Contraindications logged</div></div>',
                        unsafe_allow_html=True)
        with c4:
            cls = "a" if flag_count > 0 else ""
            st.markdown(f'<div class="sc {cls}"><div class="sc-lbl">Flags</div>'
                        f'<div class="sc-val">{flag_count}</div>'
                        f'<div class="sc-sub">{flags[:40]}</div></div>', unsafe_allow_html=True)

        st.markdown("")
        left, right = st.columns(2)
        with left:
            st.markdown(_sh("Critic Scorecard"), unsafe_allow_html=True)
            scores = _critic_scores(log_text)
            if scores:
                for k, v in scores.items():
                    st.markdown(_gate_html(k, v), unsafe_allow_html=True)
            else:
                st.markdown(_empty_box("awaiting build", "run chp run to start"),
                            unsafe_allow_html=True)
            st.markdown(_sh("Sigma-Gate Readings"), unsafe_allow_html=True)
            checks = config.get("gates", {}).get("anomaly_checks", [])
            if checks:
                html = '<div style="border:1px solid var(--ln);border-radius:4px;overflow:hidden;background:var(--sur);">'
                for ch in checks:
                    html += (f'<div class="sr"><div class="sr-dot"></div>'
                             f'<span style="flex:1;color:var(--t2);overflow:hidden;text-overflow:ellipsis;">{ch.get("metric","?")}</span>'
                             f'<span style="color:var(--t4);min-width:18px;text-align:center;">{ch.get("operator",">")}</span>'
                             f'<span style="color:var(--amber);font-weight:500;min-width:40px;">{ch.get("threshold",0)}</span>'
                             f'</div>')
                html += '</div>'
                st.markdown(html, unsafe_allow_html=True)
            st.markdown(_sh("Council Status"), unsafe_allow_html=True)
            recent = log_text[-3000:].upper()
            drift = "DRIFT:" in recent and any(x in recent for x in ["YES", "CONCERN", "RISK"])
            if drift:
                st.error("DRIFT flagged - re-read CHAIN_PROMPT.md")
            else:
                st.success("No drift detected")

        with right:
            st.markdown(_sh("Innovation Log"), unsafe_allow_html=True)
            entries = _log_entries(log_text)
            if entries:
                for entry in reversed(entries):
                    tm = re.match(r"## Turn (\d+)", entry)
                    label = f"Turn {tm.group(1)}" if tm else "Entry"
                    has_fp = "FALSE POSITIVE" in entry.upper()
                    with st.expander(f"{'FP: ' if has_fp else ''}{label}",
                                     expanded=(has_fp or entry == entries[-1])):
                        st.markdown(entry[:2000])
            else:
                st.markdown(_empty_box("no turns recorded", "run chp run to start"),
                            unsafe_allow_html=True)
            st.markdown(_sh("Contraindications"), unsafe_allow_html=True)
            des = _dead_ends(dead_text)
            if des:
                html = '<div class="cw"><div class="ch">Contraindications - do not repeat</div>'
                for i, de in enumerate(des):
                    rule = f'<div class="cr-rule">-- {de["rule"]}</div>' if de["rule"] else ""
                    html += (f'<div class="cr"><span class="cr-idx">C{i+1:02d}</span>'
                             f'<div><div class="cr-title">{de["title"]}</div>{rule}</div></div>')
                html += '</div>'
                st.markdown(html, unsafe_allow_html=True)
            else:
                st.markdown(_empty_box("no contraindications logged"), unsafe_allow_html=True)
            if experiment:
                ed = project_dir / "experiments" / experiment
                figs = _find_figures(ed) if ed.exists() else []
                if figs:
                    ago = _time_ago(figs[0].stat().st_mtime)
                    st.markdown(_sh(f"Live Figures - {len(figs)} - {ago}"),
                                unsafe_allow_html=True)
                    cols = st.columns(min(len(figs), 3))
                    for i, fig in enumerate(figs[:3]):
                        with cols[i]:
                            st.image(str(fig), use_container_width=True)
                            st.markdown(
                                f'<div style="text-align:center;font-family:var(--mono);'
                                f'font-size:0.55rem;color:var(--t3);">{fig.stem}</div>',
                                unsafe_allow_html=True)

    # TAB 2 - PROTOCOL HEALTH
    with tab_health:
        _render_protocol_health(project_dir)

    # TAB 3 - EXPERIMENT REPORT
    with tab_report:
        if report_text:
            st.markdown(_sh("Experiment Report"), unsafe_allow_html=True)
            for section in re.split(r"\n## ", report_text):
                if "FALSE POSITIVE" in section.upper()[:30]:
                    lines = section.strip().splitlines()
                    body = "\n".join(lines[1:]).strip()
                    st.markdown(
                        f'<div class="fp-box"><div class="fp-hdr">False Positive Story</div>'
                        f'<div class="fp-body">{body}</div></div>',
                        unsafe_allow_html=True)
                    break
            st.markdown(report_text)
            if experiment:
                ed = project_dir / "experiments" / experiment
                figs = _find_figures(ed) if ed.exists() else []
                if figs:
                    st.markdown(_sh("Publication Figures"), unsafe_allow_html=True)
                    fc = st.columns(2)
                    for i, fig in enumerate(figs):
                        with fc[i % 2]:
                            st.markdown('<div class="fc">', unsafe_allow_html=True)
                            st.image(str(fig), use_container_width=True)
                            desc = FIGURE_DESCRIPTIONS.get(fig.stem,
                                                           fig.stem.replace("_", " ").title())
                            st.markdown(f'<div class="fc-cap">{i+1}. {desc}</div></div>',
                                        unsafe_allow_html=True)
        else:
            st.markdown(_empty_box("no report generated yet",
                                   "complete the experiment to see results"),
                        unsafe_allow_html=True)
        st.markdown("")
        if st.button("Export Paper Appendix", use_container_width=True, key="btn_exp_tab"):
            _export(config, log_text, dead_text, sv, report_text)
            st.success("Exported to paper_appendix.md")

    # TAB 4 - EXPERIMENT GALLERY
    with tab_gallery:
        st.markdown(_sh("Experiment Registry - 9 Protocols"), unsafe_allow_html=True)
        if "selected_experiment" not in st.session_state:
            st.session_state.selected_experiment = None
        rows = ""
        for key, meta in EXPERIMENT_CATALOG.items():
            active = key == experiment
            ed = project_dir / "experiments" / key
            nfigs = len(_find_figures(ed)) if (ed / "figures").exists() else 0
            fig_td = (f'<span style="color:var(--blue);">{nfigs}</span>'
                      if nfigs else '<span style="color:var(--t5);">-</span>')
            if active:
                status = '<span class="badge b-gn">Active</span>'
                tr_cls = "act"
            elif (ed / "REPORT.md").exists():
                status = '<span class="badge b-bl">Done</span>'
                tr_cls = ""
            else:
                status = '<span class="badge b-gy">-</span>'
                tr_cls = ""
            rows += (f'<tr class="{tr_cls}"><td>{meta["icon"]}</td>'
                     f'<td><strong>{key}</strong></td>'
                     f'<td>{meta["domain"]}</td>'
                     f'<td style="font-size:0.62rem;color:var(--t3);">{meta["catches"]}</td>'
                     f'<td>{fig_td}</td><td>{status}</td></tr>')
        st.markdown(
            f'<div style="border:1px solid var(--ln);border-radius:6px;overflow:hidden;">'
            f'<table class="pt"><thead><tr><th></th><th>Experiment</th><th>Domain</th>'
            f'<th>Prior drift catches</th><th>Figs</th><th>Status</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>', unsafe_allow_html=True)
        st.markdown("")
        vcols = st.columns(3)
        for i, key in enumerate(EXPERIMENT_CATALOG):
            with vcols[i % 3]:
                if st.button(f"View {key}", key=f"btn_{key}", use_container_width=True):
                    st.session_state.selected_experiment = key
        selected = st.session_state.selected_experiment
        if selected:
            st.markdown('<div style="border-top:2px solid var(--ln);margin:16px 0 12px;"></div>',
                        unsafe_allow_html=True)
            st.markdown(_sh(f"{EXPERIMENT_CATALOG[selected]['icon']}  {selected}"),
                        unsafe_allow_html=True)
            exp_dir = next((d for d in [project_dir / "experiments" / selected,
                                         Path(__file__).parent.parent / "experiments" / selected]
                            if d.exists()), None)
            if exp_dir:
                dtabs = st.tabs(["Spec", "Frozen Rules", "Dead Ends", "Report", "Figures"])
                with dtabs[0]:
                    sp = exp_dir / "spec.md"
                    st.markdown(sp.read_text(encoding="utf-8")) if sp.exists() else st.caption("No spec.md")
                with dtabs[1]:
                    fr = exp_dir / "frozen"
                    if fr.exists():
                        for fp in sorted(fr.glob("*.md")):
                            with st.expander(fp.name, expanded=True):
                                st.markdown(fp.read_text(encoding="utf-8")[:5000])
                with dtabs[2]:
                    df = exp_dir / "dead_ends.md"
                    if df.exists():
                        des2 = _dead_ends(df.read_text(encoding="utf-8"))
                        if des2:
                            html = '<div class="cw"><div class="ch">Contraindications</div>'
                            for i, de in enumerate(des2):
                                rule = f'<div class="cr-rule">-- {de["rule"]}</div>' if de["rule"] else ""
                                html += (f'<div class="cr"><span class="cr-idx">C{i+1:02d}</span>'
                                         f'<div><div class="cr-title">{de["title"]}</div>{rule}</div></div>')
                            html += '</div>'
                            st.markdown(html, unsafe_allow_html=True)
                with dtabs[3]:
                    rp = exp_dir / "REPORT.md"
                    if rp.exists(): st.markdown(rp.read_text(encoding="utf-8"))
                    else: st.markdown(_empty_box("experiment not yet completed"), unsafe_allow_html=True)
                with dtabs[4]:
                    figs = _find_figures(exp_dir)
                    if figs:
                        st.markdown(
                            f'<div style="font-family:var(--mono);font-size:0.68rem;'
                            f'color:var(--t3);margin-bottom:10px;">'
                            f'{len(figs)} figures - most recent: {_time_ago(figs[0].stat().st_mtime)}</div>',
                            unsafe_allow_html=True)
                        fc = st.columns(2)
                        for i, fig in enumerate(figs):
                            with fc[i % 2]:
                                st.markdown('<div class="fc">', unsafe_allow_html=True)
                                st.image(str(fig), use_container_width=True)
                                desc = FIGURE_DESCRIPTIONS.get(fig.stem,
                                                               fig.stem.replace("_", " ").title())
                                sz = fig.stat().st_size / 1024
                                mod = datetime.fromtimestamp(fig.stat().st_mtime).strftime("%H:%M:%S")
                                st.markdown(f'<div class="fc-cap">{desc}<br>'
                                            f'<span style="color:var(--t4);">{sz:.0f} KB - {mod}</span>'
                                            f'</div></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(_empty_box(f"no figures yet",
                                               f"run: chp run --experiment {selected}"),
                                    unsafe_allow_html=True)
            else:
                st.warning(f"Directory not found for {selected}")

    st.markdown(
        '<div style="border-top:1px solid var(--ln);margin-top:24px;padding:10px 0;'
        'text-align:center;font-family:var(--mono);font-size:0.58rem;color:var(--t4);">'
        'Context Hacking Protocol v0.2 - 9-Layer Anti-Drift Framework - '
        '<a href="https://github.com/kepiCHelaSHen/context-hacking" '
        'style="color:var(--blue);">GitHub</a></div>', unsafe_allow_html=True)

    time.sleep(REFRESH_SECONDS)
    st.rerun()


# ── Protocol Health - CONTAINED 2-column layout ───────────────────────────────

def _render_protocol_health(project_dir: Path) -> None:
    import plotly.graph_objects as go

    telemetry_path = project_dir / ".chp" / "telemetry.json"

    CHART = dict(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#FAFBFC",
        font=dict(family="IBM Plex Mono, monospace", color="#6B7280", size=10),
        margin=dict(l=44, r=16, t=32, b=32), height=195,
        legend=dict(bgcolor="rgba(0,0,0,0)",
                    font=dict(family="IBM Plex Mono", size=9, color="#9CA3AF"),
                    orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    AX = dict(gridcolor="#EEF0F6", linecolor="#E2E5EF", zerolinecolor="#E2E5EF",
              tickfont=dict(family="IBM Plex Mono", size=9, color="#9CA3AF"), showgrid=True)

    # Contained header
    st.markdown(
        '<div style="max-width:960px;margin:0 auto;">'
        + _sh("Protocol Health - Is the loop learning?")
        + '<p style="font-size:0.73rem;color:var(--t3);margin:-4px 0 14px;">'
        'Healthy loop: declining drift - improving gate scores - '
        'faster turns - fewer fix cycles</p>',
        unsafe_allow_html=True)

    if not telemetry_path.exists():
        for lbl, val, sub in [
            ("Tokens / Line", "--", "lower = more efficient"),
            ("False Pos. Caught", "--", "killed before merge"),
            ("Dead Ends Avoided", "--", "mistakes not repeated"),
            ("First-Try Pass", "--", "no fix cycle needed"),
        ]:
            st.markdown(
                f'<div class="sc" style="margin-bottom:8px;">'
                f'<div class="sc-lbl">{lbl}</div>'
                f'<div class="sc-val" style="color:var(--t4);">{val}</div>'
                f'<div class="sc-sub">{sub}</div></div>', unsafe_allow_html=True)
        st.markdown(_empty_box("awaiting telemetry", "run chp run --method api to record")
                    + '</div>', unsafe_allow_html=True)
        return

    try:
        data = json.loads(telemetry_path.read_text(encoding="utf-8"))
        turns_data = data.get("turns", [])
    except Exception:
        st.error("Failed to load telemetry.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    if not turns_data:
        st.markdown('</div>', unsafe_allow_html=True)
        return

    total_tokens = sum(t.get("tokens_total", 0) for t in turns_data)
    total_lines  = sum(t.get("lines_written", 0) for t in turns_data)
    total_time   = sum(t.get("duration_seconds", 0) for t in turns_data)
    n_fp   = sum(1 for t in turns_data if t.get("false_positive_caught"))
    n_de   = sum(t.get("dead_ends_avoided", 0) for t in turns_data)
    tested = [t for t in turns_data if t.get("tests_passed", 0) + t.get("tests_failed", 0) > 0]
    ftr    = sum(1 for t in tested if t.get("tests_passed_first_try")) / max(len(tested), 1)
    tpl    = round(total_tokens / max(total_lines, 1), 1)

    # Stat cards - 4 col
    c1, c2, c3, c4 = st.columns(4)
    for col, lbl, val, sub in [
        (c1, "Tokens / Line",     f"{tpl}",     "lower = more efficient"),
        (c2, "False Pos. Caught", str(n_fp),    "killed before merge"),
        (c3, "Dead Ends Avoided", str(n_de),    "mistakes not repeated"),
        (c4, "First-Try Pass",    f"{ftr:.0%}", "no fix cycle needed"),
    ]:
        with col:
            st.markdown(f'<div class="sc"><div class="sc-lbl">{lbl}</div>'
                        f'<div class="sc-val">{val}</div>'
                        f'<div class="sc-sub">{sub}</div></div>', unsafe_allow_html=True)

    c5, c6, c7, c8 = st.columns(4)
    for col, lbl, val in [
        (c5, "Total Tokens", f"{total_tokens:,}"),
        (c6, "Lines Built",  f"{total_lines:,}"),
        (c7, "Total Time",   f"{total_time/60:.1f} min"),
        (c8, "Turns",        str(len(turns_data))),
    ]:
        with col:
            st.markdown(f'<div class="sc" style="border-top-color:var(--ln2);padding:9px 14px;">'
                        f'<div class="sc-lbl">{lbl}</div>'
                        f'<div class="sc-val" style="font-size:1.05rem;">{val}</div></div>',
                        unsafe_allow_html=True)

    # Contained section header
    st.markdown(
        '<div style="max-width:960px;margin:18px auto 8px;">'
        + _sh("Trends Over Time") + '</div>',
        unsafe_allow_html=True)

    turn_nums = [t.get("turn", i + 1) for i, t in enumerate(turns_data)]
    fp_turns  = [t["turn"] for t in turns_data if t.get("false_positive_caught")]

    def _fp_markers(fig: go.Figure) -> None:
        for tn in fp_turns:
            fig.add_vline(x=tn, line_color="#D97706", line_width=1, line_dash="dot")
            fig.add_annotation(x=tn, text="FP", showarrow=False,
                               font=dict(size=8, color="#D97706"),
                               yref="paper", y=1.01)

    # Row 1: Tokens | Gate scores (2-col)
    left, right = st.columns(2)
    tokens = [t.get("tokens_total", 0) for t in turns_data]
    with left:
        if any(x > 0 for x in tokens):
            avgs = [sum(tokens[max(0,i-2):i+1])/len(tokens[max(0,i-2):i+1])
                    for i in range(len(tokens))]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=turn_nums, y=tokens, name="tokens",
                                     mode="lines+markers",
                                     line=dict(color="#3B82F6", width=1.5),
                                     marker=dict(size=5)))
            fig.add_trace(go.Scatter(x=turn_nums, y=avgs, name="3T avg",
                                     mode="lines",
                                     line=dict(color="#D97706", width=1, dash="dot")))
            _fp_markers(fig)
            fig.update_layout(title="Tokens per turn", xaxis=AX, yaxis=AX, **CHART)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown(_empty_box("no token data yet"), unsafe_allow_html=True)

    g1 = [t.get("gate_1_frozen", 0) for t in turns_data]
    g3 = [t.get("gate_3_scientific", 0) for t in turns_data]
    with right:
        if any(x > 0 for x in g1):
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=turn_nums, y=g1, name="G1 Frozen",
                                     mode="lines+markers",
                                     line=dict(color="#10B981", width=1.5),
                                     marker=dict(size=5)))
            fig.add_trace(go.Scatter(x=turn_nums, y=g3, name="G3 Scientific",
                                     mode="lines+markers",
                                     line=dict(color="#F59E0B", width=1.5),
                                     marker=dict(size=5)))
            fig.add_hline(y=0.85, line_dash="dot", line_color="#D97706", line_width=1,
                          annotation_text="0.85",
                          annotation_font=dict(size=8, color="#D97706"),
                          annotation_position="bottom right")
            _fp_markers(fig)
            fig.update_layout(title="Critic gate scores", xaxis=AX,
                              yaxis=dict(**AX, range=[0.5, 1.05]), **CHART)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown(_empty_box("no gate score data yet"), unsafe_allow_html=True)

    # Row 2: Time lollipop | Key events (2-col)
    left2, right2 = st.columns(2)
    times = [t.get("duration_seconds", 0) for t in turns_data]
    with left2:
        if any(x > 0 for x in times):
            clrs = ["#10B981" if x < 300 else "#F59E0B" if x < 600 else "#EF4444"
                    for x in times]
            fig = go.Figure()
            for i, (tn, tv) in enumerate(zip(turn_nums, times)):
                fig.add_trace(go.Scatter(x=[tn, tn], y=[0, tv/60], mode="lines",
                                         line=dict(color=clrs[i], width=2),
                                         showlegend=False))
            fig.add_trace(go.Scatter(x=turn_nums, y=[t/60 for t in times],
                                     mode="markers",
                                     marker=dict(color=clrs, size=9,
                                                 line=dict(width=1.5, color="white")),
                                     showlegend=False))
            fig.update_layout(title="Time per turn (min)", xaxis=AX, yaxis=AX, **CHART)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown(_empty_box("no timing data yet"), unsafe_allow_html=True)

    with right2:
        st.markdown(_sh("Key Events"), unsafe_allow_html=True)
        has_events = False
        for t in turns_data:
            n = t.get("turn", "?")
            if t.get("false_positive_caught"):
                has_events = True
                desc = t.get("false_positive_description", "see innovation log")
                if len(desc) > 120: desc = desc[:117] + "..."
                st.markdown(
                    f'<div class="fp-box" style="padding:8px 12px;margin:4px 0;">'
                    f'<div class="fp-hdr" style="margin-bottom:2px;">'
                    f'Turn {n} - False Positive Caught</div>'
                    f'<div class="fp-body" style="font-size:0.70rem;">{desc}</div></div>',
                    unsafe_allow_html=True)
            if t.get("anomaly"):
                has_events = True
                st.markdown(
                    f'<div style="background:var(--failbg);border-left:3px solid '
                    f'var(--failbd);padding:7px 12px;margin:4px 0;'
                    f'border-radius:0 4px 4px 0;font-family:var(--mono);'
                    f'font-size:0.68rem;color:var(--fail);">'
                    f'Turn {n}: ANOMALY - sigma-gate failed</div>',
                    unsafe_allow_html=True)
        if not has_events:
            st.markdown(_empty_box("clean run", "no anomalies or false positives"),
                        unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ── Export ────────────────────────────────────────────────────────────────────

def _export(cfg: dict, log: str, dead: str, sv: dict, report: str) -> None:
    out = ["# CHP Paper Appendix\n",
           f"Project: {cfg.get('project', {}).get('name', '?')}\n",
           f"Generated: {time.strftime('%Y-%m-%d %H:%M')}\n",
           "\n## State Vector\n",
           *[f"- **{k}**: {v}\n" for k, v in sv.items()],
           "\n## Innovation Log\n", log, "\n## Dead Ends\n", dead]
    if report: out += ["\n## Experiment Report\n", report]
    Path("paper_appendix.md").write_text("\n".join(out), encoding="utf-8")


if __name__ == "__main__":
    main()
