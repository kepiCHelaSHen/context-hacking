"""
rebuild_index.py  —  run from project root: python rebuild_index.py

Does four things every time it runs:
  1. Deletes empty stub directories (no source files, no tests, no REPORT.md)
  2. Renames unprefixed experiment dirs with the correct cat-/disc-/loop- prefix
  3. Standardises internal file names (innovation_log.md, state_vector.md, dead_ends.md)
  4. Writes experiments/EXPERIMENT_INDEX.json from the actual filesystem state,
     carrying scientific metadata from the old root-level EXPERIMENT_INDEX.json
     where slugs match.

Safe to run repeatedly — idempotent.
Never touches scientific content (.py, .html, frozen/, tests/, figures/, REPORT.md).
"""

import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# PATHS
# ---------------------------------------------------------------------------

ROOT         = Path(__file__).parent.resolve()
EXPERIMENTS  = ROOT / "experiments"
NEW_INDEX    = EXPERIMENTS / "EXPERIMENT_INDEX.json"
OLD_INDEX    = ROOT / "EXPERIMENT_INDEX.json"

# ---------------------------------------------------------------------------
# DISCIPLINES
# ---------------------------------------------------------------------------

DISCIPLINES = [
    "astronomy", "audio-dsp", "biology", "chemistry", "computer-science",
    "earth-science", "economics", "engineering", "mathematics", "medicine",
    "music", "physics", "social-science", "statistics",
]

DOMAIN_DISPLAY = {
    "astronomy":        "Astronomy",
    "audio-dsp":        "Audio DSP",
    "biology":          "Biology",
    "chemistry":        "Chemistry",
    "computer-science": "Computer Science",
    "earth-science":    "Earth Science",
    "economics":        "Economics",
    "engineering":      "Engineering",
    "mathematics":      "Mathematics",
    "medicine":         "Medicine",
    "music":            "Music",
    "physics":          "Physics",
    "social-science":   "Social Science",
    "statistics":       "Statistics",
}

# ---------------------------------------------------------------------------
# EXPLICIT PREFIX MAP  (only for experiments that already exist without one)
# New experiments from sprints should arrive already prefixed.
# ---------------------------------------------------------------------------

PREFIX_MAP = {
    # Chemistry
    "chem-equilibrium":       "cat",
    "chem-kinetics":          "cat",
    "chem-buffers":           "cat",
    "chem-radioactive-decay": "cat",
    "chem-vdw-gas":           "cat",
    "chem-electrochemistry":  "cat",
    "chem-spectrophotometry": "cat",
    "chem-thermochemistry":   "cat",
    "chem-stoichiometry":     "cat",
    "chem-crystal-packing":   "cat",
    # Mathematics
    "euler-e":           "cat",
    "pi-machin":         "cat",
    "sqrt2-newton":      "cat",
    "time_sprint":       "cat",
    "omega_sentinel_1M": "cat",
    # Biology
    "sir-epidemic":       "loop",
    "lotka-volterra":     "loop",
    "izhikevich-neurons": "loop",
    # Physics
    "lorenz-attractor": "loop",
    # Social Science
    "schelling-segregation":     "loop",
    "spatial-prisoners-dilemma": "loop",
    # Computer Science
    "quantum-grover":       "loop",
    "blockchain-consensus": "loop",
    "ml-hyperparam-search": "loop",
    # Music
    "metal-harmony": "loop",
    # Audio DSP
    "schroeder-reverb": "loop",
    # Medicine
    "anatomy-viewer":     "cat",
    "anatomy-viewer-vtk": "cat",
    # Physics sprint — phys-* stubs arrived without prefix; real ones are cat-phys-*
    # These will be caught by the empty-stub pruner below (no source files)
    # but list them here as cat just in case they have content
    "phys-projectile":          "cat",
    "phys-pendulum":            "cat",
    "phys-shm":                 "cat",
    "phys-coulomb":             "cat",
    "phys-circuits":            "cat",
    "phys-blackbody":           "cat",
    "phys-doppler":             "cat",
    "phys-snell":               "cat",
    "phys-relativity":          "cat",
    "phys-kinetic-theory":      "cat",
}

# Dirs to never rename or delete regardless of contents
PROTECTED = {
    "pi-calculator",          # superseded — keep as-is
    "simsiv-v1-replication",  # staged
    "simsiv-v2-replication",  # staged
}

STATUS_OVERRIDES = {
    "pi-calculator":         "superseded",
    "simsiv-v1-replication": "staged",
    "simsiv-v2-replication": "staged",
}

# Internal file normalisation: any file ending with suffix → standard name
FILE_NORMALISE = [
    ("_innovation_log.md", "innovation_log.md"),
    ("_state_vector.md",   "state_vector.md"),
    ("_dead_ends.md",      "dead_ends.md"),
]

# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def is_empty_stub(path: Path) -> bool:
    """True if a directory has no source files and no REPORT.md — just subdirs."""
    for f in path.iterdir():
        if f.is_file() and f.suffix in (".py", ".html", ".md") and f.name not in ("metadata.json",):
            return False
    return True


