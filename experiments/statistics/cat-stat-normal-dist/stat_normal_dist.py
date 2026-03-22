"""Normal Distribution — CHP Statistics Sprint. All constants from frozen spec."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from stat_normal_dist_constants import *


def z_score(x, mu, sigma):
    """Compute z = (x − μ) / σ."""
    return (x - mu) / sigma


def pdf(x, mu=0, sigma=1):
    """Normal PDF: (1/(σ√(2π))) · exp(−(x−μ)²/(2σ²))."""
    return (1.0 / (sigma * math.sqrt(2 * math.pi))) * math.exp(-((x - mu) ** 2) / (2 * sigma ** 2))


def cdf_approx(z):
    """Standard normal CDF via erf: Φ(z) = 0.5·(1 + erf(z/√2))."""
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def percentile_from_z(z):
    """Percentile (0–1) for a standard normal z-score; same as CDF."""
    return cdf_approx(z)


def symmetric_interval(z):
    """P(−z < Z < z) = 2·Φ(z) − 1."""
    return 2 * cdf_approx(z) - 1


if __name__ == "__main__":
    print("Normal Distribution — precise vs 68-95-99.7 rule\n")
    for k in (1, 2, 3):
        precise = symmetric_interval(k)
        approx  = {1: 0.68, 2: 0.95, 3: 0.997}[k]
        print(f"  ±{k}σ  precise = {precise:.8f}  rule ≈ {approx}  "
              f"Δ = {abs(precise - approx):.6f}")
    z = z_score(X_TEST, MU_TEST, SIGMA_TEST)
    print(f"\n  Test: x={X_TEST}, μ={MU_TEST}, σ={SIGMA_TEST}")
    print(f"    z = {z:.4f}   Φ(z) = {cdf_approx(z):.10f}")
    print(f"    PDF at mean = {pdf(0):.10f}  (density, not probability)")
