"""###########################################################################
#   This file initializes the experiment and end_event structures for 
#   MEEN 357 project phase 2.
#
#   Created by: MEEN 357 Instructional Team
#   Last Modified: 24 Jan. 2022
#   Last Modified by: JWR
###########################################################################"""

import numpy as np

def experiment1():
    
    experiment = {'time_range' : np.array([0,20000]),
                  'initial_conditions' : np.array([0.3025,0]),
                  'alpha_dist' : np.array([0, 100, 200, 300, 400, 500, 600, \
                                           700, 800, 900, 1000]),
                  'alpha_deg' : np.array([11.509, 2.032, 7.182, 2.478, \
                                        5.511, 10.981, 5.601, -0.184, \
                                        0.714, 4.151, 4.042]),
                  'Crr' : 0.1}
    
    
    # Below are default values for example only: ### Modified to match Task 8, no longer example values ###
    end_event = {'max_distance' : 1000, ##Modified to 1000 m for Task 8##
                 'max_time' : 10000, ##Modified to 10,000 s for Task 8##
                 'min_velocity' : 0.01} ##Modified to 0.01 m/s for Task 8##
    
    return experiment, end_event

