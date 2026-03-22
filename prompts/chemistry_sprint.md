---
name: chp-chemistry-sprint
description: "10 verified chemistry experiments — equilibrium, kinetics, buffers, decay, real gas, electrochemistry, spectrophotometry, thermochemistry, stoichiometry, crystal packing."
tools: Read, Write, Edit, Bash
---

# CHP Chemistry Sprint — 10 Experiments

================================================================================
NAMING CONVENTION — READ THIS FIRST, APPLY EVERYWHERE
================================================================================

Every file in this sprint uses the chem_ prefix so any experiment is
instantly traceable back to chemistry. Never deviate from this.

DIRECTORY:   experiments/chem-[topic]/
FILES INSIDE:
  frozen/    chem_[topic]_constants.py
  impl:      chem_[topic].py
  tests/     test_chem_[topic].py
  figures/   chem_[topic]_[vizname].png
  logs:      chem_[topic]_innovation_log.md
             chem_[topic]_state_vector.md
             chem_[topic]_dead_ends.md
  report:    REPORT.md

SPRINT-LEVEL FILES:
  experiments/CHEMISTRY_SPRINT_RESULTS.md
  experiments/figures/chem_sprint_summary.png

================================================================================
ORIENTATION — READ THESE BEFORE WRITING ANY CODE
================================================================================

  experiments/euler-e/frozen/e_constants.py       (frozen spec format)
  experiments/euler-e/compute_e.py                (implementation format)
  experiments/euler-e/tests/test_euler_e.py       (test format)
  chp-test-run/experiments/schelling-segregation/REPORT.md  (report format)

Standard library only unless experiment explicitly requires scipy.
All constants from frozen spec. Never from memory.

================================================================================
STEP 0 — CREATE ALL DIRECTORIES FIRST
================================================================================

Run this before writing any file:

  for exp in chem-equilibrium chem-kinetics chem-buffers chem-radioactive-decay chem-vdw-gas chem-electrochemistry chem-spectrophotometry chem-thermochemistry chem-stoichiometry chem-crystal-packing; do
    mkdir -p experiments/$exp/frozen
    mkdir -p experiments/$exp/tests
    mkdir -p experiments/$exp/figures
  done
  mkdir -p experiments/figures
  echo "All chemistry directories created"

================================================================================
PER-EXPERIMENT TEMPLATE — APPLY TO ALL 10
================================================================================

For EACH experiment produce EXACTLY these files:

  frozen/chem_[topic]_constants.py
  chem_[topic].py
  tests/test_chem_[topic].py
  figures/chem_[topic]_[name].png
  chem_[topic]_innovation_log.md
  chem_[topic]_state_vector.md
  chem_[topic]_dead_ends.md
  REPORT.md

FULL TEST FILE TEMPLATE:

  """chem-[topic] — Sigma Gate Tests"""
  import sys, math
  from pathlib import Path
  import pytest

  sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
  from chem_[topic]_constants import *

  IMPL = Path(__file__).parent.parent / "chem_[topic].py"

  def _import_impl():
      if not IMPL.exists():
          pytest.skip("implementation not yet written")
      import importlib.util
      spec = importlib.util.spec_from_file_location("impl", IMPL)
      mod = importlib.util.module_from_spec(spec)
      spec.loader.exec_module(mod)
      return mod

  class TestPriorErrors:
      """Each test catches one known LLM prior error."""
      pass

  class TestCorrectness:
      """Each test verifies result against frozen spec."""
      pass

================================================================================
EXPERIMENT 1 — CHEMICAL EQUILIBRIUM
================================================================================

Directory: experiments/chem-equilibrium/

