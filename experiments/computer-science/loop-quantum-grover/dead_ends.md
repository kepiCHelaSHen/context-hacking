# Grover's Algorithm — Dead Ends Log

---

## DEAD END 1 — Classical brute-force search

**What was attempted**: Builder generated a loop that checks each item one by one
(classical linear search) and reported "found target in sqrt(N) steps on average."

**Result**: The search used random sampling with geometric success distribution
(p = 1/N per query). Average iterations = N/2, not sqrt(N). The "sqrt(N)" claim
was based on 3 lucky seeds. At 30 seeds, the distribution is clearly geometric
(classical), not peaked at floor(pi/4 * sqrt(N)) (quantum).

**Why this is a dead end**: Grover's algorithm requires a quantum state vector
(2^n complex amplitudes), Hadamard initialization, phase-flip oracle, and
diffusion operator. Classical search cannot achieve quadratic speedup regardless
of cleverness — this is provably impossible (BBBV theorem).

**Do NOT repeat**: Any search that doesn't maintain a 2^n amplitude vector.

---

## DEAD END 2 — Oracle returns True/False instead of flipping phase

**What was attempted**: Builder implemented `def oracle(x): return x == target`
which is a classical boolean function.

**Result**: Without phase manipulation, the "quantum" algorithm degenerates to
classical random sampling. The boolean oracle provides information by classical
query, not by quantum interference.

**Why this is a dead end**: The Grover oracle must modify the STATE VECTOR:
`amplitudes[target] *= -1`. It does NOT return a boolean. The phase flip is what
enables constructive interference in the diffusion step.

**Do NOT repeat**: Any oracle that returns a value. The oracle MODIFIES amplitudes.

---

## DEAD END 3 — Missing or reversed diffusion operator

**What was attempted**: Builder applied the oracle repeatedly without the
diffusion step (inversion about the mean).

**Result**: After k oracle applications, only the target state has flipped
phase. No amplitude amplification occurs. Success probability remains 1/N
regardless of k. The algorithm is equivalent to doing nothing.

**Why this is a dead end**: The diffusion operator is the "magic" of Grover's
algorithm. It converts phase information (from the oracle) into amplitude
information (probability of measurement). G = D * O, and D is required.

**Do NOT repeat**: Any Grover implementation without explicit diffusion.
Also: applying D before O reverses the interference pattern and produces
different (wrong) dynamics.
