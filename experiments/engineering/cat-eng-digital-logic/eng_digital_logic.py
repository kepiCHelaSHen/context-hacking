"""Digital Logic: Boolean Simplification — CHP Engineering Sprint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from eng_digital_logic_constants import VARIABLES, N_VARS, MINTERMS, TRUTH_TABLE


def evaluate_sop(minterms, n_vars, inputs):
    """Evaluate a Sum-of-Products function given its minterms.
    inputs: tuple of 0/1 values (MSB first), e.g. (1,0,1) for A=1,B=0,C=1.
    Returns True if the input combination is in the minterm set."""
    index = 0
    for bit in inputs:
        index = (index << 1) | bit
    return index in minterms


def demorgan_nand(a, b):
    """De Morgan's: NOT(A AND B) = (NOT A) OR (NOT B)."""
    return (not a) or (not b)


def demorgan_nor(a, b):
    """De Morgan's: NOT(A OR B) = (NOT A) AND (NOT B)."""
    return (not a) and (not b)


def simplify_single_var(minterms, n_vars):
    """If the function depends on exactly one variable, return its name.
    Strategy: for each variable, check if all minterms share the same value
    for that variable AND the complementary set has the opposite value.
    Returns the variable name string or None."""
    total = 1 << n_vars
    var_names = VARIABLES[:n_vars]
    minterm_set = set(minterms)
    for var_idx in range(n_vars):
        # Bit position: MSB is var 0, so bit position = n_vars - 1 - var_idx
        bit_pos = n_vars - 1 - var_idx
        ones_match = all(((m >> bit_pos) & 1) == 1 for m in minterm_set)
        zeros_match = all(((m >> bit_pos) & 1) == 0 for m in minterm_set)
        if ones_match and len(minterm_set) == total // 2:
            return var_names[var_idx]
        if zeros_match and len(minterm_set) == total // 2:
            return f"NOT {var_names[var_idx]}"
    return None


if __name__ == "__main__":
    print(f"F(A,B,C) = Sum_m{MINTERMS}")
    print(f"Simplified: F = {simplify_single_var(MINTERMS, N_VARS)}")
    print(f"De Morgan NAND(1,0): NOT(1 AND 0) = {demorgan_nand(True, False)}")
    print(f"De Morgan NOR(1,0):  NOT(1 OR 0)  = {demorgan_nor(True, False)}")
    print("Truth table check:")
    for inputs, expected in TRUTH_TABLE.items():
        result = evaluate_sop(MINTERMS, N_VARS, inputs)
        status = "OK" if result == bool(expected) else "FAIL"
        print(f"  {inputs} -> {int(result)} (expected {expected}) {status}")