── frozen/chem_equilibrium_constants.py ──────────────────────────────────────

  """
  Chemical Equilibrium — Frozen Constants
  Source: NIST WebBook SRD 69, Atkins Physical Chemistry 11th Ed Appendix 2D
  DO NOT MODIFY.
  """
  import math

  R_J    = 8.314462618    # J mol-1 K-1 (NIST 2018 CODATA)
  R_ATM  = 0.082057366    # L atm mol-1 K-1

  # Haber-Bosch: N2(g) + 3H2(g) = 2NH3(g) — Source: NIST Chem WebBook
  HABER_Kp_298  = 6.77e5     # at 298.15 K
  HABER_Kp_500  = 3.55e-2    # at 500 K
  HABER_Kp_700  = 7.76e-5    # at 700 K
  HABER_dH      = -92400.0   # J/mol (exothermic)
  HABER_delta_n = -2         # 2 - (1+3) = -2

  # H2 + I2 = 2HI at 700 K — Source: Atkins PC 11e Table 7C.1
  HI_Kc_700K = 57.0          # LLM prior: 54 (698K value — wrong)
  HI_Kc_298K = 794.0

  # H2O autoionization — Source: NIST SRD 46
  Kw_298 = 1.011e-14         # LLM prior: exactly 1e-14 (too rounded)
  Kw_310 = 2.42e-14          # 37 C body temperature
  Kw_373 = 5.13e-13          # 100 C boiling point

  VAN_T_HOFF_SIGN = -1       # LLM prior: +1 (sign error)

  PRIOR_ERRORS = {
      "kp_kc_same":       "LLM treats Kp=Kc, ignores delta_n",
      "van_t_hoff_sign":  "LLM writes +(dH/R) not -(dH/R)",
      "kw_temperature":   "LLM says pH=7 at all temperatures",
      "hi_kc_value":      "LLM uses 54 (698K) not 57 (700K)",
  }

── chem_equilibrium.py ──────────────────────────────────────────────────────

  Implement:
    kp_to_kc(Kp, delta_n, T_K) -> float
    kc_to_kp(Kc, delta_n, T_K) -> float
    van_t_hoff(K1, T1_K, T2_K, dH_J) -> float
    pH_from_Kw(T_K) -> float

  All import from frozen/chem_equilibrium_constants.py

  __main__ block must print:
    Haber Kp(298K), Kc(298K), ratio showing they differ
    Haber Kp(700K) via van't Hoff vs frozen value
    pH water at 25C (~7.00), 37C (~6.81, NOT 7.0), 100C (~6.14)

── tests/test_chem_equilibrium.py ────────────────────────────────────────────

  TestPriorErrors:
    test_kp_kc_differ_when_delta_n_nonzero()
      Kc = kp_to_kc(HABER_Kp_298, HABER_delta_n, 298.15)
      assert abs(Kc - HABER_Kp_298) / HABER_Kp_298 > 0.01

    test_van_t_hoff_K_decreases_with_T_for_exothermic()
      K700 = van_t_hoff(HABER_Kp_298, 298.15, 700, HABER_dH)
      assert K700 < HABER_Kp_298

    test_pH_water_varies_with_temperature()
      assert pH_from_Kw(310) < 7.0
      assert pH_from_Kw(373) < pH_from_Kw(310)

    test_hi_kc_is_57_not_54()
      assert abs(HI_Kc_700K - 57.0) < 0.1

  TestCorrectness:
    test_kp_kc_roundtrip()
    test_van_t_hoff_matches_frozen_700K()   # within 15%
    test_pH_25C_near_7()

── figures/chem_equilibrium_kp_vs_T.png ─────────────────────────────────────

  3-panel figure, white background, figsize=(14,5), dpi=150:
  Panel 1: Kp vs Temperature log scale, van't Hoff curve, mark LLM sign error
  Panel 2: Kp vs Kc bar chart showing they differ for Haber-Bosch
  Panel 3: pH of water vs temperature 273-373K, red dashed line at pH=7

================================================================================
EXPERIMENT 2 — ARRHENIUS KINETICS
================================================================================

Directory: experiments/chem-kinetics/

── frozen/chem_kinetics_constants.py ─────────────────────────────────────────

  """
  Reaction Kinetics — Frozen Constants
  Source: Moelwyn-Hughes (1971), JPL Publication 19-5 (2019)
  DO NOT MODIFY.
  """

  R = 8.314462618           # J mol-1 K-1

  # H2 + I2 -> 2HI — Source: Moelwyn-Hughes (1971)
  H2I2_Ea   = 165000.0    # J/mol — LLM prior: 165 (kJ not J)
  H2I2_A    = 1.65e13     # s-1
  H2I2_k700 = 1.65e-3     # L mol-1 s-1 at 700K (published)

  K_RELATIVE_TOLERANCE = 0.20

  PRIOR_ERRORS = {
      "ea_in_kj":        "Uses 165 instead of 165000 — kJ not J",
      "sign_in_ea_calc": "Ea = +R*ln(k2/k1)/(1/T2-1/T1) — wrong sign",
      "second_order":    "Uses C0 - kt (zero-order) for second-order",
  }

