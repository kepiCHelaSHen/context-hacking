"""Black-Scholes Option Pricing — CHP Economics Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from econ_black_scholes_constants import N

def d1(S, K, r, sigma, T):
    """Compute d1. sigma must be ANNUALIZED volatility."""
    return (math.log(S / K) + (r + sigma**2 / 2) * T) / (sigma * math.sqrt(T))

def d2_val(d1_val, sigma, T):
    """Compute d2 = d1 - sigma*sqrt(T)."""
    return d1_val - sigma * math.sqrt(T)

def black_scholes_call(S, K, r, sigma, T):
    """European call option price: C = S*N(d1) - K*e^(-rT)*N(d2)."""
    d1_v = d1(S, K, r, sigma, T)
    d2_v = d2_val(d1_v, sigma, T)
    return S * N(d1_v) - K * math.exp(-r * T) * N(d2_v)

def black_scholes_put(S, K, r, sigma, T):
    """European put option price: P = K*e^(-rT)*N(-d2) - S*N(-d1)."""
    d1_v = d1(S, K, r, sigma, T)
    d2_v = d2_val(d1_v, sigma, T)
    return K * math.exp(-r * T) * N(-d2_v) - S * N(-d1_v)

def put_call_parity_check(C, P, S, K, r, T):
    """Verify put-call parity: C - P = S - K*e^(-rT). Returns True if holds."""
    lhs = C - P
    rhs = S - K * math.exp(-r * T)
    return abs(lhs - rhs) < 1e-8

if __name__ == "__main__":
    S, K, r, sigma, T = 100, 100, 0.05, 0.20, 1.0
    C = black_scholes_call(S, K, r, sigma, T)
    P = black_scholes_put(S, K, r, sigma, T)
    print(f"d1 = {d1(S,K,r,sigma,T):.4f}")
    print(f"d2 = {d2_val(d1(S,K,r,sigma,T), sigma, T):.4f}")
    print(f"Call = ${C:.2f}")
    print(f"Put  = ${P:.2f}")
    print(f"Put-call parity holds: {put_call_parity_check(C, P, S, K, r, T)}")
