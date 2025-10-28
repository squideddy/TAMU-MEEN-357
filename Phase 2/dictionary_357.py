import numpy as np
rover = {}


speed_reducer = {
    'type':'reverted','diam_pinion':0.04,'diam_gear':0.07,'mass':1.5} #units rescpective: 0.04m, 0.07m, 1.5kg 

motor = {
    'torque_stall':170.0 ,'torque_noload':0.0,'speed_noload':3.8,'mass':5.0} # units respective: 170Nm, 0Nm, 3.8rad/s, 5.0kg

wheel = { 
    'radius':.30,'mass':1.0} # units respective: 0.30m, 1.0kg

chassis={
    'mass':659.0}
science_payload={
    'mass':75.0}
power_subsys={
    'mass':90.0} # All units in kg
 
rover['wheel_assembly'] = {
    'wheel':wheel,
    'speed_reducer':speed_reducer,
    'motor':motor
    }

rover['chassis'] = chassis
rover['science_payload'] = science_payload
rover['power_subsys'] = power_subsys

planet = {"g": 3.72}

rover['telemetry'] = {
    "time": [],
    "completion_time": 0.0,
    "velocity": [],
    "position": [],
    "distance_traveled": 0.0,
    "max_velocity": 0.0,
    "average_velocity": 0.0,
    "power": [],
    "battery_energy": 0.0,
    "energy_per_distance": 0.0
}

effcy_tau = np.array([0, 10, 20, 40, 70, 165])
effcy = np.array([0, 0.55, 0.75, 0.71, 0.50, 0.05])
# put efficiency data into the rover dict (either location is fine; pick one)
rover['wheel_assembly']['motor']['efficiency'] =  {
    "effcy_tau": effcy_tau,
    "effcy": effcy
}