"""
Memory Manager — Layer 5: Context window management.

Three external memory files that survive context resets:
  - state_vector.md: 10-15 line "save game" (written every N turns)
  - innovation_log.md: persistent turn-by-turn log (append-only)
  - dead_ends.md: failed approaches (read before every build)

The context window is a managed resource, not an infinite buffer.
"""

from __future__ import annotations

import logging
import re
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from context_hacking.core.orchestrator import Config

_log = logging.getLogger(__name__)


class MemoryManager:
    """Manages the three external memory files."""

    def __init__(self, config: "Config") -> None:
        project = config.raw.get("project", {})
        self._innovation_log_path = Path(
            project.get("innovation_log", "innovation_log.md")
        )
        self._dead_ends_path = Path(project.get("dead_ends", "dead_ends.md"))
        self._state_vector_path = Path(
            project.get("state_vector", "state_vector.md")
        )
        self._dead_ends_cache: list[str] | None = None

    # ── Dead Ends ─────────────────────────────────────────────────────────────

    @property
    def dead_ends(self) -> list[str]:
        """Return list of dead end titles."""
        return self.load_dead_ends()

    def load_dead_ends(self) -> list[str]:
        """Parse dead_ends.md and return a list of dead-end titles."""
        if not self._dead_ends_path.exists():
            return []

        text = self._dead_ends_path.read_text(encoding="utf-8")
        # Extract titles: lines starting with "## DEAD END"
        titles = re.findall(r"^## DEAD END \d+ — (.+)$", text, re.MULTILINE)
        return titles

    def add_dead_end(self, title: str, attempted: str, result: str, reason: str) -> None:
        """Append a new dead end to dead_ends.md."""
        existing = self._dead_ends_path.read_text(encoding="utf-8") if self._dead_ends_path.exists() else ""

        # Count existing dead ends
        count = len(re.findall(r"^## DEAD END", existing, re.MULTILINE))
        new_id = count + 1

        entry = f"""
---

## DEAD END {new_id} — {title}

**What was attempted**: {attempted}

**Result**: {result}

**Why this is a dead end**: {reason}

**Do NOT repeat**: {title}
"""
        with open(self._dead_ends_path, "a", encoding="utf-8") as f:
            f.write(entry)

        self._dead_ends_cache = None  # invalidate cache
        _log.info("Dead end #%d logged: %s", new_id, title)

    # ── Innovation Log ────────────────────────────────────────────────────────

    def append_innovation_log(self, turn: int, mode: str, content: str) -> None:
        """Append a turn entry to the innovation log."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        entry = f"""
---

## Turn {turn} — {timestamp}

### Mode
{mode}

{content}
"""
        with open(self._innovation_log_path, "a", encoding="utf-8") as f:
            f.write(entry)
        _log.info("Innovation log updated: Turn %d", turn)

    def last_innovation_entry(self) -> str:
        """Return the last 'What next turn should focus on' line, or empty string."""
        if not self._innovation_log_path.exists():
            return ""

        text = self._innovation_log_path.read_text(encoding="utf-8")
        # Find the last "### What next turn should focus on" section
        matches = re.findall(
            r"### What next turn should focus on\n(.*?)(?=\n---|\n## |\Z)",
            text,
            re.DOTALL,
        )
        if matches:
            return matches[-1].strip()[:200]  # truncate for log
        return ""

    def read_full_log(self) -> str:
        """Read the full innovation log (for council review)."""
        if not self._innovation_log_path.exists():
            return "Innovation log not found — no turns completed yet."
        return self._innovation_log_path.read_text(encoding="utf-8")

    # ── State Vector ──────────────────────────────────────────────────────────

    def write_state_vector(self, turn: int, mode: str, **kwargs: str) -> None:
        """Write the state vector save game (10-15 lines max)."""
        fields = {
            "TURN": str(turn),
            "MODE": mode,
            "MILESTONE": kwargs.get("milestone", "in progress"),
            "LAST_3_FAILURES": kwargs.get("failures", "none"),
            "WINNING_PARAMETERS": kwargs.get("winning_params", "none"),
            "METRIC_STATUS": kwargs.get("metric_status", "no data"),
            "OPEN_FLAGS": kwargs.get("open_flags", "none"),
            "LAST_PASSING_TAG": kwargs.get("last_tag", "none"),
            "NEXT_TURN_FOCUS": kwargs.get("next_focus", "continue"),
            "SCIENCE_GROUNDING": kwargs.get("grounding", "aligned"),
            "STAGNATION_STREAK": kwargs.get("stagnation_streak", "0"),
            "EXPLORATION_STREAK": kwargs.get("exploration_streak", "0"),
            "CONSECUTIVE_ANOMALIES": kwargs.get("consecutive_anomalies", "0"),
        }

        lines = [
            "# State Vector — Save Game",
            f"# Written at Turn {turn}, {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
        ]
        for key, value in fields.items():
            lines.append(f"{key}: {value}")

        self._state_vector_path.write_text("\n".join(lines), encoding="utf-8")
        _log.info("State vector written: Turn %d", turn)

    def read_state_vector(self) -> dict[str, str]:
        """Parse the state vector into a dict."""
        if not self._state_vector_path.exists():
            return {}

        result: dict[str, str] = {}
        text = self._state_vector_path.read_text(encoding="utf-8")
        for line in text.splitlines():
            if ":" in line and not line.startswith("#"):
                key, _, value = line.partition(":")
                result[key.strip()] = value.strip()
        return result
