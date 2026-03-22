# CHP UI — Product Requirements Document
# Version 1.0
# Source: Extracted from dashboard/app.py + architectural decisions

================================================================================
WHAT WE ARE BUILDING
================================================================================

A single web application that replaces the Streamlit dashboard entirely.
White clinical theme. Reads files, never writes them.
Does four things: sets up experiments, shows the registry, watches runs live,
and analyzes completed results.

The Streamlit dashboard proved the concept. This is the right build.

================================================================================
ARCHITECTURE DECISION
================================================================================

Stack: Single HTML file + lightweight Python server (10 lines, stdlib only)
Why: No framework lock-in. Runs anywhere. No npm, no webpack, no Streamlit.
     Reads EXPERIMENT_INDEX.json as single source of truth for registry.
     Reads .chp/telemetry.json, state_vector.md, innovation_log.md for live data.
     Polls files on a timer for live updates — no websockets needed.

Server: python -m http.server with one custom handler for file reads.
Client: Vanilla JS or minimal React. Chart.js for all charts.

================================================================================
DESIGN SYSTEM (carry over from existing dashboard — it works)
================================================================================

Colors (exact hex from current CSS):
  --bg:      #F8F9FC   page background
  --sur:     #FFFFFF   card surface
  --sur2:    #F3F4F8   alternate row / secondary surface
  --sur3:    #E9EBF2   tertiary surface
  --ln:      #E2E5EF   default border
  --ln2:     #C8CCDB   emphasis border
  --t1:      #0F1117   primary text
  --t2:      #374151   secondary text
  --t3:      #6B7280   muted text
  --t4:      #9CA3AF   hint text
  --blue:    #1D4ED8   primary action / active
  --bluebg:  #EFF6FF   blue surface
  --pass:    #065F46   gate pass text
  --passbg:  #ECFDF5   gate pass surface
  --passbd:  #34D399   gate pass border
  --fail:    #991B1B   gate fail text
  --failbg:  #FEF2F2   gate fail surface
  --failbd:  #FCA5A5   gate fail border
  --warn:    #92400E   warning text
  --warnbg:  #FFFBEB   warning surface
  --warnbd:  #FCD34D   warning border
  --amber:   #D97706   FP callout / tick marks

Typography:
  Headings/labels: IBM Plex Mono — all caps, letter-spacing 0.10em
  Body: Inter / system-ui
  Monospace values: IBM Plex Mono

================================================================================
SECTION 1 — GLOBAL HEADER (persistent, always visible)
================================================================================

Left side:
  CHP logo mark (hexagon)
  Project name badge (blue pill)
  Turn number
  Mode badge (green=VALIDATION, amber=EXPLORATION, red=EXIT)
  Dead ends count (red if > 0)
  Figure count

Right side:
  Auto-refresh interval indicator
  Current time HH:MM:SS
  Last file read timestamp

Action buttons (below header, always visible):
  [ Run Loop ]         — launches chp run in new terminal
  [ Stop Loop ]        — writes STOP file to project root
  [ Experiment ▼ ]     — dropdown of all experiments + [ Run This ]
  [ Export Paper ]     — writes paper_appendix.md
  [ Refresh ]          — manual refresh
  [ Download Figures ] — zips all figures, triggers browser download
  [ Clear Stop ]       — removes STOP file

================================================================================
SECTION 2 — TABS (four tabs, same as current)
================================================================================

Tab 1: Live Monitor
Tab 2: Protocol Health
Tab 3: Experiment Report
Tab 4: Experiment Gallery

Tab labels: monospace, all caps, 0.68rem, underline on active (blue)

================================================================================
TAB 1 — LIVE MONITOR
================================================================================

Purpose: Watch the loop as it runs, turn by turn.
Data source: state_vector.md, innovation_log.md, dead_ends.md, config.yaml
Refresh: every 5 seconds (poll file mtimes, only re-render if changed)

--- ROW 1: Four status cards ---

Card: Mode
  Value: VALIDATION / EXPLORATION / DONE / EXIT (from state_vector MODE field)
  Color: green border top for VALIDATION/DONE, amber for EXPLORATION, red for EXIT
  Sub: mode detail (everything after the -- in the mode string)

Card: Turn
  Value: current turn number (from state_vector TURN field)
  Sub: "of 50 max" (from config loop.max_turns)

Card: Dead Ends
  Value: count of ## DEAD END entries in dead_ends.md
  Color: red border top if count > 0
  Sub: "Contraindications logged"

Card: Open Flags
  Value: count of comma-separated items in state_vector OPEN_FLAGS
  Color: amber border top if count > 0
  Sub: first 40 chars of OPEN_FLAGS

--- ROW 2: Two columns ---

