"""Builder agent — The Implementer."""

from __future__ import annotations

import logging
from pathlib import Path

_log = logging.getLogger(__name__)

BUILDER_PROMPT_PATH = Path("prompts/builder.md")


def load_builder_prompt() -> str:
    """Load the builder prompt template."""
    if BUILDER_PROMPT_PATH.exists():
        return BUILDER_PROMPT_PATH.read_text(encoding="utf-8")
    _log.warning("Builder prompt not found at %s", BUILDER_PROMPT_PATH)
    return ""


def health_check_prompt() -> str:
    """3-line health check for the Builder."""
    return "Confirm active. State the first architecture rule from CHAIN_PROMPT.md."


def validate_health_check(response: str, chain_prompt_path: str = "CHAIN_PROMPT.md") -> bool:
    """Validate that the Builder's health check response cites CHAIN_PROMPT.md."""
    chain = Path(chain_prompt_path)
    if not chain.exists():
        _log.warning("CHAIN_PROMPT.md not found — cannot validate health check")
        return True  # pass if no chain prompt exists yet

    response_lower = response.lower()

    # Check if the response contains any architecture rule keyword
    keywords = ["pure library", "no print", "seeded", "randomness", "circular import"]
    return any(kw in response_lower for kw in keywords)
