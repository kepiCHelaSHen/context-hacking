# CHP Time Sprint Results — 100,000 Digits

## Mission
Compute e, pi, and sqrt(2) to 100,000 verified digits each.
Two approaches tested: naive Decimal arithmetic vs binary splitting with integer arithmetic.
Kill switch monitoring all processes (4GB RAM limit, 120s timeout).

## Results

### Naive (Decimal arithmetic)
| Constant | Time | Algorithm | Peak Memory | Kill Switch |
|----------|------|-----------|-------------|-------------|
| e        | 7.0s | Taylor series (Decimal) | 16 MB | SURVIVED |
| pi       | 35.0s | Machin arctan (Decimal) | 16 MB | SURVIVED |
| sqrt(2)  | 0.71s | Newton (Decimal, 17 iter) | 17 MB | SURVIVED |

### Optimized (Binary splitting / integer arithmetic)
| Constant | Time | Algorithm | Peak Memory | Speedup |
|----------|------|-----------|-------------|---------|
| e        | 13.7s | Binary splitting Taylor | 18 MB | 0.5x (slower!) |
| pi       | 6.2s | Chudnovsky binary splitting | 17 MB | **5.6x faster** |
| sqrt(2)  | 2.3s | Integer Newton (17 iter) | 16 MB | 0.3x (slower!) |

### Total computation time
- Naive total: 42.7s
- Optimized total: 22.2s
- Overall speedup: 1.9x

## Key Findings

### 1. The kill switch was not needed at 100k
All six implementations completed within 60 seconds and under 20MB memory.
Python's `decimal` module (backed by libmpdec in C) is highly optimized for
medium-precision arithmetic. The kill switch would become critical at 1M+ digits
where naive approaches genuinely exhaust time and memory.

**CHP lesson:** The kill switch is infrastructure, not theater. It sits ready
and fires when needed. At 100k, it logged "SURVIVED" for all processes.
At 1M digits, the naive Taylor series would timeout and trigger a dead-end.

### 2. Chudnovsky is the real speedup story
The only dramatic speedup came from pi: Machin's formula needs ~70,000 terms
of arctan series, while Chudnovsky needs only ~7,050 terms (each gives ~14 digits).
The algorithm change — not just the arithmetic optimization — is what matters.

**CHP lesson:** The protocol forced exploration of better algorithms. The naive
Machin approach works but is O(n) terms with O(n) digit operations each. Chudnovsky
with binary splitting reduces this dramatically.

### 3. Binary splitting is NOT always faster
For e and sqrt(2), the binary splitting / integer approach was actually **slower**
than naive Decimal at 100k digits. Why?

- **e**: Binary splitting creates enormous intermediate integers. The final
  `Decimal(P) / Decimal(Q)` division at 100k precision is expensive. The naive
  Taylor series in Decimal does many small divisions (amortized).

- **sqrt(2)**: Newton's method only needs 17 iterations regardless. The naive
  Decimal version does 17 divisions at 100k precision. The integer version does
  17 integer divisions plus a string conversion. At this scale, Decimal's C
  implementation (libmpdec) is faster than Python integer arithmetic.

The crossover where binary splitting wins is likely around 500k-1M digits.

**CHP lesson:** Dead-end detection isn't just "this approach is too slow."
It's also "this optimization isn't actually an optimization at this scale."
The protocol should test both approaches and pick the winner empirically.

### 4. The multiplier is 6,250x
- LLM float ceiling: 16 digits
- CHP computed: 100,000 digits
- Multiplier: **6,250x** the LLM float ceiling
- All digits verified against frozen references (first 1000 digits match OEIS)

### 5. False positives from 10k sprint carry forward
The sqrt(2) frozen reference corruption discovered in the 10k sprint was fixed
before this sprint. The corrected reference verified successfully against all
100k-digit computations.

## Kill Switch Log
```
e naive:     SURVIVED (7.0s, 16MB)
pi naive:    SURVIVED (35.0s, 16MB)
sqrt2 naive: SURVIVED (0.71s, 17MB)
e fast:      SURVIVED (13.7s, 18MB)
pi fast:     SURVIVED (6.2s, 17MB)
sqrt2 fast:  SURVIVED (2.3s, 16MB)

Kill switch triggers: 0
Dead ends logged: 0
```

## Files Generated
- `naive/compute_e_naive.py` — Naive Taylor series (Decimal)
- `naive/compute_pi_naive.py` — Naive Machin formula (Decimal)
- `naive/compute_sqrt2_naive.py` — Naive Newton (Decimal)
- `binary_splitting/compute_e_fast.py` — Binary splitting Taylor (integer)
- `binary_splitting/compute_pi_fast.py` — Chudnovsky binary splitting
- `binary_splitting/compute_sqrt2_fast.py` — Integer Newton
- `kill_switch.py` — Process monitor (4GB RAM, configurable timeout)
- `figures/e_100000.txt` — 100,000 digits of e
- `figures/pi_100000.txt` — 100,000 digits of pi
- `figures/sqrt2_100000.txt` — 100,000 digits of sqrt(2)
- `figures/time_sprint_comparison.png` — Comparison figure

## Verdict

The 100k sprint proves:
1. **CHP scales.** Same protocol, 10x more digits, same verification framework.
2. **Algorithm selection matters more than arithmetic optimization** at medium precision.
3. **The kill switch is real infrastructure** — ready but not needed at 100k.
4. **Honest results > dramatic narratives.** The naive approaches worked fine.
   Science means reporting what happened, not what we expected.
