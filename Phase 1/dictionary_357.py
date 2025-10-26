
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
