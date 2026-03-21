---
name: chp-dashboard-redesign
description: "Rewrite dashboard/app.py from scratch as a clinical scientific instrument panel."
tools: Read, Write, Edit, Bash
target_file: dashboard/app.py
---

# CHP Dashboard Redesign — Full Build Specification

This prompt drives a complete rewrite of `dashboard/app.py`.
The existing file is the reference for BEHAVIOR only — all logic, file paths,
data parsing functions, and tab structure must be preserved exactly.
Only the VISUAL LAYER changes, plus one new capability: auto-figure display.

Read this prompt in full before writing a single line.

================================================================================
STEP 0 — READ BEFORE TOUCHING ANYTHING
================================================================================

Read these files in order:

  1. dashboard/app.py                  — current implementation (behavior reference)
  2. prompts/dashboard_redesign.md     — THIS FILE (your complete specification)

Do not start writing until you have read both.

================================================================================
CONTEXT: AUTO-FIGURE GENERATION (NEW CAPABILITY)
================================================================================

CHP now auto-generates publication-quality figures per experiment as part of
the build loop. The runner saves them to:

  experiments/{experiment-name}/figures/

Each figure is a PNG or SVG file produced by matplotlib or plotly — rendered
directly from simulation output data, not from LLM image generation.

The figures directory is created automatically by the runner. It may be empty
(experiment not yet run), partially populated (in progress), or complete.

The dashboard must display these figures live — reading them as static files,
never writing to them. This is a READ-ONLY display operation like everything
else in the dashboard.

Expected figure filenames per experiment (read from the figures/ directory —
do not hardcode, discover dynamically):

  schelling-segregation:
    grid_final.png          ← 50x50 agent grid heatmap (final state)
    segregation_over_time.png ← segregation index time series
    cluster_map.png         ← cluster-labelled grid

  spatial-prisoners-dilemma:
    lattice_final.png       ← cooperator/defector lattice (final generation)
    cooperation_rate.png    ← cooperation rate over generations
    pattern_evolution.png   ← 4-panel showing pattern development

  lotka-volterra:
    population_timeseries.png ← prey + predator over time
    phase_portrait.png      ← phase space spiral
    extinction_events.png   ← if any extinctions occurred

  sir-epidemic:
    epidemic_curve.png      ← S/I/R stacked area over time
    r0_distribution.png     ← R0 estimate across seeds

  ml-hyperparam-search:
    convergence.png         ← best-so-far accuracy curve
    search_space.png        ← 2D parameter space heatmap

  lorenz-attractor:
    attractor_3d.png        ← 3D butterfly attractor (two angles)
    lyapunov_convergence.png ← Lyapunov exponent convergence

  quantum-grover:
    amplitude_bars.png      ← amplitude per basis state
    success_probability.png ← success probability vs iterations

  izhikevich-neurons:
    voltage_raster.png      ← membrane voltage traces
    isi_histogram.png       ← inter-spike interval distribution

  blockchain-consensus:
    consensus_rounds.png    ← consensus reached per round
    byzantine_threshold.png ← safety vs f Byzantine nodes

These filenames are EXPECTED but not guaranteed. Always check what actually
exists in the figures/ directory before attempting to display.

================================================================================
FROZEN BEHAVIOR — DO NOT CHANGE
================================================================================

These things are architecturally fixed. Touch them and the build fails Gate 1.

  ✗ The dashboard never writes to any CHP file (READ-ONLY contract)
  ✗ Auto-refresh every 5 seconds via time.sleep() + st.rerun()
  ✗ All four tabs: Live Monitor / Protocol Health / Experiment Report / Experiment Gallery
  ✗ All file paths: config.yaml, state_vector.md, innovation_log.md, dead_ends.md
  ✗ All data parsing functions: _sv(), _dead_ends(), _log_entries(), _critic_scores(),
    _find_report(), _detect_experiment(), _yaml(), _read()
  ✗ The _export() function and Export Paper Appendix button
  ✗ The EXPERIMENT_CATALOG dict (all 9 experiments, icons, domains, plot types)
  ✗ Session state key: st.session_state.selected_experiment
  ✗ The _render_protocol_health() function logic (charts, telemetry loading)
  ✗ All st.metric() calls — labels and values stay identical
  ✗ Experiment detail subtabs: Spec / Frozen Rules / Dead Ends / Report

NEW (add, do not modify existing):
  ✓ _find_figures(experiment_dir) → returns sorted list of image Paths
  ✓ Figure display in: Live Monitor thumbnail strip, Report tab, Gallery detail panel

You are rewriting the SKIN. The SKELETON does not move.
You are adding ONE new data source (figures/) to the existing READ-ONLY pattern.

