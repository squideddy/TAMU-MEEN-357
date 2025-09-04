

def get_mass(rover1): # Computes the total mass of the rover. Uses information in the rover dict.
    mass = rover1['wheel_assembly']['wheel']['mass'] * 6
    # put error if get_mass(a) and a is not a dictionary
    return mass

def get_gear_ratio(): #Returns the speed reduction ratio for the speed reducer based on speed_reducer dict.
    print('hi')
def tau_dcmotor(): #Returns the motor shaft torque when given motor shaft speed and a dictionary containing
    print('hi')           #important specifications for the motor.
def F_drive(): #Returns the force applied to the rover by the drive system given information about the drive
    print('hi')                #system (wheel_assembly) and the motor shaft speed.
def F_gravity(): #Returns the magnitude of the force component acting on the rover in the direction of its
    print('hi')                #translational motion due to gravity as a function of terrain inclination angle and rover
                #properties.
def F_rolling(): #Returns the magnitude of the force acting on the rover in the direction of its translational
    print('hi)')                #motion due to rolling resistances given the terrain inclination angle, rover properties, and a
                #rolling resistance coefficient.
def F_net(): #Returns the magnitude of net force acting on the rover in the direction of its translational
    print('hi)')                #motion.