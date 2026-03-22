"""
Hubble's Law — Frozen Constants
Source: Planck 2018 (H₀=67.4), SH0ES 2022 (H₀=73.04), PDG 2024 consensus ~70
DO NOT MODIFY.
"""
import math

# === Hubble constant ===
# H₀ ≈ 70 km/s/Mpc  (current best estimate; range 67–73)
# Planck CMB: 67.4 ± 0.5 km/s/Mpc
# SH0ES local: 73.04 ± 1.04 km/s/Mpc
# KEY: Hubble's original (1929) was ~500! Using old values gives ~7× wrong distance.
H0_DEFAULT = 70          # km/s/Mpc — rounded consensus
H0_PLANCK = 67.4         # km/s/Mpc — Planck 2018 CMB
H0_SHOES = 73.04         # km/s/Mpc — SH0ES 2022 local distance ladder

# === Unit conversions ===
MPC_TO_M = 3.08567758e22       # metres per Megaparsec (IAU)
MPC_TO_LY = 3.26156e6          # light-years per Megaparsec
LY_TO_M = 9.4607304725808e15   # metres per light-year
GYR_TO_S = 3.15576e16          # seconds per Gyr (1e9 Julian years)

# === Hubble's law: v = H₀ · d ===
# v in km/s, d in Mpc, H₀ in km/s/Mpc
# Rearranged: d = v / H₀

# === Hubble time: t_H = 1/H₀ ===
# Must convert H₀ to s⁻¹ first:
# H₀ [km/s/Mpc] → [s⁻¹] = H₀ * 1e3 / MPC_TO_M
H0_SI = H0_DEFAULT * 1e3 / MPC_TO_M     # s⁻¹ ≈ 2.269e-18
HUBBLE_TIME_S = 1.0 / H0_SI             # seconds ≈ 4.408e17
HUBBLE_TIME_GYR = HUBBLE_TIME_S / GYR_TO_S  # ≈ 13.97 Gyr

# === Test vectors ===
# Galaxy with v = 7000 km/s → d = 7000/70 = 100 Mpc
V_TEST = 7000           # km/s
D_TEST_MPC = 100.0      # Mpc (= 7000 / 70)
D_TEST_LY = D_TEST_MPC * MPC_TO_LY   # ≈ 3.262e8 light-years

# Galaxy with v = 21000 km/s → d = 300 Mpc
V_TEST2 = 21000
D_TEST2_MPC = 300.0

# Hubble time at Planck H₀ = 67.4
H0_PLANCK_SI = H0_PLANCK * 1e3 / MPC_TO_M
HUBBLE_TIME_PLANCK_GYR = 1.0 / H0_PLANCK_SI / GYR_TO_S  # ≈ 14.52 Gyr

# Hubble time at SH0ES H₀ = 73.04
H0_SHOES_SI = H0_SHOES * 1e3 / MPC_TO_M
HUBBLE_TIME_SHOES_GYR = 1.0 / H0_SHOES_SI / GYR_TO_S    # ≈ 13.39 Gyr

# === Known LLM errors ===
PRIOR_ERRORS = {
    "h0_outdated":       "Uses H₀ = 50 or 100 km/s/Mpc instead of modern ~70; "
                         "Hubble's original 1929 value was ~500 — any of these give "
                         "wildly wrong distances (up to 7× error)",
    "units_wrong":       "Confuses H₀ units — e.g., treats km/s/Mpc as m/s/pc "
                         "or forgets to convert to s⁻¹ when computing Hubble time",
    "hubble_time_wrong": "Incorrect conversion of 1/H₀ to years — e.g., forgets "
                         "the km→m and Mpc→m conversions needed to get s⁻¹",
}
