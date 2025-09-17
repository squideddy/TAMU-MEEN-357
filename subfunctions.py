import numpy as np
import math as m


def get_mass(rover): # Computes the total mass of the rover. Uses information in the rover dict.

    #raise errors
    if not isinstance(rover, dict): 
        raise  Exception("Error: Invalid input type. Expected a dictionary.")
    
    # find the masses of all components and sum them
    mass_tot_wheels = (rover['wheel_assembly']['wheel']['mass'] + rover['wheel_assembly']['speed_reducer']['mass']
                       + rover['wheel_assembly']['motor']['mass']) 
    mass_tot_chassis = rover['chassis']['mass'] + rover['science_payload']['mass'] + rover['power_subsys']['mass']
    m = mass_tot_wheels*6 + mass_tot_chassis

    return m

############################################################################################################
def get_gear_ratio(speed_reducer): #Returns the speed reduction ratio for the speed reducer based on speed_reducer dict.
    #gear ratio = diam_gear/diam_pinion
    
    # Raise errors
    if not isinstance(speed_reducer, dict): 
        raise  Exception("Error: Invalid input type. Expected a dictionary.")
    
    if not speed_reducer['type'].lower() == 'reverted': 
        raise  Exception("Error: Invalid input type. Expected a string with value 'reverted'.")
    
    # Calculate gear ratio
    Ng = (speed_reducer['diam_gear']/speed_reducer['diam_pinion'])**2
    return Ng

############################################################################################################
def tau_dcmotor(omega, motor): #Returns the motor shaft torque when given motor shaft speed and a dictionary containing
                        #important specifications for the motor.
    
    # Raise errors
    if isinstance(omega, np.ndarray):
        if omega.ndim != 1:
            raise Exception("Error: Invalid input type. Expected a acalar or vector numpy array of size 1.")
    elif not isinstance(omega, (int, float)):
        raise TypeError("Error: Invalid input type. Expected a scalar or vector.")
    if not isinstance(motor, dict):
        raise Exception("Error: Invalid input type. Expected a dictionary.")

    
    # Calculate torque
    mid_tau = motor['torque_stall'] - (motor['torque_stall'] - motor['torque_noload'])/(motor['speed_noload'])*omega
    tau = np.where(omega > motor['speed_noload'], 0, np.where(omega < 0, motor['torque_stall'], mid_tau))

    return tau

############################################################################################################
def F_drive(omega, rover): #Returns the force applied to the rover by the drive system given information about the drive
                        #system (wheel_assembly) and the motor shaft speed.
    
    # raise errors
    if not np.any(isinstance(omega, (int, float, np.ndarray))): 
        raise  Exception("Error: Invalid input type. Expected a number or numpy array of size 1.")
    
    if isinstance(omega, np.ndarray) and len(omega.shape) != 1:
        raise  Exception("Error: Invalid input type. Expected a number or numpy array of size 1.")
    if not isinstance(rover, dict): 
        raise   TypeError("Error: Invalid input type. Expected a dictionary.")



    # pull in variables from rover dict
    tau = tau_dcmotor(omega, rover['wheel_assembly']['motor'])
    Ng = get_gear_ratio(rover['wheel_assembly']['speed_reducer'])
    r_wheel = rover['wheel_assembly']['wheel']['radius']
    
    # equation for F_drive of the whole rover
    F_d = (tau * Ng) / r_wheel * 6

    return F_d
    
############################################################################################################
def F_gravity(terrain_angle, rover, planet): #Returns the magnitude of the force component acting on the rover in the direction of its
                    #translational motion due to gravity as a function of terrain inclination angle and rover
                    #properties.
    # Raise errors
    if isinstance(terrain_angle, np.ndarray):
        if len(terrain_angle.shape) != 1:
            raise Exception("Error: Invalid input type. Expected a number or numpy array of size 1.")
    elif not np.all(isinstance(terrain_angle, (int, float))):
        raise Exception("Error: Invalid input type. Expected a number or float.")
    
    if not (np.all(terrain_angle <= 75) and np.all(terrain_angle >= -75)):
        raise ValueError("Error: Invalid input value. Expected a number between  -75 and 75 degrees.")
    if not isinstance(rover, dict):
        raise  TypeError("Error: Invalid input type. Expected a dictionary.")
    if not isinstance(planet, dict):
        raise  TypeError("Error: Invalid input type. Expected a dictionary.")

    # pull in variables from rover and planet dicts
    mass = get_mass(rover)
    g = planet['g']
    theta = np.radians(terrain_angle)

    # equation for F_gravity x-axis
    Fgt = mass * g * np.sin(theta)
    
    Fgt = np.where(theta < 0, -Fgt, Fgt)
    
    return Fgt 
    
    
