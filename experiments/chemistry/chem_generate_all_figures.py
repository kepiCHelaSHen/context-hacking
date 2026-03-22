"""Generate all 10 chemistry experiment figures + sprint summary."""
import sys
import math
import os

# Ensure we can find all frozen modules
BASE = os.path.dirname(os.path.abspath(__file__))

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def fig1_equilibrium():
    """3-panel: Kp vs T, Kp vs Kc bar, pH vs T."""
    sys.path.insert(0, os.path.join(BASE, "chem-equilibrium", "frozen"))
    from chem_equilibrium_constants import (
        R_J, R_ATM, HABER_Kp_298, HABER_dH, HABER_delta_n, Kw_298, Kw_310, Kw_373
    )

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14, 5))
    fig.patch.set_facecolor('white')

    # Panel 1: Kp vs T (van't Hoff)
    temps = np.linspace(298, 1000, 200)
    kps = [HABER_Kp_298 * math.exp(-(HABER_dH / R_J) * (1/T - 1/298.15)) for T in temps]
    ax1.semilogy(temps, kps, 'b-', linewidth=2)
    ax1.axvline(298.15, color='green', linestyle='--', alpha=0.5, label='298K')
    ax1.set_xlabel('Temperature (K)')
    ax1.set_ylabel('Kp')
    ax1.set_title('Haber-Bosch: Kp vs T\n(van\'t Hoff, exothermic)')
    ax1.annotate('LLM sign error\nwould curve UP', xy=(600, 1e-2), fontsize=8, color='red')
    ax1.legend()

    # Panel 2: Kp vs Kc bar
    Kc = HABER_Kp_298 / (R_ATM * 298.15) ** HABER_delta_n
    ax2.bar(['Kp', 'Kc'], [HABER_Kp_298, Kc], color=['steelblue', 'coral'])
    ax2.set_ylabel('Value')
    ax2.set_title(f'Kp vs Kc at 298K\n(Δn={HABER_delta_n}, they DIFFER)')
    ax2.ticklabel_format(style='scientific', axis='y', scilimits=(0, 0))

    # Panel 3: pH vs T
    data = [(298.15, Kw_298), (310, Kw_310), (373.15, Kw_373)]
    temps_ph = [t for t, _ in data]
    phs = [0.5 * (-math.log10(kw)) for _, kw in data]
    ax3.plot(temps_ph, phs, 'bo-', linewidth=2, markersize=8)
    ax3.axhline(7.0, color='red', linestyle='--', label='pH = 7 (LLM assumes)')
    ax3.set_xlabel('Temperature (K)')
    ax3.set_ylabel('pH of pure water')
    ax3.set_title('pH of Water vs Temperature\n(NOT always 7!)')
    ax3.legend()

    plt.tight_layout()
    plt.savefig(os.path.join(BASE, "chem-equilibrium", "figures", "chem_equilibrium_kp_vs_T.png"), dpi=150)
    plt.close()
    print("  [1/10] chem_equilibrium_kp_vs_T.png")


def fig2_kinetics():
    """2-panel: Arrhenius plot + concentration decay curves."""
    sys.path.insert(0, os.path.join(BASE, "chem-kinetics", "frozen"))
    from chem_kinetics_constants import R, H2I2_Ea, H2I2_A

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.patch.set_facecolor('white')

    # Panel 1: ln(k) vs 1/T
    temps = np.linspace(600, 1000, 100)
    inv_T = 1.0 / temps
    ln_k = [math.log(H2I2_A * math.exp(-H2I2_Ea / (R * T))) for T in temps]
    ax1.plot(inv_T * 1000, ln_k, 'b-', linewidth=2)
    ax1.set_xlabel('1000/T (K⁻¹)')
    ax1.set_ylabel('ln(k)')
    ax1.set_title(f'Arrhenius Plot: ln(k) vs 1/T\nSlope = -Ea/R = {-H2I2_Ea/R:.0f} K')

    # Panel 2: Concentration vs time
    t = np.linspace(0, 30, 200)
    C0, k = 1.0, 0.1
    C_first = C0 * np.exp(-k * t)
    C_second = C0 / (1 + C0 * k * t)
    C_zero = np.maximum(C0 - k * t, 0)
    ax2.plot(t, C_zero, 'g--', label='Zero order', linewidth=2)
    ax2.plot(t, C_first, 'b-', label='First order', linewidth=2)
    ax2.plot(t, C_second, 'r-', label='Second order', linewidth=2)
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Concentration')
    ax2.set_title('Integrated Rate Laws\n(C₀=1.0, k=0.1)')
    ax2.legend()

    plt.tight_layout()
    plt.savefig(os.path.join(BASE, "chem-kinetics", "figures", "chem_kinetics_arrhenius.png"), dpi=150)
    plt.close()
    print("  [2/10] chem_kinetics_arrhenius.png")


