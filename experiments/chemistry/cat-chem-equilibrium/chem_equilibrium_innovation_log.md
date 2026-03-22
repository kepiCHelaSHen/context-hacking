# Chemical Equilibrium — Innovation Log

## Build Summary
Single-pass implementation of Kp↔Kc conversion, van't Hoff equation, and pH from Kw.

## Key Findings
- Kp ≠ Kc when Δn ≠ 0 (Haber-Bosch: Δn = -2)
- Van't Hoff sign must be NEGATIVE: K2 = K1·exp(-(ΔH/R)(1/T2 - 1/T1))
- pH of water varies with temperature: 7.00 at 25°C, 6.81 at 37°C, 6.14 at 100°C

## LLM Prior Errors Caught
1. Treating Kp = Kc (ignoring Δn)
2. Wrong sign in van't Hoff equation
3. Assuming pH = 7 at all temperatures
4. Using HI Kc = 54 instead of 57