############################################################################################################
def F_rolling(omega, terrain_angle, rover, planet, Crr): #Returns the magnitude of the force acting on the rover in the direction of its translational
               #motion due to rolling resistances given the terrain inclination angle, rover properties, and a
                #rolling resistance coefficient.
    # Raise errors
    if isinstance(omega, np.ndarray):
        if len(omega.shape) != 1:
            raise Exception("Error: Invalid input type. Expected a number or numpy array of size 1.")
    elif not np.all(isinstance(omega, (int, float))):
        raise Exception("Error: Invalid input type. Expected a number or float.")
   
    if isinstance(terrain_angle, np.ndarray):
        if len(terrain_angle.shape) != 1:
            raise Exception("Error: Invalid input type. Expected a number or numpy array of size 1.")
        elif len(terrain_angle) != len(omega):
            raise Exception("Error: Invalid input value. Expected omega and terrain_angle to be the same size.")
    elif not np.all(isinstance(terrain_angle, (int, float))):
        raise Exception("Error: Invalid input type. Expected a number or float.")
    if not np.all((terrain_angle <= 75) & (terrain_angle >= -75)):
        raise ValueError("Error: Invalid input value. Expected a number between -75 and 75 degrees.")
    if not isinstance(rover, dict):
        raise  Exception("Error: Invalid input type. Expected a dictionary.")
    if not isinstance(planet, dict):    
        raise  Exception("Error: Invalid input type. Expected a dictionary.")
    if not isinstance(Crr, (int, float, np.ndarray)) and Crr >= 0: 
        raise  Exception("Error: Invalid input type. Expected a number or positive value.")
    
    print(omega, terrain_angle, rover, planet, Crr, type(omega), type(terrain_angle), type(rover), type(planet), type(Crr))
    
    
    # rolling resistance over the whole rover
    F_normal = get_mass(rover) * planet['g'] * np.cos(np.radians(terrain_angle))
    F_r = Crr * F_normal
    v_rover = (omega * get_gear_ratio(rover) * (rover['wheel_assembly']['wheel']['diameter']/2))
    Frr = m.erf(40 * v_rover) * F_r

    return Frr

############################################################################################################
def F_net(omega, terrain_angle, rover, planet, Crr): #Returns the magnitude of net force acting on the rover in the direction of its translational
            #motion.
    # Raise errors
    
    if isinstance(omega, np.ndarray):
        if len(omega.shape) != 1:
            raise Exception("Error: Invalid input type. Expected a number or numpy array of size 1.")
    elif not np.all(isinstance(omega, (int, float))):
        raise Exception("Error: Invalid input type. Expected a number or float.")
   
    if isinstance(terrain_angle, np.ndarray):
        if len(terrain_angle.shape) != 1:
            raise Exception("Error: Invalid input type. Expected a number or numpy array of size 1.")
        elif len(terrain_angle) != len(omega):
            raise Exception("Error: Invalid input value. Expected omega and terrain_angle to be the same size.")
    elif not np.all(isinstance(terrain_angle, (int, float))):
        raise Exception("Error: Invalid input type. Expected a number or float.")
    if not np.all((terrain_angle <= 75) & (terrain_angle >= -75)):
        raise ValueError("Error: Invalid input value. Expected a number between -75 and 75 degrees.")
    if not isinstance(rover, dict):
        raise  Exception("Error: Invalid input type. Expected a dictionary.")
    if not isinstance(planet, dict):    
        raise  Exception("Error: Invalid input type. Expected a dictionary.")
    if not isinstance(Crr, (int, float, np.ndarray)) and Crr >= 0: 
        raise  Exception("Error: Invalid input type. Expected a number or positive value.")
    
    # F Net over the whole rover
    F_drive_u = F_drive(omega, rover)
    F_g_u = F_gravity(terrain_angle, rover, planet)
    F_rolling_u = F_rolling(omega, terrain_angle, rover, planet, Crr)
    F_net = F_drive_u + F_g_u + F_rolling_u

    return F_net