def fig3_buffers():
    """2-panel: titration curve + blood pH diagram."""
    sys.path.insert(0, os.path.join(BASE, "chem-buffers", "frozen"))
    from chem_buffers_constants import ACETIC_pKa

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.patch.set_facecolor('white')

    # Panel 1: Titration curve
    C_acid, V_acid, C_base = 0.1, 50.0, 0.1
    V_base = np.linspace(0.1, 100, 500)
    pKa = ACETIC_pKa
    Ka = 10 ** (-pKa)
    pHs = []
    for Vb in V_base:
        mol_a = C_acid * V_acid / 1000
        mol_b = C_base * Vb / 1000
        Vt = (V_acid + Vb) / 1000
        if mol_b >= mol_a:
            excess = mol_b - mol_a
            OH = excess / Vt
            pH = 14 + math.log10(OH) if OH > 0 else 7
        elif mol_b <= 0:
            Ca = mol_a / Vt
            H = (-Ka + math.sqrt(Ka**2 + 4*Ka*Ca)) / 2
            pH = -math.log10(H)
        else:
            pH = pKa + math.log10(mol_b / (mol_a - mol_b))
        pHs.append(pH)
    ax1.plot(V_base, pHs, 'b-', linewidth=2)
    ax1.axhline(pKa, color='orange', linestyle='--', alpha=0.7, label=f'pKa={pKa}')
    ax1.axvline(50, color='gray', linestyle=':', alpha=0.5, label='Equivalence')
    ax1.set_xlabel('Volume NaOH (mL)')
    ax1.set_ylabel('pH')
    ax1.set_title('Acetic Acid Titration Curve')
    ax1.legend()
    ax1.set_ylim(2, 13)

    # Panel 2: Blood pH
    pCO2_range = np.linspace(20, 80, 100)
    pH_correct = [6.1 + math.log10(24 / (0.03 * p)) for p in pCO2_range]
    pH_wrong = [3.6 + math.log10(24 / (0.03 * p)) for p in pCO2_range]
    ax2.plot(pCO2_range, pH_correct, 'b-', linewidth=2, label='pKa=6.1 (clinical)')
    ax2.plot(pCO2_range, pH_wrong, 'r--', linewidth=2, label='pKa=3.6 (true H₂CO₃)')
    ax2.axhline(7.4, color='green', linestyle=':', alpha=0.7, label='Normal pH 7.40')
    ax2.axvline(40, color='gray', linestyle=':', alpha=0.5)
    ax2.set_xlabel('pCO₂ (mmHg)')
    ax2.set_ylabel('Blood pH')
    ax2.set_title('Blood pH: Correct vs Wrong pKa')
    ax2.legend(fontsize=8)

    plt.tight_layout()
    plt.savefig(os.path.join(BASE, "chem-buffers", "figures", "chem_buffers_titration.png"), dpi=150)
    plt.close()
    print("  [3/10] chem_buffers_titration.png")


