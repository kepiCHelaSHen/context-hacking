# [PROJECT NAME] — Chain Prompt Master File
# This is the LIVING MASTER DOCUMENT for your project.
# Pass this file in full at the start of every agent session.
#
# It contains:
#   - All confirmed design decisions (authoritative)
#   - Scientific constraints and citations
#   - Architecture rules
#   - File inventory
#
# If this file and any other file conflict, THIS FILE WINS.
# Update this file whenever a design decision is locked in.

================================================================================
PROJECT IDENTITY
================================================================================

Name:       [YOUR PROJECT NAME]
Location:   [PROJECT ROOT]
Language:   Python 3.11+
Status:     [CURRENT PHASE]

Purpose:
  [1-3 sentences describing the scientific question this project investigates]

================================================================================
CONFIRMED DESIGN DECISIONS
================================================================================

[Add decisions here as they are made. Each should have:]
  - What was decided
  - Why (citation or reasoning)
  - Date confirmed

Example:
  DD01 — Agent update rule: synchronous (Nowak & May 1992)
  DD02 — Grid topology: 8-cell Moore neighborhood
  DD03 — Payoff matrix: b=1.8, c=1.0 (standard spatial PD)

================================================================================
ARCHITECTURE RULES
================================================================================

- Pure library: simulation has NO UI, NO print statements. All IO at the edges.
- All randomness via seeded numpy.random.Generator. Same seed = identical results.
- Models know nothing about engines — no circular imports.
- Events are dicts: {type, step, description, outcome}
- Structured logging via logging.getLogger(__name__).

================================================================================
FROZEN CODE
================================================================================

The following paths are FROZEN. Do NOT modify any file in these paths.
New code must compose WITH frozen code, not modify it.

  frozen/

If unsure whether a file is safe to touch — do not touch it.

================================================================================
FILE INVENTORY
================================================================================

[List all project files with line counts and descriptions]

| File | Lines | Description |
|------|-------|-------------|
| [path] | [N] | [what it does] |

================================================================================
CHANGE LOG
================================================================================

[Date] — [What changed and why]
