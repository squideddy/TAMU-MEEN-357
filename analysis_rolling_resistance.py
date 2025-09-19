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
import scipy.optimize as opt
from scipy.special import erf

def ARR(Crr_array, theta_0, rover1, planet):
    Ng = sf.get_gear_ratio(rover1['wheel_assembly']['speed_reducer'])
    r_wheel = cfg.rover['wheel_assembly']['wheel']['radius']
    F_normal = sf.get_mass(cfg.rover) * cfg.planet['g'] * np.cos(np.radians(theta_0))

    V_max = np.zeros(Crr_array.shape)

    for n, Crr in enumerate(Crr_array):
        F_norm_n = float(F_normal[n])
        r = r_wheel

        def f(Vv):
            # Vv: rover linear speed (m/s)
            omega = Vv / r * Ng          # motor shaft speed
            
            Fnet = sf.F_net(np.array([omega]), np.array([theta_0[n]]), rover1, planet, Crr)
            return (Fnet)
            

        try:
            V_min = 0 # minimum speed to search
            V_maximum = 100
            V_max[n] = sf.basic_bisection(f, V_min , V_maximum, err_max =1e-6, iter_max = 1000)

        except Exception:
            Vroot = np.nan
    return V_max

if __name__ == "__main__":
    Crr_array = np.linspace(0.01, 0.4, 25)
    theta_0 = np.zeros(Crr_array.shape, dtype=float)
    V_max = ARR(Crr_array, theta_0, cfg.rover, cfg.planet)
    plt.plot(Crr_array, V_max)
    plt.xlabel('Coefficient of Rolling Resistance (Crr)')
    plt.ylabel('Maximum Velocity (m/s)')
    plt.title('Rover Maximum Velocity vs Coefficient of Rolling Resistance')
    plt.show()


"find each V_max for each Crr value"
"then plot V_max vs Crr"

