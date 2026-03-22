"""
CHP Study — Rebuild EXPERIMENT_INDEX.json from filesystem.

Walks experiments/**/metadata.json, derives what it can from the filesystem,
and produces a complete index. Idempotent — always rebuilds from scratch.

Usage: python experiments/rebuild_index.py
"""
import json
import os
import sys
from pathlib import Path
from datetime import datetime, timezone

EXPERIMENTS_ROOT = Path(__file__).parent
PROJECT_ROOT = EXPERIMENTS_ROOT.parent
INDEX_PATH = PROJECT_ROOT / "EXPERIMENT_INDEX.json"

# Directories that aren't disciplines
SKIP_DIRS = {"figures", "__pycache__", ".pytest_cache"}


def derive_from_filesystem(exp_dir):
    """Derive what we can from the directory structure."""
    info = {}

    # Source files (*.py in experiment root, excluding __pycache__)
    source_files = [f.name for f in exp_dir.glob("*.py")
                    if f.name != "__init__.py"
                    and not f.name.startswith("test_")
                    and f.name != "generate_figures.py"]
    info["source_files"] = sorted(source_files)

    # Booleans from directory presence
    info["has_report"] = (exp_dir / "REPORT.md").exists()
    info["has_frozen_spec"] = any((exp_dir / "frozen").glob("*_constants.py")) if (exp_dir / "frozen").exists() else False
    info["has_figures"] = any((exp_dir / "figures").glob("*.png")) if (exp_dir / "figures").exists() else False
    info["has_tests"] = any((exp_dir / "tests").glob("test_*.py")) if (exp_dir / "tests").exists() else False

    return info


def standard_from_prefix(name):
    """Extract evidence standard from directory name prefix."""
    if name.startswith("cat-"):
        return "cat"
    elif name.startswith("disc-"):
        return "disc"
    elif name.startswith("loop-"):
        return "loop"
    return "unknown"


def load_metadata(exp_dir):
    """Load metadata.json if it exists, return empty dict otherwise."""
    meta_path = exp_dir / "metadata.json"
    if meta_path.exists():
        with open(meta_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def build_experiment_entry(discipline, exp_dir):
    """Build a complete experiment entry from metadata + filesystem."""
    exp_name = exp_dir.name
    meta = load_metadata(exp_dir)
    derived = derive_from_filesystem(exp_dir)

    # Standard from prefix (metadata can override)
    standard = meta.get("standard", standard_from_prefix(exp_name))

    entry = {
        "display_name": meta.get("display_name", exp_name),
        "standard": standard,
        "location": "direct-prompt",
        "dir": str(exp_dir.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "status": meta.get("status", "complete"),
        "domain": meta.get("domain", discipline.replace("-", " ").title()),
        "sprint": meta.get("sprint", None),
        "source_files": derived["source_files"],
        "has_report": derived["has_report"],
        "has_tests": derived["has_tests"],
        "has_figures": derived["has_figures"],
        "has_frozen_spec": derived["has_frozen_spec"],
        "key_result": meta.get("key_result", None),
        "false_positives_caught": meta.get("false_positives_caught", None),
        "turns": meta.get("turns", None),
        "gate_scores": meta.get("gate_scores", None),
        "statistical_result": meta.get("statistical_result", None),
        "meta_spec_errors": meta.get("meta_spec_errors", 0),
        "notes": meta.get("notes", None),
    }

    return entry


def rebuild():
    """Walk the filesystem and rebuild the full index."""
    experiments = {}
    domain_set = set()
    counts = {"total": 0, "complete": 0, "cat": 0, "disc": 0, "loop": 0}

    for discipline_dir in sorted(EXPERIMENTS_ROOT.iterdir()):
        if not discipline_dir.is_dir():
            continue
        if discipline_dir.name in SKIP_DIRS:
            continue

        discipline = discipline_dir.name

        for exp_dir in sorted(discipline_dir.iterdir()):
            if not exp_dir.is_dir():
                continue
            if exp_dir.name in SKIP_DIRS:
                continue
            # Must have at least a frozen dir or a .py file to count
            has_content = (
                (exp_dir / "frozen").exists()
                or any(exp_dir.glob("*.py"))
                or (exp_dir / "metadata.json").exists()
            )
            if not has_content:
                continue

            entry = build_experiment_entry(discipline, exp_dir)
            experiments[exp_dir.name] = entry

            domain_set.add(entry["domain"])
            counts["total"] += 1
            if entry["status"] == "complete":
                counts["complete"] += 1
            std = entry.get("standard", "unknown")
            if std in counts:
                counts[std] += 1

    index = {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "version": "2.0",
        "schema": {
            "metadata_source": "experiments/**/metadata.json",
            "derived_fields": ["source_files", "has_report", "has_tests", "has_figures", "has_frozen_spec", "dir"],
            "authoritative": "metadata.json for scientific fields, filesystem for structural fields",
        },
        "experiments": experiments,
        "summary": {
            "total": counts["total"],
            "complete": counts["complete"],
            "by_standard": {
                "catalog": counts["cat"],
                "discovery": counts["disc"],
                "loop": counts["loop"],
            },
            "domains": sorted(domain_set),
        },
    }

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    print(f"Index rebuilt: {counts['total']} experiments "
          f"({counts['cat']} cat, {counts['disc']} disc, {counts['loop']} loop)")
    print(f"  Complete: {counts['complete']}")
    print(f"  Domains: {len(domain_set)}")
    print(f"  Written to: {INDEX_PATH}")


if __name__ == "__main__":
    rebuild()