================================================================================
THE AESTHETIC DIRECTION
================================================================================

Target: Clinical Precision / Scientific Instrument Panel

Reference aesthetics:
  - Spectroscopy readout displays
  - ECG / cardiac monitor screens
  - Mass spectrometer output panels
  - NASA Mission Control workstations
  - Clinical trial data management systems

The operative question for every design decision:
"Does this look like it was MEASURED, or does it look like it was GENERATED?"

If it looks generated — redesign it.

What this is NOT:
  - Not a hacker terminal (kill all neon green)
  - Not a startup SaaS dashboard (no rounded cards, no purple gradients)
  - Not a generic Streamlit dark theme
  - Not "scientific-looking" via emoji and monospace fonts alone

================================================================================
DESIGN SYSTEM — IMPLEMENT EXACTLY AS SPECIFIED
================================================================================

──────────────────────────────────────────────────────
1. CSS CUSTOM PROPERTIES (root variables)
──────────────────────────────────────────────────────

Define ALL colors as CSS variables on :root. Never hardcode hex in components.

  Background hierarchy (darkest to lightest):
    --bg:          #09090E    ← page background
    --surface:     #0D0F16    ← card / panel backgrounds
    --surface-2:   #111420    ← elevated surface (gates, rows)
    --surface-3:   #171B28    ← hover state / selected

  Border hierarchy:
    --line:        #191E2E    ← hairline separators
    --line-2:      #222840    ← panel borders
    --line-3:      #2C3450    ← emphasized borders / hover

  Text hierarchy:
    --text-1:      #D6DAE8    ← primary (values, headings)
    --text-2:      #8A90A8    ← secondary (labels, descriptions)
    --text-3:      #525870    ← tertiary (metadata, timestamps)
    --text-4:      #333A50    ← disabled / placeholder

  Accent — Instrument Amber (primary accent, use sparingly):
    --amber:       #C8902A    ← active state, highlights, threshold markers
    --amber-dim:   #7A5518    ← amber borders on dark backgrounds
    --amber-glow:  rgba(200,144,42,0.10)   ← amber background tint
    --amber-glow2: rgba(200,144,42,0.05)   ← very subtle amber wash

  Semantic — Pass:
    --pass:        #2E9E6A    ← passing gates, complete status
    --pass-dim:    #1A5C3E    ← pass borders
    --pass-glow:   rgba(46,158,106,0.08)

  Semantic — Fail:
    --fail:        #C84848    ← failing gates, anomalies, exit
    --fail-dim:    #7A2C2C    ← fail borders
    --fail-glow:   rgba(200,72,72,0.08)

  Semantic — Info / Neutral active:
    --info:        #4A7AB8    ← validation mode, informational
    --warn:        #C87830    ← exploration mode, warnings

  Font stacks:
    --mono: 'IBM Plex Mono', 'Courier New', monospace
    --serif: 'Libre Baskerville', Georgia, 'Times New Roman', serif
    --sans: 'Source Sans 3', 'Helvetica Neue', Arial, sans-serif

──────────────────────────────────────────────────────
2. GOOGLE FONTS IMPORT
──────────────────────────────────────────────────────