── chem_kinetics.py ──────────────────────────────────────────────────────────

  Implement:
    arrhenius_k(A, Ea_J_per_mol, T_K) -> float
      Guard: if Ea < 1000: raise ValueError("Ea looks like kJ — must be J/mol")
    ea_from_two_temps(k1, T1, k2, T2) -> float
    half_life_first_order(k) -> float
    integrated_rate_law(C0, k, t, order) -> float  # order 0,1,2

── tests/test_chem_kinetics.py ───────────────────────────────────────────────

  TestPriorErrors:
    test_ea_units_guard()
      with pytest.raises(ValueError): arrhenius_k(H2I2_A, 165.0, 700)
    test_k_increases_with_T()
    test_ea_recovery_correct_sign()
      Ea = ea_from_two_temps(k1, 600, k2, 800)
      assert Ea > 0
    test_second_order_differs_from_zero_order()

  TestCorrectness:
    test_k700_within_tolerance()
    test_half_life_definition()

── figures/chem_kinetics_arrhenius.png ───────────────────────────────────────

  2-panel: ln(k) vs 1/T Arrhenius plot + concentration vs time 1st vs 2nd order

================================================================================
EXPERIMENT 3 — BUFFER CHEMISTRY
================================================================================

Directory: experiments/chem-buffers/

── frozen/chem_buffers_constants.py ──────────────────────────────────────────

  """
  Buffer Chemistry — Frozen Constants
  Source: CRC Handbook 103rd Ed Table 5-88, NIST SRD 46
  DO NOT MODIFY.
  """

  ACETIC_pKa       = 4.756     # LLM prior: 4.74 or 4.76
  ACETIC_Ka        = 1.754e-5
  PHOSPHATE_pKa2   = 7.198     # LLM prior: 7.2
  CARBONIC_pKa1    = 6.352     # apparent (CO2 + H2O) — LLM prior: 3.6 (true H2CO3)
  BUFFER_LN10      = 2.302585093   # must appear in buffer capacity formula

  PRIOR_ERRORS = {
      "hh_inverted":    "log([HA]/[A-]) instead of log([A-]/[HA])",
      "natural_log":    "uses ln() instead of log10()",
      "missing_ln10":   "omits 2.303 from buffer capacity",
      "true_h2co3":     "uses pKa=3.6 (true H2CO3) not 6.352 (apparent CO2)",
  }

── chem_buffers.py ────────────────────────────────────────────────────────────

  Implement:
    henderson_hasselbalch(pKa, conc_acid, conc_base) -> float
    buffer_capacity(C_total, pKa, pH) -> float   # must include BUFFER_LN10
    titration_curve(C_acid, V_acid, C_base, V_base_range, pKa) -> list
    blood_pH(pCO2_mmHg, HCO3_mM) -> float
      Uses CARBONIC_pKa1=6.352, CO2_solubility=0.0307 mM/mmHg
      Normal: pCO2=40, HCO3=24 -> pH ~7.40

── tests/test_chem_buffers.py ────────────────────────────────────────────────

  TestPriorErrors:
    test_hh_not_inverted()      # pH increases with more base
    test_hh_uses_log10()        # pH=pKa at 50/50
    test_buffer_capacity_has_ln10()
    test_blood_pH_correct_pKa() # 7.35 < blood_pH(40,24) < 7.45

  TestCorrectness:
    test_hh_equal_conc_gives_pKa()
    test_titration_curve_monotonic()

── figures/chem_buffers_titration.png ────────────────────────────────────────

  2-panel: titration curve + blood pH diagram with correct vs wrong pKa

================================================================================
EXPERIMENT 4 — RADIOACTIVE DECAY
================================================================================

Directory: experiments/chem-radioactive-decay/
Files use: chem_radioactive_decay_* naming

