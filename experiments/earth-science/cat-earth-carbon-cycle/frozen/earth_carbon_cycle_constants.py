"""Carbon Cycle — Frozen Constants. Source: IPCC AR6 WG1 Ch5; Global Carbon Project 2023. DO NOT MODIFY."""

# ── Reservoir sizes (GtC) ──────────────────────────────────────────
RESERVOIR_ATMOSPHERE   = 860.0        # GtC — well-mixed CO₂ (~415 ppm × 2.12)
RESERVOIR_OCEAN        = 38_000.0     # GtC — dissolved inorganic + organic carbon
RESERVOIR_LAND_BIO     = 2_000.0      # GtC — vegetation + soil
RESERVOIR_FOSSIL       = 10_000.0     # GtC — coal, oil, gas (pre-industrial est.)
RESERVOIR_SEDIMENTS    = 60_000_000.0 # GtC — lithosphere (carbonate rocks + kerogen)

# KEY: Ocean is BY FAR the largest *active* reservoir (~38000 GtC).
# Atmosphere (~860 GtC) is one of the SMALLEST active reservoirs.

RESERVOIRS = {
    "atmosphere":    RESERVOIR_ATMOSPHERE,
    "ocean":         RESERVOIR_OCEAN,
    "land_biosphere": RESERVOIR_LAND_BIO,
    "fossil_fuels":  RESERVOIR_FOSSIL,
    "sediments":     RESERVOIR_SEDIMENTS,
}

# ── Fluxes (GtC / yr) ──────────────────────────────────────────────
OCEAN_NET_UPTAKE       = 2.5   # GtC/yr — ocean absorbs NET from atmosphere
FOSSIL_EMISSIONS       = 10.0  # GtC/yr — fossil fuel combustion + cement
LAND_USE_CHANGE        = 1.5   # GtC/yr — deforestation, agriculture
TOTAL_EMISSIONS        = FOSSIL_EMISSIONS + LAND_USE_CHANGE  # 11.5 GtC/yr

# KEY: Ocean is a NET SINK of CO₂.  It absorbs ~2.5 GtC/yr more than it emits.
OCEAN_IS_NET_SINK      = True

# ── Airborne fraction ──────────────────────────────────────────────
AIRBORNE_FRACTION      = 0.45  # ~45% of total emissions remain in atmosphere

# ── Unit conversion ─────────────────────────────────────────────────
GTC_PER_PPM            = 2.12  # 1 ppm CO₂ ≈ 2.12 GtC in atmosphere

# ── Residence vs perturbation lifetime ──────────────────────────────
# Gross flux through atmosphere: ~210 GtC/yr (photosynthesis + ocean exchange)
GROSS_FLUX             = 210.0        # GtC/yr
RESIDENCE_TIME         = RESERVOIR_ATMOSPHERE / GROSS_FLUX  # ~4.1 years
PERTURBATION_LIFETIME  = 100.0        # years (order of magnitude — long tail)

# KEY: Residence time (~4 yr) ≠ perturbation lifetime (~100+ yr).
# A pulse of excess CO₂ takes centuries to fully equilibrate.

# ── Test cases ──────────────────────────────────────────────────────
# Atmospheric increase from emissions
TEST_ATMOS_INCREASE_GTC = TOTAL_EMISSIONS * AIRBORNE_FRACTION  # 5.175 GtC/yr
TEST_ATMOS_INCREASE_PPM = TEST_ATMOS_INCREASE_GTC / GTC_PER_PPM  # ≈ 2.44 ppm/yr

# Verify ocean is largest active reservoir
TEST_OCEAN_BIGGER_THAN_ATMOS = RESERVOIR_OCEAN > RESERVOIR_ATMOSPHERE  # True

# ── Prior errors that LLMs commonly make ────────────────────────────
PRIOR_ERRORS = {
    "ocean_is_source":              "Claims ocean emits CO₂ net — WRONG: ocean is a NET SINK absorbing ~2.5 GtC/yr",
    "atmosphere_largest":           "Claims atmosphere is the largest reservoir — WRONG: ocean (~38000 GtC) >> atmosphere (~860 GtC)",
    "residence_equals_perturbation": "Confuses ~4-yr residence time with ~100-yr perturbation lifetime — these are fundamentally different",
}
