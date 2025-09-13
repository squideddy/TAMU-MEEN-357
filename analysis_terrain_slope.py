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
import numpy as np
#import matplotlib.pyplot as plt
# 1) Import your config (rover/motor/etc.) defensively
import dictionary_357 as cfg
from subfunctions import F_net  # your array-oriented function

# Pull objects (and provide sensible defaults/fallbacks)
rover  = getattr(cfg, 'rover',  None)
motor  = getattr(cfg, 'motor',  None)
planet = 3.72  # fallback to Mars g if missing
Crr    = 0.2




#Bisection
def find_v_top(theta_deg, tol=1e-5, max_iter= 120):
    wL = 0.0 # rad/s
    wU = motor['speed_noload'] # speed_noload in rad/s
    fL = F_net(wL, theta_deg, rover, planet, Crr)
    fU = F_net(wU, theta_deg, rover, planet, Crr)

#Main Function for differnt angles 
def main():
    slope_array_deg = np.linspace(-10, 35, 25)  # degrees
    v_max = np.zeros_like(slope_array_deg, dtype=float)
    for i, th in enumerate(slope_array_deg):
        v_max[i] = find_v_top(th)

if __name__ == '__main__':
    main()