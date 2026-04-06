# Contributing to Context Hacking Protocol

Thanks for your interest in CHP! This guide covers setup, testing, and contribution guidelines.

## Setup

```bash
# Clone
git clone https://github.com/kepiCHelaSHen/context-hacking.git
cd context-hacking

# Install with dev dependencies
pip install -e ".[dev]"

# Verify installation
chp --version
python -m pytest tests/ -v
```

**Requirements:** Python 3.11+

## Running Tests

```bash
# Full suite
python -m pytest tests/ -v

# Specific test file
python -m pytest tests/test_framework.py -v

# Specific test class
python -m pytest tests/test_integration.py::TestMultiTurnLoop -v
```

## Code Quality

```bash
# Lint
ruff check .

# Type check
mypy --strict context_hacking/
```

## Project Structure

```
context_hacking/          # Core package
  core/                   # Orchestrator, gates, modes, memory, telemetry
  agents/                 # Builder, Critic, Reviewer, Council
  cli.py                  # CLI interface (chp command)
  runner.py               # Experiment execution (API + CLI modes)
tests/                    # Test suite
  test_framework.py       # Unit tests for core framework
  test_integration.py     # Multi-turn orchestrator tests
  test_parsing.py         # Parse robustness tests (critic, reviewer, council)
  test_council.py         # Council consensus detection tests
  test_runner.py          # Runner function tests
  test_cli.py             # CLI command tests
experiments/              # Showcase experiments (9 built-in)
prompts/                  # Agent prompt templates
docs/                     # Documentation and papers
```

## Adding a New Experiment

1. Create a directory under `experiments/your-experiment-name/`
2. Add: `CHAIN_PROMPT.md`, `spec.md`, `config.yaml`, `frozen/` directory
3. Add tests in `experiments/your-experiment-name/tests/`
4. Run: `chp run --experiment your-experiment-name`

No changes to the runner are needed — experiment names are not hardcoded.

## Submitting Changes

1. Fork the repo
2. Create a feature branch
3. Write tests for new functionality
4. Ensure `python -m pytest tests/ -v` passes
5. Ensure `ruff check .` passes
6. Submit a pull request with a clear description

## License

See `LICENSE.md` for terms. Free for personal and academic use; commercial use requires agreement.