── frozen/chem_radioactive_decay_constants.py ─────────────────────────────────

  """
  Radioactive Decay — Frozen Constants
  Source: NNDC BNL Nuclear Data Center (ENSDF database)
  DO NOT MODIFY.
  """
  import math
  LN2 = math.log(2)

  U238_HALF_LIFE  = 4.468e9    # years
  TH234_HALF_LIFE = 0.06617    # years = 24.10 days
  RA226_HALF_LIFE = 1600.0     # years (exact as published)

  C14_HALF_LIFE       = 5730.0   # years (Godwin 1962 — modern standard)
  C14_LIBBY_WRONG     = 5568.0   # years (outdated — DO NOT USE)

  PRIOR_ERRORS = {
      "libby_half_life":  "Uses 5568 (Libby, outdated) not 5730 (Godwin)",
      "secular_eq_atoms": "Says N1=N2 at secular equilibrium (wrong — A1=A2)",
  }

── chem_radioactive_decay.py ─────────────────────────────────────────────────

  Implement:
    decay_constant(half_life) -> float
    n_remaining(N0, half_life, t) -> float
    activity(N, half_life) -> float
    age_from_ratio(ratio, half_life) -> float
    c14_age(fraction_remaining) -> float   # uses C14_HALF_LIFE=5730
    secular_eq_ratio(lam1, lam2) -> float  # N2/N1 = lam1/lam2

── tests/test_chem_radioactive_decay.py ────────────────────────────────────────

  TestPriorErrors:
    test_c14_uses_5730_not_5568()
      age = c14_age(0.5)
      assert abs(age - 5730) < 10
      assert abs(age - C14_LIBBY_WRONG) > 100
    test_secular_eq_not_equal_atoms()
      ratio = secular_eq_ratio(lam1, lam2)
      assert ratio < 1e-6
      assert ratio != 1.0

  TestCorrectness:
    test_half_life_gives_half()
    test_ra226_exactly_1600()

── figures/chem_radioactive_decay_curves.png ─────────────────────────────────

  2-panel: C-14 decay curve marking 5730 vs 5568 + secular equilibrium bar chart

================================================================================
EXPERIMENT 5 — VAN DER WAALS REAL GAS
================================================================================

Directory: experiments/chem-vdw-gas/
Files use: chem_vdw_gas_* naming

── frozen/chem_vdw_gas_constants.py ──────────────────────────────────────────

  """
  Van der Waals — Frozen Constants
  Source: Atkins PC 11e Table 1C.3
  DO NOT MODIFY.
  """

  R_ATM = 0.082057366    # L atm mol-1 K-1

  VDW = {
      "H2":  {"a": 0.2476, "b": 0.02661},
      "N2":  {"a": 1.370,  "b": 0.03870},
      "CO2": {"a": 3.640,  "b": 0.04267},
      "H2O": {"a": 5.536,  "b": 0.03049},
      "NH3": {"a": 4.225,  "b": 0.03707},
  }

  PRIOR_ERRORS = {
      "ideal_always":     "Uses PV=nRT for CO2 at high pressure",
      "wrong_Tc_formula": "Tc = a/(Rb) not 8a/(27Rb)",
      "wrong_Pc_formula": "Pc = a/b^2 not a/(27b^2)",
      "missing_n2_term":  "Writes a/V^2 not n^2*a/V^2",
  }

── chem_vdw_gas.py ───────────────────────────────────────────────────────────

  Implement:
    ideal_gas_P(n, V_L, T_K) -> float
    vdw_P(n, V_L, T_K, gas) -> float   # n**2 * a / V**2 — critical
    compression_factor(P, V, n, T) -> float
    critical_temperature(gas) -> float  # 8a/(27Rb)
    critical_pressure(gas) -> float     # a/(27b^2)

── tests/test_chem_vdw_gas.py ────────────────────────────────────────────────

  TestPriorErrors:
    test_co2_vdw_differs_from_ideal()
      deviation = abs(ideal - vdw) / ideal
      assert deviation > 0.05
    test_critical_T_has_8_over_27()
      Tc = critical_temperature("CO2")
      assert abs(Tc - 304.2) < 5
    test_n_squared_in_attraction()
      dP_n1 and dP_n2 should scale as n^2

  TestCorrectness:
    test_h2_nearly_ideal()
    test_compression_factor_ideal()

── figures/chem_vdw_gas_deviation.png ────────────────────────────────────────

  2-panel: Z vs P for CO2/N2/H2 + VdW vs ideal pressure vs volume

