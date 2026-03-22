<!-- STATUS: run | DATE: 2026-03-21 | OUTPUT: full project consolidation -->
---
name: chp-overnight-fix
description: "Complete overnight consolidation: reports, tests, figures, index, prompt headers, telemetry backfill."
tools: Read, Write, Edit, Bash
---

# CHP Overnight Fix — Complete Project Consolidation

Run this while the human sleeps. Fix everything. Leave the project
in a state where every experiment is documented, every prompt has
a status, and a single index file tells the whole story.

Do not rush. Do not skip jobs. Do them in order.
Each job builds on the previous one.

================================================================================
START — ORIENT YOURSELF
================================================================================

Read these first to understand the full project:

  1. List chp-test-run/experiments/ (10 experiments)
  2. List experiments/ (staged and math experiments)
  3. List prompts/ (13 prompts)
  4. Read ablation/ABLATION_REPORT.md (key asset)
  5. Read experiments/MATH_SPRINT_RESULTS.md
  6. Read chp-test-run/experiments/schelling-segregation/REPORT.md
     (use as the gold standard format for all reports)

Then proceed through the 9 jobs below.

================================================================================
JOB 1 — WRITE MISSING REPORTS (4 experiments)
================================================================================

Four experiments have source code and results but no REPORT.md.
Write one for each, following the exact format of schelling REPORT.md.
Do not invent numbers — extract from source code and innovation logs.

────────────────────────────────────────────────────────────────────────────────
1A. metal-harmony REPORT.md
────────────────────────────────────────────────────────────────────────────────

Read: chp-test-run/experiments/metal-harmony/metal_analyzer.py

Key facts from the source (use these exactly):
  - Analyzes 5 Pantera reference riffs using METAL theory
  - Riffs: Walk, Cowboys From Hell, Domination, 5 Minutes Alone, Mouth for War
  - Classical theory flags parallel fifths, tritones, incomplete chords as errors
  - Metal theory: these are features, not errors
  - run_simulation() returns metrics including classical_errors_count per riff
  - Power chords detected (root + P5, no third)
  - Mode detection: Phrygian (Cowboys, Domination, 5 Minutes), Aeolian (Walk, Mouth)
  - The false positive: classical analysis flags 6-9 "errors" per riff.
    Metal analyzer returns 0 classical errors — correct for metal.
  - Gate 1=1.0, Gate 2=0.95, Gate 3=0.95, Gate 4=1.0

Write to: chp-test-run/experiments/metal-harmony/REPORT.md

Template to follow:

  # Metal Harmony — CHP Experiment Report

  ## Summary
  Metal harmony analyzer built to apply METAL theory (not classical) to
  Pantera riffs. KEY RESULT: classical analysis flags 6-9 errors per riff.
  Metal analyzer: zero errors. Prior-as-Detector confirmed: classical
  theory (the LLM prior) is the wrong framework for metal music.

  ## False Positive Story
  **The classical contamination test PASSED.**
  [Explain: LLM prior is classical harmony rules. This is the WRONG theory
  for metal. The frozen spec defines metal theory: power chords correct,
  parallel fifths idiomatic, tritones are features not errors, modal not
  functional. The classical analyzer produces 6-9 "errors" per riff that
  are not errors at all under the correct theory.]

  ## Key Results
  [Table: riff name | mode | classical_errors | metal_assessment]
  Walk | Aeolian | ~6 | power chord progression; parallel fifths (idiomatic)
  Cowboys From Hell | Phrygian | ~8 | power chord progression; tritone emphasis
  Domination | Phrygian | ~7 | power chord progression; parallel fifths
  5 Minutes Alone | Phrygian | ~6 | power chord progression
  Mouth for War | Aeolian | ~9 | power chord progression; tritone emphasis

  [Note: run metal_analyzer.py to get exact counts]

  ## Gate Scores
  [Use values above: G1=1.0, G2=0.95, G3=0.95, G4=1.0]

After writing REPORT.md, actually run the analysis to get exact numbers:

  python chp-test-run/experiments/metal-harmony/metal_analyzer.py

