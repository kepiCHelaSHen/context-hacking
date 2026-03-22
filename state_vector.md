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

TURN: framework-stable
MILESTONE: CHP v1 complete — all templates, prompts, and experiments indexed
MODE: STABLE — framework ready for new experiments
LAST_3_FAILURES: none at framework level
WINNING_PARAMETERS: 3-agent loop (builder/critic/reviewer) + 2-model council (GPT-4o/Grok)
METRIC_STATUS: 16 prompts cataloged, 9 experiments completed, all tests passing
OPEN_FLAGS: none
LAST_PASSING_TAG: none (template file — experiments track their own tags)
NEXT_TURN_FOCUS: This is a template. Copy to experiment directory to begin.
SCIENCE_GROUNDING: Framework-level — individual experiments define their own grounding
