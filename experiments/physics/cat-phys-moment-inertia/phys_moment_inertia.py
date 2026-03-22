"""Moment of Inertia — CHP Physics Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from phys_moment_inertia_constants import *

def solid_sphere(m, r): return 2/5 * m * r**2
def hollow_sphere(m, r): return 2/3 * m * r**2
def solid_cylinder(m, r): return 1/2 * m * r**2
def rod_center(m, L): return 1/12 * m * L**2
def rod_end(m, L): return 1/3 * m * L**2
def disk(m, r): return 1/2 * m * r**2
def parallel_axis(I_cm, m, d): return I_cm + m * d**2

if __name__ == "__main__":
    print(f"Solid sphere (2kg, 0.1m): {solid_sphere(2,0.1):.4f} kg·m²")
    print(f"Hollow sphere: {hollow_sphere(2,0.1):.5f} kg·m² (LARGER than solid)")
