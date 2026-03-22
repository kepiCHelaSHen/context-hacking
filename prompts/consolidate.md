<!-- STATUS: run | DATE: 2026-03-21 | OUTPUT: see EXPERIMENT_INDEX.json -->
---
name: chp-consolidate
description: "Consolidate all experiments into a single index, write missing reports, add status headers to prompts."
tools: Read, Write, Edit, Bash
---

# CHP Consolidation — Fix the Mess

The context-hacking project has grown ad-hoc. Two experiment locations,
13 prompts with no status, one experiment with no report, and no central
index anywhere. This job fixes all of it in one pass.

No new experiments. No new features. Organize what exists.

================================================================================
READ FIRST — UNDERSTAND THE STRUCTURE
================================================================================

Read these to understand what exists:

  1. Scan chp-test-run/experiments/ — list every directory
  2. Scan experiments/ — list every directory
  3. List prompts/ — all 13 files
  4. Read ablation/ABLATION_REPORT.md
  5. Read docs/methods_section.md (first 20 lines — just to know it exists)

Do not write anything until you have listed all three locations.

================================================================================
THE CONSOLIDATION DECISION — WHY WE KEEP TWO EXPERIMENT DIRS
================================================================================

DO NOT merge the two experiment directories. They represent different things:

  chp-test-run/experiments/
    "Loop-run experiments" — ran through the CHP runner loop.
    Have innovation logs, state vectors, dead ends, figures, REPORT.md.
    telemetry.json exists for schelling (others don't — that's OK).
    These are the scientific experiments.

  experiments/
    "Direct-prompt experiments" — ran via claude CLI prompts directly.
    Math sprint (e, pi, sqrt2), anatomy specs, simsiv specs.
    Well-structured with frozen/, tests/, figures/.
    These are framework demonstrations and staged experiments.

Both locations are valid. The INDEX.json just needs to know about both.

================================================================================
JOB 1 — WRITE metal-harmony REPORT.md (10 minutes)
================================================================================

This is the only experiment missing a report.

Location: chp-test-run/experiments/metal-harmony/

Read the source code:
  chp-test-run/experiments/metal-harmony/metal_analyzer.py

Understand what it does, then write REPORT.md following this template
(match exactly the format of the other experiment reports):

  # Metal Harmony — CHP Experiment Report

  ## Summary
  [2-3 sentences: what was built, what was the key result]

  ## False Positive Story
  [What prior error was caught. If uncertain from code, write what the
   experiment was designed to catch: classical harmony rules applied to
   metal music — should produce zero errors, not 6-9 like classical analysis]

  ## Key Results
  [Table or bullet points of measurable outputs from the code]

  ## Gate Scores
  | Gate | Score |
  |------|-------|
  | Frozen compliance | [read from code] |
  | Architecture | [estimate] |
  | Scientific validity | [estimate] |
  | Drift check | [estimate] |

Read metal_analyzer.py carefully. Extract:
  - What musical theory framework it uses
  - What riffs it analyzes (look for riff names in the code)
  - What the classical vs metal error counts are
  - What the false positive was

Write the REPORT.md from the actual code. Do not invent results.
If the code defines results clearly: use them.
If not: describe what the code does and note "results require execution."

================================================================================
JOB 2 — BUILD EXPERIMENT_INDEX.json
================================================================================

Write: EXPERIMENT_INDEX.json at D:\EXPERIMENTS\context-hacking\EXPERIMENT_INDEX.json

This is the single source of truth for all experiments.
The dashboard, analysis scripts, and future prompts all read from this file.

Schema (one entry per experiment):

