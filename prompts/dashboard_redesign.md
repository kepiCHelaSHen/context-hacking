<!-- STATUS: run | DATE: 2026-03-21 | OUTPUT: dashboard/app.py white theme -->
---
name: chp-dashboard-redesign
description: "Fix dashboard/app.py: white clinical theme + control panel at top."
tools: Read, Write, Edit, Bash
---

# CHP Dashboard Fix — Two Jobs Only

You have exactly TWO jobs in this task. Do not do anything else.

JOB 1: Replace the dark theme with a clean white clinical theme.
JOB 2: Add a control panel bar at the very top of the dashboard.

================================================================================
STEP 0 — READ THE FILE FIRST
================================================================================

Read dashboard/app.py in full before touching anything.

================================================================================
JOB 1: WHITE CLINICAL THEME
================================================================================

The current CSS has dark backgrounds (#09090E, #0D0F16, etc).
Replace the ENTIRE <style> block with this exact CSS:

```css
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;500;600&family=Inter:wght@300;400;500;600&display=swap');

:root {
    --bg:        #F8F9FC;
    --surface:   #FFFFFF;
    --surface-2: #F3F4F8;
    --surface-3: #E9EBF2;
    --line:      #E2E5EF;
    --line-2:    #C8CCDB;

    --text-1:    #0F1117;
    --text-2:    #374151;
    --text-3:    #6B7280;
    --text-4:    #9CA3AF;

    --blue:      #1D4ED8;
    --blue-bg:   #EFF6FF;
    --blue-line: #93C5FD;

    --pass:      #065F46;
    --pass-bg:   #ECFDF5;
    --pass-line: #34D399;

    --fail:      #991B1B;
    --fail-bg:   #FEF2F2;
    --fail-line: #FCA5A5;

    --warn:      #92400E;
    --warn-bg:   #FFFBEB;
    --warn-line: #FCD34D;

    --mono: 'IBM Plex Mono', monospace;
    --sans: 'Inter', system-ui, sans-serif;
}

html, body, .main, .stApp {
    background-color: var(--bg) !important;
    font-family: var(--sans) !important;
    color: var(--text-1) !important;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* Tabs */
div[data-testid="stTabs"] > div:first-child {
    background: var(--surface) !important;
    border-bottom: 2px solid var(--line) !important;
    padding: 0 24px !important;
}
button[role="tab"] {
    font-family: var(--mono) !important;
    font-size: 0.70rem !important;
    color: var(--text-3) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.10em !important;
    padding: 12px 16px !important;
    border-bottom: 2px solid transparent !important;
    background: transparent !important;
    margin-bottom: -2px !important;
}
button[role="tab"][aria-selected="true"] {
    color: var(--blue) !important;
    border-bottom-color: var(--blue) !important;
    font-weight: 600 !important;
}

/* Expanders */
div[data-testid="stExpander"] {
    background: var(--surface) !important;
    border: 1px solid var(--line) !important;
    border-radius: 6px !important;
}
div[data-testid="stExpander"] summary {
    font-family: var(--mono) !important;
    font-size: 0.75rem !important;
    color: var(--text-2) !important;
}

/* Buttons */
.stButton button {
    font-family: var(--mono) !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    border-radius: 4px !important;
    border: 1.5px solid var(--line-2) !important;
    background: var(--surface) !important;
    color: var(--text-2) !important;
    transition: all 0.15s !important;
}
.stButton button:hover {
    border-color: var(--blue) !important;
    color: var(--blue) !important;
    background: var(--blue-bg) !important;
}

/* Metrics */
div[data-testid="stMetricValue"] {
    font-family: var(--mono) !important;
    color: var(--text-1) !important;
    font-size: 1.6rem !important;
    font-weight: 600 !important;
}
div[data-testid="stMetricLabel"] {
    font-family: var(--sans) !important;
    font-size: 0.62rem !important;
    color: var(--text-3) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.10em !important;
}

/* Alerts */
div[data-testid="stAlert"] {
    border-radius: 4px !important;
    font-family: var(--mono) !important;
    font-size: 0.75rem !important;
}

/* Scrollbars */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--line-2); border-radius: 3px; }

/* Component: stat card */
.stat-card {
    background: var(--surface);
    border: 1px solid var(--line);
    border-top: 3px solid var(--blue);
    border-radius: 6px;
    padding: 14px 18px;
    font-family: var(--mono);
}
.stat-card .label {
    font-size: 0.58rem;
    color: var(--text-3);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 4px;
}
.stat-card .value {
    font-size: 1.5rem;
    color: var(--text-1);
    font-weight: 600;
    line-height: 1.1;
}
.stat-card .sub {
    font-size: 0.62rem;
    color: var(--text-4);
    margin-top: 3px;
}

/* Component: gate meter */
.gate-meter {
    background: var(--surface);
    border: 1px solid var(--line);
    border-left: 3px solid var(--line-2);
    border-radius: 4px;
    padding: 10px 14px;
    margin: 4px 0;
    font-family: var(--mono);
}
.gate-meter.pass { border-left-color: var(--pass-line); }
.gate-meter.fail { border-left-color: var(--fail-line); }
.gate-meter.warn { border-left-color: var(--warn-line); }
.gate-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 6px;
}
.gate-name { font-size: 0.65rem; color: var(--text-3); text-transform: uppercase; letter-spacing: 0.10em; }
.gate-score { font-size: 0.90rem; font-weight: 600; }
.gate-score.pass { color: var(--pass); }
.gate-score.fail { color: var(--fail); }
.gate-score.warn { color: var(--warn); }
.gate-track {
    height: 4px;
    background: var(--surface-3);
    border-radius: 2px;
    position: relative;
}
.gate-fill {
    height: 100%;
    border-radius: 2px;
}
.gate-fill.pass { background: var(--pass-line); }
.gate-fill.fail { background: var(--fail-line); }
.gate-fill.warn { background: var(--warn-line); }

/* Component: section header */
.sec-head {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 20px 0 10px;
}
.sec-head-label {
    font-family: var(--sans);
    font-size: 0.72rem;
    font-weight: 600;
    color: var(--text-2);
    text-transform: uppercase;
    letter-spacing: 0.10em;
    white-space: nowrap;
}
.sec-head-line { flex: 1; height: 1px; background: var(--line); }

/* Component: control panel */
.control-panel {
    background: var(--surface);
    border-bottom: 2px solid var(--line);
    padding: 14px 28px;
    display: flex;
    align-items: center;
    gap: 16px;
    flex-wrap: wrap;
}
.control-panel-title {
    font-family: var(--mono);
    font-size: 0.80rem;
    font-weight: 600;
    color: var(--text-1);
    letter-spacing: 0.05em;
    margin-right: 8px;
}
.control-panel-project {
    font-family: var(--mono);
    font-size: 0.72rem;
    color: var(--blue);
    background: var(--blue-bg);
    border: 1px solid var(--blue-line);
    border-radius: 4px;
    padding: 3px 10px;
}
.control-panel-sep {
    color: var(--line-2);
    font-size: 1rem;
}
.control-panel-stat {
    font-family: var(--mono);
    font-size: 0.68rem;
    color: var(--text-3);
}
.control-panel-stat span {
    color: var(--text-1);
    font-weight: 600;
}

/* Component: dead end row */
.dead-row {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 9px 14px;
    border-bottom: 1px solid var(--line);
    background: var(--surface);
    font-family: var(--mono);
}
.dead-row:last-child { border-bottom: none; }
.dead-row:nth-child(even) { background: var(--surface-2); }
.dead-idx { font-size: 0.62rem; color: var(--fail); min-width: 28px; font-weight: 600; }
.dead-title { font-size: 0.72rem; color: var(--text-2); flex: 1; }
.dead-rule { font-size: 0.65rem; color: var(--text-4); font-style: italic; margin-top: 2px; }

/* Component: log entry */
.log-entry {
    border-left: 3px solid var(--line);
    background: var(--surface);
    padding: 10px 14px;
    margin: 6px 0;
    border-radius: 0 4px 4px 0;
    font-family: var(--mono);
    font-size: 0.70rem;
    color: var(--text-3);
}
.log-entry.latest { border-left-color: var(--blue); }
.log-entry.fp { border-left-color: var(--warn-line); background: var(--warn-bg); }

/* Component: fp callout */
.fp-callout {
    background: var(--warn-bg);
    border: 1px solid var(--warn-line);
    border-left: 4px solid #D97706;
    border-radius: 4px;
    padding: 14px 18px;
    margin: 8px 0;
    font-family: var(--sans);
    font-size: 0.80rem;
    color: var(--text-2);
    line-height: 1.6;
}
.fp-callout-header {
    font-family: var(--mono);
    font-size: 0.60rem;
    color: #D97706;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    margin-bottom: 8px;
    font-weight: 600;
}

/* Component: figure panel */
.fig-panel {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 6px;
    overflow: hidden;
}
.fig-caption {
    font-family: var(--mono);
    font-size: 0.62rem;
    color: var(--text-3);
    padding: 6px 10px;
    background: var(--surface-2);
    border-top: 1px solid var(--line);
    text-align: center;
}

/* Protocol table */
.proto-table {
    width: 100%;
    border-collapse: collapse;
    font-family: var(--mono);
    font-size: 0.70rem;
}
.proto-table th {
    text-align: left;
    padding: 9px 14px;
    border-bottom: 2px solid var(--line-2);
    color: var(--text-3);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.10em;
    background: var(--surface-2);
}
.proto-table td {
    padding: 9px 14px;
    border-bottom: 1px solid var(--line);
    color: var(--text-2);
    vertical-align: middle;
    background: var(--surface);
}
.proto-table tr:hover td { background: var(--blue-bg); }
.proto-table tr.active td {
    background: var(--blue-bg);
    color: var(--text-1);
}
.proto-table tr.active td:first-child {
    border-left: 3px solid var(--blue);
}

/* Status badges */
.badge {
    display: inline-block;
    font-family: var(--mono);
    font-size: 0.60rem;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 3px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.badge-pass  { background: var(--pass-bg);  color: var(--pass); border: 1px solid var(--pass-line); }
.badge-fail  { background: var(--fail-bg);  color: var(--fail); border: 1px solid var(--fail-line); }
.badge-warn  { background: var(--warn-bg);  color: var(--warn); border: 1px solid var(--warn-line); }
.badge-info  { background: var(--blue-bg);  color: var(--blue); border: 1px solid var(--blue-line); }
.badge-grey  { background: var(--surface-2); color: var(--text-3); border: 1px solid var(--line-2); }
```

IMPORTANT: Apply these color overrides to ALL Plotly charts too:
- paper_bgcolor: "rgba(0,0,0,0)"
- plot_bgcolor: "#FFFFFF"
- font color: "#6B7280"
- gridcolor: "#E2E5EF"
- All chart backgrounds white, not dark

================================================================================
JOB 2: CONTROL PANEL AT THE VERY TOP
================================================================================

Before the st.tabs() call, render a full-width control panel bar.
This is the FIRST thing rendered after st.set_page_config().

The control panel must contain:

LEFT SIDE — identity:
  "⬡ CHP" label + project name badge + turn/mode/dead-end stats

RIGHT SIDE — action buttons (these are the "cool options"):
  Button 1: "▶ Run Loop"
    On click: runs `chp run` in a subprocess (non-blocking)
    Shows spinner while starting, then success message

  Button 2: "▶ Run Experiment"  
    On click: shows a selectbox of the 9 experiments
    Then runs `chp run --experiment {selected}` 

  Button 3: "📄 Export Paper"
    On click: calls _export() and shows download confirmation

  Button 4: "🔄 Refresh Now"
    On click: st.rerun()

  Button 5: "⬇ Download All Figures"
    On click: zips everything in experiments/*/figures/ into chp_figures.zip
    Uses Python zipfile module
    Shows download confirmation with file count + total size

Here is the exact implementation for the control panel:

```python
def _render_control_panel(config, sv, dead_text, project_dir):
    """Render the top control panel with run options and stats."""
    import zipfile, io

    project = config.get("project", {}).get("name", "CHP Project")
    turn    = sv.get("TURN", "0")
    mode    = sv.get("MODE", "—")
    de_count = len(_dead_ends(dead_text))

    # Mode color
    if "COMPLETE" in mode.upper() or "DONE" in mode.upper():
        mode_cls = "badge-pass"
    elif "EXPLORATION" in mode.upper():
        mode_cls = "badge-warn"
    elif "EXIT" in mode.upper():
        mode_cls = "badge-fail"
    else:
        mode_cls = "badge-info"

    st.markdown(f"""
    <div style="background:#FFFFFF;border-bottom:2px solid #E2E5EF;
                padding:12px 28px;display:flex;align-items:center;
                justify-content:space-between;flex-wrap:wrap;gap:12px;">
      <div style="display:flex;align-items:center;gap:14px;flex-wrap:wrap;">
        <span style="font-family:'IBM Plex Mono',monospace;font-size:0.85rem;
                     font-weight:600;color:#0F1117;">⬡ CHP</span>
        <span style="font-family:'IBM Plex Mono',monospace;font-size:0.72rem;
                     color:#1D4ED8;background:#EFF6FF;border:1px solid #93C5FD;
                     border-radius:4px;padding:3px 10px;">{project}</span>
        <span style="font-family:'IBM Plex Mono',monospace;font-size:0.68rem;color:#6B7280;">
          T:<strong style="color:#0F1117;">{turn}</strong>
          &nbsp;·&nbsp;
          <span class="badge {mode_cls}">{mode.split("—")[0].strip()}</span>
          &nbsp;·&nbsp;
          <strong style="color:{'#991B1B' if de_count > 0 else '#9CA3AF'};">{de_count}</strong> dead ends
        </span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Action buttons row
    b1, b2, b3, b4, b5, b6 = st.columns([1.2, 1.5, 1.2, 1, 1.5, 0.5])

    with b1:
        if st.button("▶  Run Loop", use_container_width=True, key="btn_run"):
            try:
                subprocess.Popen(
                    ["chp", "run"],
                    cwd=str(project_dir),
                    creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform=="win32" else 0,
                )
                st.success("Loop started")
            except FileNotFoundError:
                st.error("`chp` not found — activate your venv")

    with b2:
        exp_choice = st.selectbox(
            "Experiment",
            ["— select —"] + list(EXPERIMENT_CATALOG.keys()),
            key="ctrl_exp_select",
            label_visibility="collapsed",
        )
        if exp_choice != "— select —":
            if st.button("▶  Run Experiment", use_container_width=True, key="btn_run_exp"):
                try:
                    subprocess.Popen(
                        ["chp", "run", "--experiment", exp_choice],
                        cwd=str(project_dir),
                        creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform=="win32" else 0,
                    )
                    st.success(f"Started: {exp_choice}")
                except FileNotFoundError:
                    st.error("`chp` not found — activate your venv")

    with b3:
        if st.button("📄  Export Paper", use_container_width=True, key="btn_export"):
            cfg    = _yaml(project_dir / "config.yaml")
            log    = _read(project_dir / "innovation_log.md")
            dead   = _read(project_dir / "dead_ends.md")
            sv_d   = _sv(_read(project_dir / "state_vector.md"))
            report = _find_report(project_dir)
            _export(cfg, log, dead, sv_d, report)
            st.success("Saved: paper_appendix.md")

    with b4:
        if st.button("🔄  Refresh", use_container_width=True, key="btn_refresh"):
            st.rerun()

    with b5:
        if st.button("⬇  Download All Figures", use_container_width=True, key="btn_dl_figs"):
            zip_buf = io.BytesIO()
            count = 0
            total_bytes = 0
            with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
                for exp_name in EXPERIMENT_CATALOG:
                    figs_dir = project_dir / "experiments" / exp_name / "figures"
                    if figs_dir.exists():
                        for fig in figs_dir.glob("*"):
                            if fig.suffix.lower() in (".png", ".svg", ".jpg", ".jpeg"):
                                zf.write(fig, f"{exp_name}/{fig.name}")
                                count += 1
                                total_bytes += fig.stat().st_size
            zip_buf.seek(0)
            if count > 0:
                st.download_button(
                    label=f"⬇ Save ZIP ({count} figs, {total_bytes//1024}KB)",
                    data=zip_buf,
                    file_name="chp_figures.zip",
                    mime="application/zip",
                    key="btn_dl_figs_actual",
                )
            else:
                st.warning("No figures found yet — run an experiment first")

    with b6:
        if st.button("⏹  Stop", use_container_width=True, key="btn_stop"):
            stop_file = project_dir / "STOP"
            stop_file.touch()
            st.warning("STOP file created — loop will halt at next turn check")

    st.markdown('<div style="height:1px;background:#E2E5EF;margin:0;"></div>',
                unsafe_allow_html=True)
```

Call _render_control_panel(config, sv, dead_text, project_dir) as the FIRST
thing in main(), before any tabs.

================================================================================
HOW TO DETECT project_dir
================================================================================

At the top of main(), detect the project root:

```python
# Try common locations: cwd, parent, chp-test-run sibling
_candidates = [
    Path.cwd(),
    Path.cwd().parent,
    Path(__file__).parent.parent,
    Path(__file__).parent.parent / "chp-test-run",
]
project_dir = next(
    (p for p in _candidates if (p / "config.yaml").exists()),
    Path.cwd(),
)
```

Then use project_dir everywhere instead of hardcoded Path(".").

================================================================================
EXPERIMENT CATALOG (keep exactly as-is, just verify it's present)
================================================================================

EXPERIMENT_CATALOG = {
    "schelling-segregation":      {"domain": "Social Science",      "icon": "🏘️"},
    "spatial-prisoners-dilemma":  {"domain": "Game Theory",         "icon": "🎲"},
    "lotka-volterra":             {"domain": "Ecology",             "icon": "🐺"},
    "sir-epidemic":               {"domain": "Epidemiology",        "icon": "🦠"},
    "ml-hyperparam-search":       {"domain": "Machine Learning",    "icon": "🤖"},
    "lorenz-attractor":           {"domain": "Chaos Theory",        "icon": "🦋"},
    "quantum-grover":             {"domain": "Quantum Computing",   "icon": "⚛️"},
    "izhikevich-neurons":         {"domain": "Neuroscience",        "icon": "🧠"},
    "blockchain-consensus":       {"domain": "Distributed Systems", "icon": "🔗"},
}

================================================================================
ALSO ADD: _find_figures() helper
================================================================================

```python
def _find_figures(experiment_dir: Path) -> list[Path]:
    """Return sorted list of image files from experiment's figures/ dir."""
    figs_dir = experiment_dir / "figures"
    if not figs_dir.exists():
        return []
    return sorted(
        [p for p in figs_dir.iterdir()
         if p.suffix.lower() in (".png", ".svg", ".jpg", ".jpeg")],
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
```

================================================================================
KEEP EVERYTHING ELSE
================================================================================

All tabs, all data parsing functions, all existing logic — keep untouched.
The only changes are:
  1. The CSS block → white theme as specified above
  2. Add _render_control_panel() function
  3. Call _render_control_panel() first in main()
  4. Add _find_figures() helper
  5. Add project_dir detection in main()
  6. Apply white Plotly theme to all charts

================================================================================
SELF-CHECK BEFORE FINISHING
================================================================================

  □ Is the background white (#F8F9FC or #FFFFFF)? FAIL if dark
  □ Is the text dark (#0F1117)? FAIL if light-on-dark
  □ Is the control panel the first thing rendered? FAIL if no
  □ Does "Download All Figures" button exist and produce a ZIP? FAIL if no
  □ Does "Run Loop" button call `chp run`? FAIL if no
  □ Does "Stop" button create a STOP file? FAIL if no
  □ Are Plotly charts white background? FAIL if dark
  □ Does the dashboard still auto-refresh? FAIL if no
  □ Are all 4 original tabs still present? FAIL if no

================================================================================
RUN AFTER WRITING
================================================================================

After writing the file, verify it parses:
  python -c "import ast; ast.parse(open('dashboard/app.py').read()); print('OK')"

If it fails, fix the syntax error before finishing.

================================================================================
DONE
================================================================================

Report: "Dashboard fixed. White theme applied. Control panel added with 6 buttons."