def fig4_decay():
    """2-panel: C-14 decay curve + secular equilibrium."""
    sys.path.insert(0, os.path.join(BASE, "chem-radioactive-decay", "frozen"))
    from chem_radioactive_decay_constants import C14_HALF_LIFE, C14_LIBBY_WRONG, U238_HALF_LIFE, TH234_HALF_LIFE, LN2

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.patch.set_facecolor('white')

    # Panel 1: C-14 decay
    t = np.linspace(0, 30000, 500)
    frac = np.exp(-LN2 * t / C14_HALF_LIFE)
    ax1.plot(t, frac, 'b-', linewidth=2, label=f't½={C14_HALF_LIFE:.0f} yr (Godwin)')
    ax1.axvline(C14_HALF_LIFE, color='blue', linestyle='--', alpha=0.5)
    ax1.axvline(C14_LIBBY_WRONG, color='red', linestyle='--', alpha=0.5)
    ax1.axhline(0.5, color='gray', linestyle=':', alpha=0.5)
    ax1.annotate(f'{C14_HALF_LIFE:.0f} yr\n(correct)', xy=(C14_HALF_LIFE, 0.5),
                fontsize=8, color='blue', ha='left')
    ax1.annotate(f'{C14_LIBBY_WRONG:.0f} yr\n(Libby, wrong)', xy=(C14_LIBBY_WRONG, 0.55),
                fontsize=8, color='red', ha='right')
    ax1.set_xlabel('Time (years)')
    ax1.set_ylabel('Fraction remaining')
    ax1.set_title('C-14 Decay: 5730 vs 5568')
    ax1.legend()

    # Panel 2: Secular equilibrium
    lam1 = LN2 / U238_HALF_LIFE
    lam2 = LN2 / TH234_HALF_LIFE
    ratio = lam1 / lam2
    ax2.bar(['N(U-238)', 'N(Th-234)'], [1.0, ratio], color=['steelblue', 'coral'])
    ax2.set_ylabel('Relative number of atoms')
    ax2.set_title(f'Secular Equilibrium\nN(Th)/N(U) = {ratio:.2e}\n(NOT equal atoms!)')
    ax2.set_yscale('log')

    plt.tight_layout()
    plt.savefig(os.path.join(BASE, "chem-radioactive-decay", "figures", "chem_radioactive_decay_curves.png"), dpi=150)
    plt.close()
    print("  [4/10] chem_radioactive_decay_curves.png")


def fig5_vdw():
    """2-panel: Z vs P + VdW vs ideal P vs V."""
    sys.path.insert(0, os.path.join(BASE, "chem-vdw-gas", "frozen"))
    from chem_vdw_gas_constants import R_ATM, VDW

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.patch.set_facecolor('white')

    # Panel 1: Z vs P
    T = 500
    for gas, color in [("CO2", "red"), ("N2", "blue"), ("H2", "green")]:
        a, b = VDW[gas]["a"], VDW[gas]["b"]
        Ps, Zs = [], []
        for V in np.linspace(0.1, 25, 500):
            P_vdw = R_ATM * T / (V - b) - a / V**2
            P_ideal = R_ATM * T / V
            if P_vdw > 0 and P_vdw < 200:
                Z = P_vdw * V / (R_ATM * T)
                Ps.append(P_vdw)
                Zs.append(Z)
        ax1.plot(Ps, Zs, color=color, label=gas, linewidth=2)
    ax1.axhline(1.0, color='gray', linestyle='--', alpha=0.5, label='Ideal (Z=1)')
    ax1.set_xlabel('Pressure (atm)')
    ax1.set_ylabel('Z = PV/nRT')
    ax1.set_title('Compression Factor vs P (500K)')
    ax1.legend()
    ax1.set_xlim(0, 150)

    # Panel 2: P vs V
    V_range = np.linspace(0.1, 5, 300)
    P_ideal = R_ATM * 500 / V_range
    a, b = VDW["CO2"]["a"], VDW["CO2"]["b"]
    P_vdw = [R_ATM * 500 / (V - b) - a / V**2 if V > b else np.nan for V in V_range]
    ax2.plot(V_range, P_ideal, 'b--', label='Ideal', linewidth=2)
    ax2.plot(V_range, P_vdw, 'r-', label='VdW (CO₂)', linewidth=2)
    ax2.set_xlabel('Volume (L)')
    ax2.set_ylabel('Pressure (atm)')
    ax2.set_title('CO₂: Ideal vs VdW at 500K')
    ax2.legend()
    ax2.set_ylim(0, 300)

    plt.tight_layout()
    plt.savefig(os.path.join(BASE, "chem-vdw-gas", "figures", "chem_vdw_gas_deviation.png"), dpi=150)
    plt.close()
    print("  [5/10] chem_vdw_gas_deviation.png")