================================================================================
EXPERIMENT 6 — ELECTROCHEMISTRY
================================================================================

Directory: experiments/chem-electrochemistry/

── frozen/chem_electrochemistry_constants.py ─────────────────────────────────

  """
  Electrochemistry — Frozen Constants
  Source: NIST SRD 20, Atkins PC 11e Appendix 2B
  DO NOT MODIFY.
  """

  F    = 96485.33212    # C mol-1 (CODATA 2018)
  R    = 8.314462618
  T298 = 298.15

  E0 = {
      "F2/F-":       +2.866,
      "Cl2/Cl-":     +1.358,
      "O2/H2O":      +1.229,
      "Cu2+/Cu":     +0.3419,
      "H+/H2":        0.0000,   # SHE — exactly zero by definition
      "Fe2+/Fe":     -0.4402,
      "Zn2+/Zn":     -0.7618,
      "Al3+/Al":     -1.676,
      "Li+/Li":      -3.0401,
  }

  RT_F_298 = R * T298 / F    # 0.025693 V

  PRIOR_ERRORS = {
      "nernst_sign":   "E = E0 + (RT/nF)*ln(Q) — should be MINUS",
      "cell_reversed": "E = E_anode - E_cathode — should be cathode minus anode",
      "deltaG_sign":   "deltaG = +nFE0 — should be MINUS",
  }

── chem_electrochemistry.py ──────────────────────────────────────────────────

  Implement:
    cell_potential(cathode, anode) -> float   # E0_cathode - E0_anode
    nernst(E0_cell, n, Q, T_K=298.15) -> float   # E0 - (RT/nF)*ln(Q)
    eq_constant_from_E0(E0, n, T_K=298.15) -> float
    delta_G(E0, n) -> float   # -n*F*E0

── tests/test_chem_electrochemistry.py ────────────────────────────────────────

  TestPriorErrors:
    test_nernst_Q_gt_1_decreases_E()
    test_nernst_Q_lt_1_increases_E()
    test_delta_G_negative_spontaneous()
    test_cell_cathode_minus_anode()

  TestCorrectness:
    test_daniell_cell()   # abs(E - 1.1037) < 0.001
    test_nernst_Q1_is_E0()
    test_SHE_is_zero()

── figures/chem_electrochemistry_nernst.png ──────────────────────────────────

  2-panel: Nernst E vs log(Q) + standard reduction potential chart

================================================================================
EXPERIMENT 7 — BEER-LAMBERT SPECTROPHOTOMETRY
================================================================================

Directory: experiments/chem-spectrophotometry/

── frozen/chem_spectrophotometry_constants.py ─────────────────────────────────

  """
  Beer-Lambert — Frozen Constants
  Source: NIST Chemistry WebBook, Sigma-Aldrich spectral library
  DO NOT MODIFY.
  """

  EPSILON = {
      "KMnO4_525":   2360,     # L mol-1 cm-1
      "CuSO4_800":   12.0,
      "NADH_340":    6220,
  }

  DNA_A260_FACTORS = {
      "dsDNA": 50.0,   # ug/mL per A260
      "RNA":   40.0,   # LLM prior for dsDNA
      "ssDNA": 33.0,
  }

  BEER_LAMBERT_BASE = "log10"   # NOT ln — frozen

  PRIOR_ERRORS = {
      "uses_ln":        "A = -ln(T) not -log10(T) — off by 2.303x",
      "sign_error":     "A = log10(T) not -log10(T)",
      "no_path_length": "Ignores l in A=epsilon*c*l",
      "dna_rna_factor": "Uses 40 ug/mL (RNA) for dsDNA (should be 50)",
  }

── chem_spectrophotometry.py ─────────────────────────────────────────────────

  Implement:
    absorbance_from_T(T_fractional) -> float   # -log10(T) NOT -ln(T)
    T_from_absorbance(A) -> float
    concentration(A, epsilon, path_cm) -> float
    absorbance(c, epsilon, path_cm) -> float
    dna_conc(A260, molecule_type="dsDNA") -> float
    percent_T_to_A(percent_T) -> float   # A = 2 - log10(%T)

