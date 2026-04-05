"""Reviewer agent — The Linter."""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path

_log = logging.getLogger(__name__)

REVIEWER_PROMPT_PATH = Path("prompts/reviewer.md")


@dataclass
class ReviewIssue:
    """A single code review issue."""

    severity: str  # CRITICAL, WARNING, MINOR
    file: str
    line: int | None
    description: str


@dataclass
class ReviewResult:
    """Structured output from a Reviewer pass."""

    issues: list[ReviewIssue] = field(default_factory=list)
    verdict: str = "APPROVE"  # APPROVE | APPROVE WITH NOTES | NEEDS REVISION

    @property
    def critical_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "CRITICAL")

    @property
    def warning_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "WARNING")

    @property
    def needs_revision(self) -> bool:
        return self.verdict in ("NEEDS REVISION", "PARSE_FAILED") or self.critical_count > 0


def load_reviewer_prompt() -> str:
    """Load the reviewer prompt template."""
    if REVIEWER_PROMPT_PATH.exists():
        return REVIEWER_PROMPT_PATH.read_text(encoding="utf-8")
    _log.warning("Reviewer prompt not found at %s", REVIEWER_PROMPT_PATH)
    return ""


def health_check_prompt() -> str:
    """3-line health check for the Reviewer."""
    return "Confirm active. You are The Linter. What do you NOT evaluate?"


def validate_health_check(response: str) -> bool:
    """Validate that the Reviewer knows its scope."""
    r = response.lower()
    return ("science" in r or "scientific" in r) and (
        "architecture" in r or "not" in r
    )


def parse_review(raw_text: str) -> ReviewResult:
    """Parse raw Reviewer output into a structured ReviewResult."""
    if not raw_text or not raw_text.strip():
        return ReviewResult(
            issues=[ReviewIssue(severity="CRITICAL", file="", line=0,
                               description="PARSE_FAILED: empty reviewer response")],
            verdict="PARSE_FAILED",
        )

    result = ReviewResult()

    # Extract issues: lines matching [CRITICAL|WARNING|MINOR] pattern
    # Handles: CRITICAL: file.py:42 — desc
    #          **CRITICAL**: `sim.py:42` — desc
    #          WARNING: model.py line 10 - desc
    #          MINOR - desc (bare severity, no file)
    issue_pattern = re.compile(
        r"\*?\*?(CRITICAL|WARNING|MINOR)\*?\*?:?\s*"
        r"(?:`?([^`\n:—-]+(?::\d+)?)`?)?\s*[-—]?\s*(.+)",
        re.IGNORECASE,
    )

    for match in issue_pattern.finditer(raw_text):
        severity = match.group(1).upper()
        location = match.group(2) or ""
        description = match.group(3).strip()

        # Parse file:line from location
        file_path = ""
        line_num = None
        if ":" in location:
            parts = location.rsplit(":", 1)
            file_path = parts[0].strip()
            try:
                line_num = int(parts[1])
            except ValueError:
                file_path = location.strip()
        elif re.search(r"\bline\s+(\d+)", location, re.IGNORECASE):
            # Handle "file.py line 10" notation
            m = re.search(r"(.+?)\s+line\s+(\d+)", location, re.IGNORECASE)
            if m:
                file_path = m.group(1).strip()
                line_num = int(m.group(2))
        else:
            file_path = location.strip()

        # Check if description starts with "file line N" (location was empty)
        if not file_path and not line_num:
            line_match = re.match(
                r"(\S+\.(?:py|js|ts|md|yaml|toml|cfg|txt|rs|go|java|c|cpp|h))"
                r"\s+line\s+(\d+)\s*[-—]\s*(.+)",
                description, re.IGNORECASE,
            )
            if line_match:
                file_path = line_match.group(1)
                line_num = int(line_match.group(2))
                description = line_match.group(3).strip()

        result.issues.append(
            ReviewIssue(
                severity=severity,
                file=file_path,
                line=line_num,
                description=description,
            )
        )

    # Extract verdict
    if re.search(r"NEEDS REVISION", raw_text, re.IGNORECASE):
        result.verdict = "NEEDS REVISION"
    elif re.search(r"APPROVE WITH NOTES", raw_text, re.IGNORECASE):
        result.verdict = "APPROVE WITH NOTES"
    elif re.search(r"APPROVE", raw_text, re.IGNORECASE):
        result.verdict = "APPROVE"

    return result
