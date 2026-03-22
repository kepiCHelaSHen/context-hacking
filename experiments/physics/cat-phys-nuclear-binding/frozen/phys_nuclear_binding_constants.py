"""
Nuclear Binding Energy — Frozen Constants
Source: CODATA 2018, Krane Nuclear Physics 3rd Ed, AME2020
DO NOT MODIFY.
"""

# Masses (atomic mass units, u)
M_PROTON_U  = 1.007276466621   # u (CODATA 2018)
M_NEUTRON_U = 1.00866491595    # u
M_ELECTRON_U = 5.48579909065e-4  # u

# 1 u = 931.494 MeV/c²
U_TO_MEV = 931.49410242       # MeV/c² per u

# Selected nuclear masses (AME2020, atomic masses in u)
ATOMIC_MASS = {
    "H1":   1.00782503207,
    "He4":  4.00260325413,    # alpha particle
    "C12": 12.00000000000,    # defined as exactly 12
    "Fe56": 55.9349375,       # peak binding energy per nucleon
    "U238": 238.0507882,
}

# Binding energy: B = [Z·m_H + N·m_n - M_atom] · c²
# Fe-56: Z=26, N=30
BE_FE56 = (26 * ATOMIC_MASS["H1"] + 30 * M_NEUTRON_U - ATOMIC_MASS["Fe56"]) * U_TO_MEV
# ≈ 492.3 MeV
BE_PER_NUCLEON_FE56 = BE_FE56 / 56  # ≈ 8.79 MeV/nucleon (near peak)

# He-4: Z=2, N=2
BE_HE4 = (2 * ATOMIC_MASS["H1"] + 2 * M_NEUTRON_U - ATOMIC_MASS["He4"]) * U_TO_MEV
BE_PER_NUCLEON_HE4 = BE_HE4 / 4  # ≈ 7.07 MeV/nucleon

PRIOR_ERRORS = {
    "mass_defect_dir":     "Subtracts nuclear mass FROM constituents (reversed)",
    "atomic_vs_nuclear":   "Uses nuclear mass when atomic mass needed (or vice versa)",
    "fe56_peak":           "Claims Fe-56 has highest TOTAL BE (it's per nucleon that peaks)",
    "u_to_mev_rounded":    "Uses 931 or 931.5 instead of 931.494 MeV/u",
}
