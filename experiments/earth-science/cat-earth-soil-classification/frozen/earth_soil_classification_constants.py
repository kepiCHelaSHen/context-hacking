"""USDA Soil Texture Triangle — Frozen Constants. Source: USDA-NRCS Soil Texture Triangle. DO NOT MODIFY."""

# Soil texture: %clay + %silt + %sand = 100 ALWAYS
# USDA texture triangle classifies based on clay/silt/sand percentages

# --- Key Texture Class Boundaries ---
CLAY_MIN_FOR_CLAY_CLASS = 40       # clay >= 40% => "clay" texture class
SAND_MIN_FOR_SAND_CLASS = 85       # sand >= 85% AND clay < 10% => "sand"
CLAY_MAX_FOR_SAND_CLASS = 10       # upper limit on clay for sand class

# Loam boundaries (the "ideal" soil)
LOAM_CLAY_MIN = 7
LOAM_CLAY_MAX = 27
LOAM_SILT_MIN = 28
LOAM_SILT_MAX = 50
LOAM_SAND_MAX = 52

# Sandy loam boundaries
SANDY_LOAM_SAND_MIN = 43
SANDY_LOAM_SAND_MAX = 85
SANDY_LOAM_CLAY_MAX = 20

# Loamy sand boundaries
LOAMY_SAND_SAND_MIN = 70
LOAMY_SAND_SAND_MAX = 90
LOAMY_SAND_CLAY_MAX = 15

# Silt loam boundaries
SILT_LOAM_SILT_MIN = 50
SILT_LOAM_CLAY_MAX = 27

# --- Composition Validation ---
COMPOSITION_SUM = 100
TOLERANCE = 0.5  # absolute tolerance for sum check

# --- Test Vectors ---
TEST_LOAM = {"clay": 20, "silt": 40, "sand": 40, "expected": "loam"}
TEST_CLAY = {"clay": 50, "silt": 25, "sand": 25, "expected": "clay"}
TEST_LOAMY_SAND = {"clay": 10, "silt": 10, "sand": 80, "expected": "loamy sand"}
TEST_SAND = {"clay": 5, "silt": 5, "sand": 90, "expected": "sand"}
TEST_INVALID = {"clay": 30, "silt": 30, "sand": 30, "expected_valid": False}  # sums to 90

PRIOR_ERRORS = {
    "sum_not_100":          "Gives clay/silt/sand percentages that do not sum to 100",
    "clay_boundary_wrong":  "Wrong clay percentage threshold for the clay texture class (must be >=40%)",
    "loam_definition_wrong": "Wrong boundaries for loam class (7-27% clay, 28-50% silt, <=52% sand)",
}
