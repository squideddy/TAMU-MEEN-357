'''your team has been asked to conduct a study of the impact on EDL performance of changing the parachute
size. For this task, you must do two things: (1) create a Python script called
study_parachute_size.py that conducts the analysis and generates useful visualizations of the
results'''

import numpy as np
import matplotlib.pyplot as plt
from define_edl_system import *
from subfunctions_EDL import *
from define_planet import *
from define_mission_events import *

def landing_success(edl_out, t, Y):
    # final EDL state
    speed_edl   = Y[0, -1]
    altitude_edl = Y[1, -1]
    vel_rov_rel = Y[5, -1]
    pos_rov_rel = Y[6, -1]   # not used in logic, but here if you want it

    rover_touchdown_speed = speed_edl + vel_rov_rel

    danger_speed    = edl_out['sky_crane']['danger_speed']
    danger_altitude = edl_out['sky_crane']['danger_altitude']

    # if the rover never actually “landed” in the sim, it’s a failure
    if not edl_out['rover']['on_ground']:
        return 0

    # SUCCESS: same as first branch in update_edl_state
    if (altitude_edl >= danger_altitude and
        abs(rover_touchdown_speed) <= abs(danger_speed)):
        return 1
    else:
        # includes both “too fast” and “too low” failure conditions
        return 0
    
# *************************************
# load dicts that define the EDL system (includes rover), planet,
# mission events and so forth.
mars = define_planet()
mission_events = define_mission_events()

#parachute diameters to study
diameters = np.arange(14,19.5,0.5)

terminal_times = [] #  final simulated time for each diameter
landing_speeds = [] # final rover speed ( relative to ground)
landing_success_vals = [] # 1 = success, 0 = failure

tmax = 2000   # [s] maximum simulated time

# Overrides what might be in the loaded data to establish our desired
# initial conditions
for D in diameters:
    # fresh EDL system fro each run
    edl_system = define_edl_system_1()

    edl_system['altitude'] = 11000    # [m] initial altitude
    edl_system['velocity'] = -590     # [m/s] initial velocity
    # rockets are off initially
    edl_system['parachute']['deployed'] = True   # our parachute is open
    edl_system['parachute']['ejected'] = False   # and still attached
    edl_system['parachute']['diameter'] = D # this allows evaluation of simulation at a certain diameter
    # heat shield is not ejected initially
    # sky crane is off initially
    # speed controller is off initially
    # postion controller is off initially
    edl_system['rover']['on_ground'] = False # the rover has not yet landed

    # run the simulation; last argument False to supress message spam
    t, Y, edl_out = simulate_edl(edl_system, mars, mission_events, tmax, False)

    # used values above for state variables y = Y, see below
    terminal_times.append(t[-1])
    landing_speeds.append(Y[0,-1])
    landing_success_vals.append(landing_success(edl_out,t,Y))

    '''# unpack the input state vector into variables with more readable names
    # 
    vel_edl = y[0]       # [m/s] velocity of EDL system
    altitude_edl = y[1]  # [m] altitude of EDL system
    fuel_mass = y[2]     # [kg] total mass of fuel in EDL system 
    ei_vel = y[3]        # [m/s] error integral for velocity error 
    ei_pos = y[4]        # [m] error integral for position (altitude) error 
    vel_rov = y[5]       # [m/s] velocity of rover relative to sky crane
    pos_rov = y[6]       # [m] position of rover relative to sky crane'''

# ----------------------------------------------------------
# ONE PAGE: All three analysis plots stacked vertically
# ----------------------------------------------------------
fig, axs = plt.subplots(3, 1, figsize=(8, 12))
plt.tight_layout(pad=4.0)

# 1. Termination time vs diameter
axs[0].plot(diameters, terminal_times, marker='o')
axs[0].set_xlabel('Parachute diameter [m]')
axs[0].set_ylabel('Termination time [s]')
axs[0].set_title('Termination Time vs Parachute Diameter')
axs[0].grid(True)

# 2. Touchdown speed vs diameter
axs[1].plot(diameters, landing_speeds, marker='o')
axs[1].set_xlabel('Parachute diameter [m]')
axs[1].set_ylabel('Touchdown Speed [m/s]')
axs[1].set_title('Touchdown Speed vs Parachute Diameter')
axs[1].grid(True)

# 3. Landing success vs diameter
colors = ['green' if s == 1 else 'red' for s in landing_success_vals]
axs[2].bar(diameters, landing_success_vals,
           width=0.35,
           color=colors)
axs[2].set_xlabel('Parachute Diameter [m]')
axs[2].set_ylabel('Landing Success (1=success, 0=failure)')
axs[2].set_title('Landing Success vs Parachute Diameter')
axs[2].set_ylim(-0.1, 1.2)
axs[2].grid(axis='y')

plt.show()

# Plot Simulated time (i.e., time at termination of simulation) vs. parachute diameter
# Plot Rover speed (relative to ground) at simulation termination vs. parachute diameter
# Plot Rover landing success (1=success; 0=failure) vs. parachute diameter

