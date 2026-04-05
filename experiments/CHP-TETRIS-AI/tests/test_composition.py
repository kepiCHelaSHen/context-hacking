"""Tests for composition.py — TDD, written before implementation."""
import json
import numpy as np
import pytest
from composition import (
    parse_weights_from_response,
    validate_weights,
    build_evaluate_fn,
    generate_code_display,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

ALL_KEYS = [
    "aggregate_height",
    "complete_lines",
    "holes",
    "bumpiness",
    "well_depth",
    "tetris_readiness",
    "column_transitions",
    "row_transitions",
]

VALID_WEIGHTS = {
    "aggregate_height": -4.5,
    "complete_lines": 1.76,
    "holes": -4.5,
    "bumpiness": -2.31,
    "well_depth": 0.65,
    "tetris_readiness": 3.2,
    "column_transitions": -1.0,
    "row_transitions": -0.5,
}

EMPTY_BOARD = np.zeros((20, 10), dtype=np.int8)


def _board_with_piece():
    """A board with one piece placed in the bottom-left corner."""
    board = np.zeros((20, 10), dtype=np.int8)
    board[19, 0] = 1  # single filled cell
    return board


# ---------------------------------------------------------------------------
# TestParseWeights
# ---------------------------------------------------------------------------

class TestParseWeights:

    def test_extracts_json_from_surrounding_text(self):
        """JSON embedded in natural language should be extracted."""
        payload = json.dumps(VALID_WEIGHTS)
        text = f"Here are my weights: {payload} I changed holes because tunneling."
        result = parse_weights_from_response(text)
        assert result is not None
        assert result == VALID_WEIGHTS

    def test_returns_none_when_no_json(self):
        """Plain text with no JSON returns None."""
        result = parse_weights_from_response("No JSON here at all.")
        assert result is None

    def test_returns_none_for_unknown_keys(self):
        """JSON with keys not in FEATURE_NAMES returns None."""
        bad = {"foo": 1.0, "bar": 2.0}
        text = json.dumps(bad)
        result = parse_weights_from_response(text)
        assert result is None

    def test_returns_none_for_wrong_key_count(self):
        """JSON with fewer than 8 keys returns None."""
        partial = {k: VALID_WEIGHTS[k] for k in ALL_KEYS[:5]}
        text = json.dumps(partial)
        result = parse_weights_from_response(text)
        assert result is None

    def test_returns_none_for_non_numeric_values(self):
        """JSON with string values returns None."""
        bad = {k: "not_a_number" for k in ALL_KEYS}
        text = json.dumps(bad)
        result = parse_weights_from_response(text)
        assert result is None

    def test_handles_multiline_json(self):
        """Pretty-printed JSON spanning multiple lines should be parsed."""
        payload = json.dumps(VALID_WEIGHTS, indent=2)
        text = f"Reasoning...\n{payload}\nDone."
        result = parse_weights_from_response(text)
        assert result is not None
        assert set(result.keys()) == set(ALL_KEYS)

    def test_prefers_json_with_most_matching_keys(self):
        """When multiple JSON objects exist, prefer the most complete one."""
        partial = {k: 0.0 for k in ALL_KEYS[:3]}
        full = dict(VALID_WEIGHTS)
        text = f"old: {json.dumps(partial)} new: {json.dumps(full)}"
        result = parse_weights_from_response(text)
        assert result is not None
        assert set(result.keys()) == set(ALL_KEYS)

    def test_integer_values_are_accepted(self):
        """Integer weights (e.g. 0) should be considered float-like and valid."""
        int_weights = {k: 0 for k in ALL_KEYS}
        text = json.dumps(int_weights)
        result = parse_weights_from_response(text)
        assert result is not None


# ---------------------------------------------------------------------------
# TestValidateWeights
# ---------------------------------------------------------------------------

class TestValidateWeights:

    def test_valid_8_key_dict_returns_true(self):
        assert validate_weights(VALID_WEIGHTS) is True

    def test_missing_key_returns_false(self):
        bad = {k: v for k, v in VALID_WEIGHTS.items() if k != "holes"}
        assert validate_weights(bad) is False

    def test_extra_key_returns_false(self):
        bad = dict(VALID_WEIGHTS)
        bad["extra_feature"] = 9.9
        assert validate_weights(bad) is False

    def test_non_numeric_value_returns_false(self):
        bad = dict(VALID_WEIGHTS)
        bad["holes"] = "oops"
        assert validate_weights(bad) is False

    def test_integer_values_pass(self):
        int_weights = {k: 0 for k in ALL_KEYS}
        assert validate_weights(int_weights) is True

    def test_empty_dict_returns_false(self):
        assert validate_weights({}) is False

    def test_none_value_returns_false(self):
        bad = dict(VALID_WEIGHTS)
        bad["holes"] = None
        assert validate_weights(bad) is False


# ---------------------------------------------------------------------------
# TestBuildEvaluateFn
# ---------------------------------------------------------------------------

class TestBuildEvaluateFn:

    def test_returns_callable(self):
        fn = build_evaluate_fn(VALID_WEIGHTS)
        assert callable(fn)

    def test_empty_board_evaluates_to_zero(self):
        """All features return 0.0 on an empty board."""
        fn = build_evaluate_fn(VALID_WEIGHTS)
        result = fn(EMPTY_BOARD)
        assert result == pytest.approx(0.0)

    def test_non_trivial_board_produces_nonzero_result(self):
        """A board with a piece should produce a non-zero score."""
        board = _board_with_piece()
        fn = build_evaluate_fn(VALID_WEIGHTS)
        result = fn(board)
        assert result != 0.0

    def test_zero_weight_features_dont_affect_result(self):
        """Setting a weight to 0 should not change the result."""
        weights_with_zero = dict(VALID_WEIGHTS)
        weights_with_zero["complete_lines"] = 0.0
        weights_with_zero["tetris_readiness"] = 0.0

        fn_full = build_evaluate_fn(VALID_WEIGHTS)
        fn_zeroed = build_evaluate_fn(weights_with_zero)

        # On an empty board, complete_lines and tetris_readiness are both 0,
        # so zeroing them makes no difference.
        board = EMPTY_BOARD
        assert fn_full(board) == pytest.approx(fn_zeroed(board))

        # On a non-trivial board that still has 0 complete lines and 0
        # tetris_readiness, zeroing those weights should yield the same score.
        board2 = _board_with_piece()
        assert fn_full(board2) == pytest.approx(fn_zeroed(board2))

    def test_result_matches_manual_calculation(self):
        """Spot-check: result should equal manual weighted sum."""
        board = _board_with_piece()
        # aggregate_height=1, everything else is 0 for a single filled cell
        # except row_transitions (walls + 1 filled cell = 2 transitions)
        # and column_transitions (none, only 1 cell in col 0).
        from features import FEATURE_FNS
        manual = sum(
            VALID_WEIGHTS[name] * FEATURE_FNS[name](board)
            for name in ALL_KEYS
        )
        fn = build_evaluate_fn(VALID_WEIGHTS)
        assert fn(board) == pytest.approx(manual)


# ---------------------------------------------------------------------------
# TestGenerateCodeDisplay
# ---------------------------------------------------------------------------

class TestGenerateCodeDisplay:

    def test_contains_def_evaluate(self):
        code = generate_code_display(VALID_WEIGHTS)
        assert "def evaluate(board):" in code

    def test_is_syntactically_valid_python(self):
        code = generate_code_display(VALID_WEIGHTS)
        try:
            compile(code, "<string>", "exec")
        except SyntaxError as exc:
            pytest.fail(f"Generated code has a syntax error: {exc}")

    def test_zero_weight_features_excluded(self):
        weights = dict(VALID_WEIGHTS)
        weights["complete_lines"] = 0.0
        code = generate_code_display(weights)
        assert "complete_lines" not in code

    def test_nonzero_weights_present(self):
        code = generate_code_display(VALID_WEIGHTS)
        # Every key with a non-zero weight should appear in the output
        for key, val in VALID_WEIGHTS.items():
            if val != 0.0:
                assert key in code, f"Expected '{key}' in generated code"

    def test_all_zero_weights_produces_valid_code(self):
        """Edge case: if every weight is zero the function should still compile."""
        zero_weights = {k: 0.0 for k in ALL_KEYS}
        code = generate_code_display(zero_weights)
        try:
            compile(code, "<string>", "exec")
        except SyntaxError as exc:
            pytest.fail(f"All-zero generated code has a syntax error: {exc}")