── tests/test_chem_spectrophotometry.py ───────────────────────────────────────

  TestPriorErrors:
    test_uses_log10_not_ln()
      assert abs(absorbance_from_T(0.01) - 2.0) < 0.001
    test_sign_correct()
    test_path_length_doubles_absorbance()
    test_dna_not_rna_factor()
      assert dna_conc(1.0, "dsDNA") == 50.0

  TestCorrectness:
    test_T1_gives_A0()
    test_roundtrip()
    test_percent_T_conversion()

── figures/chem_spectrophotometry_beer_lambert.png ───────────────────────────

  2-panel: A vs concentration at different path lengths + log10 vs ln comparison

================================================================================
EXPERIMENT 8 — THERMOCHEMISTRY
================================================================================

Directory: experiments/chem-thermochemistry/

── frozen/chem_thermochemistry_constants.py ──────────────────────────────────

  """
  Thermochemistry — Frozen Constants
  Source: NIST WebBook, Atkins PC 11e Appendix 2A (kJ/mol at 298.15K, 1 bar)
  DO NOT MODIFY.
  """

  DHF = {
      "H2(g)":       0.0,
      "O2(g)":       0.0,
      "C(graphite)": 0.0,
      "H2O(l)":    -285.830,
      "H2O(g)":    -241.826,    # LLM uses -285 for gas — WRONG
      "CO2(g)":    -393.509,
      "CO(g)":     -110.527,
      "CH4(g)":     -74.87,
      "C2H4(g)":    +52.47,     # POSITIVE — LLM often gives negative
      "NO(g)":      +90.29,     # POSITIVE — LLM often gives negative
      "NO2(g)":     +33.20,
      "SO2(g)":    -296.83,
      "NH3(g)":     -45.90,
  }

  BOND_ENTHALPY = {
      "C-H": 414, "C-C": 347, "C=C": 614,
      "O-H": 463, "O=O": 498,
      "N#N": 945, "H-H": 436, "H-Cl": 432,
  }

  PRIOR_ERRORS = {
      "h2o_gas_liquid": "Uses H2O(l) dHf=-285 for H2O(g)",
      "c2h4_sign":      "Gives negative dHf for C2H4(g) — should be +52.47",
      "no_sign":        "Gives negative dHf for NO(g) — should be +90.29",
      "hess_reversed":  "Uses reactants - products not products - reactants",
      "bond_direction": "Bond formation absorbs energy (wrong)",
  }

── chem_thermochemistry.py ───────────────────────────────────────────────────

  Implement:
    hess_law(products, reactants) -> float
      products/reactants: list of (species, stoich_coeff)
      returns sum(n*DHF[p]) - sum(n*DHF[r])   # products MINUS reactants
    bond_enthalpy_dH(bonds_broken, bonds_formed) -> float
      returns sum(broken) - sum(formed)

── tests/test_chem_thermochemistry.py ────────────────────────────────────────

  TestPriorErrors:
    test_hess_products_minus_reactants()
    test_c2h4_positive()   assert DHF["C2H4(g)"] > 0
    test_no_positive()     assert DHF["NO(g)"] > 0
    test_h2o_gas_not_liquid()
    test_bond_breaking_endothermic()

  TestCorrectness:
    test_water_formation()   # dH = -285.830 kJ/mol
    test_methane_combustion()   # -950 < dH < -830

── figures/chem_thermochemistry_formation.png ────────────────────────────────

  2-panel: dHf bar chart (positive values highlighted) + Hess's law diagram

================================================================================
EXPERIMENT 9 — STOICHIOMETRY
================================================================================

Directory: experiments/chem-stoichiometry/

── frozen/chem_stoichiometry_constants.py ─────────────────────────────────────

  """
  Stoichiometry — Frozen Atomic Weights
  Source: IUPAC 2021 Table of Standard Atomic Weights
  Pure and Applied Chemistry Vol 93 No 6 2021
  DO NOT MODIFY.
  """

  AW = {
      "H":  1.008,   "C":  12.011,  "N":  14.007,
      "O":  15.999,  "F":  18.998,  "Na": 22.990,
      "Mg": 24.305,  "Al": 26.982,  "Si": 28.085,
      "P":  30.974,  "S":  32.06,   "Cl": 35.45,
      "K":  39.098,  "Ca": 40.078,  "Fe": 55.845,
      "Cu": 63.546,  "Zn": 65.38,   "Ag": 107.87,
      "I":  126.90,  "Au": 196.97,  "Pb": 207.2,
  }

  AVOGADRO = 6.02214076e23   # mol-1 (CODATA 2018)

  PRIOR_ERRORS = {
      "integer_masses":        "H=1, C=12, N=14, O=16 — loses precision",
      "avogadro_3sf":          "6.022e23 — drops 5 significant figures",
      "no_limiting_reagent":   "Uses all of each reagent without finding limit",
  }

