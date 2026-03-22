"""PID Controller — Frozen Constants. Source: Ogata, Modern Control Engineering 5th Ed. DO NOT MODIFY."""
# PID control law: u(t) = Kp*e(t) + Ki*integral(e(tau)dtau) + Kd*de(t)/dt
# e(t) = setpoint - measured  (error signal)
# P: proportional to current error
# I: proportional to accumulated error (integral)
# D: proportional to rate of change of error (derivative)
# Discrete form: u[n] = Kp*e[n] + Ki*sum(e[k]*dt) + Kd*(e[n]-e[n-1])/dt
# KEY: derivative acts on ERROR (not process variable) in basic PID form

# --- Test gains ---
KP = 2.0
KI = 0.5
KD = 0.1
DT = 0.1

# --- Step response test: error sequence ---
# Setpoint = 1, process variable approaches setpoint
ERRORS = [1.0, 1.0, 1.0, 0.5, 0.2]

# --- Pre-computed outputs per step ---
# Step 0: P=2.0, I_sum=0.1, I_term=0.05, D=0 (no prev)   -> u=2.05
# Step 1: P=2.0, I_sum=0.2, I_term=0.10, D=0              -> u=2.10
# Step 2: P=2.0, I_sum=0.3, I_term=0.15, D=0              -> u=2.15
# Step 3: P=1.0, I_sum=0.35, I_term=0.175, D=-0.5         -> u=0.675
# Step 4: P=0.4, I_sum=0.37, I_term=0.185, D=-0.3         -> u=0.285
U_EXPECTED = [2.05, 2.10, 2.15, 0.675, 0.285]

# Individual term values per step
P_TERMS = [2.0, 2.0, 2.0, 1.0, 0.4]
I_TERMS = [0.05, 0.10, 0.15, 0.175, 0.185]
D_TERMS = [0.0, 0.0, 0.0, -0.5, -0.3]

# Integral sums (cumulative error * dt)
I_SUMS = [0.1, 0.2, 0.3, 0.35, 0.37]

PRIOR_ERRORS = {
    "integral_no_dt":       "Forgets dt in integral sum (sums e[k] instead of e[k]*dt)",
    "derivative_wrong_sign": "Uses e[n-1]-e[n] instead of e[n]-e[n-1] (wrong sign on D term)",
    "derivative_on_pv":     "Applies D term to process variable instead of error signal",
}
