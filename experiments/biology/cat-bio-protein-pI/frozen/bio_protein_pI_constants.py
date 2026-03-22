"""Isoelectric Point (pI) — Frozen Constants. Source: standard biochemistry pKa tables. DO NOT MODIFY."""
import math

# pI = average of the two pKa values that flank the zwitterionic (net-zero) form.
#
# For a SIMPLE amino acid (no ionizable side chain):
#   Only two ionizable groups: α-COOH (pKa1 ≈ 2.0-2.4) and α-NH₃⁺ (pKa2 ≈ 9.0-10.5)
#   pI = (pKa1 + pKa2) / 2
#
# For an ACIDIC amino acid (Asp, Glu) — side chain has COOH:
#   Three ionizable groups, ranked low→high: pKa1 < pKaR < pKa2
#   The zwitterion is flanked by the TWO LOWEST pKa values.
#   pI = (pKa1 + pKaR) / 2        ← NOT (pKa1 + pKa2)/2!
#
# For a BASIC amino acid (Lys, Arg, His) — side chain has NH₃⁺ or guanidinium:
#   Three ionizable groups, ranked low→high: pKa1 < pKa2 < pKaR
#   The zwitterion is flanked by the TWO HIGHEST pKa values.
#   pI = (pKa2 + pKaR) / 2        ← NOT (pKa1 + pKa2)/2!

# ── Glycine (simple, no ionizable side chain) ────────────────────────
GLY_PKA1 = 2.34    # α-COOH
GLY_PKA2 = 9.60    # α-NH₃⁺
GLY_PI   = (GLY_PKA1 + GLY_PKA2) / 2   # 5.97

assert math.isclose(GLY_PI, 5.97, rel_tol=1e-9), f"Gly pI should be 5.97, got {GLY_PI}"

# ── Aspartate (ACIDIC side chain: β-COOH) ────────────────────────────
ASP_PKA1  = 2.09    # α-COOH         (lowest)
ASP_PKAR  = 3.86    # β-COOH side chain (middle)
ASP_PKA2  = 9.82    # α-NH₃⁺         (highest)
# pI uses the TWO LOWEST pKa values: pKa1 and pKaR
ASP_PI    = (ASP_PKA1 + ASP_PKAR) / 2  # 2.975

assert math.isclose(ASP_PI, 2.975, rel_tol=1e-9), f"Asp pI should be 2.975, got {ASP_PI}"
# The WRONG answer: averaging pKa1 and pKa2 (ignoring side chain role)
ASP_PI_WRONG = (ASP_PKA1 + ASP_PKA2) / 2  # 5.955 — WRONG!
assert not math.isclose(ASP_PI, ASP_PI_WRONG, rel_tol=0.01), (
    "Asp pI must NOT equal (pKa1+pKa2)/2 — that ignores the acidic side chain!"
)

# ── Lysine (BASIC side chain: ε-NH₃⁺) ────────────────────────────────
LYS_PKA1  = 2.18    # α-COOH         (lowest)
LYS_PKA2  = 8.95    # α-NH₃⁺         (middle)
LYS_PKAR  = 10.53   # ε-NH₃⁺ side chain (highest)
# pI uses the TWO HIGHEST pKa values: pKa2 and pKaR
LYS_PI    = (LYS_PKA2 + LYS_PKAR) / 2  # 9.74

assert math.isclose(LYS_PI, 9.74, rel_tol=1e-9), f"Lys pI should be 9.74, got {LYS_PI}"
# The WRONG answer: averaging pKa1 and pKa2 (ignoring side chain role)
LYS_PI_WRONG = (LYS_PKA1 + LYS_PKA2) / 2  # 5.565 — WRONG!
assert not math.isclose(LYS_PI, LYS_PI_WRONG, rel_tol=0.01), (
    "Lys pI must NOT equal (pKa1+pKa2)/2 — that ignores the basic side chain!"
)

PRIOR_ERRORS = {
    "wrong_pka_pair":      "Averages the wrong pair of pKa values (e.g., pKa1+pKa2 for Asp instead of pKa1+pKaR)",
    "pka_values_wrong":    "Uses incorrect pKa values for amino acid ionizable groups",
    "forgets_side_chain":  "Ignores the ionizable side chain and treats all amino acids as simple (pKa1+pKa2)/2",
}