── chem_stoichiometry.py ─────────────────────────────────────────────────────

  Implement:
    parse_formula(formula) -> dict   # "H2O" -> {"H":2,"O":1}
    molecular_weight(formula) -> float
    moles(mass_g, formula) -> float
    grams(moles, formula) -> float
    limiting_reagent(reagents) -> tuple(str, float)
      reagents: {formula: {"grams": x, "stoich": n}}
    percent_yield(actual_g, theoretical_g) -> float

── tests/test_chem_stoichiometry.py ──────────────────────────────────────────

  TestPriorErrors:
    test_water_not_integer_mw()
      assert abs(molecular_weight("H2O") - 18.015) < 0.001
      assert molecular_weight("H2O") != 18.0
    test_glucose_mw()
      assert abs(molecular_weight("C6H12O6") - 180.156) < 0.01
    test_limiting_reagent_found()

  TestCorrectness:
    test_formula_parsing()
    test_moles_roundtrip()
    test_aspirin_MW()   # abs(MW("C9H8O4") - 180.157) < 0.01

── figures/chem_stoichiometry_mw_comparison.png ──────────────────────────────

  2-panel: IUPAC vs integer MW scatter + limiting reagent diagram

================================================================================
EXPERIMENT 10 — CRYSTAL PACKING
================================================================================

Directory: experiments/chem-crystal-packing/
Files use: chem_crystal_packing_* naming

── frozen/chem_crystal_packing_constants.py ──────────────────────────────────

  """
  Crystal Packing — Frozen Constants
  Source: Ashcroft & Mermin Solid State Physics (1976), CRC Handbook 103rd Ed
  Packing efficiencies are exact mathematical results.
  DO NOT MODIFY.
  """
  import math

  PACKING = {
      "SC":      math.pi / 6,
      "BCC":     math.pi * math.sqrt(3) / 8,
      "FCC":     math.pi / (3*math.sqrt(2)),   # = 0.7405 — maximum possible
      "HCP":     math.pi / (3*math.sqrt(2)),
      "diamond": math.pi * math.sqrt(3) / 16,
  }

  ATOMS_PER_CELL = {"SC": 1, "BCC": 2, "FCC": 4, "diamond": 8}
  # LLM prior for FCC: says 8 (counts corners only, forgets face atoms)

  COORD_NUMBER = {"SC": 6, "BCC": 8, "FCC": 12, "diamond": 4}

  RADIUS = {"Cu": 128, "Al": 143, "Fe": 126, "Na": 186}  # pm
  STRUCTURE = {"Cu": "FCC", "Al": "FCC", "Fe": "BCC", "Na": "BCC"}

  AVOGADRO = 6.02214076e23

  PRIOR_ERRORS = {
      "fcc_8_atoms":   "Says FCC has 8 atoms — forgets face-center (4 atoms)",
      "formula_swap":  "Uses FCC formula for BCC or vice versa",
      "kepler_unknown":"Doesn't know FCC = maximum possible packing",
  }

── chem_crystal_packing.py ────────────────────────────────────────────────────

  Implement:
    packing_efficiency(structure) -> float
    atoms_per_cell(structure) -> int
    unit_cell_edge(element) -> float   # pm
      FCC: a = 2*sqrt(2)*r
      BCC: a = 4*r/sqrt(3)
    density(element, molar_mass) -> float   # g/cm3

── tests/test_chem_crystal_packing.py ─────────────────────────────────────────

  TestPriorErrors:
    test_fcc_4_atoms_not_8()
      assert atoms_per_cell("FCC") == 4
    test_fcc_beats_bcc()
    test_fcc_is_maximum()
      for s in ["SC","BCC","diamond"]:
          assert packing_efficiency(s) < packing_efficiency("FCC")
    test_fcc_packing_exact()

  TestCorrectness:
    test_bcc_packing_exact()   # abs(val - 0.6802) < 0.0001
    test_copper_density()      # abs(rho - 8.96) < 0.5

