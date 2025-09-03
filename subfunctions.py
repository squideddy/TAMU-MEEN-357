
def get_mass(): # Computes the total mass of the rover. Uses information in the rover dict.
    

def get_gear_ratio(): #Returns the speed reduction ratio for the speed reducer based on speed_reducer dict.
def tau_dcmotor(): #Returns the motor shaft torque when given motor shaft speed and a dictionary containing
                #important specifications for the motor.
def F_drive(): #Returns the force applied to the rover by the drive system given information about the drive
                #system (wheel_assembly) and the motor shaft speed.
def F_gravity(): #Returns the magnitude of the force component acting on the rover in the direction of its
                #translational motion due to gravity as a function of terrain inclination angle and rover
                #properties.
def F_rolling(): #Returns the magnitude of the force acting on the rover in the direction of its translational
                #motion due to rolling resistances given the terrain inclination angle, rover properties, and a
                #rolling resistance coefficient.
def F_net(): #Returns the magnitude of net force acting on the rover in the direction of its translational
                #motion.