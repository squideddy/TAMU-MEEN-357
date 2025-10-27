
from subfunctions import *
import matplotlib.pyplot as plt
import numpy as np
import dictionary_357
from scipy.interpolate import interp1d


# Extract efficiency data from dictionary_357
effcy_tau = dictionary_357.effcy_tau
effcy = dictionary_357.effcy

# Build cubic interpolation function (cubic spline)
effcy_fun = interp1d(effcy_tau, effcy, kind='cubic') # fit the cubic spline

# 100 evenly spaced torque values between min and max torque
tau_eval = np.linspace(effcy_tau.min(), effcy_tau.max(), 100)

# Evaluate spline at those locations
effcy_eval = effcy_fun(tau_eval)

# Plot: stars for given data, line for spline
plt.figure(figsize=(8,4.5))
plt.plot(tau_eval, effcy_eval, label='Cubic interpolation', linewidth=2)
plt.plot(effcy_tau, effcy, '*', markersize=10, label='Given data')
plt.xlabel('Motor Shaft Torque [Nm]')
plt.ylabel('Motor Efficiency [%]')
plt.title('Fig 2: Motor Efficiency vs. Motor Shaft Torque')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()