── figures/chem_crystal_packing_structures.png ────────────────────────────────

  2-panel: packing efficiency bar chart + atoms per unit cell breakdown

================================================================================
AFTER ALL 10 — MASTER FIGURE AND RESULTS
================================================================================

Write and run: experiments/chem_sprint_summary.py

Output: experiments/figures/chem_sprint_summary.png
figsize=(20,10), dpi=150, white background, 2x5 grid
One mini-panel per experiment with key visualization + red LLM prior annotation

Write: experiments/CHEMISTRY_SPRINT_RESULTS.md

  # CHP Chemistry Sprint — Results
  Generated: [date]
  Sprint tag: chemistry-sprint-2026

  | # | Experiment | Key Result | LLM Prior Errors | FPs |
  |---|-----------|-----------|-----------------|-----|
  | 1 | chem-equilibrium | Kp/Kc differ by (RT)^2 | Kp=Kc, sign | 2 |
  | 2 | chem-kinetics | Ea in J not kJ | units, sign | 2 |
  | 3 | chem-buffers | Blood pH 7.40 correct | inverted, ln | 3 |
  | 4 | chem-radioactive-decay | 5730 not 5568 yr | Libby, secular | 2 |
  | 5 | chem-vdw-gas | CO2 deviates 5%+ | n^2 missing | 2 |
  | 6 | chem-electrochemistry | Daniell E=1.1037V | sign, cathode | 2 |
  | 7 | chem-spectrophotometry | log10 not ln | ln, DNA | 2 |
  | 8 | chem-thermochemistry | C2H4/NO dHf positive | sign | 3 |
  | 9 | chem-stoichiometry | H2O=18.015 not 18 | integer MW | 1 |
  |10 | chem-crystal-packing | FCC=4 atoms, 74.05% | 8 atoms | 2 |

  Total false positives: [N]
  All verified: NIST, IUPAC 2021, CODATA 2018, Atkins PC 11e, CRC 103rd Ed

================================================================================
UPDATE EXPERIMENT INDEX
================================================================================

After all 10 complete, read EXPERIMENT_INDEX.json and add entries for all 10.

Each entry needs these fields plus:
  "sprint":        "chemistry-sprint-2026",
  "domain_group":  "chemistry",

Validate:
  python -c "import json; d=json.load(open('EXPERIMENT_INDEX.json')); print(d['summary']['total'], 'experiments')"

================================================================================
RUN ALL TESTS
================================================================================

  python -m pytest experiments/chem-equilibrium/tests/ \
                   experiments/chem-kinetics/tests/ \
                   experiments/chem-buffers/tests/ \
                   experiments/chem-radioactive-decay/tests/ \
                   experiments/chem-vdw-gas/tests/ \
                   experiments/chem-electrochemistry/tests/ \
                   experiments/chem-spectrophotometry/tests/ \
                   experiments/chem-thermochemistry/tests/ \
                   experiments/chem-stoichiometry/tests/ \
                   experiments/chem-crystal-packing/tests/ \
                   -v --tb=short

All must pass before generating summary figure.

================================================================================
SELF-CHECK
================================================================================

  [ ] 10 x frozen/chem_[topic]_constants.py written
  [ ] 10 x chem_[topic].py written and runnable
  [ ] 10 x tests/test_chem_[topic].py written and passing
  [ ] 10 x REPORT.md written
  [ ] 10 x figures/chem_[topic]_*.png generated
  [ ] 10 x innovation_log, state_vector, dead_ends written
  [ ] experiments/figures/chem_sprint_summary.png generated
  [ ] experiments/CHEMISTRY_SPRINT_RESULTS.md written
  [ ] EXPERIMENT_INDEX.json updated

Verify linkage:
  grep -r "chemistry-sprint-2026" EXPERIMENT_INDEX.json | wc -l
  Expected: 10

================================================================================
DONE
================================================================================

Print when complete:

  "CHP Chemistry Sprint complete.
   10 experiments. All tests passing. All verified against NIST/IUPAC.
   Sprint tag: chemistry-sprint-2026
   See experiments/CHEMISTRY_SPRINT_RESULTS.md"
