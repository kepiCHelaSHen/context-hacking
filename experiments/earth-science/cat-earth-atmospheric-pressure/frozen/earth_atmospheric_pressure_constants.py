"""
Atmospheric Pressure (Barometric Formula) — Frozen Constants
Source: ICAO Standard Atmosphere, CODATA 2018
DO NOT MODIFY.
"""
import math

R_GAS = 8.314462           # J/(mol·K) — universal gas constant (CODATA 2018)
T_STD = 288.15             # K — standard atmosphere temperature (15 °C)
M_AIR = 0.028964           # kg/mol — molar mass of dry air (ICAO)
G_STD = 9.80665            # m/s² — standard gravity (exact by definition)
P0 = 101325.0              # Pa — sea-level standard pressure (ICAO)

# Scale height: H = RT / (Mg)
H_SCALE = R_GAS * T_STD / (M_AIR * G_STD)   # ≈ 8434.78 m
# LLM prior: 8000 m or 8500 m — both wrong; correct is ~8434.78 m

# Reference pressures computed from P(h) = P₀ · exp(−h/H)
P_5500 = P0 * math.exp(-5500.0 / H_SCALE)   # ≈ 52787.3 Pa
P_EVEREST = P0 * math.exp(-8848.0 / H_SCALE) # ≈ 35493.3 Pa (~35 % of sea level)

PRIOR_ERRORS = {
    "scale_height_wrong":  "Uses H = 8000 or 10000 instead of ~8434.78 (from R·T/(M·g))",
    "forgets_exp":         "Uses linear P = P₀·(1 − h/H) instead of exponential decay",
    "wrong_gas_constant":  "Uses wrong R (e.g., 8.314 rounded) or wrong M (0.029 rounded)",
}
