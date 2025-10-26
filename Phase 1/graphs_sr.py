"""Create a py-file script called graphs_sr.py that is similar to graphs_motor.py EXCEPT that it uses the
speed, torque, and power of the speed reducer output shaft (the motor shaft now is the input to the
speed reducer; your graphs should be of the torque, speed, and power of the speed reducer output). As
in the previous case, please label your axes properly.
"""
import matplotlib.pyplot as plt
import numpy as np
import dictionary_357
import subfunctions as sf

# Get gear ratio from speed reducer
Ng = sf.get_gear_ratio(dictionary_357.speed_reducer)

# Generate omega_motor (motor shaft speed) values
omega_motor = np.linspace(0, dictionary_357.motor['speed_noload'], 100)

# Calculate motor shaft torque using subfunctions
tau_motor = sf.tau_dcmotor(omega_motor, dictionary_357.motor)

# Calculate speed reducer output values
omega_sr = omega_motor / Ng
tau_sr = tau_motor * Ng
power_sr = tau_sr * omega_sr

plt.figure(figsize=(8, 10))

# 1. Speed reducer output shaft speed vs. torque
plt.subplot(3,1,1)
plt.plot(tau_sr, omega_sr)
plt.xlabel("Speed Reducer Output Shaft Torque [Nm]")
plt.ylabel("Speed Reducer Output Shaft Speed [rad/s]")

# 2. Speed reducer output power vs. torque
plt.subplot(3,1,2)
plt.plot(tau_sr, power_sr)
plt.xlabel("Speed Reducer Output Shaft Torque [Nm]")
plt.ylabel("Speed Reducer Output Power [W]")

# 3. Speed reducer output power vs. speed
plt.subplot(3,1,3)
plt.plot(omega_sr, power_sr)
plt.xlabel("Speed Reducer Output Shaft Speed [rad/s]")
plt.ylabel("Speed Reducer Output Power [W]")


# Show the plots
plt.tight_layout()
plt.show()