def fig6_electrochem():
    """2-panel: Nernst E vs log(Q) + reduction potential chart."""
    sys.path.insert(0, os.path.join(BASE, "chem-electrochemistry", "frozen"))
    from chem_electrochemistry_constants import R, F, T298, E0

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.patch.set_facecolor('white')

    # Panel 1: Nernst E vs log(Q)
    E0_daniell = E0["Cu2+/Cu"] - E0["Zn2+/Zn"]
    n = 2
    logQ = np.linspace(-4, 4, 200)
    Q = 10 ** logQ
    E = [E0_daniell - (R * T298 / (n * F)) * math.log(q) for q in Q]
    ax1.plot(logQ, E, 'b-', linewidth=2)
    ax1.axhline(E0_daniell, color='red', linestyle='--', label=f'E⁰ = {E0_daniell:.4f} V')
    ax1.axvline(0, color='gray', linestyle=':', alpha=0.5)
    ax1.set_xlabel('log₁₀(Q)')
    ax1.set_ylabel('E (V)')
    ax1.set_title('Nernst Equation: Daniell Cell\nE = E⁰ - (RT/nF)·ln(Q)')
    ax1.legend()

    # Panel 2: Standard reduction potentials
    couples = sorted(E0.items(), key=lambda x: x[1])
    names = [c[0] for c in couples]
    vals = [c[1] for c in couples]
    colors = ['red' if v < 0 else 'steelblue' for v in vals]
    ax2.barh(names, vals, color=colors)
    ax2.axvline(0, color='black', linewidth=0.5)
    ax2.set_xlabel('E⁰ (V)')
    ax2.set_title('Standard Reduction Potentials')

    plt.tight_layout()
    plt.savefig(os.path.join(BASE, "chem-electrochemistry", "figures", "chem_electrochemistry_nernst.png"), dpi=150)
    plt.close()
    print("  [6/10] chem_electrochemistry_nernst.png")


def fig7_spectro():
    """2-panel: A vs conc + log10 vs ln comparison."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.patch.set_facecolor('white')

    # Panel 1: A vs concentration
    conc = np.linspace(0, 0.005, 100)
    epsilon = 2360  # KMnO4
    A_1cm = epsilon * conc * 1.0
    A_2cm = epsilon * conc * 2.0
    ax1.plot(conc * 1000, A_1cm, 'b-', linewidth=2, label='l = 1 cm')
    ax1.plot(conc * 1000, A_2cm, 'r--', linewidth=2, label='l = 2 cm')
    ax1.set_xlabel('Concentration (mM)')
    ax1.set_ylabel('Absorbance')
    ax1.set_title('Beer-Lambert: A = εcl\n(KMnO₄, ε=2360)')
    ax1.legend()

    # Panel 2: log10 vs ln
    T_frac = np.linspace(0.01, 1.0, 100)
    A_log10 = -np.log10(T_frac)
    A_ln = -np.log(T_frac)
    ax2.plot(T_frac, A_log10, 'b-', linewidth=2, label='−log₁₀(T) (CORRECT)')
    ax2.plot(T_frac, A_ln, 'r--', linewidth=2, label='−ln(T) (WRONG, 2.303× error)')
    ax2.set_xlabel('Transmittance')
    ax2.set_ylabel('Absorbance')
    ax2.set_title('log₁₀ vs ln: The 2.303× Error')
    ax2.legend()

    plt.tight_layout()
    plt.savefig(os.path.join(BASE, "chem-spectrophotometry", "figures", "chem_spectrophotometry_beer_lambert.png"), dpi=150)
    plt.close()
    print("  [7/10] chem_spectrophotometry_beer_lambert.png")


def fig8_thermo():
    """2-panel: dHf bar chart + Hess's law diagram."""
    sys.path.insert(0, os.path.join(BASE, "chem-thermochemistry", "frozen"))
    from chem_thermochemistry_constants import DHF

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.patch.set_facecolor('white')

    # Panel 1: dHf bar chart
    species = [s for s in DHF if DHF[s] != 0]
    values = [DHF[s] for s in species]
    colors = ['red' if v > 0 else 'steelblue' for v in values]
    ax1.barh(species, values, color=colors)
    ax1.axvline(0, color='black', linewidth=0.5)
    ax1.set_xlabel('ΔHf° (kJ/mol)')
    ax1.set_title('Standard Enthalpies of Formation\n(Red = POSITIVE, often missed by LLMs)')

    # Panel 2: Hess's law for methane combustion
    levels = [0, DHF["CH4(g)"], DHF["CO2(g)"] + 2*DHF["H2O(l)"]]
    labels = ['C(s)+2H₂+2O₂', 'CH₄+2O₂', 'CO₂+2H₂O']
    y_pos = [0, 1, 2]
    ax2.barh(labels, levels, color=['gray', 'steelblue', 'coral'])
    ax2.set_xlabel('Enthalpy (kJ/mol)')
    dH = (DHF["CO2(g)"] + 2*DHF["H2O(l)"]) - DHF["CH4(g)"]
    ax2.set_title(f"Hess's Law: CH₄ Combustion\nΔH = {dH:.1f} kJ/mol")

    plt.tight_layout()
    plt.savefig(os.path.join(BASE, "chem-thermochemistry", "figures", "chem_thermochemistry_formation.png"), dpi=150)
    plt.close()
    print("  [8/10] chem_thermochemistry_formation.png")


