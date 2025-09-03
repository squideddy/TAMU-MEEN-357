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