If it has a main block or run_simulation(), call it and capture the
classical_errors_count for each riff. Update the report with exact numbers.

────────────────────────────────────────────────────────────────────────────────
1B. euler-e REPORT.md
────────────────────────────────────────────────────────────────────────────────

Read: experiments/euler-e/innovation_log.md (has all the facts)
Read: experiments/euler-e/compute_e.py

Key facts (from innovation log):
  - Taylor series: e = sum(1/n!)
  - 10,000 digits, 0.11s
  - LLM ceiling: 15 digits. Multiplier: 667x.
  - False positives caught: 0 (correct from start)
  - Tests: 17/17 pass
  - Gate scores: G1=1.0 G2=1.0 G3=1.0 G4=1.0
  - Verified against OEIS A001113

Write to: experiments/euler-e/REPORT.md

────────────────────────────────────────────────────────────────────────────────
1C. pi-machin REPORT.md
────────────────────────────────────────────────────────────────────────────────

Read: experiments/pi-machin/innovation_log.md

Key facts:
  - Machin's formula: pi/4 = 4*arctan(1/5) - arctan(1/239)
  - 10,000 digits, 0.36s
  - LLM ceiling: 15 digits. Multiplier: 667x.
  - False positives caught: 0
  - Prior errors AVOIDED: Leibniz series (too slow), Monte Carlo (wrong),
    math.pi (float only)
  - Gate scores: G1=1.0 G2=1.0 G3=1.0 G4=1.0
  - Verified against OEIS A000796

Write to: experiments/pi-machin/REPORT.md

────────────────────────────────────────────────────────────────────────────────
1D. sqrt2-newton REPORT.md
────────────────────────────────────────────────────────────────────────────────

Read: experiments/sqrt2-newton/innovation_log.md

Key facts:
  - Newton's method: x_{n+1} = (x_n + 2/x_n) / 2
  - 10,000 digits, 0.04s, 14 iterations (quadratic convergence)
  - LLM ceiling: 16 digits. Multiplier: 625x.
  - FALSE POSITIVE CAUGHT: frozen reference contained LLM-hallucinated
    digits after position 50. Meta-level FP — CHP caught bad data in its
    own frozen spec. Algorithm is the real ground truth.
  - Gate scores: G1=1.0* G2=1.0 G3=1.0 G4=1.0 (*G1 failed initially)

Write to: experiments/sqrt2-newton/REPORT.md

================================================================================
JOB 2 — WRITE MISSING TESTS (9 experiments)
================================================================================

Only schelling-segregation has a proper test suite.
The other 9 loop-run experiments have no tests at all.
This means there is no way to verify their code still works.

For each experiment below, write a minimal but real test file.
Read the source code first. Test real behavior, not just imports.
Each test file should have 3-5 tests minimum.

Tests go in: chp-test-run/experiments/[name]/tests/test_[name].py
Create the tests/ directory if it doesn't exist.

────────────────────────────────────────────────────────────────────────────────
2A. spatial-prisoners-dilemma
────────────────────────────────────────────────────────────────────────────────

Read: chp-test-run/experiments/spatial-prisoners-dilemma/spatial_pd.py

Write: chp-test-run/experiments/spatial-prisoners-dilemma/tests/test_spatial_pd.py

Must test:
  - SpatialPDGrid initializes without error
  - cooperation_rate() returns float in [0, 1]
  - One step runs without error
  - Deterministic: same seed → same cooperation_rate after 10 steps
  - b=1.8 produces cooperation rate in [0.1, 0.9] after 50 generations
    (the Nowak & May coexistence regime — zero cooperation would be wrong)

────────────────────────────────────────────────────────────────────────────────
2B. sir-epidemic
────────────────────────────────────────────────────────────────────────────────

Read: chp-test-run/experiments/sir-epidemic/sir_model.py

Write: chp-test-run/experiments/sir-epidemic/tests/test_sir.py

Must test:
  - run_simulation(seed=42) returns dict with required keys
  - I(t) is integer type at all times (not float — this is the prior error)
  - Final size fraction in [0.5, 0.99] for non-fadeout seeds
  - Deterministic: seed=42 → same peak_infected both runs
  - Population conserved: S + I + R = N at all ticks

