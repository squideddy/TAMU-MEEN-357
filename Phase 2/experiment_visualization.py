# experiment_visualization.py
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# Import the factory function, then call it to get the dicts
from define_experiment import experiment1

experiment, end_event = experiment1()  # returns two dicts
alpha_dist = np.array(experiment['alpha_dist'], dtype=float)
alpha_deg  = np.array(experiment['alpha_deg'],  dtype=float)

# Build cubic interpolation function (cubic spline)
alpha_fun = interp1d(alpha_dist, alpha_deg, kind='cubic', fill_value='extrapolate')

# 100 evenly spaced x-locations between min and max distance
x_eval = np.linspace(alpha_dist.min(), alpha_dist.max(), 100)

# Evaluate spline at those locations
alpha_eval = alpha_fun(x_eval)

# Plot: stars for given data, line for spline
plt.figure(figsize=(8,4.5))
plt.plot(x_eval, alpha_eval, label='Cubic interpolation', linewidth=2)
plt.plot(alpha_dist, alpha_deg, '*', markersize=10, label='Given data')
plt.xlabel('Distance along path')
plt.ylabel('Terrain angle (deg)')
plt.title('Terrain Angle vs. Position')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()