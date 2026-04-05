from prior_errors import KNOWN_TRAPS

class TestKnownTraps:
    def test_traps_list_not_empty(self):
        assert len(KNOWN_TRAPS) >= 1

    def test_trap_has_required_fields(self):
        for trap in KNOWN_TRAPS:
            assert "name" in trap
            assert "detect" in trap
            assert callable(trap["detect"])
            assert "description" in trap
            assert "correction_hint" in trap

    def test_greedy_line_clear_trap_detected(self):
        """LLMs over-weight complete_lines, under-weight holes."""
        greedy_weights = {
            "aggregate_height": -1.0,
            "complete_lines": 5.0,
            "holes": -1.0,
            "bumpiness": -1.0,
            "well_depth": 0.0,
            "tetris_readiness": 0.0,
            "column_transitions": 0.0,
            "row_transitions": 0.0,
        }
        trap = next(t for t in KNOWN_TRAPS if "greed" in t["name"].lower())
        assert trap["detect"](greedy_weights) is True

    def test_good_weights_not_flagged(self):
        good_weights = {
            "aggregate_height": -3.0,
            "complete_lines": 1.5,
            "holes": -4.5,
            "bumpiness": -2.0,
            "well_depth": 0.5,
            "tetris_readiness": 2.0,
            "column_transitions": 0.0,
            "row_transitions": 0.0,
        }
        for trap in KNOWN_TRAPS:
            assert trap["detect"](good_weights) is False

    def test_borderline_not_flagged(self):
        """Weights where holes penalty equals line reward should not trigger."""
        borderline = {
            "aggregate_height": -2.0,
            "complete_lines": 2.0,
            "holes": -2.0,
            "bumpiness": -1.0,
            "well_depth": 0.0,
            "tetris_readiness": 0.0,
            "column_transitions": 0.0,
            "row_transitions": 0.0,
        }
        trap = next(t for t in KNOWN_TRAPS if "greed" in t["name"].lower())
        assert trap["detect"](borderline) is False