@import url('https://fonts.googleapis.com/css2?
  family=IBM+Plex+Mono:wght@300;400;500;600;700&
  family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&
  family=Source+Sans+3:wght@300;400;500;600&
  display=swap');

All three families must load. No fallback to Inter, Roboto, or system fonts.

──────────────────────────────────────────────────────
3. GLOBAL OVERRIDES
──────────────────────────────────────────────────────

  html, body, .main, .stApp:
    background-color: var(--bg)
    font-family: var(--sans)
    color: var(--text-1)

  Hide Streamlit chrome:
    #MainMenu, footer, header → visibility: hidden
    .block-container → padding: 0; max-width: 100%

  Scrollbars:
    width/height: 4px, no border-radius
    thumb color: var(--line-2), hover: var(--amber-dim)

  Streamlit metric widget overrides:
    div[data-testid="stMetricValue"]:
      font-family: var(--mono)
      font-size: 1.55rem
      font-weight: 500
      color: var(--text-1)

    div[data-testid="stMetricLabel"]:
      font-family: var(--sans)
      font-size: 0.60rem
      color: var(--text-3)
      text-transform: uppercase
      letter-spacing: 0.12em

  Streamlit tabs:
    Tab buttons → var(--mono), 0.70rem, uppercase, letter-spacing: 0.12em
    Inactive: var(--text-3), no underline
    Active: var(--amber), 2px bottom border in var(--amber)
    Tab bar: border-bottom: 1px solid var(--line-2)
    Background: var(--surface)

  Streamlit expanders:
    background: var(--surface)
    border: 1px solid var(--line)
    border-radius: 0
    Summary font: var(--mono), 0.72rem, var(--text-2)

  Streamlit buttons:
    border-radius: 0
    border: 1px solid var(--line-2)
    background: var(--surface-2)
    font-family: var(--mono), 0.70rem, uppercase, letter-spacing: 0.10em
    color: var(--text-2)
    Hover: border-color var(--amber), color var(--amber), bg var(--amber-glow2)

  Alert boxes:
    border-radius: 0
    font-family: var(--mono), 0.72rem

──────────────────────────────────────────────────────
4. SCANLINE TEXTURE (subtle — do not overdo)
──────────────────────────────────────────────────────

Apply via .stApp::before pseudo-element:
  position: fixed, inset: 0, pointer-events: none, z-index: 0

  background: repeating-linear-gradient(
    0deg,
    transparent, transparent 2px,
    rgba(0,0,0,0.06) 2px, rgba(0,0,0,0.06) 3px
  )

Opacity should be subtle — 0.06 max. This gives instrument depth, not CRT aesthetic.

================================================================================
NEW HELPER FUNCTION: _find_figures()
================================================================================

Add this function to the file alongside the other file reader helpers:

def _find_figures(experiment_dir: Path) -> list[Path]:
    """Return sorted list of PNG/SVG figures from the experiment's figures/ dir.

    Discovers files dynamically — does not hardcode filenames.
    Returns empty list if directory does not exist or is empty.
    """
    figures_dir = experiment_dir / "figures"
    if not figures_dir.exists():
        return []
    found = sorted(
        [p for p in figures_dir.iterdir()
         if p.suffix.lower() in (".png", ".svg", ".jpg", ".jpeg")],
        key=lambda p: p.stat().st_mtime,   # most recently modified first
    )
    return found

Call sites (described in Component 12 and layout sections below):
  - Live Monitor tab: active experiment thumbnail strip
  - Experiment Report tab: figures section after gate scores
  - Experiment Gallery detail panel: new "Figures" subtab

================================================================================
COMPONENT SPECIFICATIONS — BUILD EACH EXACTLY
================================================================================

──────────────────────────────────────────────────────
COMPONENT 1: Fixed Instrument Header
──────────────────────────────────────────────────────

Class: .chp-header

  Layout: full-width horizontal bar, single row, no wrapping
  Position: sticky top-0, z-index: 100
  Background: var(--surface)
  Bottom border: 1px solid var(--amber-dim)   ← amber rule, not grey
  Padding: 12px 28px
  Font-family: var(--mono)

  Left section:
    Glyph: ⬡ (Unicode hexagon U+2B21) in var(--amber), font-size 0.90rem
    Separator: · in var(--text-4)
    Label: "CHP" in var(--text-3), 0.68rem, letter-spacing 0.15em, uppercase
    Separator: ·
    Project name: from config — color var(--amber), font-weight 500

  Center section (the critical state readout):
    "T:{turn}" in var(--text-1), font-weight 600
    separator ·
    Mode lamp (see Component 2 — inline version, compact)
    separator ·
    "{dead_end_count} DEAD ENDS" in var(--text-3) if > 0, else var(--text-4)
    separator ·
    "{flag_count} FLAGS" — same color logic
    separator ·
    "{figure_count} FIGS" — count of figures found for active experiment
      color: var(--info) if figure_count > 0, else var(--text-4)
      This gives a live signal that figures are accumulating

  Right section:
    "AUTO-REFRESH {N}s" in var(--text-4), 0.62rem
    separator ·
    Live timestamp in var(--text-3), 0.62rem

  Implementation note: render as st.markdown(html, unsafe_allow_html=True).
  Place BEFORE st.tabs() call.

──────────────────────────────────────────────────────
COMPONENT 2: Mode Status Lamp
──────────────────────────────────────────────────────

Class: .mode-lamp (full size) and .mode-lamp-inline (compact for header)

  Full size (used in Live Monitor tab):
    A cluster of 5 indicator lamps in a horizontal row:
      [LOOP] [VALIDATION] [EXPLORATION] [ANOMALY] [COUNCIL]

    Each lamp is a div:
      8x8px circle (border-radius: 50%)
      Label below in var(--mono), 0.55rem, uppercase, letter-spacing 0.10em

    Active lamp: color = semantic color, box-shadow: 0 0 8px 2px {color}
    Inactive lamp: background var(--line-2), no glow, label in var(--text-4)

    Active states based on sv["MODE"]:
      VALIDATION → [LOOP] and [VALIDATION] lit in var(--info)
      EXPLORATION → [LOOP], [EXPLORATION] lit in var(--warn)
      COMPLETE / DONE → [LOOP] off, all lamps dim, no animation
      EXIT → [LOOP] lit in var(--fail), pulsing

    Pulsing animation for active lamps (except COMPLETE):
      @keyframes lamp-pulse { 0%,100% { opacity:1 } 50% { opacity:0.35 } }
      animation: lamp-pulse 2s ease-in-out infinite

    Below the lamp cluster: large mode readout
      Font: var(--mono), 1.0rem, var(--text-1)
      Format: "VALIDATION · TURN {N}" or "EXPLORATION · TURN {N}"
      For COMPLETE: "✓ COMPLETE — ALL MILESTONES DELIVERED" in var(--pass)
      For EXIT: "✕ EXIT — {reason}" in var(--fail)

  Inline (header version):
    Single dot (6px) + mode text only, no lamp cluster
    Same color logic

  Replace _mode_html() entirely with this system.

──────────────────────────────────────────────────────
COMPONENT 3: Section Header
──────────────────────────────────────────────────────

Class: .sec-head

  Layout: flex row, align-items center, gap 12px
  Margin: 22px 0 10px

  Elements:
    Left: italic serif label (font: var(--serif), font-style: italic,
          font-size: 0.82rem, color: var(--text-2), white-space: nowrap)
    Center: flex-grow horizontal rule (height: 1px, background: var(--line-2))
    Right: index tag (font: var(--mono), 0.56rem, var(--text-4),
           letter-spacing 0.10em — e.g. "§ 01", "§ 02")

  Usage: replace all st.markdown("### ...") headers inside tabs with this component.

  Example rendered HTML:
    <div class="sec-head">
      <span class="sec-head-label">Critic Scorecard</span>
      <div class="sec-head-line"></div>
      <span class="sec-head-index">§ 01</span>
    </div>

──────────────────────────────────────────────────────
COMPONENT 4: Precision Gate Meter
──────────────────────────────────────────────────────

Class: .gate-meter

Structure:
  Outer div: padding 10px 14px, background var(--surface), margin 5px 0
    Left border: 3px solid — pass/fail/warn color
    No border-radius

  Row 1 (header):
    Left: gate name — var(--mono), 0.65rem, uppercase, letter-spacing 0.10em,
          color var(--text-2). Format: "G1 · FROZEN COMPLIANCE"
    Right: score value — var(--mono), 0.90rem, font-weight 600
           Color: var(--pass) if passing, var(--fail) if failing,
                  var(--warn) if within 0.05 of threshold

  Row 2 (track):
    Height: 3px
    Track background: var(--surface-3)
    Fill: width = score * 100%, color matches score color
    Threshold marker: position: absolute, left = threshold * 100%
      Width: 1px, height: 9px, top: -3px, color: var(--amber)
      ::after → tiny label: "0.85" or "1.0" in var(--mono) 0.52rem var(--amber-dim)

  Row 3 (metadata):
    font: var(--sans), 0.63rem, var(--text-3)
    Only show if a description exists

  Gate name mapping:
    Gate 1 → "G1 · FROZEN COMPLIANCE" — threshold 1.0
    Gate 2 → "G2 · ARCHITECTURE" — threshold 0.85
    Gate 3 → "G3 · SCIENTIFIC VALIDITY" — threshold 0.85
    Gate 4 → "G4 · DRIFT CHECK" — threshold 0.85

  Blocking indicator:
    If Gate 1 failing: 1px amber right border + tiny "BLOCKING" badge

──────────────────────────────────────────────────────
COMPONENT 5: Sigma Reading Row
──────────────────────────────────────────────────────

Class: .sigma-reading

  Layout: flex row, align-items center, gap 10px
  Padding: 7px 14px
  Border-bottom: 1px solid var(--line)
  Alternating background: var(--surface) / var(--surface-2)

  Elements:
    Left dot: 5px circle, no-data → var(--text-4)
    Metric name: var(--mono), 0.68rem, var(--text-2), flex-grow, ellipsis
    Operator: var(--mono), 0.65rem, var(--text-4), min-width 18px
    Threshold: var(--mono), 0.72rem, var(--amber), font-weight 500, min-width 45px

  Wrap in .sigma-table: border 1px solid var(--line-2), no border-radius

──────────────────────────────────────────────────────
COMPONENT 6: Turn Timeline (Innovation Log)
──────────────────────────────────────────────────────

Class: .turn-timeline

  Outer container: position relative, padding-left 32px

  Vertical axis line:
    position: absolute, left: 11px, top: 0, bottom: 0
    width: 1px, background: var(--line-2)

  Per turn entry (.turn-node):
    Node indicator: 12px circle, left: -26px, top: 14px, z-index 1
      Node color logic:
        FALSE POSITIVE → var(--amber), use ◆ diamond glyph
        ANOMALY → var(--fail)
        EXPLORATION → var(--warn)
        Latest → var(--pass)
        Default → var(--line-3)

    Content area:
      background: var(--surface), border: 1px solid var(--line), border-left: none
      padding: 10px 14px

      Turn header (always visible):
        "TURN {N}" var(--mono) 0.62rem + timestamp + mode badge + expand chevron
        FALSE POSITIVE badge: "◆ FALSE POSITIVE CAUGHT" var(--amber) var(--mono) 0.60rem

      Inline metric badges:
        gate_1: {score} ✓/✗  |  gate_3: {score} ✓/✗  |  seeds: {n}
        var(--mono) 0.58rem, pill: var(--surface-3) bg, border-radius 2px

      Expanded content: full log entry markdown, var(--sans) 0.78rem var(--text-2)

  Use st.expander() overridden by CSS. First entry expanded by default.

──────────────────────────────────────────────────────
COMPONENT 7: Contraindications Panel (Dead Ends)
──────────────────────────────────────────────────────

Class: .contra-panel

  Section label: "Contraindications" (not "Dead Ends")

  If dead ends exist:
    Header: "CONTRAINDICATIONS — DO NOT REPEAT THESE APPROACHES"
      background: var(--fail-glow), border: 1px solid var(--fail-dim)
      font: var(--mono), 0.60rem, var(--fail), uppercase

    Per entry (.contra-row): flex row
      Index: "C01", "C02" — var(--mono) 0.65rem var(--fail-dim)
      Title: var(--mono) 0.72rem var(--text-2)
      Right: ✗ var(--fail)
      Expanded: "Do NOT repeat" rule — italic, var(--fail-dim)

  If no dead ends: empty state (Component 10)

──────────────────────────────────────────────────────
COMPONENT 8: Custom Plotly Theme
──────────────────────────────────────────────────────

Apply to ALL go.Figure() calls in _render_protocol_health():

  paper_bgcolor: "rgba(0,0,0,0)"
  plot_bgcolor:  "#0D0F16"
  font.family:   "IBM Plex Mono, monospace"
  font.color:    "#525870"
  font.size:     10
  margin: dict(l=40, r=20, t=36, b=36)
  height: 240

  Axes: gridcolor "#191E2E", tickfont IBM Plex Mono size 9 color "#525870"
  Legend: transparent bg, IBM Plex Mono size 9

  Token chart: primary line "#4A7AB8", 3T rolling avg "--" in var(--amber)
  Gate chart: Gate1 "#2E9E6A", Gate3 "#C87830", threshold hline var(--amber) dotted
  Drift chart: fill rgba(200,72,72,0.08), line "#C84848"
  Time chart: lollipop (scatter markers + error_y bars from 0, not bar chart)

  Event markers on ALL time series:
    False positive turn → dotted vline "#C8902A" + "◆ FP" annotation
    Anomaly turn → dotted vline "#C84848"

──────────────────────────────────────────────────────
COMPONENT 9: Protocol Index Table (Experiment Gallery)
──────────────────────────────────────────────────────

Replace 3-column card grid with full-width HTML table.

  Section header: "EXPERIMENT REGISTRY — 9 PROTOCOLS"

  Columns: # | EXPERIMENT | DOMAIN | PRIOR DRIFT CATCHES | FIGS | STATUS

  Note the new FIGS column:
    Shows figure count for each experiment: "3 figs" in var(--info) if > 0,
    "—" in var(--text-4) if 0 or experiment not run
    Computed by calling _find_figures() for each experiment's directory

  CSS: .protocol-table — full width, border-collapse, var(--mono) 0.70rem
    th: amber-dim bottom border, var(--text-3), uppercase, letter-spacing
    td: var(--line) bottom border, var(--text-2), 9px 14px padding
    tr:hover: var(--surface-2) background
    Active row: var(--amber-glow2) bg, amber left border on first cell

  Status column: lamp dot + text (ACTIVE/COMPLETE/IN PROGRESS/NOT STARTED)

  Row click → st.session_state.selected_experiment = key
  (same behavior as current button, different trigger mechanism)

──────────────────────────────────────────────────────
COMPONENT 10: Empty / Diagnostic States
──────────────────────────────────────────────────────

  Gate meters (no data): fills at 0%, scores "—", threshold tick visible
    Footer: "awaiting build · run chp run" in var(--text-4)

  Turn timeline (no turns): 3 ghost nodes, axis line,
    "no turns recorded · run chp run to start the protocol"

  Protocol health (no telemetry): "—" values, flatline EKG frames
    "awaiting telemetry" centered in chart frame

  Contraindications (no dead ends):
    "— NO CONTRAINDICATIONS LOGGED —" centered var(--text-4)

  Figures (no figures yet):
    "— NO FIGURES GENERATED YET —" centered var(--text-4)
    Sub: "figures appear here as the experiment loop runs"
    Style: same border/background as figure panel, content centered

──────────────────────────────────────────────────────
COMPONENT 11: Experiment Report Tab
──────────────────────────────────────────────────────

Parse REPORT.md into sections:
  "## Summary"           → .stat-cell metric cards
  "## False Positive Story" → FP callout box (Component 11a)
  "## Key Results"       → .protocol-table styled table
  "## Gate Scores"       → compact gate meters (2px track)
  Other sections         → prose with Component 3 section headers

After gate scores section — insert Component 12 (figure panel)
  Section header: "Publication Figures"
  Source: figures from active experiment directory

FP Callout Box (Component 11a):
  background rgba(200,120,48,0.06), border 1px var(--warn), border-left 3px var(--amber)
  Header: "◆ FALSE POSITIVE STORY" var(--mono) 0.62rem var(--amber) uppercase
  Content: var(--sans) 0.78rem var(--text-2) line-height 1.6

──────────────────────────────────────────────────────
COMPONENT 12: Live Figure Panel (NEW)
──────────────────────────────────────────────────────

Class: .figure-panel

This is the new component that displays auto-generated experiment figures.
It appears in three locations:

  A. Live Monitor tab — thumbnail strip (compact, right column bottom)
  B. Experiment Report tab — full-size gallery after gate scores
  C. Experiment Gallery detail panel — dedicated "Figures" subtab

─────────────────────────────────────
12A: Live Monitor Thumbnail Strip
─────────────────────────────────────

Location: bottom of right column in Live Monitor tab, below Contraindications
Only shows if the active experiment has figures (experiment != None and figures exist)

Structure:
  Section header (Component 3): "Live Figures" / "§ 03"

  Panel container (.figure-strip):
    background: var(--surface)
    border: 1px solid var(--line-2)
    border-top: 2px solid var(--amber-dim)
    padding: 10px
    overflow-x: auto
    white-space: nowrap
    display: flex, gap: 8px

  Per figure thumbnail (.fig-thumb):
    width: 120px, flex-shrink: 0
    border: 1px solid var(--line-2)
    background: var(--surface-2)
    padding: 4px
    cursor: pointer

    Image: st.image(str(fig_path), width=112)
    Caption below image: fig_path.stem (filename without extension)
      font: var(--mono), 0.55rem, var(--text-3), text-align: center
      Truncate with ellipsis if > 15 chars

    On click (via st.button hidden behind, or session state):
      Sets st.session_state["expanded_figure"] = str(fig_path)
      Opens full-size modal via st.dialog() or expander below strip

  Expanded figure view (below the strip):
    If st.session_state.get("expanded_figure"):
      Full-width st.image() of the selected figure
      Caption: filename + file size + modification timestamp
        font: var(--mono) 0.65rem var(--text-3)
      Close button: small ✕ via st.button

  Figure count badge:
    Small text in header: "{N} figures · last updated {time_ago}"
    time_ago: compute from the most recently modified figure's mtime
    Format: "2m ago", "14s ago", "just now"
    Color: var(--info) if < 60s ago (live update just happened), else var(--text-3)

  If no figures:
    Show Component 10 empty state for figures (compact version)
    Height: 60px, no overflow

─────────────────────────────────────
12B: Report Tab Full Gallery
─────────────────────────────────────

Location: Experiment Report tab, after gate scores section

Structure:
  Section header (Component 3): "Publication Figures" / "§ 05"

  Two-column grid using st.columns(2):
    Each figure: full-size st.image() + caption below
    Caption format: "{index}. {filename_stem}" — var(--mono) 0.68rem var(--text-2)

  Below grid: file path disclosure
    "Source: {figures_dir}" in var(--mono) 0.62rem var(--text-4)

  If figures have a known semantic mapping (e.g. "grid_final.png" for Schelling):
    Add descriptive caption below the filename:
      "Final agent configuration — segregation index measured from this state"
    Source: a dict mapping filename stems to descriptions, defined at module level

  Publication-ready caption dict (define as FIGURE_DESCRIPTIONS at module top):
    {
      "grid_final": "Final agent grid — segregation index measured from this state",
      "segregation_over_time": "Segregation index over simulation steps",
      "cluster_map": "Cluster labels — spatially contiguous same-type groups",
      "lattice_final": "Final cooperator/defector lattice (blue=cooperate, red=defect)",
      "cooperation_rate": "Cooperation rate per generation",
      "pattern_evolution": "Spatial pattern development — 4 representative generations",
      "population_timeseries": "Prey and predator population dynamics over time",
      "phase_portrait": "Phase space — prey vs predator population trajectory",
      "extinction_events": "Extinction events across 30-seed battery",
      "epidemic_curve": "Stochastic SIR epidemic curve (S/I/R) — one representative run",
      "r0_distribution": "R0 estimate distribution across seeds",
      "convergence": "Bayesian optimization convergence — best validation accuracy",
      "search_space": "2D hyperparameter search space heatmap",
      "attractor_3d": "Lorenz strange attractor — 3D phase space trajectory",
      "lyapunov_convergence": "Lyapunov exponent convergence across time",
      "amplitude_bars": "Grover amplitude per basis state at optimal iterations",
      "success_probability": "Grover success probability vs iteration count",
      "voltage_raster": "Izhikevich neuron membrane voltage traces",
      "isi_histogram": "Inter-spike interval distribution by firing pattern",
      "consensus_rounds": "PBFT consensus reached per round (with Byzantine faults)",
      "byzantine_threshold": "Safety vs f Byzantine nodes — threshold f < N/3",
    }

  If no figures:
    Component 10 empty state for figures (full height version, 200px)

─────────────────────────────────────
12C: Gallery Detail Panel — Figures Subtab
─────────────────────────────────────

Location: Experiment Gallery tab, inside the selected-experiment detail panel

Add "📊 Figures" as a NEW 5th subtab to the existing detail tabs:
  Current: Spec | Frozen Rules | Dead Ends | Report
  New:     Spec | Frozen Rules | Dead Ends | Report | 📊 Figures

Tab implementation: add to the existing detail_tabs = st.tabs([...]) call

Content:
  If figures exist:
    stat-cell at top: "{N} figures · {most_recent_time}" 
    Then: same two-column grid as 12B
    Differs from 12B: shows ALL figures, not just report-relevant ones
    Also show figure file sizes below captions:
      "{size_kb} KB · modified {datetime}" in var(--mono) 0.58rem var(--text-4)

  If figures dir exists but is empty:
    "figures/ directory exists — experiment has run but no figures generated yet"
    hint: "figures are generated automatically when the simulation data is computed"

  If figures dir does not exist:
    "experiment has not been run yet · run chp run --experiment {name}"
    Component 10 empty state

Implementation notes for _find_figures():
  - Call once per tab render, not per figure
  - Cache result in st.session_state with a TTL (invalidate every 5s on refresh)
  - Or simply re-call on every refresh — files are small metadata ops
  - Sort by mtime descending so newest figures appear first
  - Filter: only .png, .svg, .jpg, .jpeg — ignore .npy, .csv, .json in figures/

================================================================================
STAT CELL COMPONENT
================================================================================

Class: .stat-cell

  No border-radius
  Background: var(--surface)
  Border: 1px solid var(--line)
  Border-top: 2px solid var(--amber-dim)
  Padding: 12px 16px

  Label: var(--sans), 0.58rem, var(--text-3), uppercase, letter-spacing 0.14em
  Value: var(--mono), 1.50rem, var(--text-1), font-weight 500, line-height 1
  Sub: var(--sans), 0.62rem, var(--text-3), margin-top 3px

  No gradients. No glow effects. No border-radius. Clean rectangle.

================================================================================
INFORMATION DENSITY REQUIREMENTS
================================================================================

Live Monitor tab: all primary information above the fold at 1920×1080.

  Gate meters: max 70px each
  Sigma readings: max 30px per row
  Section headers: max 38px
  Dead ends: max 120px before scroll
  Turn timeline: max 3 visible entries
  Figure strip: max 140px tall (thumbnails + caption)

Padding reductions vs current:
  Gate rows: 10px vertical
  Section headers: 22px top margin
  Tab content: 16px horizontal padding

================================================================================
LAYOUT CHANGES
================================================================================

Tab 1 (Live Monitor):
  Left column: Mode lamp | Critic Scorecard | sigma-Gates | Council Status
  Right column: Innovation Log (timeline) | Contraindications | Figure Strip (12A)

  Replace the top c1-c5 column row with the fixed header (Component 1)
  Mode lamp moves into left column below the section header

Tab 2 (Protocol Health):
  Keep all logic. Apply Component 8 Plotly theme. Use .stat-cell for metrics.

Tab 3 (Experiment Report):
  Apply Component 11 section parsing.
  Add Component 12B (figures gallery) after gate scores.
  Keep Export button, restyle as instrument action.

Tab 4 (Experiment Gallery):
  Replace card grid with Component 9 protocol index table (with FIGS column).
  Add "📊 Figures" as 5th subtab in experiment detail panel (Component 12C).

================================================================================
BUILDER SELF-CRITIQUE CHECKLIST (run before submitting)
================================================================================

After writing the full file, verify:

  □ Does neon green (#00ff88) appear anywhere? → FAIL
  □ Does JetBrains Mono appear anywhere? → FAIL
  □ Does Inter appear as a primary font? → FAIL
  □ Does any data component border-radius exceed 2px? → FAIL
  □ Do gate meters show threshold tick marks? → FAIL if no
  □ Is IBM Plex Mono loaded via @import? → FAIL if no
  □ Is Libre Baskerville loaded? → FAIL if no
  □ Is Source Sans 3 loaded? → FAIL if no
  □ Is the dashboard still READ-ONLY? → FAIL if any write call exists
  □ Does auto-refresh still work (time.sleep + st.rerun)? → FAIL if no
  □ Are all 4 original tabs present with original names? → FAIL if no
  □ Do all 9 experiments appear in EXPERIMENT_CATALOG? → FAIL if no
  □ Does _export() still write paper_appendix.md? → FAIL if no
  □ Is the fixed header present above the tabs? → FAIL if no
  □ Is _find_figures() implemented? → FAIL if no
  □ Does Component 12A appear in Live Monitor (thumbnail strip)? → FAIL if no
  □ Does Component 12B appear in Report tab (figures after gate scores)? → FAIL if no
  □ Does Component 12C appear as 5th subtab in Gallery detail? → FAIL if no
  □ Does the Gallery table have a FIGS column? → FAIL if no
  □ Does the header show "{N} FIGS" for the active experiment? → FAIL if no
  □ Are figure empty states implemented for all 3 locations? → FAIL if no
  □ Is FIGURE_DESCRIPTIONS dict defined at module level? → FAIL if no
  □ Does time_ago logic work in the thumbnail strip badge? → FAIL if no

================================================================================
CRITIC GATES — UI BUILD
================================================================================

Gate 1 — Behavior preservation (must = 1.0 — hard blocker):
  Did any frozen behavior change? (data parsing, file paths, tab count, read-only)
  Does _find_figures() follow the READ-ONLY contract?
  Are all 4 original tabs intact with original content?
  If any frozen behavior changed → reject, do not merge.

Gate 2 — Design system compliance (must >= 0.90):
  All colors from CSS variables only?
  Three required fonts loading?
  Neon green eliminated?
  Gate meters showing threshold ticks?
  Scanline texture present but subtle (opacity ≤ 0.06)?

Gate 3 — Component completeness (must >= 0.85):
  All 12 components implemented?
  Fixed header present?
  Empty states for all three figure locations?
  Plotly theme applied to all protocol health charts?
  FIGURE_DESCRIPTIONS dict present and used?
  Gallery table has FIGS column?

Gate 4 — Density & readability (must >= 0.85):
  Live Monitor above the fold at 1080p (estimate)?
  Typography hierarchy correct (serif headers, mono values, sans body)?
  Section headers using .sec-head?
  Dead ends labeled "Contraindications"?
  Figure thumbnails render without layout overflow?

================================================================================
OUTPUT
================================================================================

Write the complete rewritten dashboard/app.py as a single file.

The file must:
  - Be a single file (all styles inline via st.markdown)
  - Update the module docstring to mention figure display
  - Preserve all original imports, add PIL/pathlib as needed
  - Define FIGURE_DESCRIPTIONS at module level before main()
  - Define _find_figures() alongside other file reader helpers
  - Pass the 23-item self-critique checklist above
  - Pass all 4 critic gates

After writing the file, run:
  streamlit run dashboard/app.py --server.headless true &
  sleep 5
  curl -s http://localhost:8501 | head -20

Verify no ImportError or SyntaxError. Fix before reporting complete.

Write self-assessment:
  - Which of the 12 components were implemented
  - How _find_figures() integrates with the existing refresh cycle
  - The most difficult behavioral preservation challenge
  - Any known limitations or deferred polish items

================================================================================
DONE
================================================================================

When complete:
  "Dashboard redesign complete. dashboard/app.py rewritten.
   12 components implemented. _find_figures() added. All 4 critic gates passed."
