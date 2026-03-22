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

| Discipline | Cat | Disc | Loop | Total |
|---|---|---|---|---|
| Chemistry | 10 | 0 | 0 | 10 |
| Physics | 30 | 0 | 1 | 31 |
| Mathematics | 5 | 0 | 0 | 5 |
| Statistics | 25 | 0 | 0 | 25 |
| Biology | 30 | 0 | 3 | 33 |
| Engineering | 25 | 0 | 0 | 25 |
| Economics | 20 | 0 | 0 | 20 |
| Earth Science | 20 | 0 | 0 | 20 |
| Astronomy | 20 | 0 | 0 | 20 |
| Social Science | 0 | 0 | 2 | 2+2 staged |
| Computer Science | 0 | 0 | 3 | 3 |
| Medicine | 2 | 0 | 0 | 2 |
| Audio DSP | 0 | 0 | 1 | 1 |
| Music | 0 | 0 | 1 | 1 |
| **Total** | **187** | **0** | **13** | **201** |

### What each type validates

- **cat-** experiments validate **Layer 1 (Prior-as-Detector)** and **Layer 3 (Frozen Code Forcing)** — they catalog predictable LLM errors and prove frozen specs catch them
- **loop-** experiments validate **all 9 CHP layers** — full Builder/Critic/Reviewer with sigma gates, dead ends, and mode switching
- **disc-** experiments validate **Layer 1 in the wild** — proving errors occur naturally, not just in constructed test cases

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
# All catalog experiments (by discipline)
python -m pytest experiments/statistics/cat-stat-*/tests/ -q
python -m pytest experiments/biology/cat-bio-*/tests/ -q
python -m pytest experiments/engineering/cat-eng-*/tests/ -q
python -m pytest experiments/economics/cat-econ-*/tests/ -q
python -m pytest experiments/earth-science/cat-earth-*/tests/ -q
python -m pytest experiments/astronomy/cat-astro-*/tests/ -q
python -m pytest experiments/physics/cat-phys-*/tests/ -q
python -m pytest experiments/chemistry/cat-chem-*/tests/ -q

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
