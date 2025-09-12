import numpy as np
import math as m
def get_mass(rover1): # Computes the total mass of the rover. Uses information in the rover dict.
    mass_tot_wheels = (rover1['wheel_assembly']['wheel']['mass']+rover1['wheel_assembly']['speed_reducer']['mass2']+rover1['wheel_assembly']['motor']['mass'])* 6
    mass_tot_chassis = rover1['chassis']['mass'] + rover1['science_payload']['mass'] + rover1['power_subsys']['mass']
    return mass_tot_wheels + mass_tot_chassis


def get_gear_ratio(speed_reducer): #Returns the speed reduction ratio for the speed reducer based on speed_reducer dict.
    #gear ratio = diam_gear/diam_pinion
    
    # Raise errors
    if not isinstance(speed_reducer, dict): 
        raise   TypeError("Error: Invalid input type. Expected a dictionary.")
    
    # Calculate gear ratio
    Ng = (speed_reducer['diam_gear']/speed_reducer['diam_pinion'])**2
    return Ng

def tau_dcmotor(omega, motor): #Returns the motor shaft torque when given motor shaft speed and a dictionary containing
                        #important specifications for the motor.
    
    # Raise errors
    if not isinstance(motor, dict): 
        raise   TypeError("Error: Invalid input type. Expected a dictionary.")
    if not isinstance(omega, (int, float,np.ndarray)): 
        raise   TypeError("Error: Invalid input type. Expected a number.")
    
    # Calculate torque
    tau = np.where(omega > motor['speed_noload'], 0,
        np.where(omega < 0, motor['torque_stall'])
        )
    return tau


def F_drive(omega, rover): #Returns the force applied to the rover by the drive system given information about the drive
                        #system (wheel_assembly) and the motor shaft speed.
    
    # raise errors
    if not isinstance(omega, (int, float,np.ndarray)): 
        raise   TypeError("Error: Invalid input type. Expected a number.")
    if not isinstance(rover, dict): 
        raise   TypeError("Error: Invalid input type. Expected a dictionary.")

    # pull in variables from rover dict
    tau_dcmotor = tau_dcmotor(omega, rover['wheel_assembly']['motor'])
    Ng = get_gear_ratio(rover['wheel_assembly']['speed_reducer'])
    r_wheel = rover['wheel_assembly']['wheel']['diameter']/2
    
    # equation for F_drive of the whole rover
    F_d = (tau_dcmotor * Ng) / r_wheel *6
    return F_d
    

def F_gravity(terrain_angle, rover, planet): #Returns the magnitude of the force component acting on the rover in the direction of its
                    #translational motion due to gravity as a function of terrain inclination angle and rover
                    #properties.
    # Raise errors
    if not isinstance(terrain_angle, (int, float,np.ndarray)): 
        raise   TypeError("Error: Invalid input type. Expected a number.")
    if not isinstance (terrain_angle <= 75 and terrain_angle >= -75):
        raise ValueError("Error: Invalid input value. Expected a number between -75 and 75 degrees.")
    if not isinstance(rover, dict):
        raise   TypeError("Error: Invalid input type. Expected a dictionary.")
    if not isinstance(planet, dict):
        raise   TypeError("Error: Invalid input type. Expected a dictionary.")
    
    # pull in variables from rover and planet dicts
    mass = get_mass(rover)
    g = planet['gravity']
    theta = np.radians(terrain_angle)

    # equation for F_gravity x-axis
    Fgt = mass * g * np.sin(theta)
    if theta < 0:
        Fgt = -Fgt
    return Fgt 
    
    

def F_rolling(omega, terrain_angle, rover, planet, Crr): #Returns the magnitude of the force acting on the rover in the direction of its translational
               #motion due to rolling resistances given the terrain inclination angle, rover properties, and a
                #rolling resistance coefficient.
    # Raise errors
    if not isinstance(omega, (int, float,np.ndarray)): 
        raise   TypeError("Error: Invalid input type. Expected a number.")
    if not isinstance(terrain_angle, (int, float,np.ndarray)): 
        raise   TypeError("Error: Invalid input type. Expected a number.")
    if not isinstance(len(terrain_angle) == len(omega)):
        raise ValueError("Error: Invalid input value. Expected omega and terrain_angle to be the same length.")
    if not isinstance (terrain_angle <= 75 and terrain_angle >= -75): 
        raise ValueError("Error: Invalid input value. Expected a number between -75 and 75 degrees.")
    if not isinstance(rover, dict):
        raise   TypeError("Error: Invalid input type. Expected a dictionary.")
    if not isinstance(planet, dict):    
        raise   TypeError("Error: Invalid input type. Expected a dictionary.")
    if not isinstance(Crr, (int, float) and Crr >= 0): 
        raise   TypeError("Error: Invalid input type. Expected a number or positive value.")
    

    # rolling resistance over the whole rover
    F_normal = get_mass(rover) * planet['gravity'] * np.cos(np.radians(terrain_angle))
    F_r = Crr * F_normal
    v_rover = omega * get_gear_ratio(rover) * (rover['wheel_assembly']['wheel']['diameter']/2)
    Frr = m.erf(40 * v_rover)*F_r
    return Frr


def F_net(omega, terrain_angle, rover, planet, Crr): #Returns the magnitude of net force acting on the rover in the direction of its translational
            #motion.
    # Raise errors
    if not isinstance(omega, (int, float,np.ndarray)): 
        raise   TypeError("Error: Invalid input type. Expected a number.")
    if not isinstance(terrain_angle, (int, float,np.ndarray)): 
        raise   TypeError("Error: Invalid input type. Expected a number.")
    if not isinstance(len(terrain_angle) == len(omega)):
        raise ValueError("Error: Invalid input value. Expected omega and terrain_angle to be the same length.")
    if not isinstance (terrain_angle <= 75 and terrain_angle >= -75): 
        raise ValueError("Error: Invalid input value. Expected a number between -75 and 75 degrees.")
    if not isinstance(rover, dict):
        raise   TypeError("Error: Invalid input type. Expected a dictionary.")
    if not isinstance(planet, dict):    
        raise   TypeError("Error: Invalid input type. Expected a dictionary.")
    if not isinstance(Crr, (int, float) and Crr >= 0): 
        raise   TypeError("Error: Invalid input type. Expected a number or positive value.")
    
    # F Net over the whole rover
    omega = np.asarray(omega)
    terrain_angle = np.asarray(terrain_angle)

    F_drive = F_drive(omega, rover)
    F_gravity = F_gravity(terrain_angle, rover, planet)
    F_rolling = F_rolling(omega, terrain_angle, rover, planet, Crr)
    F_net = F_drive - F_gravity - F_rolling 

    return F_net