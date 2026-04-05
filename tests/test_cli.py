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


class TestValidate:
    def test_validate_good_config(self, runner, tmp_path):
        """chp validate with valid config exits 0."""
        import yaml
        os.chdir(tmp_path)
        (tmp_path / "config.yaml").write_text(yaml.dump({
            "project": {"name": "test"},
            "loop": {"max_turns": 10},
        }))
        result = runner.invoke(main, ["validate"])
        assert result.exit_code == 0
        assert "Config OK" in result.output

    def test_validate_missing_config(self, runner, tmp_path):
        """chp validate without config.yaml fails."""
        os.chdir(tmp_path)
        result = runner.invoke(main, ["validate"])
        assert result.exit_code != 0 or "Error" in (result.output + (result.stderr or ""))

    def test_validate_shows_project_name(self, runner, tmp_path):
        """chp validate displays project name."""
        import yaml
        os.chdir(tmp_path)
        (tmp_path / "config.yaml").write_text(yaml.dump({
            "project": {"name": "my-cool-project"},
        }))
        result = runner.invoke(main, ["validate"])
        assert "my-cool-project" in result.output


class TestResumeErrors:
    def test_resume_without_state_vector(self, runner, tmp_path):
        """--resume without state_vector.md produces error."""
        os.chdir(tmp_path)
        result = runner.invoke(main, ["run", "--resume"])
        # Should fail — no state_vector.md
        assert result.exit_code != 0 or "state_vector" in result.output.lower() or "Error" in result.output


class TestResume:
    def test_resume_flag_in_help(self):
        """run command shows --resume flag in help."""
        from click.testing import CliRunner
        from context_hacking.cli import main
        runner = CliRunner()
        result = runner.invoke(main, ["run", "--help"])
        assert "--resume" in result.output
