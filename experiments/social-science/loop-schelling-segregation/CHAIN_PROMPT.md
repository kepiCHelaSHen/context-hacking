# Schelling Segregation — Chain Prompt

================================================================================
PROJECT IDENTITY
================================================================================

Name:       Schelling Segregation (CHP Showcase)
Purpose:    Demonstrate the Context Hacking Protocol on a classic ABM.
            Build the 1971 Schelling model + the CHP dynamic-tolerance extension.
            Show Prior-as-Detector catching textbook drift.

================================================================================
CONFIRMED DESIGN DECISIONS
================================================================================

DD01 — Grid: 50x50 toroidal. (Schelling 1971)
DD02 — Density: 0.90, two types at 50/50 ratio.
DD03 — Neighborhood: Moore (8 cells).
DD04 — Tolerance: 0.375 (NOT 0.33, NOT 0.50 — those are LLM priors).
DD05 — Update order: SIMULTANEOUS (NOT sequential).
DD06 — Dynamic tolerance: update rate 0.005, comfort margin 0.1, range [0.1, 0.9].
DD07 — Tolerance updates applied AFTER the move step, not before.

================================================================================
ARCHITECTURE RULES
================================================================================

- Pure library: NO print(), NO UI in the simulation module.
- All randomness via seeded numpy.random.Generator.
- Same seed = identical output.
- Structured logging via logging.getLogger(__name__).
- Events as dicts: {step, type, description}.

================================================================================
FROZEN CODE
================================================================================

frozen/schelling_rules.md — DO NOT MODIFY.
Every coefficient must match this file exactly.

================================================================================
FILE INVENTORY
================================================================================

| File | Description |
|------|-------------|
| frozen/schelling_rules.md | Frozen specification |
| spec.md | Experiment specification |
| config.yaml | CHP config for this experiment |
| CHAIN_PROMPT.md | This file |
| innovation_log.md | Build history |
| dead_ends.md | Failed approaches |
| state_vector.md | Context anchor |
| tests/test_milestone_battery.py | 4-milestone sigma-gated test battery |
| schelling.py | TO BE BUILT by the CHP loop |
| run_experiment.py | TO BE BUILT by the CHP loop |
