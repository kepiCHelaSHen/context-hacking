# SIMSIV v2 Replication — Chain Prompt

================================================================================
PROJECT IDENTITY
================================================================================

Name:       SIMSIV v2 Replication (CHP Crown Jewel #2)
Purpose:    Reproduce the North vs Bowles/Gintis result (p<0.0001) from a
            frozen specification. Catch the known false positive (n=3 → n=10).
            Prove CHP's self-correction on a real scientific question.

================================================================================
CONFIRMED DESIGN DECISIONS
================================================================================

All design decisions in frozen/simsiv_v2_spec.md.
v1 codebase is FROZEN — build v2 ON TOP without modifying v1.
Per-band Config enables institutional differentiation.
Composition pattern: Band HAS-A Society.

================================================================================
ARCHITECTURE RULES
================================================================================

- Pure library: NO print(), NO UI.
- All randomness via seeded numpy.random.Generator.
- Per-band rng isolation (band.rng for intra-band, shared rng for inter-band).
- Models know nothing about engines (TYPE_CHECKING guards).
- Events are dicts.
- Structured logging.

================================================================================
FROZEN CODE
================================================================================

frozen/simsiv_v2_spec.md — DO NOT MODIFY.
The v1 codebase (built in experiment #10) is also frozen.

================================================================================
THE FALSE POSITIVE TO CATCH
================================================================================

At Milestone 7, n=3 seeds may show interaction effect +0.03 to +0.05.
THE CRITIC MUST SAY: "Replicate at n=10."
At n=10: the effect vanishes (p > 0.90).
This is Dead End 1 + Dead End 7 in action.
Scale to 20 bands for the real result: North wins, p<0.0001.
