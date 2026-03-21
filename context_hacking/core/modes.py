"""
Mode Manager — Layer 7: Two-mode negative feedback loop.

VALIDATION (default):
  - Full literature grounding required
  - Critic is a hard blocker
  - Council runs BEFORE build
  - Use for: known mechanisms, calibration, fixing issues

EXPLORATION (when stuck or novelty needed):
  - Literature grounding relaxed — state hypothesis instead of citation
  - Critic is advisory only
  - Council runs AFTER build
  - Reversion protocol active
  - Max K consecutive turns, then forced return to Validation
  - K Exploration turns with no improvement → EXIT 2

Automatic switching:
  - No improvement for N turns → switch to Exploration
  - Exploration anomaly → Reversion Protocol → back to Validation
  - K Exploration turns with no improvement → EXIT 2
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from context_hacking.core.orchestrator import Config

_log = logging.getLogger(__name__)

VALIDATION = "VALIDATION"
EXPLORATION = "EXPLORATION"


class ModeManager:
    """Manages the Validation/Exploration mode switching logic."""

    def __init__(self, config: "Config") -> None:
        self._mode: str = VALIDATION
        self._stagnation_streak: int = 0
        self._exploration_streak: int = 0
        self._max_stagnation: int = config.stagnation_threshold
        self._max_exploration: int = config.max_consecutive_exploration

    @property
    def current_mode(self) -> str:
        return self._mode

    @property
    def stagnation_streak(self) -> int:
        return self._stagnation_streak

    @property
    def exploration_streak(self) -> int:
        return self._exploration_streak

    def record_turn(self, metrics_improved: bool, anomaly: bool) -> None:
        """Record turn outcome and potentially switch modes."""
        if metrics_improved:
            self._stagnation_streak = 0
        else:
            self._stagnation_streak += 1

        if self._mode == EXPLORATION:
            self._exploration_streak += 1

            # Exploration anomaly → revert to Validation
            if anomaly:
                _log.warning(
                    "Exploration anomaly at streak %d — reverting to VALIDATION",
                    self._exploration_streak,
                )
                self._switch_to_validation()
                return

            # Max exploration turns → forced return
            if self._exploration_streak >= self._max_exploration:
                _log.info(
                    "Max Exploration turns (%d) reached — returning to VALIDATION",
                    self._max_exploration,
                )
                self._switch_to_validation()
                return

        elif self._mode == VALIDATION:
            # Stagnation → switch to Exploration
            if self._stagnation_streak >= self._max_stagnation:
                _log.info(
                    "Stagnation streak %d >= %d — switching to EXPLORATION",
                    self._stagnation_streak,
                    self._max_stagnation,
                )
                self._switch_to_exploration()
                return

    def force_mode(self, mode: str) -> None:
        """Force a specific mode (for milestone-level overrides)."""
        if mode == EXPLORATION:
            self._switch_to_exploration()
        else:
            self._switch_to_validation()

    def _switch_to_validation(self) -> None:
        self._mode = VALIDATION
        self._exploration_streak = 0
        _log.info("Mode: VALIDATION")

    def _switch_to_exploration(self) -> None:
        self._mode = EXPLORATION
        self._exploration_streak = 0
        _log.info("Mode: EXPLORATION")

    @property
    def critic_is_blocker(self) -> bool:
        """In Validation, critic blocks. In Exploration, critic is advisory."""
        return self._mode == VALIDATION

    @property
    def council_before_build(self) -> bool:
        """In Validation, council runs before build. In Exploration, after."""
        return self._mode == VALIDATION

    @property
    def reversion_active(self) -> bool:
        """Reversion protocol is active only in Exploration mode."""
        return self._mode == EXPLORATION
