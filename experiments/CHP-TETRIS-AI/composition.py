"""Composition layer — bridges frozen features to mutable weights."""
import json
import re
from typing import Callable

import numpy as np

from features import FEATURE_NAMES, FEATURE_FNS


# ---------------------------------------------------------------------------
# parse_weights_from_response
# ---------------------------------------------------------------------------

def parse_weights_from_response(text: str) -> dict | None:
    """Extract and validate a weight dict from the Builder's API response.

    Scans *text* for JSON objects, picks the one with the most matching
    FEATURE_NAMES keys, validates it, and returns the weight dict.
    Returns None if no valid weight dict is found.
    """
    # Find all {...} spans in the text (greedy outermost match).
    # We use a simple brace-depth scanner so we capture nested braces correctly.
    candidates = _extract_json_objects(text)

    best: dict | None = None
    best_match_count = -1

    for raw in candidates:
        try:
            obj = json.loads(raw)
        except (json.JSONDecodeError, ValueError):
            continue
        if not isinstance(obj, dict):
            continue

        matching = sum(1 for k in obj if k in FEATURE_NAMES)
        if matching > best_match_count:
            best_match_count = matching
            best = obj

    if best is None:
        return None

    if validate_weights(best):
        return best
    return None


def _extract_json_objects(text: str) -> list[str]:
    """Return a list of candidate JSON-object strings found in *text*."""
    results = []
    i = 0
    while i < len(text):
        if text[i] == "{":
            depth = 0
            in_string = False
            escape_next = False
            start = i
            j = i
            while j < len(text):
                ch = text[j]
                if escape_next:
                    escape_next = False
                elif ch == "\\" and in_string:
                    escape_next = True
                elif ch == '"':
                    in_string = not in_string
                elif not in_string:
                    if ch == "{":
                        depth += 1
                    elif ch == "}":
                        depth -= 1
                        if depth == 0:
                            results.append(text[start : j + 1])
                            break
                j += 1
        i += 1
    return results


# ---------------------------------------------------------------------------
# validate_weights
# ---------------------------------------------------------------------------

def validate_weights(weights: dict) -> bool:
    """Return True iff *weights* has exactly the 8 feature keys, all numeric."""
    if not isinstance(weights, dict):
        return False
    if set(weights.keys()) != set(FEATURE_NAMES):
        return False
    for v in weights.values():
        if not isinstance(v, (int, float)):
            return False
    return True


# ---------------------------------------------------------------------------
# build_evaluate_fn
# ---------------------------------------------------------------------------

def build_evaluate_fn(weights: dict) -> Callable[[np.ndarray], float]:
    """Return a board-evaluation function using *weights*.

    The returned function computes the weighted sum of all features.
    Features with weight 0.0 are skipped for efficiency.
    """
    # Pre-compute the list of (feature_fn, weight) pairs, dropping zeros.
    active = [
        (FEATURE_FNS[name], float(w))
        for name, w in weights.items()
        if w != 0.0
    ]

    def evaluate(board: np.ndarray) -> float:
        return sum(fn(board) * w for fn, w in active)

    return evaluate


# ---------------------------------------------------------------------------
# generate_code_display
# ---------------------------------------------------------------------------

def generate_code_display(weights: dict) -> str:
    """Generate a readable, syntactically valid Python function string.

    Zero-weight features are excluded.  The function can be compiled with
    ``compile(code, '<string>', 'exec')``.
    """
    non_zero = [(name, float(w)) for name, w in weights.items() if w != 0.0]

    lines = ['def evaluate(board):']
    lines.append('    """Weighted evaluation."""')

    if not non_zero:
        lines.append('    return 0.0')
        return "\n".join(lines) + "\n"

    # Build the return expression — first term uses `(`, subsequent use `+`.
    term_lines = []
    for name, w in non_zero:
        term_lines.append(f"        {w:+.3f} * {name}(board)")

    lines.append("    return (")
    # First line: no leading operator
    first_w, first_name = non_zero[0][1], non_zero[0][0]
    expr_lines = [f"        {first_w:+.3f} * {first_name}(board)"]
    for name, w in non_zero[1:]:
        expr_lines.append(f"      + {w:+.3f} * {name}(board)")

    lines.extend(expr_lines)
    lines.append("    )")
    return "\n".join(lines) + "\n"
