# Euler's Number e — Frozen Reference
# Source: Wolfram Alpha / OEIS A001113
# Verified independently by multiple computation records
#
# DO NOT MODIFY THIS FILE.
# This is the ground truth. The code must match this. Not the other way around.
#
# The starting point: what a standard LLM float gives you
LLM_FLOAT_PRECISION = 15
LLM_FLOAT_VALUE = "2.718281828459045"
# This is where current LLMs cap out with float arithmetic.
# Everything below is what CHP pushes past.

# The reference: first 1000 digits of e
# Source: https://oeis.org/A001113
# Verified against Wolfram Alpha and multiple independent computations
E_1000_DIGITS = (
    "2."
    "71828182845904523536028747135266249775724709369995"
    "95749669676277240766303535475945713821785251664274"
    "27466391932003059921817413596629043572900334295260"
    "59563073813232862794349076323382988075319525101901"
    "15738341879307021540891499348841675092447614606680"
    "82264800168477411853742345442437107539077744992069"
    "55170276183860626133138458300075204493382656029760"
    "67371132007093287091274437470472306969772093101416"
    "92836819025515108657463772111252389784425056953696"
    "77078544996996794686445490598793163688923009879312"
    "77361782154249992295763514822082698951936680331825"
    "28869398496465105820939239829488793320362509443117"
    "30123819706841614039701983767932068328237646480429"
    "53118023287825098194558153017567173613320698112509"
    "96181881593041690351598888519345807273866738589422"
    "87922849989208680582574927961048419844436346324496"
    "84875602336248270419786232090021609902353043699418"
    "49146314093431738143640546253152096183690888707016"
    "76839642437814059271456354906130310720851038375051"
    "01157477041718986106873969655212671546889570350354"
)

# Digit checkpoints — used for sigma gates at each precision milestone
# These are the correct digits at specific positions (0-indexed after decimal)
CHECKPOINTS = {
    20:   "71828182845904523536",      # digits 1-20
    50:   "7182818284590452353602874713526624977572470936999",
    100:  "71828182845904523536028747135266249775724709369995957496696762772407663035354759",
    200:  "the first 200 digits match E_1000_DIGITS[:202]",
    500:  "match E_1000_DIGITS[:502]",
    1000: "match E_1000_DIGITS",
}

# The target: what CHP will compute
TARGET_DIGITS = 10000

# Algorithm specification — FROZEN
# The Builder MUST use one of these algorithms.
# Using math.e or mpmath.e is PROHIBITED — that is the LLM prior (cheating).
REQUIRED_ALGORITHM = "taylor_series_with_binary_splitting"

# Taylor series: e = sum(1/n!) for n=0 to infinity
# Binary splitting for fast convergence at high precision
# Reference: Haible & Papanikolaou (1997)
# "Fast multiprecision evaluation of series of rational numbers"

# Convergence spec:
# At N terms, error < 1/(N!) which is < 10^(-N*log10(N)) roughly
# For 10000 digits: need approximately 3249 terms
# Verify: len(str(factorial(3249))) > 10000
TERMS_FOR_10000_DIGITS = 3500  # conservative upper bound

# Prohibited patterns (Prior-as-Detector targets):
PROHIBITED = [
    "import mpmath",          # external arbitrary precision library (cheating)
    "mpmath.e",               # direct lookup (cheating)
    "math.e",                 # float precision only (15 digits max)
    "scipy",                  # not allowed
    "sympy.E",                # direct lookup (cheating)
    "from mpmath",            # mpmath import variant
]

# What is ALLOWED:
ALLOWED = [
    "from decimal import Decimal, getcontext",   # standard library only
    "decimal.Decimal",                            # arbitrary precision
    "factorial",                                  # for Taylor series
    "fractions.Fraction",                         # optional exact arithmetic
]
