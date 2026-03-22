"""
Carnot Cycle — Frozen Constants
Source: Zemansky & Dittman Heat & Thermodynamics 8th Ed, Callen Thermodynamics 2nd Ed
DO NOT MODIFY.
"""

# Carnot efficiency: η = 1 - Tc/Th (temperatures in KELVIN)
# LLM prior: uses Celsius → dramatically wrong

# Test: Th = 500K, Tc = 300K
TH_TEST = 500.0  # K
TC_TEST = 300.0   # K
ETA_CARNOT = 1.0 - TC_TEST / TH_TEST  # = 0.40 (40%)
# LLM prior with Celsius (227°C, 27°C): η = 1 - 27/227 = 0.881 (WRONG)

# COP heat pump: COP_hp = Th/(Th-Tc) = 1/η
COP_HP = TH_TEST / (TH_TEST - TC_TEST)  # = 2.5
# COP refrigerator: COP_ref = Tc/(Th-Tc)
COP_REF = TC_TEST / (TH_TEST - TC_TEST)  # = 1.5
# Note: COP_hp = COP_ref + 1 (ALWAYS)

# Real engine efficiency is ALWAYS less than Carnot
# Typical coal plant: ~33%, typical car: ~25%

PRIOR_ERRORS = {
    "celsius_not_kelvin":  "Uses T in °C instead of K — gives wildly wrong η",
    "cop_formula":         "Confuses COP_hp and COP_ref (differ by 1)",
    "cop_less_than_1":     "Claims COP must be < 1 (it can be much > 1)",
    "reversible_possible": "Claims real engines can achieve Carnot efficiency",
}
