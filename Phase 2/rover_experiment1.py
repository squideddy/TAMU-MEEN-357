
"""Run a rover simulation (Task 5.8) using the provided subfunctions.

This script calls `simulate_rover` from `subfunctions.py` with
the `experiment1` setup in `define_experiment.py` and the rover
and planet dictionaries in `dictionary_357.py`. It then plots
velocity, position, and power vs time and saves the figure.
"""

import numpy as np
import matplotlib.pyplot as plt

from subfunctions import simulate_rover
from define_experiment import experiment1
import dictionary_357 as dict


def run_and_plot():
	rover = getattr(dict, 'rover', None)
	planet = getattr(dict, 'planet', None)
	experiment_dict, end_event = experiment1()

	telemetry = simulate_rover(rover, planet, experiment_dict, end_event)

	t = telemetry['time']
	v = telemetry['velocity']
	x = telemetry['position']
	power = telemetry.get('power', None)

	fig, axes = plt.subplots(3, 1, figsize=(8, 10), sharex=True)
	axes[0].plot(t, v)
	axes[0].set_ylabel('Velocity [m/s]')
	axes[0].grid(True)

	axes[1].plot(t, x)
	axes[1].set_ylabel('Position [m]')
	axes[1].grid(True)

	if power is not None:
		axes[2].plot(t, power)
		axes[2].set_ylabel('Mechanical Power [W]')
	else:
		axes[2].text(0.5, 0.5, 'No power data', ha='center')
	axes[2].set_xlabel('Time [s]')
	axes[2].grid(True)

	plt.suptitle('Rover Simulation: Experiment 1')
	plt.tight_layout(rect=[0, 0.03, 1, 0.95])
	plt.savefig('rover_experiment1_results.png', dpi=200)
	plt.show()


if __name__ == '__main__':
	run_and_plot()


