# CHP Multi-Discipline Experiment Study

**Goal**: 500 verified computational experiments across 14 scientific disciplines,
systematically cataloging LLM prior errors caught by frozen-spec verification.

**Core thesis**: A protocol that compares computed results against frozen reference
constants catches errors at every layer — including errors in its own specifications.
The 500 experiments provide the statistical power to show this is systematic.

## Evidence Standards

Every experiment is prefixed with its evidence standard:

| Prefix | Standard | What It Proves |
|--------|----------|----------------|
| `cat-` | Catalog | Pre-specified errors, single-pass verification. "LLMs get this wrong." |
| `disc-` | Discovery | LLM runs without spec first; error captured then corrected. "We proved it happens." |
| `loop-` | Loop | Full multi-turn Builder/Critic with gate scores. "The protocol finds and fixes it." |
| `superseded-` | Superseded | Replaced by a better experiment. Kept for history. |

## Directory Structure

```
experiments/
  README.md                  <- you are here
  FINDINGS.md                <- aggregate findings across all disciplines
  STUDY_PLAN.md              <- master plan: all 500 experiments listed with types
  rebuild_index.py           <- rebuilds EXPERIMENT_INDEX.json from filesystem
  figures/                   <- cross-discipline summary figures

  astronomy/                 <- stellar, planetary, cosmology, orbital mechanics
  audio-dsp/                 <- signal processing, reverb, synthesis
  biology/                   <- epidemiology, ecology, neuroscience, genetics
  chemistry/                 <- equilibrium, kinetics, buffers, electrochemistry, ...
  computer-science/          <- quantum, distributed systems, ML
  earth-science/             <- geology, meteorology, oceanography, climate
  economics/                 <- micro, macro, finance, game theory
  engineering/               <- circuits, structures, fluids, materials, controls
  mathematics/               <- constants (e, pi, sqrt2), computation, number theory
  medicine/                  <- anatomy, pharmacology, physiology
  music/                     <- harmony analysis, theory
  physics/                   <- mechanics, thermodynamics, E&M, chaos, quantum
  social-science/            <- agent-based models, game theory, segregation
  statistics/                <- distributions, hypothesis testing, Bayesian, regression
```

## Per-Experiment Structure

Every experiment follows the same template:

```
experiments/<discipline>/<prefix>-<name>/
  metadata.json              <- scientific metadata (authoritative for index)
  frozen/                    <- constants from authoritative sources (DO NOT MODIFY)
    <name>_constants.py
  <name>.py                  <- implementation (imports from frozen/)
  tests/
    test_<name>.py           <- TestPriorErrors + TestCorrectness classes
  figures/
    <name>_*.png             <- generated visualizations
  REPORT.md                  <- human-readable narrative
  <name>_innovation_log.md   <- (loop experiments only)
  <name>_state_vector.md     <- (loop experiments only)
  <name>_dead_ends.md        <- (loop experiments only)
```

### metadata.json

Each experiment writes a `metadata.json` that the rebuild script reads. This is
the authoritative source for scientific fields in the index.

```json
{
  "display_name": "Projectile Motion",
  "standard": "cat",
  "domain": "Physics",
  "sprint": "physics-sprint-2026",
  "status": "complete",
  "key_result": "Drag reduces range 30%+; g=9.80665 not 10",
  "false_positives_caught": 2,
  "turns": null,
  "gate_scores": null,
  "statistical_result": null,
  "meta_spec_errors": 0,
  "notes": null
}
```

The rebuild script derives structural fields (source_files, has_tests, has_figures,
etc.) from the filesystem. No manual index editing.

## Current Status

| Discipline | Cat | Loop | Total | Target |
|---|---|---|---|---|
| Chemistry | 10 | 0 | 10 | 50 |
| Physics | 20 | 1 | 21 | 50 |
| Mathematics | 5 | 0 | 5 | 50 |
| Biology | 0 | 3 | 3 | 50 |
| Social Science | 0 | 2 | 2+2 staged | 30 |
| Computer Science | 0 | 3 | 3 | 40 |
| Medicine | 2 | 0 | 2 | 20 |
| Engineering | 0 | 0 | 0 | 40 |
| Statistics | 0 | 0 | 0 | 40 |
| Economics | 0 | 0 | 0 | 30 |
| Earth Science | 0 | 0 | 0 | 30 |
| Astronomy | 0 | 0 | 0 | 30 |
| Audio DSP | 0 | 1 | 1 | 10 |
| Music | 0 | 1 | 1 | 10 |
| **Total** | **37** | **13** | **51** | **500** |

## Error Taxonomy

Every LLM prior error falls into one of these categories:

1. **Unit errors** — kJ vs J, pm vs nm, degrees vs radians
2. **Sign errors** — van't Hoff, Nernst, Hess's law direction
3. **Formula errors** — wrong exponent, missing term, inverted ratio
4. **Constant precision** — rounded values, outdated measurements
5. **Conceptual errors** — wrong model applied (e.g., ideal gas for CO2)
6. **Convention errors** — clinical vs thermodynamic pKa, Libby vs Godwin half-life
7. **Meta-specification errors** — the frozen spec itself contains LLM-generated errors

Category 7 is the key finding: the protocol catches errors regardless of which
layer introduced them.

## Running Tests

```bash
# All catalog experiments
python -m pytest experiments/chemistry/cat-*/tests/ experiments/physics/cat-*/tests/ -v --tb=short

# Single discipline
python -m pytest experiments/chemistry/ -v --tb=short

# Single experiment
python -m pytest experiments/chemistry/cat-chem-equilibrium/tests/ -v --tb=short

# Rebuild index from filesystem
python experiments/rebuild_index.py
```

## Adding New Experiments

1. Choose a discipline directory
2. Create `<prefix>-<name>/` with frozen/, tests/, figures/ subdirs
3. Write `frozen/<name>_constants.py` with authoritative source citations
4. Write `tests/test_<name>.py` with TestPriorErrors and TestCorrectness
5. Write `<name>.py` importing only from frozen constants
6. Write `metadata.json` with key_result, false_positives_caught, etc.
7. Run tests, generate figures, write REPORT.md
8. Run `python experiments/rebuild_index.py` to update the index
