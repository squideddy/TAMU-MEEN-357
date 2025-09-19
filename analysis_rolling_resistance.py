"""Create a py-file script called analysis_rolling_resistance.py in which you use a root-finding method (e.g.,
bisection method, secant method, etc.) to determine the speed of the rover at various values for the
coefficient of rolling resistance. This analysis is very similar to what you must do for the terrain slope.
• Assume a terrain slope of 0 degrees (horizontal terrain)
• Generate rolling resistance coefficients to test with the following line of code:
o Crr_array = numpy.linspace(0.01,0.4,25);
• Store the maximum velocity [m/s] at each angle in a vector called v_max.
• Plot v_max versus Crr_array. Make sure to label the axes and indicate their units.
• Do not display anything to the console
• The hints for the previous problem apply here as well."""
import numpy as np
import matplotlib.pyplot as plt
import subfunctions as sf
import dictionary_357 as cfg

Crr_array = np.linspace(0.01, 0.4, 25)
theta_0 = np.zeros(size=Crr_array.shape, dtype=float)

Ng = sf.get_gear_ratio(cfg.rover)
r_wheel = cfg.rover['wheel_assembly']['wheel']['radius']
F_normal = sf.get_mass(cfg.rover) * cfg.planet['g'] * np.cos(np.radians(theta_0))

omegq_motor = Velocity / r_wheel * Ng


T_motor = cfg.motor['torque_stall'] - ((cfg.motor['torque_stall'] ...
        - cfg.motor['torque_noload'])/ cfg.motor['speed_noload']) * omega_motor
accel_0 = 



plt.plot(Crr_array, V_max)
plt.xlabel('Coefficient of Rolling Resistance (Crr)')
plt.ylabel('Maximum Velocity (m/s)')
plt.title('Rover Maximum Velocity vs Coefficient of Rolling Resistance')

