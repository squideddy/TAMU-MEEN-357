
rover = {}


speed_reducer = {
    'type':'reverted','diam_pinion':0.04,'diam_gear':0.07,'mass2':1.5}

motor = {
    'torque_stall':170.0 ,'torque_noload':0.0,'speed_noload':3.8,'mass':5.0}

wheel = {
    'radius':.30,'mass':1.0}

chassis={
    'mass':659.0}
science_payload={
    'mass':75.0}
power_subsys={
    'mass':90.0}
 
rover['wheel_assembly'] = {
    'wheel':wheel,
    'speed_reducer':speed_reducer,
    'motor':motor
    }

rover['chassis'] = chassis
rover['science_payload'] = science_payload
rover['power_subsys'] = power_subsys\

planet = {}
planet['gravity'] = 3.71 #m/s^2 for mars