LEFT COLUMN:

  Section: Critic Scorecard
    Source: parse last gate_N_xxx: 0.XX lines from innovation_log.md
    Four gate bars (Gate 1, 2, 3, 4):
      - Label: G1 - FROZEN COMPLIANCE, G2 - ARCHITECTURE, etc.
      - Score value right-aligned
      - Progress bar (fill to score %)
      - Threshold tick mark at 0.85 (amber vertical line)
      - Color: green if >= threshold, amber if within 0.05, red if below
    Empty state: "awaiting build / run chp run to start"

  Section: Sigma-Gate Readings
    Source: config.yaml gates.anomaly_checks
    Table rows: metric name | operator | threshold
    One row per anomaly check defined in config
    Live value column (if available from telemetry)

  Section: Council Status
    Source: scan last 3000 chars of innovation_log for DRIFT keyword
    If DRIFT flagged: red error box "DRIFT flagged — re-read CHAIN_PROMPT.md"
    If clean: green success "No drift detected"

RIGHT COLUMN:

  Section: Innovation Log
    Source: innovation_log.md — last 15 entries split by --- separator
    Each entry: collapsible expander labeled "Turn N"
    Auto-expand: most recent turn AND any turn with FALSE POSITIVE in text
    FP entries get "FP:" prefix in the expander label
    Content truncated at 2000 chars per entry
    Newest entries at top

  Section: Contraindications (Dead Ends)
    Source: dead_ends.md
    Bordered box with red header "CONTRAINDICATIONS — DO NOT REPEAT"
    Each entry: C01, C02... index | title | "-- do not repeat" rule italic below
    Alternating row backgrounds

  Section: Live Figures (conditional — only if experiment detected)
    Source: experiments/[detected-experiment]/figures/*.png|svg|jpg
    Shows up to 3 most recent figures by mtime
    Caption: figure stem name
    Timestamp: "X min ago"
    Section header shows total figure count + time of most recent

================================================================================
TAB 2 — PROTOCOL HEALTH
================================================================================

Purpose: Is the loop learning? Track efficiency over turns.
Data source: .chp/telemetry.json
Max width: 960px centered

--- ROW 1: Section header ---
"Protocol Health — Is the loop learning?"
Sub: "Healthy loop: declining drift · improving gate scores · faster turns · fewer fix cycles"

--- ROW 2: Four primary stat cards ---

Card: Tokens / Line
  Value: total_tokens / total_lines_written (round to 1 decimal)
  Sub: "lower = more efficient"

Card: False Pos. Caught
  Value: count of turns where false_positive_caught = true
  Sub: "killed before merge"

Card: Dead Ends Avoided
  Value: sum of dead_ends_avoided across all turns
  Sub: "mistakes not repeated"

Card: First-Try Pass
  Value: % of turns where tests_passed_first_try = true (among turns with tests)
  Sub: "no fix cycle needed"

--- ROW 3: Four secondary stat cards (smaller) ---
Total Tokens | Lines Built | Total Time (minutes) | Turns

--- ROW 4: Section header "Trends Over Time" ---

--- ROW 5: Two charts side by side ---

Chart LEFT: Tokens per Turn
  Type: Line chart with markers
  X: turn number
  Y: tokens_total per turn
  Series 1: actual tokens (blue line)
  Series 2: 3-turn rolling average (amber dashed)
  Vertical dotted lines at turns where FP caught (amber, labeled "FP")
  Height: 195px

Chart RIGHT: Critic Gate Scores
  Type: Line chart with markers
  X: turn number
  Y: gate score 0-1
  Series 1: Gate 1 Frozen (green)
  Series 2: Gate 3 Scientific (amber)
  Horizontal dashed line at 0.85 threshold (amber)
  Y range: 0.5 to 1.05
  Vertical FP markers same as left chart
  Height: 195px

--- ROW 6: Two panels side by side ---

Chart LEFT: Time per Turn (Lollipop)
  Type: Lollipop / stem chart
  X: turn number
  Y: duration_seconds / 60 (minutes)
  Stem color: green < 5min, amber < 10min, red >= 10min
  Dot at top of each stem, same color
  Height: 195px

Panel RIGHT: Key Events
  Source: turns where false_positive_caught=true OR anomaly=true
  FP events: amber left-border box
    Header: "Turn N — False Positive Caught"
    Body: false_positive_description (truncated at 120 chars)
  Anomaly events: red left-border box
    "Turn N: ANOMALY — sigma-gate failed"
  Empty state: green "clean run / no anomalies or false positives"

Empty state (no telemetry): show all stat cards with "--" values
  + empty box: "awaiting telemetry / run chp run --method api to record"

================================================================================
TAB 3 — EXPERIMENT REPORT
================================================================================

Purpose: Read and present the completed experiment report.
Data source: REPORT.md (searched recursively from project dir)

--- False Positive Story (if found) ---
Scan report for section starting with ## FALSE POSITIVE (case insensitive)
If found: render in amber callout box
  Header: "FALSE POSITIVE STORY" (monospace, amber, all caps)
  Body: section content, 0.78rem, line-height 1.6

--- Full Report ---
Render full REPORT.md content as markdown

--- Publication Figures ---
Source: experiments/[detected-experiment]/figures/
2-column grid
Each figure:
  Image full width
  Caption bar below: figure name from FIGURE_DESCRIPTIONS dict (or stem if not found)
  Sub-caption: file size KB · last modified time

--- Export Button ---
"Export Paper Appendix" button
Writes paper_appendix.md with:
  Project name + timestamp
  State vector (all key/value pairs as bullet list)
  Full innovation log
  Full dead ends file
  Full report (if exists)

Empty state: "no report generated yet / complete the experiment to see results"

================================================================================
TAB 4 — EXPERIMENT GALLERY
================================================================================

Purpose: Browse all experiments, see status, drill into any one.
Data source: EXPERIMENT_INDEX.json (primary) + file system for live status

--- Registry Table ---
Header: "Experiment Registry"
Columns: icon | name | domain | prior drift catches | figs | status
Status badges:
  Active: blue "Active" (current experiment from config)
  Done: blue "Done" (REPORT.md exists)
  Staged: gray "-" (no REPORT.md)
Active row: blue left border + blue background tint
Hover: blue background tint on any row

--- View Buttons ---
3 per row: "View [experiment-name]" button for each
Clicking sets selected experiment

--- Experiment Detail Panel (appears on selection) ---
Horizontal rule separator
Section header with experiment icon + name

Five sub-tabs:
  Spec       — render spec.md
  Frozen     — render all frozen/*.md files, one expander each
  Dead Ends  — render dead_ends.md as contraindications list (same format as Tab 1)
  Report     — render REPORT.md
  Figures    — figure grid same as Tab 3

Figure count + last modified header above figure grid
2-column figure grid
Each: image + caption bar (name | size KB | modified time)
Empty state: "no figures yet / run: chp run --experiment [name]"

================================================================================
SECTION 3 — EXPERIMENT SETUP WIZARD (NEW — not in current dashboard)
================================================================================

New tab: "New Experiment" (add as 5th tab)

Purpose: Generate frozen spec and chain prompt from a form.
Output: writes to experiments/[name]/ directory structure.

Step 1 — Identity
  Field: Experiment name (slug, lowercase, hyphens)
  Field: Research question (one sentence)
  Field: Domain (dropdown: Social Science, Physics, Chemistry, Biology,
         Economics, Mathematics, Music, Distributed Systems, Other)
  Field: Source citation (e.g. "Schelling (1971)")

Step 2 — Prior Errors
  Repeating field group (add up to 10):
    Prior error name
    What the LLM generates (the wrong value)
    What the frozen spec says (the correct value)
    Why the LLM gets it wrong (one sentence)

Step 3 — Sigma Gates
  Repeating field group (add up to 10):
    Metric name
    Operator (dropdown: >, >=, <, <=, ==)
    Threshold value
    Description

Step 4 — Review + Generate
  Preview of generated files:
    frozen/[name]_constants.py
    CHAIN_PROMPT.md
    dead_ends.md (pre-loaded from prior errors)
    state_vector.md (turn 0 template)
    innovation_log.md (blank template)
  [ Generate Experiment ] button
  Writes all files to experiments/[name]/

================================================================================
SECTION 4 — DATA SOURCES AND REFRESH
================================================================================

File polling: check mtime every 5 seconds
Only re-render components whose source files changed
No websockets, no server-sent events — simple polling is fine

Primary sources:
  state_vector.md         → Tab 1 status cards + header
  innovation_log.md       → Tab 1 log + council status + critic scores
  dead_ends.md            → Tab 1 contraindications
  config.yaml             → sigma gate definitions + project name + experiment detection
  .chp/telemetry.json     → Tab 2 all charts and stats
  REPORT.md               → Tab 3
  experiments/*/figures/  → Tab 1 live figures + Tab 3 + Tab 4
  EXPERIMENT_INDEX.json   → Tab 4 registry table

