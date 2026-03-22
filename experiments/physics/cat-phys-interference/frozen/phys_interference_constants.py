"""Thin Film Interference — Frozen Constants. Source: Hecht Optics 5th Ed. DO NOT MODIFY."""
import math
# Thin film: path difference = 2nt (at normal incidence)
# Phase change of π at reflection from higher-n surface
# Constructive: 2nt = (m+½)λ when ONE phase change (most common case)
# Destructive: 2nt = mλ when ONE phase change
# LLM prior: forgets the phase change at reflection
# Test: oil film (n=1.40) on water (n=1.33), thickness=300nm
# Light reflects from air→oil (phase change) and oil→water (no change, n_oil > n_water)
# One phase change: constructive when 2nt = (m+½)λ
N_OIL = 1.40
N_WATER = 1.333
N_GLASS = 1.52
T_FILM = 300e-9  # m
# For m=0: λ = 2nt/(m+½) = 2(1.40)(300e-9)/0.5 = 1680nm (IR, not visible)
# For m=1: λ = 2(1.40)(300e-9)/1.5 = 560nm (green — visible!)
LAMBDA_CONSTRUCTIVE_M1 = 2 * N_OIL * T_FILM / 1.5  # = 560 nm
# Newton's rings, anti-reflection coatings
PRIOR_ERRORS = {
    "no_phase_change":   "Forgets π phase change at higher-n reflection",
    "wrong_constructive":"Uses 2nt=mλ for constructive (that's destructive with 1 phase change)",
    "both_surfaces":     "Counts phase change at both surfaces (only higher-n reflection)",
}
