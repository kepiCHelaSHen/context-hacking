# Chemical Equilibrium — CHP Experiment Report

## Executive Summary
Implemented Kp↔Kc conversion, van't Hoff equation, and temperature-dependent pH.
Caught 4 common LLM prior errors. All 7 tests passing.

## Key Results
- Haber-Bosch at 298K: Kp = 6.77×10⁵, Kc differs by factor of (RT)^Δn
- Van't Hoff correctly predicts K decreases with T for exothermic reactions
- Water pH: 7.00 (25°C), 6.81 (37°C), 6.14 (100°C) — NOT always 7

## LLM Prior Errors (False Positives Caught: 2)
| Error | Description | How Caught |
|-------|------------|------------|
| Kp=Kc | Ignores Δn in conversion | test_kp_kc_differ |
| Van't Hoff sign | Uses +ΔH/R instead of -ΔH/R | test_van_t_hoff_K_decreases |
| pH always 7 | Ignores Kw temperature dependence | test_pH_water_varies |
| HI Kc=54 | Uses 698K value, not 700K | test_hi_kc_is_57 |

## Verification
All constants from NIST WebBook SRD 69 and Atkins Physical Chemistry 11th Edition.
