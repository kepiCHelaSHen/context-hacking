# CHP Chemistry Sprint — Results
Generated: 2026-03-22
Sprint tag: chemistry-sprint-2026

| # | Experiment | Key Result | LLM Prior Errors | FPs |
|---|-----------|-----------|-----------------|-----|
| 1 | chem-equilibrium | Kp/Kc differ by (RT)^Δn | Kp=Kc, sign | 2 |
| 2 | chem-kinetics | Ea in J not kJ | units, sign | 2 |
| 3 | chem-buffers | Blood pH 7.40 correct | inverted, ln | 3 |
| 4 | chem-radioactive-decay | 5730 not 5568 yr | Libby, secular | 2 |
| 5 | chem-vdw-gas | CO2 deviates 5%+ | n² missing | 2 |
| 6 | chem-electrochemistry | Daniell E=1.1037V | sign, cathode | 2 |
| 7 | chem-spectrophotometry | log10 not ln | ln, DNA | 2 |
| 8 | chem-thermochemistry | C2H4/NO dHf positive | sign | 3 |
| 9 | chem-stoichiometry | H2O=18.015 not 18 | integer MW | 1 |
|10 | chem-crystal-packing | FCC=4 atoms, 74.05% | 8 atoms | 2 |

Total false positives caught: 21
Total tests: 61 passing, 0 failing
All verified: NIST, IUPAC 2021, CODATA 2018, Atkins PC 11e, CRC 103rd Ed

## Per-Experiment Detail

### 1. Chemical Equilibrium
- **Functions**: kp_to_kc, kc_to_kp, van_t_hoff, pH_from_Kw
- **Key insight**: Kp ≠ Kc when Δn ≠ 0; pH of water varies with temperature
- **Tests**: 7 (4 prior error + 3 correctness)

### 2. Arrhenius Kinetics
- **Functions**: arrhenius_k (with Ea guard), ea_from_two_temps, half_life_first_order, integrated_rate_law
- **Key insight**: Ea must be in J/mol not kJ; rate law differs by order
- **Tests**: 6 (4 prior error + 2 correctness)

### 3. Buffer Chemistry
- **Functions**: henderson_hasselbalch, buffer_capacity, titration_curve, blood_pH
- **Key insight**: pH = pKa + log₁₀([A⁻]/[HA]) NOT inverted; blood uses clinical pKa=6.1
- **Tests**: 6 (4 prior error + 2 correctness)

### 4. Radioactive Decay
- **Functions**: decay_constant, n_remaining, activity, age_from_ratio, c14_age, secular_eq_ratio
- **Key insight**: C-14 uses 5730 yr (Godwin) not 5568 (Libby); secular eq: A₁=A₂ not N₁=N₂
- **Tests**: 4 (2 prior error + 2 correctness)

### 5. Van der Waals Gas
- **Functions**: ideal_gas_P, vdw_P, compression_factor, critical_temperature, critical_pressure
- **Key insight**: n² in attraction term; Tc = 8a/(27Rb); CO₂ deviates significantly from ideal
- **Tests**: 5 (3 prior error + 2 correctness)

### 6. Electrochemistry
- **Functions**: cell_potential, nernst, eq_constant_from_E0, delta_G
- **Key insight**: E = E⁰ - (RT/nF)·ln(Q) MINUS sign; ΔG = -nFE⁰
- **Tests**: 7 (4 prior error + 3 correctness)

### 7. Beer-Lambert Spectrophotometry
- **Functions**: absorbance_from_T, T_from_absorbance, concentration, absorbance, dna_conc, percent_T_to_A
- **Key insight**: A = -log₁₀(T) not -ln(T); dsDNA factor = 50 not 40
- **Tests**: 7 (4 prior error + 3 correctness)

### 8. Thermochemistry
- **Functions**: hess_law, bond_enthalpy_dH
- **Key insight**: Products minus reactants; C₂H₄ and NO have positive ΔHf
- **Tests**: 7 (5 prior error + 2 correctness)

### 9. Stoichiometry
- **Functions**: parse_formula, molecular_weight, moles, grams, limiting_reagent, percent_yield
- **Key insight**: IUPAC 2021 atomic weights, not integers; H₂O = 18.015 not 18
- **Tests**: 6 (3 prior error + 3 correctness)

### 10. Crystal Packing
- **Functions**: packing_efficiency, atoms_per_cell, unit_cell_edge, density
- **Key insight**: FCC = 4 atoms (not 8); FCC = maximum packing (74.05%)
- **Tests**: 6 (4 prior error + 2 correctness)