────────────────────────────────────────────────────────────────────────────────
2C. lorenz-attractor
────────────────────────────────────────────────────────────────────────────────

Read: chp-test-run/experiments/lorenz-attractor/lorenz.py

Write: chp-test-run/experiments/lorenz-attractor/tests/test_lorenz.py

Must test:
  - run_simulation() returns dict with x, y, z arrays
  - No euler integration (no 'dt' variable, uses scipy solve_ivp)
  - Attractor bounded: |x|<25, |y|<30, |z|<55
  - Not a fixed point: std(x[-100:]) > 1.0 (tail is chaotic)
  - IC is (1.0, 1.0, 1.0) — not the original Lorenz IC (0, 1, 0)

────────────────────────────────────────────────────────────────────────────────
2D. izhikevich-neurons
────────────────────────────────────────────────────────────────────────────────

Read: chp-test-run/experiments/izhikevich-neurons/izhikevich.py

Write: chp-test-run/experiments/izhikevich-neurons/tests/test_izhikevich.py

Must test:
  - run_simulation() returns dict with v_trace, spike_count, isi_cv
  - Only 2 state variables (v, u) — no m, h, n (Hodgkin-Huxley contamination)
  - RS pattern: spike_count > 0, isi_cv < 0.15 (regular spiking)
  - FS pattern: spike_count > RS spike_count (fast spiking fires more)
  - All 5 patterns produce spikes at I=10

────────────────────────────────────────────────────────────────────────────────
2E. quantum-grover
────────────────────────────────────────────────────────────────────────────────

Read: chp-test-run/experiments/quantum-grover/grover.py

Write: chp-test-run/experiments/quantum-grover/tests/test_grover.py

Must test:
  - GroverSimulator(n_qubits=10) initializes, N=1024
  - success_probability() after 25 iterations > 0.90
  - k_opt = floor(pi/4 * sqrt(1024)) = 25 exactly
  - Overshoot: probability at k=35 < probability at k=25 (sinusoidal profile)
  - Oracle is phase flip: amplitude *= -1, not boolean return

────────────────────────────────────────────────────────────────────────────────
2F. blockchain-consensus
────────────────────────────────────────────────────────────────────────────────

Read: chp-test-run/experiments/blockchain-consensus/consensus.py

Write: chp-test-run/experiments/blockchain-consensus/tests/test_consensus.py

Must test:
  - run_simulation(seed=42, n_byzantine=0) reaches consensus
  - run_simulation with f=3 Byzantine nodes: consensus reached, no safety violation
  - Quorum is 2f+1=7, NOT f+1=4 (Raft contamination check)
  - f=4 Byzantine: no consensus BUT no safety violation (graceful failure)
  - 3 message phases present: pre_prepare, prepare, commit

────────────────────────────────────────────────────────────────────────────────
2G. lotka-volterra
────────────────────────────────────────────────────────────────────────────────

Read: chp-test-run/experiments/lotka-volterra/lotka_volterra.py

Write: chp-test-run/experiments/lotka-volterra/tests/test_lotka_volterra.py

Must test:
  - run_simulation(seed=42) returns prey_trajectory, predator_trajectory
  - Trajectories are noisy (std > 0) — confirms agent-based, not ODE
  - No ODE variables in source (no alpha, beta, gamma, delta as floats)
  - Population trajectories are integer-valued (agent counts)
  - Across 5 seeds: at least 1 seed has predator extinction
    (impossible in ODE — confirms agent-based stochasticity)

────────────────────────────────────────────────────────────────────────────────
2H. ml-hyperparam-search
────────────────────────────────────────────────────────────────────────────────

Read: chp-test-run/experiments/ml-hyperparam-search/hyperparam_search.py

Write: chp-test-run/experiments/ml-hyperparam-search/tests/test_hyperparam.py

Must test:
  - run_search(seed=42) returns val_accuracy
  - val_accuracy in [0.85, 0.98] — no leakage (>0.98 means training data)
  - Method is Bayesian (not grid search): evaluated points are
    non-regular (not a meshgrid)
  - Train/val/test split is strict: no shuffling after split
  - Deterministic: seed=42 → same val_accuracy both runs