{
  "experiments": {
    "[experiment-name]": {
      "name": "[display name]",
      "location": "loop-run OR direct-prompt",
      "path": "[relative path from context-hacking root]",
      "status": "complete OR staged OR incomplete",
      "domain": "[Social Science / Math / Physics / etc]",
      "has_report": true/false,
      "has_tests": true/false,
      "has_figures": true/false,
      "has_telemetry": true/false,
      "has_frozen_spec": true/false,
      "turns": [number or null],
      "false_positives": [number or null],
      "false_positive_descriptions": ["..."] or [],
      "key_result": "[one sentence from REPORT.md summary, or null]",
      "gate_scores": {"g1": x, "g2": x, "g3": x, "g4": x} or null,
      "p_value": "[string or null]",
      "effect_size": "[string or null]",
      "notes": "[anything notable — missing telemetry, superseded by another exp, etc]"
    }
  },
  "meta": {
    "generated": "[ISO timestamp]",
    "total_experiments": N,
    "complete": N,
    "staged": N,
    "loop_run": N,
    "direct_prompt": N,
    "total_false_positives": N
  }
}

Populate the index by reading each experiment's REPORT.md.
For experiments without REPORT.md: status = "incomplete", all fields null.
For staged experiments (spec exists, never run): status = "staged".

Here are the experiments to index — populate ALL of them:

LOOP-RUN (chp-test-run/experiments/):
  - schelling-segregation (4 turns, telemetry, full report)
  - spatial-prisoners-dilemma (report exists)
  - sir-epidemic (report exists)
  - lorenz-attractor (report exists)
  - izhikevich-neurons (report exists)
  - quantum-grover (report exists)
  - blockchain-consensus (report exists)
  - lotka-volterra (report exists)
  - ml-hyperparam-search (report exists)
  - metal-harmony (no report yet — write it in Job 1 first, then index it)

DIRECT-PROMPT (experiments/):
  - euler-e (complete — compute_e.py, tests, 10k digits)
  - pi-machin (complete — compute_pi.py, frozen spec)
  - sqrt2-newton (complete — compute_sqrt2.py, Newton 14 iter)
  - anatomy-viewer (staged — full spec, tests, never run)
  - anatomy-viewer-vtk (staged — full spec, never run)
  - simsiv-v1-replication (staged — spec exists)
  - simsiv-v2-replication (staged — spec exists)
  - schroeder-reverb (staged)
  - pi-calculator (note: superseded by pi-machin — mark as such)

FRAMEWORK ASSETS (not experiments, but worth noting in meta):
  - ablation/ — 3-condition ablation study, results JSON, publishable
  - docs/methods_section.md — 17KB publication-ready methods section
  - prompts/ — 13 CLI prompts

================================================================================
JOB 3 — ADD STATUS HEADERS TO ALL PROMPTS
================================================================================

For each file in prompts/, add a 5-line status block at the very top,
BEFORE the existing --- frontmatter:

  <!--
  STATUS: [run / not-run / superseded / template / agent-role]
  DATE_RUN: [date if known, else "unknown"]
  OUTPUT: [brief description of what it produced, or "none"]
  SUPERSEDED_BY: [if superseded, by what]
  -->

Use these classifications:

  prompts/math_sprint.md
    STATUS: run
    DATE_RUN: 2026-03-21
    OUTPUT: euler-e, pi-machin, sqrt2-newton in experiments/ — all complete

  prompts/euler_e.md
    STATUS: run
    DATE_RUN: 2026-03-21
    OUTPUT: experiments/euler-e/compute_e.py, 10k digits, tests passing

  prompts/dashboard_sync.md
    STATUS: run
    DATE_RUN: 2026-03-21
    OUTPUT: figures.py synced, health_patch.py deleted, icons fixed

  prompts/dashboard_redesign.md
    STATUS: run
    DATE_RUN: 2026-03-21
    OUTPUT: dashboard/app.py white clinical theme

  prompts/anatomy_viewer.md
    STATUS: not-run
    DATE_RUN: none
    OUTPUT: none — spec and tests written but never executed

  prompts/anatomy_viewer_vtk.md
    STATUS: not-run
    DATE_RUN: none
    OUTPUT: none — staged only

  prompts/builder.md
    STATUS: agent-role
    DATE_RUN: n/a
    OUTPUT: used as role context in CHP loop turns

  prompts/critic.md
    STATUS: agent-role
    DATE_RUN: n/a
    OUTPUT: used as role context in CHP loop turns

  prompts/reviewer.md
    STATUS: agent-role
    DATE_RUN: n/a
    OUTPUT: used as role context in CHP loop turns

  prompts/council_gpt.md
    STATUS: agent-role
    DATE_RUN: n/a
    OUTPUT: send to GPT-4o for council review

  prompts/council_grok.md
    STATUS: agent-role
    DATE_RUN: n/a
    OUTPUT: send to Grok for council review

  prompts/loop_template.md
    STATUS: template
    DATE_RUN: n/a
    OUTPUT: generic starting point for new experiment prompts

  prompts/health_check.md
    STATUS: template
    DATE_RUN: n/a
    OUTPUT: utility prompt for checking CHP loop health