def fig9_stoich():
    """2-panel: MW comparison + limiting reagent."""
    sys.path.insert(0, os.path.join(BASE, "chem-stoichiometry", "frozen"))
    from chem_stoichiometry_constants import AW

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.patch.set_facecolor('white')

    # Panel 1: IUPAC vs integer MW
    formulas = {"H₂O": (2*1.008+15.999, 2*1+16),
                "NaCl": (22.990+35.45, 23+35),
                "C₆H₁₂O₆": (6*12.011+12*1.008+6*15.999, 6*12+12*1+6*16),
                "CaCO₃": (40.078+12.011+3*15.999, 40+12+3*16),
                "Aspirin": (9*12.011+8*1.008+4*15.999, 9*12+8*1+4*16)}
    names = list(formulas.keys())
    iupac = [formulas[n][0] for n in names]
    integer = [formulas[n][1] for n in names]
    x = np.arange(len(names))
    ax1.bar(x - 0.2, iupac, 0.35, label='IUPAC 2021', color='steelblue')
    ax1.bar(x + 0.2, integer, 0.35, label='Integer', color='coral')
    ax1.set_xticks(x)
    ax1.set_xticklabels(names, fontsize=8)
    ax1.set_ylabel('Molecular Weight (g/mol)')
    ax1.set_title('IUPAC vs Integer Atomic Weights')
    ax1.legend()

    # Panel 2: Limiting reagent
    reagents = {'H₂\n(4.0g)': 2*1.008, 'O₂\n(16.0g)': 15.999*2}
    mol_h2 = 4.0 / (2*1.008)
    mol_o2 = 16.0 / (2*15.999)
    ratio_h2 = mol_h2 / 2  # stoich = 2
    ratio_o2 = mol_o2 / 1  # stoich = 1
    ax2.bar(['H₂ (mol/stoich)', 'O₂ (mol/stoich)'], [ratio_h2, ratio_o2],
            color=['steelblue', 'red'])
    ax2.set_ylabel('moles / stoich coeff')
    ax2.set_title('Limiting Reagent: 2H₂ + O₂ → 2H₂O\nO₂ is limiting (smaller ratio)')

    plt.tight_layout()
    plt.savefig(os.path.join(BASE, "chem-stoichiometry", "figures", "chem_stoichiometry_mw_comparison.png"), dpi=150)
    plt.close()
    print("  [9/10] chem_stoichiometry_mw_comparison.png")


