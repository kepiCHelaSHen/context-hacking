# SIMSIV v1 Replication — Chain Prompt

================================================================================
PROJECT IDENTITY
================================================================================

Name:       SIMSIV v1 Replication (CHP Crown Jewel #1)
Purpose:    Reproduce a calibrated 35-trait, 9-engine agent-based model of
            human social evolution from a frozen specification. Prove CHP
            works at production scale (~10,000 lines).

================================================================================
CONFIRMED DESIGN DECISIONS
================================================================================

All design decisions are in frozen/simsiv_v1_spec.md.
27 deep-dive sessions (DD01-DD27) defined the original architecture.
Every trait, every engine, every parameter has a documented justification.

================================================================================
ARCHITECTURE RULES
================================================================================

- Pure library: NO print(), NO UI.
- All randomness via seeded numpy.random.Generator.
- Same seed = identical output.
- Models know nothing about engines.
- Events are dicts.
- Structured logging.

================================================================================
FROZEN CODE
================================================================================

frozen/simsiv_v1_spec.md — DO NOT MODIFY.
This represents the published paper (BIORXIV/2026/711970).