def infer_standard(slug: str):
    for p in ("cat-", "disc-", "loop-"):
        if slug.startswith(p):
            return p.rstrip("-")
    return None


def infer_status(exp_dir: Path, slug: str) -> str:
    if slug in STATUS_OVERRIDES:
        return STATUS_OVERRIDES[slug]
    if (exp_dir / "REPORT.md").exists():
        return "complete"
    # Has tests or frozen but no report → staged
    has_tests  = (exp_dir / "tests").is_dir() and any((exp_dir / "tests").iterdir())
    has_frozen = (exp_dir / "frozen").is_dir() and any((exp_dir / "frozen").iterdir())
    if has_tests or has_frozen:
        return "staged"
    return "unknown"


def get_figures(exp_dir: Path):
    d = exp_dir / "figures"
    if not d.is_dir():
        return []
    return sorted(f.name for f in d.iterdir()
                  if f.is_file() and f.suffix.lower() in (".png", ".svg", ".jpg", ".jpeg", ".pdf"))


def get_source_files(exp_dir: Path):
    return sorted(f.name for f in exp_dir.iterdir()
                  if f.is_file() and f.suffix.lower() in (".py", ".html"))


def load_old_index() -> dict:
    if OLD_INDEX.exists():
        with open(OLD_INDEX, encoding="utf-8") as f:
            return json.load(f).get("experiments", {})
    return {}


def find_old_entry(slug: str, old: dict):
    """Match new prefixed slug back to an old (unprefixed) index entry."""
    if slug in old:
        return old[slug]
    # Strip prefix
    for p in ("cat-", "disc-", "loop-"):
        if slug.startswith(p):
            bare = slug[len(p):]
            if bare in old:
                return old[bare]
            # underscore variant (e.g. time_sprint, omega_sentinel_1M)
            bare_u = bare.replace("-", "_")
            if bare_u in old:
                return old[bare_u]
    return None

# ---------------------------------------------------------------------------
# STEP 1 — PRUNE EMPTY STUBS
# ---------------------------------------------------------------------------

def prune_stubs():
    print("\n── STEP 1: Pruning empty stub directories ──")
    pruned = 0
    for disc in DISCIPLINES:
        disc_dir = EXPERIMENTS / disc
        if not disc_dir.is_dir():
            continue
        for entry in sorted(disc_dir.iterdir()):
            if not entry.is_dir():
                continue
            if entry.name in PROTECTED:
                continue
            # Only prune if it has no prefix AND is empty
            has_prefix = entry.name.startswith(("cat-", "disc-", "loop-"))
            if not has_prefix and is_empty_stub(entry):
                shutil.rmtree(entry)
                print(f"  PRUNED   {disc}/{entry.name}")
                pruned += 1
    if pruned == 0:
        print("  Nothing to prune.")
    else:
        print(f"  {pruned} stub(s) removed.")

# ---------------------------------------------------------------------------
# STEP 2 — RENAME UNPREFIXED DIRS
# ---------------------------------------------------------------------------

def rename_dirs():
    print("\n── STEP 2: Renaming unprefixed experiment directories ──")
    renamed = 0
    for disc in DISCIPLINES:
        disc_dir = EXPERIMENTS / disc
        if not disc_dir.is_dir():
            continue
        for entry in sorted(disc_dir.iterdir()):
            if not entry.is_dir():
                continue
            name = entry.name
            if name.startswith(("cat-", "disc-", "loop-")):
                continue  # already correct
            if name in PROTECTED:
                print(f"  PROTECTED  {disc}/{name}")
                continue
            prefix = PREFIX_MAP.get(name)
            if not prefix:
                print(f"  UNKNOWN    {disc}/{name}  — no prefix rule, skipping")
                continue
            new_name = f"{prefix}-{name}"
            # Normalise underscores to hyphens in the slug
            new_name = new_name.replace("_", "-")
            new_path = disc_dir / new_name
            if new_path.exists():
                print(f"  EXISTS     {disc}/{name} → {new_name} (target already exists, skipping)")
            else:
                entry.rename(new_path)
                print(f"  RENAMED    {disc}/{name} → {new_name}")
                renamed += 1
    if renamed == 0:
        print("  Nothing to rename.")

# ---------------------------------------------------------------------------
# STEP 3 — NORMALISE INTERNAL FILE NAMES
# ---------------------------------------------------------------------------

def normalise_files():
    print("\n── STEP 3: Normalising internal file names ──")
    changes = 0
    for disc in DISCIPLINES:
        disc_dir = EXPERIMENTS / disc
        if not disc_dir.is_dir():
            continue
        for exp in sorted(disc_dir.iterdir()):
            if not exp.is_dir():
                continue
            for suffix, standard in FILE_NORMALISE:
                standard_path = exp / standard
                candidates = [
                    f for f in exp.iterdir()
                    if f.is_file() and f.name.endswith(suffix) and f.name != standard
                ]
                for c in candidates:
                    if standard_path.exists():
                        c.unlink()
                        print(f"  DELETED  {disc}/{exp.name}/{c.name}  (standard exists)")
                    else:
                        c.rename(standard_path)
                        print(f"  RENAMED  {disc}/{exp.name}/{c.name} → {standard}")
                    changes += 1
    if changes == 0:
        print("  All files already normalised.")

