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
import subfunctions as sf


plt.subplot(3,1,1)
plt.plot(sf.tau_dcmotor(), sf.omega())
plt.xlabel("Motor Shaft Torque [Nm]")
plt.ylabel("Motor Shaft Speed [rad/s]")

plt.subplot(3,1,2)
plt.plot(sf.tau_dcmotor(), sf.power())
plt.xlabel("Motor Shaft Torque [Nm]")
plt.ylabel("Motor Power [W]")

plt.subplot(3,1,3)
plt.plot(sf.omega(), sf.power())
plt.xlabel("Motor Shaft Speed [rad/s]")
plt.ylabel("Motor Power [W]")




