"""Critic agent — The Pessimist."""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_log = logging.getLogger(__name__)

CRITIC_PROMPT_PATH = Path("prompts/critic.md")


@dataclass
class CriticVerdict:
    """Structured output from a Critic review."""

    gate_1_frozen: float = 0.0
    gate_2_architecture: float = 0.0
    gate_3_scientific: float = 0.0
    gate_4_drift: float = 0.0
    blocking_issues: list[str] | None = None
    nonblocking_issues: list[str] | None = None
    verdict: str = "NEEDS_IMPROVEMENT"
    next_priority: str = ""

    @property
    def passed(self) -> bool:
        return self.verdict == "PASS"

    @property
    def all_gates_met(self) -> bool:
        return (
            self.gate_1_frozen >= 1.0
            and self.gate_2_architecture >= 0.85
            and self.gate_3_scientific >= 0.85
            and self.gate_4_drift >= 0.85
        )

    @property
    def has_blocking(self) -> bool:
        return bool(self.blocking_issues)


def load_critic_prompt(config: dict[str, Any] | None = None) -> str:
    """Load the critic prompt template, injecting config overrides."""
    if CRITIC_PROMPT_PATH.exists():
        prompt = CRITIC_PROMPT_PATH.read_text(encoding="utf-8")
    else:
        _log.warning("Critic prompt not found at %s", CRITIC_PROMPT_PATH)
        prompt = ""

    # Inject custom mindset/instruction from config
    if config:
        mindset = config.get("mindset", "")
        instruction = config.get("instruction", "")
        if mindset:
            prompt += f"\n\nMINDSET OVERRIDE: {mindset}"
        if instruction:
            prompt += f"\n\nINSTRUCTION OVERRIDE: {instruction}"

    return prompt


def health_check_prompt() -> str:
    """3-line health check for the Critic."""
    return (
        "Confirm active. You are The Pessimist. "
        "What is Gate 1 and its threshold? "
        "What is your specific mission regarding the frozen specification?"
    )


def validate_health_check(response: str) -> bool:
    """Validate that the Critic knows its role."""
    r = response.lower()
    has_gate1 = "frozen" in r and ("1.0" in r or "100%" in r or "must" in r)
    has_mission = "violat" in r or "frozen" in r or "specification" in r
    return has_gate1 and has_mission


def parse_verdict(raw_text: str) -> CriticVerdict:
    """Parse a raw Critic response into a structured CriticVerdict."""
    verdict = CriticVerdict()

    # Extract gate scores
    g1 = re.search(r"gate_1[^:]*:\s*([0-9.]+)", raw_text, re.IGNORECASE)
    g2 = re.search(r"gate_2[^:]*:\s*([0-9.]+)", raw_text, re.IGNORECASE)
    g3 = re.search(r"gate_3[^:]*:\s*([0-9.]+)", raw_text, re.IGNORECASE)
    g4 = re.search(r"gate_4[^:]*:\s*([0-9.]+)", raw_text, re.IGNORECASE)

    if g1:
        verdict.gate_1_frozen = float(g1.group(1))
    if g2:
        verdict.gate_2_architecture = float(g2.group(1))
    if g3:
        verdict.gate_3_scientific = float(g3.group(1))
    if g4:
        verdict.gate_4_drift = float(g4.group(1))

    # Extract verdict
    if re.search(r"verdict:\s*PASS", raw_text, re.IGNORECASE):
        verdict.verdict = "PASS"
    else:
        verdict.verdict = "NEEDS_IMPROVEMENT"

    # Extract blocking issues
    blocking_match = re.search(
        r"blocking_issues:?\s*\n(.*?)(?=\nnonblocking|$)",
        raw_text,
        re.DOTALL | re.IGNORECASE,
    )
    if blocking_match:
        text = blocking_match.group(1).strip()
        if text.upper() != "NONE" and text != "-":
            verdict.blocking_issues = [
                line.strip().lstrip("- ")
                for line in text.splitlines()
                if line.strip() and line.strip() != "-"
            ]

    # Extract next priority
    next_match = re.search(
        r"next_turn_priority:?\s*(.+)", raw_text, re.IGNORECASE
    )
    if next_match:
        verdict.next_priority = next_match.group(1).strip()

    return verdict
