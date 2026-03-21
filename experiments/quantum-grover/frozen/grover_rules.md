# Grover's Search Algorithm — Frozen Specification
# Source: Grover (1996) "A fast quantum mechanical algorithm for database search"
#         Proceedings of STOC '96, pp. 212-219
# Reference: Nielsen & Chuang (2010) Ch. 6.1-6.3
# THIS FILE IS FROZEN. No agent may modify it.

================================================================================
OVERVIEW
================================================================================

Grover's algorithm searches an unstructured database of N items for a marked
item using O(sqrt(N)) quantum queries, a quadratic speedup over classical
O(N) search. This is a SIMULATION of the quantum algorithm using classical
state-vector representation of the qubit register.

The key scientific point: LLMs confuse Grover's QUANTUM search with classical
RANDOM search. Both find items, but the iteration profile is fundamentally
different. Classical random search has a geometric success distribution
(p = 1/N per query). Grover's has a PEAKED distribution at exactly
floor(pi/4 * sqrt(N)) iterations. The Prior-as-Detector catches classical
contamination by checking the iteration-count distribution.

================================================================================
QUANTUM CIRCUIT
================================================================================

REGISTER: n qubits representing N = 2^n basis states.
  Default: n = 10 (N = 1024 items).

TARGET: One marked item |w> (index chosen per seed).

INITIAL STATE: Equal superposition.
  |psi_0> = H^n |0>^n = (1/sqrt(N)) * sum_{x=0}^{N-1} |x>

  where H is the Hadamard gate applied to each qubit.

GROVER ITERATION (one "query"):
  G = D * O

  where:
    O = Oracle operator (phase flip on target):
        O|x> = -|x> if x == w (the marked item)
        O|x> = |x>  otherwise

        In matrix form: O = I - 2|w><w|

    D = Diffusion operator (inversion about the mean):
        D = 2|psi_0><psi_0| - I

        This reflects every amplitude about the mean amplitude.

        NOTE: The diffusion operator is sometimes written as
        D = H^n (2|0><0| - I) H^n. Both are equivalent. The frozen
        spec uses D = 2|psi_0><psi_0| - I for clarity.

  ORDER MATTERS: Apply O first, then D. G = D * O.

  NOTE: LLMs sometimes reverse the order (O * D) or omit the diffusion
  operator entirely (just applying the oracle repeatedly). Without
  diffusion, the oracle is just a phase flip with no amplitude amplification.
  This is the most common quantum algorithm drift.

OPTIMAL ITERATIONS:
  k_opt = floor(pi/4 * sqrt(N))

  For N = 1024: k_opt = floor(pi/4 * sqrt(1024)) = floor(pi/4 * 32) = floor(25.13) = 25

  NOTE: This is EXACT for the ideal algorithm. LLMs commonly generate
  "sqrt(N)" iterations (32 for N=1024) which OVERSHOOTS the optimal
  and reduces success probability.

MEASUREMENT:
  After k_opt iterations of G, measure the register in the computational basis.
  Success probability: P(w) = sin^2((2k+1) * theta)
  where theta = arcsin(1/sqrt(N)).

  At k_opt: P(w) >= 1 - 1/N (approaches 1 for large N).
  For N=1024: P(w) >= 0.999

================================================================================
METRICS
================================================================================

  success_probability: P(measuring |w>) after k_opt iterations
    Expected: > 0.95 for N=1024

  target_amplitude: |<w|psi>|^2 after k_opt iterations
    Expected: > 0.95 for N=1024

  optimal_iterations: k_opt = floor(pi/4 * sqrt(N))
    For N=1024: exactly 25

  amplitude_evolution: |<w|psi>|^2 as a function of iteration count k
    Should show sinusoidal growth peaking near k_opt

  quadratic_speedup_verified: boolean
    True if the algorithm finds the target in O(sqrt(N)) iterations,
    not O(N) (classical) or O(1) (cheating by hardcoding the answer).

================================================================================
CLASSICAL CONTAMINATION WARNING
================================================================================

LLMs generate classical search algorithms when asked for "Grover's algorithm"
because:
  1. The concept of "searching a database" triggers classical DB lookup priors
  2. The quantum circuit (Hadamard, oracle, diffusion) is non-trivial to generate
  3. Classical simulation of quantum states is just linear algebra, but LLMs
     often skip the state-vector math and implement classical brute-force

Signs of classical contamination:
  - Success after random number of iterations (geometric distribution)
  - No state vector (array of 2^n complex amplitudes)
  - No Hadamard gate or diffusion operator
  - Iteration count = N or N/2 instead of sqrt(N)
  - Oracle that RETURNS the answer instead of FLIPPING a phase

If the oracle function returns True/False (classical), it's wrong.
The oracle must apply a PHASE FLIP: amplitude[w] *= -1.

================================================================================
EXACT COEFFICIENTS (for drift detection)
================================================================================

  N_QUBITS: 10
  N_ITEMS: 1024  (= 2^10)
  K_OPTIMAL: 25  (= floor(pi/4 * sqrt(1024)))
  ORACLE_TYPE: "phase_flip"  (NOT "boolean_return")
  DIFFUSION_TYPE: "inversion_about_mean"
  ORDER: "oracle_then_diffusion"  (G = D * O, NOT O * D)
  INITIAL_STATE: "equal_superposition"
  SUCCESS_THRESHOLD: 0.95
