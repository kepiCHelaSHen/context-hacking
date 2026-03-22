"""GDP Deflator — CHP Economics Sprint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from econ_gdp_deflator_constants import (
    BASE_PRICES, BASE_QUANTS, YEAR1_PRICES, YEAR1_QUANTS
)


def nominal_gdp(prices, quantities):
    """Nominal GDP = Σ Pᵢ_current × Qᵢ_current."""
    return sum(p * q for p, q in zip(prices, quantities))


def real_gdp(base_prices, current_quantities):
    """Real GDP = Σ Pᵢ_base × Qᵢ_current (BASE YEAR prices × current quantities)."""
    return sum(p * q for p, q in zip(base_prices, current_quantities))


def gdp_deflator(nominal, real):
    """GDP Deflator = (Nominal GDP / Real GDP) × 100."""
    return (nominal / real) * 100


def inflation_rate(deflator_t, deflator_t1):
    """Inflation rate = (deflator_t − deflator_{t−1}) / deflator_{t−1} × 100."""
    return (deflator_t - deflator_t1) / deflator_t1 * 100


if __name__ == "__main__":
    # Year 0 (base year)
    nom0 = nominal_gdp(BASE_PRICES, BASE_QUANTS)
    real0 = real_gdp(BASE_PRICES, BASE_QUANTS)
    def0 = gdp_deflator(nom0, real0)
    print(f"Year 0: Nominal={nom0}, Real={real0}, Deflator={def0:.2f}")

    # Year 1
    nom1 = nominal_gdp(YEAR1_PRICES, YEAR1_QUANTS)
    real1 = real_gdp(BASE_PRICES, YEAR1_QUANTS)
    def1 = gdp_deflator(nom1, real1)
    inf01 = inflation_rate(def1, def0)
    print(f"Year 1: Nominal={nom1}, Real={real1}, Deflator={def1:.2f}")
    print(f"Inflation (Y0->Y1): {inf01:.2f}%")
