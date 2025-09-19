"""Crete a py-file script called analysis_terrain_slope.py in which you use a root-finding method (e.g.,
bisection method, secant method, etc.) to determine the speed of the rover at various terrain slopes.
• Assume a coefficient of rolling resistance of 𝐶𝑟𝑟 = 0.2.
• Generate terrain angles to test with the following line of code:
o slope_array_deg = numpy.linspace(-10,35,25);
o Note that this gives you angles in DEGREES.
• Store the maximum velocity [m/s] at each angle in a vector called v_max.
• Plot v_max versus slope_array_deg. Make sure to label the axes and indicate their units.
• Do not display anything to the console
• *** Hint: Since we are not using a speed controller in this model, your rover will travel at the
fastest speed it can in any given situation. Its top speed is the velocity it is at when it stops
accelerating. This means you must look for the operating point of the motor at which the net force
acting on the rover is zero. ***
• Hint: You can use the no-load and stall speeds of the motor to define an initial bracket for the
root-finding method. Alternatively, provide an open method with any value on this range."""
#!/usr/bin/env python3
# analysis_terrain_slope.py
# Uses dictionary_357.py and subfunctions.py to find top speed vs slope by solving F_net(v)=0 via bisection.

import numpy as np
import matplotlib.pyplot as plt

# --- Load your rover/motor/planet/Crr config ---
import dictionary_357 as cfg
from subfunctions import F_net as F_net_array  # your array-oriented function

# Pull config (with safe fallbacks for planet, Crr)
rover  = getattr(cfg, 'rover',  None)
motor  = getattr(cfg, 'motor',  None)
planet = getattr(cfg, 'planet', {'gravity': 3.72})
Crr    = getattr(cfg, 'Crr',    0.2)

if rover is None or motor is None:
    raise RuntimeError("dictionary_357.py must define 'rover' and 'motor'.")

# --- Geometry / gearing helpers (computed locally; no changes to your subfunctions) ---
def gear_ratio_from_rover(rvr):
    sr = rvr['wheel_assembly']['speed_reducer']
    return (sr['diam_gear'] / sr['diam_pinion'])**2

def omega_to_v(omega_motor, rvr):
    Ng = gear_ratio_from_rover(rvr)
    r  = rvr['wheel_assembly']['wheel']['radius']
    return (omega_motor / Ng) * r  # omega_wheel = omega_m / Ng; v = omega_wheel * r

def v_to_omega(v, rvr):
    Ng = gear_ratio_from_rover(rvr)
    r  = rvr['wheel_assembly']['wheel']['radius']
    return (v / r) * Ng

def v_no_load_wheel(rvr):
    return omega_to_v(float(motor['speed_noload']), rvr)

# --- Adapter: make your array-style F_net(omega, angle, ...) usable with scalar bisection in v ---
def F_net_in_v(v, theta_deg):
    # Your F_net requires omega and angle to be arrays of equal length; pass 1-element arrays:
    omega = v_to_omega(v, rover)
    val = F_net_array(np.array([omega]), np.array([theta_deg]), rover, planet, Crr)
    return float(np.asarray(val).reshape(()))

# --- Bisection over linear speed v (root: F_net_in_v(v,theta)=0) ---
def find_v_top(theta_deg, tol=1e-5, max_iter=120):
    vL = 0.0
    vU = max(1e-6, v_no_load_wheel(rover) * 2.0)  # give some headroom
    fL = F_net_in_v(vL, theta_deg)
    fU = F_net_in_v(vU, theta_deg)

    if fL <= 0.0:
        return 0.0  # can't move on this slope

    # expand until sign change or limit
    for _ in range(10):
        if fL * fU <= 0.0:
            break
        vU *= 1.8
        fU = F_net_in_v(vU, theta_deg)

    # if still no sign change, pick best candidate on [0, vU]
    if fL * fU > 0.0:
        candidates = np.linspace(vL, vU, 48)
        vals = [abs(F_net_in_v(c, theta_deg)) for c in candidates]
        return float(max(0.0, candidates[int(np.argmin(vals))]))

    # bisection
    it = 0
    while it < max_iter and (vU - vL) > tol:
        vM = 0.5 * (vL + vU)
        fM = F_net_in_v(vM, theta_deg)
        if abs(fM) < tol:
            return float(max(0.0, vM))
        if fL * fM <= 0.0:
            vU, fU = vM, fM
        else:
            vL, fL = vM, fM
        it += 1
    return float(max(0.0, 0.5 * (vL + vU)))

# --- Main: sweep slopes, store v_max, save plot (no console output) ---
def main():
    slope_array_deg = np.linspace(-10, 35, 25)  # degrees
    v_max = np.zeros_like(slope_array_deg, dtype=float)
    for i, th in enumerate(slope_array_deg):
        v_max[i] = find_v_top(th)

    plt.figure()    
    plt.plot(slope_array_deg, v_max, marker='o', linewidth=2)
    plt.xlabel('Slope angle, θ [deg]')
    plt.ylabel('Top speed v_max [m/s]')
    plt.title('Rover Top Speed vs Terrain Slope')
    plt.grid(True)
    plt.tight_layout()
    plt.show()  # <-- pops up a window; keep this LAST

if __name__ == '__main__':
    main()