"""Tests for optimizer utility functions (synchronous only — no API calls)."""

import tempfile
import os

import pytest

from optimizer import (
    load_env,
    check_cv_gate,
    is_improvement,
    build_builder_prompt,
    build_critic_prompt,
    build_reviewer_prompt,
    build_health_check_prompt,
)


ALL_WEIGHTS = {
    "aggregate_height": -0.5,
    "complete_lines": 1.0,
    "holes": -3.5,
    "bumpiness": -0.2,
    "well_depth": 0.1,
    "tetris_readiness": 0.5,
    "column_transitions": -0.3,
    "row_transitions": -0.2,
}

FEATURE_DESCS = {
    "aggregate_height": "Sum of all column heights",
    "complete_lines": "Number of fully filled rows",
    "holes": "Empty cells below filled cells",
    "bumpiness": "Height differences between adjacent columns",
    "well_depth": "Depth of wells",
    "tetris_readiness": "1.0 if any well >= 4 deep",
    "column_transitions": "Transitions within columns",
    "row_transitions": "Transitions within rows",
}


class TestLoadEnv:
    def test_load_env_parses_keys(self, tmp_path):
        env_file = tmp_path / "test.env"
        env_file.write_text(
            'API_KEY="sk-test-12345"\n'
            'OTHER_KEY="hello world"\n'
            '# comment line\n'
            'EMPTY_VAL=""\n'
        )
        result = load_env(str(env_file))
        assert result["API_KEY"] == "sk-test-12345"
        assert result["OTHER_KEY"] == "hello world"
        assert result["EMPTY_VAL"] == ""
        assert "# comment line" not in result

    def test_load_env_strips_quotes(self, tmp_path):
        env_file = tmp_path / "test.env"
        env_file.write_text('MY_KEY="quoted_value"\n')
        result = load_env(str(env_file))
        assert result["MY_KEY"] == "quoted_value"

    def test_load_env_missing_file(self, tmp_path):
        result = load_env(str(tmp_path / "nonexistent.env"))
        assert result == {}


class TestCvGate:
    def test_cv_gate_pass(self):
        scores = [100, 105, 98, 102, 101, 99, 103, 97, 104, 100]
        passed, cv = check_cv_gate(scores, 0.15)
        assert passed is True
        assert cv < 0.15

    def test_cv_gate_fail(self):
        scores = [100, 500, 50, 800, 20, 600, 10, 900, 30, 700]
        passed, cv = check_cv_gate(scores, 0.15)
        assert passed is False

    def test_cv_gate_zero_mean(self):
        scores = [0, 0, 0]
        passed, cv = check_cv_gate(scores, 0.15)
        assert passed is False
        assert cv == float("inf")

    def test_cv_gate_single_value(self):
        scores = [100.0]
        passed, cv = check_cv_gate(scores, 0.15)
        assert passed is True
        assert cv == 0.0


class TestIsImprovement:
    def test_is_improvement_true(self):
        assert is_improvement(2400, 1800) is True

    def test_is_improvement_false(self):
        assert is_improvement(1800, 2400) is False

    def test_is_improvement_equal(self):
        assert is_improvement(1800, 1800) is False


class TestBuildBuilderPrompt:
    def test_contains_context(self):
        prompt = build_builder_prompt(
            weights=ALL_WEIGHTS,
            best_score=500,
            dead_ends=["pure line-clear maximization"],
            innovation_log_tail="Turn 1: baseline",
            feature_descriptions=FEATURE_DESCS,
            mode="VALIDATION",
        )
        assert "holes" in prompt
        assert "500" in prompt
        assert "pure line-clear" in prompt
        assert "VALIDATION" in prompt

    def test_contains_all_feature_names(self):
        prompt = build_builder_prompt(
            weights=ALL_WEIGHTS,
            best_score=0,
            dead_ends=[],
            innovation_log_tail="",
            feature_descriptions=FEATURE_DESCS,
            mode="EXPLORATION",
        )
        for name in ALL_WEIGHTS:
            assert name in prompt

    def test_mode_specific_guidance(self):
        val_prompt = build_builder_prompt(
            weights=ALL_WEIGHTS,
            best_score=100,
            dead_ends=[],
            innovation_log_tail="",
            feature_descriptions=FEATURE_DESCS,
            mode="VALIDATION",
        )
        exp_prompt = build_builder_prompt(
            weights=ALL_WEIGHTS,
            best_score=100,
            dead_ends=[],
            innovation_log_tail="",
            feature_descriptions=FEATURE_DESCS,
            mode="EXPLORATION",
        )
        # Both should mention their mode
        assert "VALIDATION" in val_prompt
        assert "EXPLORATION" in exp_prompt


class TestBuildCriticPrompt:
    def test_includes_gates(self):
        prompt = build_critic_prompt(
            weights=ALL_WEIGHTS,
            old_weights=ALL_WEIGHTS,
            scores=[100, 110, 95],
            cv=0.07,
            prior_traps_detected=[],
            mode="VALIDATION",
        )
        assert "gate" in prompt.lower() or "Gate" in prompt

    def test_includes_trap_warning(self):
        prompt = build_critic_prompt(
            weights=ALL_WEIGHTS,
            old_weights=ALL_WEIGHTS,
            scores=[100],
            cv=0.05,
            prior_traps_detected=["Line-Clear Greed Trap"],
            mode="VALIDATION",
        )
        assert "Line-Clear Greed Trap" in prompt

    def test_mode_in_prompt(self):
        prompt = build_critic_prompt(
            weights=ALL_WEIGHTS,
            old_weights=ALL_WEIGHTS,
            scores=[100],
            cv=0.05,
            prior_traps_detected=[],
            mode="EXPLORATION",
        )
        assert "EXPLORATION" in prompt


class TestBuildReviewerPrompt:
    def test_mentions_hygiene(self):
        prompt = build_reviewer_prompt(weights=ALL_WEIGHTS)
        assert "hygiene" in prompt.lower() or "valid" in prompt.lower()

    def test_contains_weights(self):
        prompt = build_reviewer_prompt(weights=ALL_WEIGHTS)
        assert "aggregate_height" in prompt


class TestBuildHealthCheckPrompt:
    def test_builder_prompt(self):
        prompt = build_health_check_prompt("builder")
        assert "builder" in prompt.lower() or "confirm" in prompt.lower()

    def test_critic_prompt(self):
        prompt = build_health_check_prompt("critic")
        assert "critic" in prompt.lower() or "pessimist" in prompt.lower()

    def test_reviewer_prompt(self):
        prompt = build_health_check_prompt("reviewer")
        assert "reviewer" in prompt.lower() or "linter" in prompt.lower()
