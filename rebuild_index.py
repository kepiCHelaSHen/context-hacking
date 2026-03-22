"""
CHP Study — Rebuild EXPERIMENT_INDEX.json from filesystem.

Walks experiments/**/metadata.json, derives what it can from the filesystem,
and produces a complete index. Idempotent — always rebuilds from scratch.

Usage (from project root): python rebuild_index.py
"""
import json
from pathlib import Path
from datetime import datetime, timezone

PROJECT_ROOT     = Path(__file__).parent
EXPERIMENTS_ROOT = PROJECT_ROOT / "experiments"
INDEX_PATH       = PROJECT_ROOT / "EXPERIMENT_INDEX.json"

SKIP_DIRS = {"figures", "__pycache__", ".pytest_cache", "statistics"}


def derive_from_filesystem(exp_dir):
    source_files = sorted(
        f.name for f in exp_dir.glob("*.py")
        if f.name not in ("__init__.py", "generate_figures.py")
        and not f.name.startswith("test_")
    )
    source_files += sorted(f.name for f in exp_dir.glob("*.html"))

    has_frozen  = (exp_dir / "frozen").is_dir() and any((exp_dir / "frozen").iterdir())
    has_figures = (exp_dir / "figures").is_dir() and any((exp_dir / "figures").iterdir())
    has_tests   = (exp_dir / "tests").is_dir()   and any((exp_dir / "tests").glob("test_*.py"))

    return {
        "source_files":   source_files,
        "has_report":     (exp_dir / "REPORT.md").exists(),
        "has_frozen":     has_frozen,
        "has_figures":    has_figures,
        "has_tests":      has_tests,
        "has_innovation_log": (exp_dir / "innovation_log.md").exists(),
        "has_state_vector":   (exp_dir / "state_vector.md").exists(),
        "has_dead_ends":      (exp_dir / "dead_ends.md").exists(),
        "figures": sorted(
            f.name for f in (exp_dir / "figures").iterdir()
            if (exp_dir / "figures").is_dir() and f.is_file()
            and f.suffix.lower() in (".png", ".svg", ".jpg", ".jpeg", ".pdf")
        ) if (exp_dir / "figures").is_dir() else [],
    }


def standard_from_prefix(name):
    for p in ("cat-", "disc-", "loop-"):
        if name.startswith(p):
            return p.rstrip("-")
    return None


def load_metadata(exp_dir):
    meta_path = exp_dir / "metadata.json"
    if meta_path.exists():
        with open(meta_path, encoding="utf-8") as f:
            return json.load(f)
    return {}


def build_entry(discipline, exp_dir):
    meta    = load_metadata(exp_dir)
    derived = derive_from_filesystem(exp_dir)
    slug    = exp_dir.name
    std     = meta.get("standard") or standard_from_prefix(slug)

    status = meta.get("status")
    if not status:
        status = "complete" if derived["has_report"] else "staged"

    return {
        "slug":                   slug,
        "display_name":           meta.get("display_name", slug),
        "standard":               std,
        "discipline":             discipline,
        "domain":                 meta.get("domain", discipline.replace("-", " ").title()),
        "dir":                    f"experiments/{discipline}/{slug}",
        "status":                 status,
        "sprint":                 meta.get("sprint"),
        "source_files":           derived["source_files"],
        "has_report":             derived["has_report"],
        "has_tests":              derived["has_tests"],
        "has_figures":            derived["has_figures"],
        "has_frozen":             derived["has_frozen"],
        "has_innovation_log":     derived["has_innovation_log"],
        "has_state_vector":       derived["has_state_vector"],
        "has_dead_ends":          derived["has_dead_ends"],
        "figures":                derived["figures"],
        "key_result":             meta.get("key_result"),
        "false_positives_caught": meta.get("false_positives_caught"),
        "turns":                  meta.get("turns"),
        "gate_scores":            meta.get("gate_scores"),
        "statistical_result":     meta.get("statistical_result"),
        "meta_spec_errors":       meta.get("meta_spec_errors", 0),
        "notes":                  meta.get("notes"),
    }


def rebuild():
    if not EXPERIMENTS_ROOT.is_dir():
        print(f"ERROR: experiments/ directory not found at {EXPERIMENTS_ROOT}")
        return

    experiments = {}
    counts = {"total": 0, "complete": 0, "staged": 0,
              "cat": 0, "disc": 0, "loop": 0}
    by_discipline = {}
    all_domains   = set()

    for disc_dir in sorted(EXPERIMENTS_ROOT.iterdir()):
        if not disc_dir.is_dir() or disc_dir.name in SKIP_DIRS:
            continue

        discipline = disc_dir.name
        disc_count = 0

        for exp_dir in sorted(disc_dir.iterdir()):
            if not exp_dir.is_dir() or exp_dir.name in SKIP_DIRS:
                continue

            # Must have metadata.json OR frozen/ OR a source file to count
            has_content = (
                (exp_dir / "metadata.json").exists()
                or (exp_dir / "frozen").is_dir()
                or any(exp_dir.glob("*.py"))
                or any(exp_dir.glob("*.html"))
            )
            if not has_content:
                print(f"  SKIP (empty)  {discipline}/{exp_dir.name}")
                continue

            entry = build_entry(discipline, exp_dir)
            experiments[entry["slug"]] = entry

            counts["total"] += 1
            disc_count += 1
            if entry["status"] == "complete": counts["complete"] += 1
            if entry["status"] == "staged":   counts["staged"]   += 1
            std = entry.get("standard")
            if std in counts: counts[std] += 1
            all_domains.add(entry["domain"])
            print(f"  OK  {discipline}/{entry['slug']}  [{entry['status']}]")

        if disc_count:
            by_discipline[discipline] = disc_count

    total_fp = sum(
        e["false_positives_caught"] for e in experiments.values()
        if isinstance(e.get("false_positives_caught"), int)
    )

    index = {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "version":   "2.0",
        "experiments": experiments,
        "summary": {
            "total":       counts["total"],
            "complete":    counts["complete"],
            "staged":      counts["staged"],
            "by_standard": {
                "cat":  counts["cat"],
                "disc": counts["disc"],
                "loop": counts["loop"],
            },
            "by_discipline":         by_discipline,
            "total_false_positives": total_fp,
            "domains":               sorted(all_domains),
        },
    }

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    print(f"\nDone. {counts['total']} experiments indexed.")
    print(f"  complete={counts['complete']}  staged={counts['staged']}")
    print(f"  cat={counts['cat']}  disc={counts['disc']}  loop={counts['loop']}")
    print(f"  total FPs caught: {total_fp}")
    print(f"  written to: {INDEX_PATH}")


if __name__ == "__main__":
    rebuild()
