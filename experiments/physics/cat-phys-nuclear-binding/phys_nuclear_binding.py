"""Nuclear Binding Energy — CHP Physics Sprint. All constants from frozen spec."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from phys_nuclear_binding_constants import M_PROTON_U, M_NEUTRON_U, U_TO_MEV, ATOMIC_MASS

def binding_energy(Z, N, atomic_mass_u):
    """B = [Z·m_H + N·m_n - M_atom]·c². Returns MeV."""
    mass_defect = Z * ATOMIC_MASS["H1"] + N * M_NEUTRON_U - atomic_mass_u
    return mass_defect * U_TO_MEV

def binding_energy_per_nucleon(Z, N, atomic_mass_u):
    """B/A where A = Z + N."""
    return binding_energy(Z, N, atomic_mass_u) / (Z + N)

def mass_defect(Z, N, atomic_mass_u):
    """Δm = Z·m_H + N·m_n - M_atom (in u)."""
    return Z * ATOMIC_MASS["H1"] + N * M_NEUTRON_U - atomic_mass_u

if __name__ == "__main__":
    BE_fe = binding_energy(26, 30, ATOMIC_MASS["Fe56"])
    BE_he = binding_energy(2, 2, ATOMIC_MASS["He4"])
    print(f"Fe-56: BE = {BE_fe:.1f} MeV, BE/A = {BE_fe/56:.2f} MeV/nucleon")
    print(f"He-4:  BE = {BE_he:.1f} MeV, BE/A = {BE_he/4:.2f} MeV/nucleon")
    print(f"Fe-56 has highest BE/A (near peak of curve)")
