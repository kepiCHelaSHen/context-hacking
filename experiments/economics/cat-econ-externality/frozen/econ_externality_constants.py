"""Externalities — Frozen Constants. Source: Mankiw Principles 9th Ed Ch 10, Stiglitz. DO NOT MODIFY."""

# Negative externality: MSC = MPC + MEC (marginal social > marginal private)
# Market equilibrium: MPC = MB (ignores external cost)
# Social optimum: MSC = MB (includes external cost)
# Pigouvian tax = MEC at social optimum (internalizes externality)
# Market OVERPRODUCES with negative externality (Q_mkt > Q_soc)

# LLM prior: claims MSC = MPC (ignores MEC entirely), or evaluates tax at market Q

# Test curves (linear):
#   MPC = a_mpc + b_mpc * Q  = 2 + 0.5Q  (private marginal cost)
#   MEC = b_mec * Q          = 0.1Q       (marginal external cost)
#   MB  = a_mb - b_mb * Q    = 20 - Q     (marginal benefit / demand)
A_MPC = 2.0
B_MPC = 0.5
B_MEC = 0.1
A_MB  = 20.0
B_MB  = 1.0

# MSC = MPC + MEC = 2 + 0.5Q + 0.1Q = 2 + 0.6Q
B_MSC = B_MPC + B_MEC  # 0.6

# Market equilibrium: MPC = MB → 2 + 0.5Q = 20 - Q → 1.5Q = 18
Q_MKT = 18.0 / (B_MPC + B_MB)    # 12.0
P_MKT = A_MB - B_MB * Q_MKT       # 8.0

# Social optimum: MSC = MB → 2 + 0.6Q = 20 - Q → 1.6Q = 18
Q_SOC = 18.0 / (B_MSC + B_MB)    # 11.25
P_SOC = A_MB - B_MB * Q_SOC       # 8.75

# Pigouvian tax = MEC at social optimum (NOT at market equilibrium)
TAX_PIGOUVIAN = B_MEC * Q_SOC    # 0.1 * 11.25 = 1.125

# Deadweight loss from market overproduction
# DWL = 0.5 * (Q_mkt - Q_soc) * (MSC(Q_mkt) - MB(Q_mkt))
MSC_AT_MKT = A_MPC + B_MSC * Q_MKT  # 2 + 0.6*12 = 9.2
MB_AT_MKT  = A_MB - B_MB * Q_MKT     # 20 - 12 = 8.0
DWL = 0.5 * (Q_MKT - Q_SOC) * (MSC_AT_MKT - MB_AT_MKT)  # 0.5 * 0.75 * 1.2 = 0.45

PRIOR_ERRORS = {
    "msc_equals_mpc":        "Ignores MEC — claims MSC = MPC (should be MSC = MPC + MEC)",
    "underproduction":       "Claims market underproduces with negative externality (it OVERproduces)",
    "tax_equals_mec_at_market": "Evaluates Pigouvian tax as MEC at market Q instead of social Q",
}
