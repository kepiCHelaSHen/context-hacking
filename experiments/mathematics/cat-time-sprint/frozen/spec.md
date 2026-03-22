# Time Sprint — Frozen Specification
# 100,000-digit computation of e, pi, sqrt(2)
# DO NOT MODIFY.

## Target
- e:      100,000 decimal digits
- pi:     100,000 decimal digits
- sqrt(2): 100,000 decimal digits

## Precision Requirements
- All digits verified against reference (first 1000 from frozen constants)
- Standard library `decimal` module for naive implementations
- Binary splitting with integer arithmetic for optimized implementations
- No mpmath, sympy, or external math libraries

## Memory Constraint
- Hard limit: 4 GB RSS per process
- Kill switch monitors and terminates processes exceeding this limit
- Exceeding memory = DEAD_END, must be logged

## Algorithm Requirements
### Naive (expected to fail at 100k)
- e: Taylor series sum(1/n!) with Decimal
- pi: Machin arctan series with Decimal
- sqrt(2): Newton's method with Decimal

### Optimized (binary splitting)
- e: Binary splitting of Taylor series using integer arithmetic
- pi: Chudnovsky formula with binary splitting
- sqrt(2): Newton's method with mpz integers (no Decimal overhead)

## Verification
- First 1000 digits must match frozen references from 10k sprint
- Deterministic: same input = same output (no randomness)
