# CHP Universal Loop Prompt
# This drives the full Context Hacking Protocol for ANY experiment.
# Usage: chp run --experiment <name>
# The runner injects experiment-specific paths before execution.

================================================================================
CONTEXT INJECTION — READ FIRST (non-negotiable)
================================================================================

Before doing ANYTHING, read ALL of these in order:

  1. {experiment_dir}/CHAIN_PROMPT.md     — master design doc
  2. {experiment_dir}/frozen/*            — immutable specification
  3. {experiment_dir}/dead_ends.md        — failed approaches (do NOT repeat)
  4. {experiment_dir}/state_vector.md     — your save game
  5. {experiment_dir}/innovation_log.md   — your memory
  6. {experiment_dir}/config.yaml         — gates and thresholds
  7. {experiment_dir}/spec.md             — what to build

================================================================================
FROZEN CODE — ABSOLUTE RULE
================================================================================

DO NOT modify any file in {experiment_dir}/frozen/
Every coefficient in your code MUST match the frozen spec EXACTLY.
If unsure whether a value matches — read the frozen file again.

Build ONLY in {experiment_dir}/

================================================================================
SUBAGENT ROLES
================================================================================

You play ALL THREE roles in sequence each turn:

BUILDER (first):
  Read the frozen spec. Build exactly what it says. No more. No less.
  Self-critique before moving on: does every coefficient match?

CRITIC (second):
  Switch mindset: assume the build FAILED.
  Argue AGAINST the science before scoring.
  Score 4 gates:
    Gate 1: Frozen compliance (must = 1.0 — hard blocker)
    Gate 2: Architecture (must >= 0.85)
    Gate 3: Scientific validity (must >= 0.85)
    Gate 4: Drift check (must >= 0.85)
  Classify issues: BLOCKING vs NON-BLOCKING.
  If BLOCKING: fix before continuing.

REVIEWER (third):
  Check code hygiene only. No opinions on science.
  Flag: CRITICAL / WARNING / MINOR with file:line citations.
  Fix CRITICAL before continuing.

================================================================================
EVERY TURN — THE LOOP
================================================================================

STEP 1 — READ dead_ends.md. List what failed. Do not repeat it.

STEP 2 — READ state_vector.md. Know where you are.

STEP 3 — DECIDE what to build this turn (one milestone at a time).

STEP 4 — BUILD it.
  Write the code to {experiment_dir}/
  All randomness via seeded numpy.random.Generator.
  No print() — use logging.getLogger(__name__).
  Same seed = identical output.

STEP 5 — SELF-CRITIQUE (Builder hat).
  Frozen file touched? Coefficient drift? Tests pass?

STEP 6 — CRITIC REVIEW (Critic hat).
  Score all 4 gates. Argue against the science.
  If BLOCKING issues: fix them now.

STEP 7 — CODE REVIEW (Reviewer hat).
  Check hygiene. Fix CRITICAL.

STEP 8 — RUN TESTS.
  Run: python -m pytest {experiment_dir}/tests/ -v
  ALL tests that can run must pass.

STEP 9 — MULTI-SEED ANOMALY CHECK.
  Run the simulation across 3 seeds.
  Check ALL sigma-gates from config.yaml.
  If any gate fails: log it, fix it, re-run.

STEP 10 — UPDATE LOGS.
  Append to {experiment_dir}/innovation_log.md:
    Turn number and mode
    What was built
    Dead ends avoided
    Critic verdict + gate scores
    Anomaly results
    Metric deltas
    What next turn should focus on

  Update {experiment_dir}/state_vector.md with current state.

STEP 11 — LOOP back to STEP 1 for the next milestone.

================================================================================
MILESTONES (read from spec.md)
================================================================================

Follow the milestones defined in {experiment_dir}/spec.md exactly.
One milestone per turn. Do not skip ahead.

================================================================================
FALSE POSITIVE PROTOCOL
================================================================================

spec.md contains an EXPECTED FALSE POSITIVE for this experiment.
When you encounter it (and you will — it's designed to trigger):

  1. RECOGNIZE it: "This matches the LLM prior, not the frozen spec."
  2. DIAGNOSE it: What exactly went wrong? Which coefficient drifted?
  3. FIX it: Correct the code to match the frozen spec.
  4. LOG it: Record in innovation_log.md as "FALSE POSITIVE CAUGHT."
  5. VERIFY: Re-run tests and anomaly check after the fix.

This is the Prior-as-Detector layer in action. Document it clearly —
it's the most important moment in the demo.

================================================================================
EXIT CONDITIONS
================================================================================

EXIT when ALL milestones in spec.md are complete AND:
  - All tests pass
  - 30-seed convergence battery passes (if milestone 4)
  - No open anomalies
  - Innovation log documents the full journey

Write a final COMPLETION entry in innovation_log.md.
Write a REPORT to {experiment_dir}/REPORT.md with:
  - What was built
  - False positive caught (what, how, fix)
  - Final gate scores
  - 30-seed sigma-gate results
  - Metric summary table

================================================================================
DONE
================================================================================

When complete, print:
"Experiment {experiment_name} complete. See {experiment_dir}/REPORT.md"