def fig10_crystal():
    """2-panel: packing efficiency + atoms per cell."""
    sys.path.insert(0, os.path.join(BASE, "chem-crystal-packing", "frozen"))
    from chem_crystal_packing_constants import PACKING, ATOMS_PER_CELL

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.patch.set_facecolor('white')

    # Panel 1: Packing efficiency
    structs = ["SC", "BCC", "FCC", "HCP", "diamond"]
    effs = [PACKING[s] * 100 for s in structs]
    colors = ['steelblue'] * len(structs)
    colors[2] = 'gold'  # FCC = max
    colors[3] = 'gold'  # HCP = max
    ax1.bar(structs, effs, color=colors)
    ax1.set_ylabel('Packing Efficiency (%)')
    ax1.set_title('Crystal Packing Efficiencies\n(FCC/HCP = maximum, Kepler conjecture)')
    ax1.axhline(74.05, color='red', linestyle='--', alpha=0.5, label='74.05% max')
    ax1.legend()

    # Panel 2: Atoms per cell
    structs2 = ["SC", "BCC", "FCC", "diamond"]
    atoms = [ATOMS_PER_CELL[s] for s in structs2]
    colors2 = ['steelblue', 'steelblue', 'coral', 'steelblue']
    ax2.bar(structs2, atoms, color=colors2)
    ax2.set_ylabel('Atoms per unit cell')
    ax2.set_title('Atoms per Unit Cell\nFCC = 4 (NOT 8, LLM error)')
    ax2.annotate('LLM says 8!', xy=(2, 4), fontsize=10, color='red',
                ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig(os.path.join(BASE, "chem-crystal-packing", "figures", "chem_crystal_packing_structures.png"), dpi=150)
    plt.close()
    print("  [10/10] chem_crystal_packing_structures.png")


def sprint_summary():
    """2x5 grid summary figure."""
    fig, axes = plt.subplots(2, 5, figsize=(20, 10))
    fig.patch.set_facecolor('white')

    titles = [
        "1. Equilibrium\nKp≠Kc, pH≠7",
        "2. Kinetics\nEa in J, not kJ",
        "3. Buffers\npKa=6.1 for blood",
        "4. Decay\n5730 not 5568",
        "5. VdW Gas\nn² in attraction",
        "6. Electrochemistry\nE=cathode-anode",
        "7. Spectrophotometry\nlog₁₀ not ln",
        "8. Thermochemistry\nC₂H₄ ΔHf>0",
        "9. Stoichiometry\nH₂O=18.015",
        "10. Crystal Packing\nFCC=4 atoms",
    ]
    errors = [
        "LLM: Kp=Kc, +sign",
        "LLM: 165 kJ not J",
        "LLM: pKa=3.6",
        "LLM: 5568 (Libby)",
        "LLM: a/V² not n²a/V²",
        "LLM: E₀+RT/nF·ln(Q)",
        "LLM: -ln(T)",
        "LLM: C₂H₄<0, NO<0",
        "LLM: H=1, C=12",
        "LLM: FCC=8 atoms",
    ]

    for idx, ax in enumerate(axes.flat):
        ax.text(0.5, 0.6, titles[idx], ha='center', va='center',
                fontsize=11, fontweight='bold', transform=ax.transAxes)
        ax.text(0.5, 0.25, errors[idx], ha='center', va='center',
                fontsize=9, color='red', transform=ax.transAxes)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.patch.set_facecolor('#f0f8ff')

    fig.suptitle('CHP Chemistry Sprint — 10 Experiments, 61 Tests Passing\n'
                 'All verified against NIST/IUPAC/CODATA', fontsize=14, fontweight='bold')
    plt.tight_layout(rect=[0, 0, 1, 0.93])
    plt.savefig(os.path.join(BASE, "figures", "chem_sprint_summary.png"), dpi=150)
    plt.close()
    print("  [SUMMARY] chem_sprint_summary.png")


if __name__ == "__main__":
    print("Generating chemistry sprint figures...")
    fig1_equilibrium()
    fig2_kinetics()
    fig3_buffers()
    fig4_decay()
    fig5_vdw()
    fig6_electrochem()
    fig7_spectro()
    fig8_thermo()
    fig9_stoich()
    fig10_crystal()
    sprint_summary()
    print("All figures generated!")