Add the block to each file. Do not change anything else in the files.
Find the exact start of each file, prepend the block, save.

================================================================================
JOB 4 — WRITE PROMPTS_INDEX.md
================================================================================

Write: prompts/PROMPTS_INDEX.md

A simple human-readable index of all prompts:

  # Prompts Index
  Last updated: [date]

  ## Run — executed, results exist
  | Prompt | Date run | Output |
  |--------|----------|--------|
  | math_sprint.md | 2026-03-21 | 3 math experiments complete |
  | euler_e.md | 2026-03-21 | 10k digits of e |
  | dashboard_sync.md | 2026-03-21 | figures.py sync |
  | dashboard_redesign.md | 2026-03-21 | white dashboard theme |

  ## Not Run — staged, ready to execute
  | Prompt | What it does | Run with |
  |--------|-------------|----------|
  | anatomy_viewer.md | HTML canvas anatomy viewer | claude < prompts/anatomy_viewer.md |
  | anatomy_viewer_vtk.md | VTK 3D anatomy viewer | claude < prompts/anatomy_viewer_vtk.md |

  ## Agent Roles — used inside the loop
  | Prompt | Role |
  |--------|------|
  | builder.md | Builder agent context |
  | critic.md | Critic (Pessimist) context |
  | reviewer.md | Reviewer (Linter) context |
  | council_gpt.md | Send to GPT-4o for council review |
  | council_grok.md | Send to Grok for council review |

  ## Templates — starting points
  | Prompt | Use for |
  |--------|---------|
  | loop_template.md | New experiment loop |
  | health_check.md | Check loop state |

  ## How to run a prompt
    cd D:\EXPERIMENTS\context-hacking
    claude --dangerously-skip-permissions < prompts/[name].md

================================================================================
JOB 5 — FIX THE ROOT CHAIN_PROMPT.md
================================================================================

The root CHAIN_PROMPT.md is a blank template with placeholder text.
It should be clearly marked as a template, not mistaken for an active project.

Add this block at the very top of CHAIN_PROMPT.md (before everything else):

  # ⚠ THIS IS A TEMPLATE — NOT AN ACTIVE PROJECT
  # This is the blank CHAIN_PROMPT.md template for new CHP experiments.
  # To use: copy this file to your experiment directory and fill in the sections.
  # Active projects: see chp-test-run/ and experiments/
  # Central index: see EXPERIMENT_INDEX.json
  #
  # ─────────────────────────────────────────────────────────────────────────────

Do not change anything else.

================================================================================
JOB 6 — WRITE A MASTER README SECTION
================================================================================

The README.md is 28KB and already exists. Do NOT rewrite it.

