"""graphs_motor.py
Create a py-file script called graphs_motor.py according to the following specifications:
• It does not display anything to the console
• It plots the following three graphs in a 3x1 array (use the matplotlib.pyplot.subplot
command to achieve this) in the following order top to bottom:
o motor shaft speed [rad/s] vs. motor shaft torque [Nm] (use torque on the x-axis)
o motor power [W] vs. motor shaft torque [Nm] (use torque on the x-axis)
o motor power [W] vs. motor shaft speed [rad/s] (use speed on the x-axis)
• All graphs should have both axes labeled clearly (with units indicated). Use the
matplotlib.pyplot.xlabel and matplotlib.pyplot.ylabel commands.
• Use the functions you created to generate the graphs """
import matplotlib.pyplot as plt
import dictionary_357
import numpy as np
import subfunctions


# Generate omega (motor speed) values using subfunctions
omega = np.linspace(0, dictionary_357.motor['speed_noload'], 100)
# Calculate torque using subfunctions
tau = subfunctions.tau_dcmotor(omega, dictionary_357.motor)
# Calculate power: power = torque * omega
power = tau * omega

plt.figure(figsize=(8, 10))

# 1. Motor shaft speed vs. torque
plt.subplot(3,1,1)
plt.plot(tau, omega)
plt.xlabel("Motor Shaft Torque [Nm]")
plt.ylabel("Motor Shaft Speed [rad/s]")

# 2. Motor power vs. torque
plt.subplot(3,1,2)
plt.plot(tau, power)
plt.xlabel("Motor Shaft Torque [Nm]")
plt.ylabel("Motor Power [W]")

# 3. Motor power vs. speed
plt.subplot(3,1,3)
plt.plot(omega, power)
plt.xlabel("Motor Shaft Speed [rad/s]")
plt.ylabel("Motor Power [W]")

# Show the plots
plt.tight_layout()  # Adjusts spacing between subplots
plt.show()