# ---------------------------------------------------------------------------
# STEP 4 — BUILD INDEX
# ---------------------------------------------------------------------------

def build_index():
    print("\n── STEP 4: Building EXPERIMENT_INDEX.json ──")
    old = load_old_index()
    experiments = {}

    for disc in DISCIPLINES:
        disc_dir = EXPERIMENTS / disc
        if not disc_dir.is_dir():
            continue
        for exp in sorted(disc_dir.iterdir()):
            if not exp.is_dir():
                continue

            slug   = exp.name
            o      = find_old_entry(slug, old)
            status = infer_status(exp, slug)
            std    = infer_standard(slug)

            def carry(field, default=None):
                return o.get(field, default) if o else default

            entry = {
                "slug":                slug,
                "display_name":        carry("display_name", slug.replace("-", " ").title()),
                "standard":            std,
                "discipline":          disc,
                "domain":              DOMAIN_DISPLAY.get(disc, disc),
                "dir":                 f"experiments/{disc}/{slug}",
                "status":              status,
                # — filesystem-derived flags —
                "has_report":          (exp / "REPORT.md").exists(),
                "has_innovation_log":  (exp / "innovation_log.md").exists(),
                "has_state_vector":    (exp / "state_vector.md").exists(),
                "has_dead_ends":       (exp / "dead_ends.md").exists(),
                "has_figures":         bool(get_figures(exp)),
                "has_frozen":          (exp / "frozen").is_dir() and any((exp / "frozen").iterdir()),
                "has_tests":           (exp / "tests").is_dir() and any((exp / "tests").iterdir()),
                "figures":             get_figures(exp),
                "source_files":        get_source_files(exp),
                # — scientific metadata from old index —
                "false_positives_caught": carry("false_positives_caught"),
                "key_result":             carry("key_result"),
                "turns":                  carry("turns"),
                "gate_scores":            carry("gate_scores"),
                "statistical_result":     carry("statistical_result"),
                "meta_spec_errors":       carry("meta_spec_errors", 0),
                "sprint":                 carry("sprint"),
                "notes":                  carry("notes"),
            }

            experiments[slug] = entry
            print(f"  {disc}/{slug}  [{status}]")

    # Summary
    statuses   = [e["status"]   for e in experiments.values()]
    standards  = [e["standard"] for e in experiments.values() if e["standard"]]
    total_fp   = sum(
        e["false_positives_caught"] for e in experiments.values()
        if isinstance(e.get("false_positives_caught"), int)
    )
    by_disc = {
        d: sum(1 for e in experiments.values() if e["discipline"] == d)
        for d in DISCIPLINES
        if any(e["discipline"] == d for e in experiments.values())
    }

    index = {
        "generated":    datetime.now(timezone.utc).isoformat(),
        "version":      "2.0",
        "project_root": str(ROOT).replace("\\", "/"),
        "experiments":  experiments,
        "summary": {
            "total":       len(experiments),
            "complete":    statuses.count("complete"),
            "staged":      statuses.count("staged"),
            "superseded":  statuses.count("superseded"),
            "unknown":     statuses.count("unknown"),
            "by_standard": {
                "cat":  standards.count("cat"),
                "disc": standards.count("disc"),
                "loop": standards.count("loop"),
            },
            "by_discipline":        by_disc,
            "total_false_positives": total_fp,
            "disciplines": [DOMAIN_DISPLAY[d] for d in DISCIPLINES if d in by_disc],
        },
    }

    with open(NEW_INDEX, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    print(f"\n  Written → {NEW_INDEX}")
    return index

# ---------------------------------------------------------------------------
# STEP 5 — VERIFY
# ---------------------------------------------------------------------------

def verify(index):
    print("\n── STEP 5: Verification ──")
    errors = []
    for slug, e in index["experiments"].items():
        p = ROOT / e["dir"]
        if not p.exists():
            errors.append(f"  MISSING DIR    {e['dir']}")
        elif e["has_report"] and not (p / "REPORT.md").exists():
            errors.append(f"  MISSING REPORT {slug}")

    if errors:
        print(f"  {len(errors)} error(s):")
        for err in errors:
            print(err)
    else:
        print("  All paths verified OK.")

    s = index["summary"]
    print(f"""
  Total        : {s['total']}
  Complete     : {s['complete']}
  Staged       : {s['staged']}
  Superseded   : {s['superseded']}
  Unknown      : {s['unknown']}
  cat / disc / loop : {s['by_standard']['cat']} / {s['by_standard']['disc']} / {s['by_standard']['loop']}
  Total FPs    : {s['total_false_positives']}
""")

# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print(f"rebuild_index.py")
    print(f"Root : {ROOT}")

    prune_stubs()
    rename_dirs()
    normalise_files()
    index = build_index()
    verify(index)

    print("Done.")
