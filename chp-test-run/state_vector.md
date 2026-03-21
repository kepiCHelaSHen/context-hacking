# State Vector — Save Game
# Written every N turns (configurable in config.yaml).
# This is the anchor after context resets. Exactly 10-15 lines.
#
# Required fields:
#   TURN: [current turn number]
#   MILESTONE: [current milestone and status]
#   MODE: [VALIDATION or EXPLORATION, and why]
#   LAST_3_FAILURES: [brief description]
#   WINNING_PARAMETERS: [any values found to work]
#   METRIC_STATUS: [current value vs target for primary metrics]
#   OPEN_FLAGS: [any unresolved anomaly/instability/degradation]
#   LAST_PASSING_TAG: [git tag of last successful build]
#   NEXT_TURN_FOCUS: [one sentence]
#   SCIENCE_GROUNDING: [one sentence — are we still on target?]

TURN: 0
MILESTONE: Not started
MODE: VALIDATION — initial
LAST_3_FAILURES: none
WINNING_PARAMETERS: none
METRIC_STATUS: no data yet
OPEN_FLAGS: none
LAST_PASSING_TAG: none
NEXT_TURN_FOCUS: Begin first build turn
SCIENCE_GROUNDING: Aligned with CHAIN_PROMPT.md
