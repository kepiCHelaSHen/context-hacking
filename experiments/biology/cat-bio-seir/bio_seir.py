"""SEIR Epidemic Model — CHP Biology Sprint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from bio_seir_constants import *


def seir_derivatives(S, E, I, R, N, beta, sigma, gamma):
    """Compute SEIR model derivatives.

    dS/dt = -beta * S * I / N
    dE/dt =  beta * S * I / N - sigma * E
    dI/dt =  sigma * E - gamma * I
    dR/dt =  gamma * I

    Returns (dS, dE, dI, dR).
    """
    dS = -beta * S * I / N
    dE = beta * S * I / N - sigma * E
    dI = sigma * E - gamma * I
    dR = gamma * I
    return (dS, dE, dI, dR)


def r0(beta, gamma):
    """Basic reproduction number R0 = beta / gamma.

    KEY: R0 depends ONLY on beta and gamma.
    The exposed-compartment rate sigma does NOT affect R0.
    This is the same formula for both SIR and SEIR models.
    """
    return beta / gamma


def herd_immunity_threshold(R0):
    """Herd immunity threshold = 1 - 1/R0.

    Same formula for both SIR and SEIR models.
    """
    return 1 - 1 / R0


def conservation_check(S, E, I, R, N):
    """Check that S + E + I + R = N (population conservation).

    Returns True if compartments sum to N within floating-point tolerance.
    """
    import math
    return math.isclose(S + E + I + R, N, rel_tol=1e-9)


if __name__ == "__main__":
    print(f"SEIR Model: beta={BETA}, sigma={SIGMA}, gamma={GAMMA}, N={N}")
    print(f"R0 = beta/gamma = {r0(BETA, GAMMA):.1f}")
    print(f"Herd immunity threshold = {herd_immunity_threshold(r0(BETA, GAMMA)):.1%}")
    print()
    print(f"Test state: S={TEST_S}, E={TEST_E}, I={TEST_I}, R={TEST_R}")
    derivs = seir_derivatives(TEST_S, TEST_E, TEST_I, TEST_R, N, BETA, SIGMA, GAMMA)
    print(f"dS/dt = {derivs[0]:.4f}")
    print(f"dE/dt = {derivs[1]:.4f}")
    print(f"dI/dt = {derivs[2]:.4f}")
    print(f"dR/dt = {derivs[3]:.4f}")
    print(f"Sum of derivatives = {sum(derivs):.12f}")
    print(f"Conservation: {conservation_check(TEST_S, TEST_E, TEST_I, TEST_R, N)}")