================================================================================
SECTION 5 — WHAT IS NOT IN SCOPE
================================================================================

- Writing to any CHP file (except paper_appendix.md export and new experiment setup)
- Authentication
- Multi-user
- Cloud deployment
- Database
- Real-time push (polling is sufficient)
- Dark mode (white clinical theme only)

================================================================================
SECTION 6 — BUILD ORDER
================================================================================

Phase 1: Static registry
  - Read EXPERIMENT_INDEX.json
  - Render Tab 4 gallery table
  - No live data yet
  - Verify file reading works

Phase 2: Live monitor
  - Add file polling
  - Render Tab 1 with real data
  - Add status cards + innovation log + dead ends + figures

Phase 3: Protocol health
  - Tab 2 with all charts
  - Chart.js integration

Phase 4: Report + export
  - Tab 3 markdown rendering
  - Export to paper_appendix.md

Phase 5: Setup wizard
  - Tab 5 form
  - File generation

Phase 6: Header + action buttons
  - Run/Stop loop
  - Download figures ZIP

================================================================================
OPEN QUESTIONS
================================================================================

1. Should the header Run Loop button launch claude CLI directly or just
   write a run.sh script for the user to execute?
   (Recommend: write the script — don't auto-execute)

2. Should the experiment gallery read from EXPERIMENT_INDEX.json only,
   or also scan the filesystem for experiments not in the index?
   (Recommend: index is source of truth, filesystem is fallback)

3. What port does the server run on?
   (Recommend: 8765 — avoids conflict with Streamlit 8501/8502)
