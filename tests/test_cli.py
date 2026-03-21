"""Tests for the CLI commands."""

import os
import shutil
from pathlib import Path

import pytest
from click.testing import CliRunner

from context_hacking.cli import main


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def tmp_project(tmp_path):
    """Create a temporary project directory."""
    os.chdir(tmp_path)
    yield tmp_path
    os.chdir(Path(__file__).parent.parent)


class TestInit:
    def test_init_creates_files(self, runner, tmp_path):
        result = runner.invoke(main, ["init", str(tmp_path / "test-proj")])
        assert result.exit_code == 0
        assert (tmp_path / "test-proj" / "config.yaml").exists()
        assert (tmp_path / "test-proj" / "CHAIN_PROMPT.md").exists()
        assert (tmp_path / "test-proj" / "dead_ends.md").exists()
        assert (tmp_path / "test-proj" / "state_vector.md").exists()
        assert (tmp_path / "test-proj" / "innovation_log.md").exists()

    def test_init_creates_prompts(self, runner, tmp_path):
        result = runner.invoke(main, ["init", str(tmp_path / "test-proj")])
        assert result.exit_code == 0
        prompts = tmp_path / "test-proj" / "prompts"
        assert prompts.exists()
        assert (prompts / "critic.md").exists()
        assert (prompts / "builder.md").exists()

    def test_init_existing(self, runner, tmp_path):
        os.chdir(tmp_path)
        result = runner.invoke(main, ["init", ".", "--existing"])
        assert result.exit_code == 0
        assert (tmp_path / "config.yaml").exists()

    def test_init_with_experiment(self, runner, tmp_path):
        result = runner.invoke(main, ["init", str(tmp_path / "proj"), "--experiment", "schelling"])
        assert result.exit_code == 0
        exp_dir = tmp_path / "proj" / "experiments" / "schelling-segregation"
        assert exp_dir.exists()


class TestVersion:
    def test_version(self, runner):
        result = runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "0.2.0" in result.output


class TestHelp:
    def test_help(self, runner):
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "init" in result.output
        assert "run" in result.output
        assert "status" in result.output
        assert "dashboard" in result.output
        assert "install-skills" in result.output

    def test_run_help(self, runner):
        result = runner.invoke(main, ["run", "--help"])
        assert result.exit_code == 0
        assert "--experiment" in result.output
        assert "--method" in result.output
        assert "--all-experiments" in result.output
