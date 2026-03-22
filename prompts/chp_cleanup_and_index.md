# CHP Cleanup & Index Generation Prompt

You are working inside the `D:\EXPERIMENTS\context-hacking\` project.

Your job is to do three things in order:
1. Rename every completed experiment directory with the correct prefix
2. Standardize file names inside each experiment
3. Write a clean `experiments/EXPERIMENT_INDEX.json` the UI can consume

Do NOT modify any scientific content — source files, frozen constants, test files,
figures, or REPORT.md. Only rename directories and files. Do NOT touch staged or
superseded experiments.

---

## STEP 1 — Understand the Evidence Standards

Every experiment gets one of three prefixes based on its evidence standard:

| Prefix | Standard  | Criteria |
|--------|-----------|----------|
| `cat-` | Catalog   | Single-pass. Errors were pre-specified in the frozen spec before running. |
| `disc-`| Discovery | LLM was run WITHOUT the spec first to capture the raw error, then corrected. |
| `loop-`| Loop      | Full multi-turn Builder/Critic cycle with gate scores. |

---

## STEP 2 — Prefix Assignment for All 28 Complete Experiments

Apply these renames exactly. If the directory already has the correct prefix, skip it.

### Chemistry — `experiments/chemistry/`
```
chem-equilibrium          → cat-chem-equilibrium
chem-kinetics             → cat-chem-kinetics
chem-buffers              → cat-chem-buffers
chem-radioactive-decay    → cat-chem-radioactive-decay
chem-vdw-gas              → cat-chem-vdw-gas
chem-electrochemistry     → cat-chem-electrochemistry
chem-spectrophotometry    → cat-chem-spectrophotometry
chem-thermochemistry      → cat-chem-thermochemistry
chem-stoichiometry        → cat-chem-stoichiometry
chem-crystal-packing      → cat-chem-crystal-packing
```

### Mathematics — `experiments/mathematics/`
```
euler-e            → cat-euler-e
pi-machin          → cat-pi-machin
sqrt2-newton       → cat-sqrt2-newton
time_sprint        → cat-time-sprint
omega_sentinel_1M  → cat-omega-sentinel-1M
pi-calculator      → (DO NOT RENAME — status is superseded, leave as-is)
```

### Biology — `experiments/biology/`
```
sir-epidemic          → loop-sir-epidemic
lotka-volterra        → loop-lotka-volterra
izhikevich-neurons    → loop-izhikevich-neurons
```

### Physics — `experiments/physics/`
```
lorenz-attractor   → loop-lorenz-attractor
```

### Social Science — `experiments/social-science/`
```
schelling-segregation          → loop-schelling-segregation
spatial-prisoners-dilemma      → loop-spatial-prisoners-dilemma
simsiv-v1-replication          → (DO NOT RENAME — staged)
simsiv-v2-replication          → (DO NOT RENAME — staged)
```

### Computer Science — `experiments/computer-science/`
```
quantum-grover         → loop-quantum-grover
blockchain-consensus   → loop-blockchain-consensus
ml-hyperparam-search   → loop-ml-hyperparam-search
```

### Music — `experiments/music/`
```
metal-harmony   → loop-metal-harmony
```

### Audio DSP — `experiments/audio-dsp/`
```
schroeder-reverb   → loop-schroeder-reverb
```

### Medicine — `experiments/medicine/`
```
anatomy-viewer      → cat-anatomy-viewer
anatomy-viewer-vtk  → cat-anatomy-viewer-vtk
```

---

## STEP 3 — Standardize File Names Inside Each Experiment

After renaming directories, standardize the file names inside each experiment
to a consistent schema. The UI looks for these exact names:

| File | Standard Name |
|------|---------------|
| Innovation log | `innovation_log.md` |
| State vector   | `state_vector.md`   |
| Dead ends      | `dead_ends.md`      |
| Report         | `REPORT.md`         |

Some experiments use prefixed names like `chem_equilibrium_innovation_log.md`.
Rename these to the standard names. Rules:

- Any file matching `*_innovation_log.md` → rename to `innovation_log.md`
- Any file matching `*_state_vector.md`   → rename to `state_vector.md`
- Any file matching `*_dead_ends.md`      → rename to `dead_ends.md`
- `REPORT.md` is already correct — do not rename
- Do NOT rename Python source files, test files, frozen files, or figures

If a standard-named file already exists (e.g., `innovation_log.md` already
exists alongside `chem_equilibrium_innovation_log.md`), keep the standard-named
one and delete the prefixed duplicate.

---

## STEP 4 — Write `experiments/EXPERIMENT_INDEX.json`

After all renames are complete, write a fresh `experiments/EXPERIMENT_INDEX.json`
by walking the `experiments/` directory tree. Do NOT copy from the old root-level
`EXPERIMENT_INDEX.json` — derive everything from the actual filesystem state.

### Schema for each experiment entry:

```json
{
  "slug": "loop-schelling-segregation",
  "display_name": "Schelling Segregation",
  "standard": "loop",
  "discipline": "social-science",
  "dir": "experiments/social-science/loop-schelling-segregation",
  "status": "complete",
  "has_report": true,
  "has_innovation_log": true,
  "has_state_vector": true,
  "has_dead_ends": true,
  "has_figures": true,
  "has_frozen": true,
  "has_tests": true,
  "figures": ["segregation_dynamics.png", "grid_comparison.png"],
  "source_files": ["schelling.py"],
  "false_positives_caught": 1,
  "key_result": "...",
  "turns": 4,
  "gate_scores": {"g1": 1.00, "g2": 0.95, "g3": 0.92, "g4": 0.95},
  "statistical_result": "p < 0.000001",
  "domain": "Social Science",
  "sprint": null,
  "notes": "..."
}
```

### Rules for populating each field:

- `slug` — the directory name after renaming (e.g. `loop-schelling-segregation`)
- `standard` — first segment of the slug: `cat`, `disc`, or `loop`
- `discipline` — the parent directory name (e.g. `social-science`, `chemistry`)
- `dir` — relative path from project root: `experiments/<discipline>/<slug>`
- `status` — `"complete"` if REPORT.md exists, `"staged"` if no REPORT.md but
  spec or frozen exists, `"superseded"` for pi-calculator
- `has_report` — true if REPORT.md exists in the directory
- `has_innovation_log` — true if innovation_log.md exists
- `has_state_vector` — true if state_vector.md exists
- `has_dead_ends` — true if dead_ends.md exists
- `has_figures` — true if figures/ directory exists and contains at least one file
- `has_frozen` — true if frozen/ directory exists and is non-empty
- `has_tests` — true if tests/ directory exists and is non-empty
- `figures` — list of filenames in the figures/ directory (just filenames, not paths)
- `source_files` — list of .py or .html files in the experiment root (not in subdirs)
- `false_positives_caught` — copy from old EXPERIMENT_INDEX.json where it exists,
  otherwise null for newly discovered entries
- `key_result` — copy from old EXPERIMENT_INDEX.json where it exists, otherwise null
- `turns` — copy from old index where it exists (loop experiments), otherwise null
- `gate_scores` — copy from old index where it exists, otherwise null
- `statistical_result` — copy from old index where it exists, otherwise null
- `domain` — human-readable discipline name (e.g. "Social Science", "Chemistry")
- `sprint` — copy from old index where it exists (e.g. "chemistry-sprint-2026"), else null
- `notes` — copy from old index where it exists, otherwise null

### Top-level summary block:

```json
{
  "generated": "<ISO timestamp>",
  "version": "2.0",
  "project_root": "D:/EXPERIMENTS/context-hacking",
  "experiments": { ... },
  "summary": {
    "total": N,
    "complete": N,
    "staged": N,
    "superseded": N,
    "by_standard": { "cat": N, "disc": N, "loop": N },
    "by_discipline": {
      "chemistry": N,
      "mathematics": N,
      ...
    },
    "total_false_positives": N,
    "disciplines": [...]
  }
}
```

---

## STEP 5 — Verify

After writing the index, do a quick sanity check:
- Every entry's `dir` path should exist on disk
- Every entry with `has_report: true` should have a REPORT.md at that path
- Every entry with `has_figures: true` should have at least one file in figures/
- Print a summary: N experiments indexed, N complete, N staged, N superseded

---

## What NOT to do

- Do NOT modify any .py, .html, test_, or frozen/ file contents
- Do NOT delete REPORT.md, figures, frozen/, or tests/
- Do NOT rename staged or superseded experiments
- Do NOT copy from the old root-level EXPERIMENT_INDEX.json for `dir` paths —
  those are wrong. Derive all paths from the actual filesystem.
- Do NOT create new experiments or run any experiments