Instead, append this section at the very end of README.md:

  ---

  ## Experiment Registry

  All experiments are indexed in `EXPERIMENT_INDEX.json` at the project root.

  ### Completed experiments (loop-run via CHP runner)
  Located in `chp-test-run/experiments/`:
  - schelling-segregation — Social science · 4 turns · p<0.000001 · d=-1.83
  - spatial-prisoners-dilemma — Game theory · coop=0.41 · std=0.017
  - sir-epidemic — Epidemiology · fadeout=3% · stochastic confirmed
  - lorenz-attractor — Chaos theory · RK45 · Lyapunov=0.35
  - izhikevich-neurons — Neuroscience · 5 firing patterns · no HH contamination
  - quantum-grover — Quantum computing · P=0.9995 at k=25
  - blockchain-consensus — Distributed systems · PBFT safety confirmed f<N/3
  - lotka-volterra — Ecology · predator extinction confirmed (impossible in ODE)
  - ml-hyperparam-search — Machine learning · val acc 0.87-0.92 · no leakage
  - metal-harmony — Music theory · classical flags 6-9 errors · metal: zero

  ### Completed experiments (direct-prompt via CLI)
  Located in `experiments/`:
  - euler-e — e to 10,000 digits · 667x LLM ceiling · Taylor series · 0.11s
  - pi-machin — pi to 10,000 digits · 667x LLM ceiling · Machin formula · 0.36s
  - sqrt2-newton — sqrt(2) to 10,000 digits · Newton 14 iterations · 0.04s

  ### Staged experiments (spec written, never run)
  Located in `experiments/`:
  - anatomy-viewer — HTML canvas anatomy viewer (Gray's Anatomy frozen spec)
  - anatomy-viewer-vtk — VTK 3D anatomy viewer (same frozen spec)
  - simsiv-v1-replication, simsiv-v2-replication, schroeder-reverb

  ### Framework assets
  - `ablation/` — 3-condition ablation study proving each CHP layer matters
  - `docs/methods_section.md` — Publication-ready methods section
  - `prompts/` — 13 CLI prompts, see `prompts/PROMPTS_INDEX.md`

  ### Running experiments
  ```bash
  cd D:\EXPERIMENTS\context-hacking
  claude --dangerously-skip-permissions < prompts/[prompt_name].md
  ```

================================================================================
ORDER OF OPERATIONS
================================================================================

Do these in order. Do not skip any.

  1. Read metal_analyzer.py thoroughly
  2. Write chp-test-run/experiments/metal-harmony/REPORT.md
  3. Scan all experiment directories (both locations)
  4. Build EXPERIMENT_INDEX.json
  5. Add status headers to all 13 prompts in prompts/
  6. Write prompts/PROMPTS_INDEX.md
  7. Add template warning to root CHAIN_PROMPT.md
  8. Append experiment registry section to README.md

================================================================================
SELF-CHECK BEFORE FINISHING
================================================================================

  [ ] chp-test-run/experiments/metal-harmony/REPORT.md exists?
  [ ] EXPERIMENT_INDEX.json exists at project root?
  [ ] EXPERIMENT_INDEX.json has entries for all 19 experiments?
  [ ] EXPERIMENT_INDEX.json meta.total_experiments == 19?
  [ ] All 13 prompts in prompts/ have status headers?
  [ ] prompts/PROMPTS_INDEX.md exists?
  [ ] README.md has "## Experiment Registry" section?
  [ ] Root CHAIN_PROMPT.md has template warning at top?

================================================================================
DONE
================================================================================

When all jobs complete, print:

  "Consolidation complete.
   Jobs done:
   1. metal-harmony/REPORT.md written
   2. EXPERIMENT_INDEX.json built — [N] experiments indexed
   3. [13] prompts updated with status headers
   4. prompts/PROMPTS_INDEX.md written
   5. CHAIN_PROMPT.md marked as template
   6. README.md experiment registry appended

   Complete experiments: [N]
   Staged experiments:   [N]
   Total false positives across all completed experiments: [N]

   Run the dashboard to see the full picture:
   cd chp-test-run
   python -m streamlit run ..\dashboard\app.py --server.port 8502"