────────────────────────────────────────────────────────────────────────────────
2I. metal-harmony
────────────────────────────────────────────────────────────────────────────────

Read: chp-test-run/experiments/metal-harmony/metal_analyzer.py

Write: chp-test-run/experiments/metal-harmony/tests/test_metal_harmony.py

Must test:
  - run_simulation(seed=42) returns dict with riff_results
  - power_chord_accuracy == 1.0 (all Pantera riffs are power chords)
  - functional_contamination == 0.0 (no classical Roman numeral analysis)
  - Walk riff mode in ['aeolian', 'chromatic'] (not major/minor functional)
  - Cowboys riff mode == 'phrygian'
  - classical_errors_count > 0 for at least 3 riffs (classical theory
    does flag errors — that's the point of the experiment)

────────────────────────────────────────────────────────────────────────────────
2J. schroeder-reverb
────────────────────────────────────────────────────────────────────────────────

Read: experiments/schroeder-reverb/reverb.py

Write: experiments/schroeder-reverb/tests/test_reverb.py

Must test:
  - FreeverbReverb (or equivalent) initializes with correct comb delays
    [1116, 1188, 1277, 1356, 1422, 1491, 1557, 1617] — EXACT (frozen spec)
  - 8 comb filters (not 4 — textbook prior uses 4)
  - 4 allpass filters (not 2)
  - Allpass feedback = 0.5 (not 0.7 — textbook prior)
  - Output signal has different RT60 than textbook version
    (Freeverb: ~0.33s, Textbook: ~0.41s)

Run all new tests after writing them:
  python -m pytest chp-test-run/experiments/ -v --tb=short 2>&1 | head -100
  python -m pytest experiments/schroeder-reverb/tests/ -v --tb=short

Fix any import errors or path issues. The tests must actually pass.

================================================================================
JOB 3 — GENERATE MISSING FIGURES (2 experiments)
================================================================================

Two loop-run experiments have no figures directory or empty figures directories.

────────────────────────────────────────────────────────────────────────────────
3A. lotka-volterra figures
────────────────────────────────────────────────────────────────────────────────

Read: chp-test-run/experiments/lotka-volterra/lotka_volterra.py

Create: chp-test-run/experiments/lotka-volterra/figures/

Write and run: chp-test-run/experiments/lotka-volterra/generate_figures.py

The figure should show (white background, publication style):
  - Left panel: prey and predator population over time for seed=42
    Label: "Prey and Predator Populations (seed=42)"
    Note on plot: "Jagged = agent-based (not ODE smooth curve)"
  - Right panel: phase portrait (prey vs predator)
    Label: "Phase Portrait"
    Note: "Spiral = stochastic (not closed orbit of ODE)"
  - Title: "Agent-Based Lotka-Volterra — Prior-as-Detector Demo"
    Subtitle: "ODE predicts 0% extinction. Agent-based: extinction in 1+/5 seeds."

Save to: chp-test-run/experiments/lotka-volterra/figures/lotka_volterra_dynamics.png

Then show extinction evidence:
  - Run 5 seeds, count extinctions
  - Add text box to figure: "Predator extinction: N/5 seeds
    (impossible in ODE — confirms agent-based stochasticity)"

────────────────────────────────────────────────────────────────────────────────
3B. ml-hyperparam-search figures
────────────────────────────────────────────────────────────────────────────────

Read: chp-test-run/experiments/ml-hyperparam-search/hyperparam_search.py

Create: chp-test-run/experiments/ml-hyperparam-search/figures/

Write and run: chp-test-run/experiments/ml-hyperparam-search/generate_figures.py

Two figures:
  convergence.png — validation accuracy vs BO iteration
    Show how accuracy improves as Bayesian optimization explores
    Red dashed line at 0.98 labeled "Leakage threshold"
    Title: "Bayesian Optimization Convergence — No Data Leakage"

  search_space.png — scatter plot of evaluated hyperparameter points
    X axis: learning_rate (log scale), Y axis: hidden_size
    Color: validation accuracy
    Show the non-regular spacing that confirms Bayesian (not grid) search
    Title: "Hyperparameter Search Space — Bayesian (not Grid)"

Save to: chp-test-run/experiments/ml-hyperparam-search/figures/

================================================================================
JOB 4 — BACKFILL TELEMETRY (9 experiments)
================================================================================

Only schelling-segregation has telemetry.json.
The other 9 have enough data in their REPORT.md to reconstruct
approximate telemetry. This is not falsification — it is reconstruction
from the documented record.

For each experiment, create: chp-test-run/experiments/[name]/.chp/telemetry.json

Use the REPORT.md gate scores and turn count.
Where turns are unknown, estimate from the report narrative.
Mark all backfilled records with "backfilled": true.

Schema (match the schelling telemetry.json format exactly):

  {
    "project_name": "[experiment-name]",
    "start_time": "2026-03-21",
    "backfilled": true,
    "backfill_source": "REPORT.md",
    "turns": [
      {
        "turn": 1,
        "timestamp": "2026-03-21",
        "mode": "VALIDATION",
        "gate_1_frozen": [from REPORT],
        "gate_2_architecture": [from REPORT],
        "gate_3_scientific": [from REPORT],
        "gate_4_drift": [from REPORT],
        "critic_verdict": "PASS",
        "false_positive_caught": [true if FP mentioned in REPORT],
        "false_positive_description": "[from REPORT false positive story]",
        "seeds_run": [3 if not specified],
        "seeds_passed": [3 if not specified],
        "anomaly": false,
        "tokens_total": null,
        "duration_seconds": null,
        "lines_written": null
      }
    ]
  }

Experiments to backfill (read each REPORT.md for values):
  - spatial-prisoners-dilemma (gate scores: 1.0/0.95/0.92/0.95)
  - sir-epidemic (1.0/0.95/0.95/0.95, FP caught)
  - lorenz-attractor (1.0/0.95/0.88/0.95, FP caught)
  - izhikevich-neurons (1.0/0.95/0.92/0.95, FP caught)
  - quantum-grover (1.0/0.98/0.98/0.98, FP caught)
  - blockchain-consensus (1.0/0.95/0.95/0.98, FP caught)
  - lotka-volterra (1.0/0.95/0.88/0.95, FP caught)
  - ml-hyperparam-search (1.0/0.92/0.90/0.95, FP caught)
  - metal-harmony (1.0/0.95/0.95/1.0, FP caught)

================================================================================
JOB 5 — BUILD EXPERIMENT_INDEX.json
================================================================================

Write: EXPERIMENT_INDEX.json at the project root.

Read every REPORT.md and extract structured data.
After completing Jobs 1-4, you have all the data needed.

{
  "generated": "[ISO timestamp]",
  "version": "1.0",
  "experiments": {
    "[name]": {
      "display_name": "[human readable]",
      "location": "loop-run | direct-prompt",
      "dir": "[relative path from project root]",
      "status": "complete | staged | superseded",
      "domain": "[domain]",
      "source_files": ["[list of .py files]"],
      "has_report": true/false,
      "has_tests": true/false,
      "has_figures": true/false,
      "has_telemetry": true/false,
      "has_frozen_spec": true/false,
      "turns": N or null,
      "false_positives_caught": N or null,
      "false_positive_summary": "[one sentence]" or null,
      "key_result": "[one sentence from report]" or null,
      "gate_scores": {"g1":x,"g2":x,"g3":x,"g4":x} or null,
      "statistical_result": "[p-value or key metric]" or null,
      "multiplier": "[e.g. 667x LLM ceiling]" or null,
      "notes": "[anything notable]"
    }
  },
  "summary": {
    "total": N,
    "complete": N,
    "staged": N,
    "superseded": N,
    "loop_run_complete": N,
    "direct_prompt_complete": N,
    "total_false_positives": N,
    "domains": ["list of unique domains"]
  }
}

All 19 experiments + schroeder-reverb must be indexed.

Confirm index is valid JSON before saving:
  python -c "import json; json.load(open('EXPERIMENT_INDEX.json'))"

================================================================================
JOB 6 — PROMPT STATUS HEADERS
================================================================================

Add a status block to the top of each file in prompts/.
Find the exact start of each file and prepend — do not change content.

prompts/math_sprint.md:
  <!-- STATUS: run | DATE: 2026-03-21 | OUTPUT: experiments/euler-e, pi-machin, sqrt2-newton -->

prompts/euler_e.md:
  <!-- STATUS: run | DATE: 2026-03-21 | OUTPUT: experiments/euler-e/compute_e.py, 10k digits -->

prompts/dashboard_sync.md:
  <!-- STATUS: run | DATE: 2026-03-21 | OUTPUT: figures.py synced, icons fixed -->

prompts/dashboard_redesign.md:
  <!-- STATUS: run | DATE: 2026-03-21 | OUTPUT: dashboard/app.py white theme -->

prompts/consolidate.md:
  <!-- STATUS: run | DATE: 2026-03-21 | OUTPUT: see EXPERIMENT_INDEX.json -->

prompts/anatomy_viewer.md:
  <!-- STATUS: not-run | DATE: none | OUTPUT: none — staged, ready to execute -->

prompts/anatomy_viewer_vtk.md:
  <!-- STATUS: not-run | DATE: none | OUTPUT: none — staged, ready to execute -->

prompts/builder.md:
  <!-- STATUS: agent-role | USAGE: role context for Builder in CHP loop -->

prompts/critic.md:
  <!-- STATUS: agent-role | USAGE: role context for Critic in CHP loop -->

prompts/reviewer.md:
  <!-- STATUS: agent-role | USAGE: role context for Reviewer in CHP loop -->

prompts/council_gpt.md:
  <!-- STATUS: agent-role | USAGE: send to GPT-4o for council review -->

prompts/council_grok.md:
  <!-- STATUS: agent-role | USAGE: send to Grok for council review -->

prompts/loop_template.md:
  <!-- STATUS: template | USAGE: starting point for new experiment prompts -->

prompts/health_check.md:
  <!-- STATUS: template | USAGE: check CHP loop health -->

================================================================================
JOB 7 — WRITE PROMPTS_INDEX.md
================================================================================

Write: prompts/PROMPTS_INDEX.md

  # CHP Prompts Index
  Last updated: [date]

  ## How to run any prompt
  ```bash
  cd D:\EXPERIMENTS\context-hacking
  claude --dangerously-skip-permissions < prompts/[name].md
  ```

  ## Run — executed, results exist
  | Prompt | Date | Output | Status |
  |--------|------|--------|--------|
  | math_sprint.md | 2026-03-21 | 3 math experiments, 10k digits each | complete |
  | euler_e.md | 2026-03-21 | experiments/euler-e/ | complete |
  | dashboard_sync.md | 2026-03-21 | figures.py synced, icons fixed | complete |
  | dashboard_redesign.md | 2026-03-21 | dashboard white theme | complete |
  | consolidate.md | 2026-03-21 | EXPERIMENT_INDEX.json, all reports | complete |

  ## Ready to run — not yet executed
  | Prompt | What it does | Est. time |
  |--------|-------------|-----------|
  | anatomy_viewer.md | HTML canvas anatomy viewer (Gray's Anatomy) | ~30min |
  | anatomy_viewer_vtk.md | VTK 3D anatomy viewer | ~45min |

  ## Agent role prompts — use inside CHP loop
  | Prompt | Role | When to use |
  |--------|------|------------|
  | builder.md | Builder agent | Start of each turn |
  | critic.md | Critic (Pessimist) | After build |
  | reviewer.md | Reviewer (Linter) | After critic |
  | council_gpt.md | GPT-4o council review | Send externally |
  | council_grok.md | Grok council review | Send externally |

  ## Templates — copy and adapt
  | Prompt | Purpose |
  |--------|---------|
  | loop_template.md | New experiment loop structure |
  | health_check.md | Check current loop state |

================================================================================
JOB 8 — FIX ROOT-LEVEL TEMPLATE FILES
================================================================================

The root context-hacking folder has blank template files that look like
an active project but are not. Fix them clearly.

8A. Add template warning to CHAIN_PROMPT.md (top of file):

  # THIS IS A TEMPLATE — NOT AN ACTIVE PROJECT
  # Copy to your experiment directory and fill in sections.
  # Active experiment: chp-test-run/ (schelling-segregation)
  # All experiments: see EXPERIMENT_INDEX.json
  # ────────────────────────────────────────────────────────

8B. Update root innovation_log.md:

  Replace the "No turns recorded" placeholder with:

  # CHP Framework — Innovation Log
  # This is the ROOT framework log — not an experiment log.
  # Experiment logs live in: chp-test-run/experiments/[name]/innovation_log.md
  #
  # Framework changes:
  # 2026-03-21: Dashboard white theme, health tab 2-col layout
  # 2026-03-21: figures.py FIGURE_DESCRIPTIONS single source of truth
  # 2026-03-21: EXPERIMENT_INDEX.json created — full project registry
  # 2026-03-21: Tests written for all 10 loop-run experiments
  # 2026-03-21: REPORT.md written for metal-harmony, euler-e, pi-machin, sqrt2-newton

8C. Update root state_vector.md:

  TURN: N/A — framework level
  MILESTONE: Consolidation complete
  MODE: STABLE
  OPEN_FLAGS: none
  NEXT_TURN_FOCUS: Run anatomy-viewer or simsiv-v1-replication
  SCIENCE_GROUNDING: See EXPERIMENT_INDEX.json for full picture

================================================================================
JOB 9 — APPEND REGISTRY TO README.md + CLEAN UP DUPLICATES
================================================================================

9A. Mark pi-calculator as superseded.
    Read: experiments/pi-calculator/
    Add a README.md inside it:

      # pi-calculator — SUPERSEDED
      This is an early draft, superseded by experiments/pi-machin/.
      See experiments/pi-machin/ for the working Machin formula implementation.
      Do not use this directory.

9B. Append to the END of README.md (do not change existing content):

  ---

  ## Experiment Registry

  Full machine-readable index: [`EXPERIMENT_INDEX.json`](EXPERIMENT_INDEX.json)

  ### Loop-run experiments (`chp-test-run/experiments/`)
  Built through the full CHP orchestrator loop with innovation logs and telemetry.

  | Experiment | Domain | Turns | FPs | Key Result |
  |-----------|--------|-------|-----|-----------|
  | schelling-segregation | Social Science | 4 | 1 | p<0.000001, d=-1.83 |
  | spatial-prisoners-dilemma | Game Theory | 3 | 1 | coop=0.41, std=0.017 |
  | sir-epidemic | Epidemiology | 2 | 1 | fadeout=3% (impossible in ODE) |
  | lorenz-attractor | Chaos Theory | 2 | 1 | RK45, Lyapunov=0.35 |
  | izhikevich-neurons | Neuroscience | 2 | 1 | 5 patterns, no HH contamination |
  | quantum-grover | Quantum Computing | 2 | 1 | P=0.9995 at k_opt=25 |
  | blockchain-consensus | Distributed Systems | 2 | 1 | PBFT safety f<N/3 confirmed |
  | lotka-volterra | Ecology | 2 | 1 | extinction confirmed (impossible in ODE) |
  | ml-hyperparam-search | Machine Learning | 2 | 1 | val=0.87-0.92, no leakage |
  | metal-harmony | Music Theory | 1 | 1 | classical: 6-9 errors. metal: 0 |

  ### Direct-prompt experiments (`experiments/`)
  Built via single CLI prompt, verified against frozen reference.

  | Experiment | Domain | Algorithm | Digits | Multiplier |
  |-----------|--------|-----------|--------|-----------|
  | euler-e | Mathematics | Taylor series | 10,000 | 667x LLM ceiling |
  | pi-machin | Mathematics | Machin formula | 10,000 | 667x LLM ceiling |
  | sqrt2-newton | Mathematics | Newton (14 iter) | 10,000 | 625x LLM ceiling |
  | schroeder-reverb | Audio DSP | Freeverb | N/A | 8 combs vs 4 (prior) |

  ### Staged experiments — spec written, not yet run
  | Experiment | What it will build |
  |-----------|-------------------|
  | anatomy-viewer | HTML canvas body systems viewer (Gray's Anatomy spec) |
  | anatomy-viewer-vtk | VTK 3D medical viewer |
  | simsiv-v1-replication | 35-trait social evolution sim, ~10k lines |
  | simsiv-v2-replication | SIMSIV with institutional differentiation |

  ### Framework assets
  - `ablation/` — 3-condition ablation study: no spec (36% accuracy) →
    spec only (100% values) → full CHP (behavioral verification)
  - `docs/methods_section.md` — publication-ready methods section
  - `prompts/PROMPTS_INDEX.md` — index of all 13 CLI prompts

================================================================================
SELF-CHECK — DO BEFORE FINISHING
================================================================================

Run each check. Report PASS or FAIL.

  [ ] python -m pytest chp-test-run/experiments/ -v --tb=short
      Expected: all new tests pass
      FAIL if any new test errors out (fix the test or the source)

  [ ] ls chp-test-run/experiments/metal-harmony/REPORT.md
      Expected: file exists
      FAIL if missing

  [ ] ls experiments/euler-e/REPORT.md
      Expected: file exists

  [ ] ls experiments/pi-machin/REPORT.md
      Expected: file exists

  [ ] ls experiments/sqrt2-newton/REPORT.md
      Expected: file exists

  [ ] ls chp-test-run/experiments/lotka-volterra/figures/
      Expected: contains at least one .png

  [ ] ls chp-test-run/experiments/ml-hyperparam-search/figures/
      Expected: contains at least one .png

  [ ] python -c "import json; d=json.load(open('EXPERIMENT_INDEX.json')); print(d['summary']['total'], 'experiments indexed')"
      Expected: prints "19 experiments indexed" or higher
      FAIL if JSON invalid or count wrong

  [ ] grep -l "STATUS:" prompts/*.md | wc -l
      Expected: 14 (all prompts including new PROMPTS_INDEX)

  [ ] ls prompts/PROMPTS_INDEX.md
      Expected: file exists

  [ ] grep "Experiment Registry" README.md
      Expected: found
      FAIL if missing

  [ ] ls experiments/pi-calculator/README.md
      Expected: file exists with "SUPERSEDED" in content

  [ ] ls chp-test-run/experiments/spatial-prisoners-dilemma/tests/
      Expected: contains test_spatial_pd.py

  [ ] python -m pytest chp-test-run/experiments/sir-epidemic/tests/ -v
      Expected: PASS

================================================================================
FINAL REPORT
================================================================================

When all 9 jobs and all checks pass, print a summary:

  ╔══════════════════════════════════════════════════════════╗
  ║         CHP OVERNIGHT CONSOLIDATION — COMPLETE           ║
  ╚══════════════════════════════════════════════════════════╝

  Jobs completed:
    1. Reports written:     metal-harmony, euler-e, pi-machin, sqrt2-newton
    2. Tests written:       9 experiments now have test suites
    3. Figures generated:   lotka-volterra, ml-hyperparam-search
    4. Telemetry backfilled: 9 experiments
    5. EXPERIMENT_INDEX.json: [N] experiments indexed
    6. Prompt headers:      14 files updated
    7. PROMPTS_INDEX.md:    written
    8. Template warnings:   CHAIN_PROMPT.md, innovation_log.md, state_vector.md
    9. README.md:           experiment registry appended

  State of the project:
    Complete experiments:   [N]
    Staged experiments:     [N]
    Total false positives:  [N]
    Experiments with tests: [N] / 14
    Experiments with telemetry: [N] / 14

  What to do next (in priority order):
    1. Run: claude < prompts/anatomy_viewer.md       (HTML anatomy viewer)
    2. Run: claude < prompts/anatomy_viewer_vtk.md   (VTK 3D viewer)
    3. Run simsiv-v1-replication                     (biggest experiment)
    4. Open dashboard: cd chp-test-run && python -m streamlit run ..\dashboard\app.py --server.port 8502
