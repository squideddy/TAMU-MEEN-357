
rover = {}
rover['wheel_assembly'] = {
    'wheel':{
        'radius':.30,'mass':1.0},
    'speed_reducer':{
        'type':'reverted','diam_pinion':0.04,'diam_gear':0.07,'mass2':1.5}, 
    'motor':{
        'torque_stall':170.0 ,'torque_noload':0.0,'speed_noload':3.8,'mass':5.0}
    }

rover['chassis']={
    'mass':659.0}
rover['science_payload']={
    'mass':75.0}
rover['power_subsys']={
    'mass':90.0}
 