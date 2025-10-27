
"""Run a rover simulation (Task 5.8) using the provided subfunctions.

This script calls `simulate_rover` from `subfunctions.py` with
the `experiment1` setup in `define_experiment.py` and the rover
and planet dictionaries in `dictionary_357.py`. It then plots
velocity, position, and power vs time and saves the figure.
"""
import json
import numpy as np
import matplotlib.pyplot as plt

from subfunctions import simulate_rover
from define_experiment import experiment1
import dictionary_357 as dict

# get rover and planet dictionaries
rover = getattr(dict, 'rover', None)
planet = getattr(dict, 'planet', None)
experiment_dict, end_event = experiment1()

# pull the telemetry data from the simulation
telemetry = simulate_rover(rover, planet, experiment_dict, end_event)

# define time, velocity, position, and power for plotting
t = telemetry['time']
v = telemetry['velocity']
x = telemetry['position']
power = telemetry.get('power', None)

# save summary data to JSON file
with open("C:\\Users\\edwar\\OneDrive\\Documents\\TAMU files\\5 - Fall 2025\\MEEN 357 - Engr Analysis for mech\\TAMU-MEEN-357\\Phase 2\\summary.json", "w") as json_file:
    json.dump({
        "completion_time": t[-1] ,
        "distance_traveled": x[-1] ,
        "max_velocity": max(v) ,
        "average_velocity": np.mean(v) ,
        "battery_energy": telemetry.get('battery_energy', 0),
        "batt_energy_per_distance": telemetry.get('energy_per_distance', 0)
    }, json_file)

## create subplots for velocity, position, and power
# position
fig, axes = plt.subplots(3, 1, figsize=(8, 10), sharex=True)
axes[0].set_title('Position vs. Time')
axes[0].plot(t, x)
axes[0].set_ylabel('Position [m]')
axes[0].grid(True)

# velocity
axes[1].set_title('Velocity vs. Time')
axes[1].plot(t, v)
axes[1].set_ylabel('Velocity [m/s]')
axes[1].grid(True)

#power
axes[2].set_title('Power vs. Time')
axes[2].plot(t, power)
axes[2].set_ylabel('Total Electric Power [W]')
axes[2].set_xlabel('Time [s]')
axes[2].grid(True)

# overall title and layout adjustments and show/save
plt.suptitle('Rover Simulation: Experiment 1')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('rover_experiment1_results.png', dpi=200)
plt.show()



