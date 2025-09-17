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
    """
    Force component along the direction of motion due to gravity.
    Positive terrain_angle (uphill) should yield NEGATIVE force.
    Inputs:
      - terrain_angle: scalar (deg) or 1-D vector (deg)
      - rover: dict (must be a dictionary)
      - planet: dict with gravity in m/s^2 (key 'gravity' or 'g')
    """
    # --- validate rover & planet dicts ---
    if not isinstance(rover, dict):
        raise Exception("Error: Invalid input type. Expected rover to be a dictionary.")
    if not isinstance(planet, dict):
        raise Exception("Error: Invalid input type. Expected planet to be a dictionary.")

    # --- get gravity (m/s^2) ---
    if 'gravity' in planet:
        g = planet['gravity']
    elif 'g' in planet:
        g = planet['g']
    else:
        raise Exception("Error: planet dictionary must include 'gravity' (m/s^2).")

    # --- normalize angle to numpy array, allow scalar or 1-D vector ---
    theta_arr = np.asarray(terrain_angle)
    if theta_arr.ndim > 1:
        raise Exception("Error: Invalid input type. Expected terrain_angle to be a scalar or 1-D vector.")

    # --- range check in degrees ---
    if theta_arr.ndim == 0:
        theta_deg = float(theta_arr)
        if not (-75.0 <= theta_deg <= 75.0):
            raise Exception("Error: Invalid input value. terrain_angle must be between -75 and 75 degrees.")
        # physics (units: N)
        m_rover = get_mass(rover)                 # MUST call get_mass
        theta_rad = np.deg2rad(theta_deg)
        # sign convention: uphill (+θ) => negative force
        return float(- m_rover * g * np.sin(theta_rad))
    else:
        # 1-D vector
        if not np.all((-75.0 <= theta_arr) & (theta_arr <= 75.0)):
            raise Exception("Error: Invalid input value. All terrain_angle elements must be between -75 and 75 degrees.")
        m_rover = get_mass(rover)
        theta_rad = np.deg2rad(theta_arr.astype(float))
        return - m_rover * g * np.sin(theta_rad)
    
############################################################################################################
def F_rolling(omega, terrain_angle, rover, planet, Crr): #Returns the magnitude of the force acting on the rover in the direction of its translational
               #motion due to rolling resistances given the terrain inclination angle, rover properties, and a
                #rolling resistance coefficient.
    try:
        from scipy.special import erf as erf_vec
    except Exception:
        import math as m
        erf_vec = np.vectorize(m.erf, otypes=[float])
   # --- normalize inputs ---
    om = np.asarray(omega)
    th = np.asarray(terrain_angle)

    # --- shape/type validation ---
    if om.ndim > 1 or th.ndim > 1:
        raise Exception("Error: Invalid input type. Expected omega and terrain_angle to be scalars or 1-D vectors.")
    # same length or one scalar
    if om.size != 1 and th.size != 1 and om.size != th.size:
        raise Exception("Error: Invalid input value. Expected omega and terrain_angle to be the same length or one scalar.")
    # angle range
    if not np.all((-75.0 <= th) & (th <= 75.0)):
        raise Exception("Error: Invalid input value. Expected a number between -75 and 75 degrees.")
    # dicts
    if not isinstance(rover, dict):
        raise Exception("Error: Invalid input type. Expected a dictionary.")
    if not isinstance(planet, dict):
        raise Exception("Error: Invalid input type. Expected a dictionary.")
 

    # rolling resistance over the whole rover
    F_normal = get_mass(rover) * planet['g'] * np.cos(np.radians(th))
    F_r = Crr * F_normal
    sr = rover['wheel_assembly']['speed_reducer']
    v_rover = (om / get_gear_ratio(sr)) * (rover['wheel_assembly']['wheel']['radius'])
    Frr = -erf_vec(40 * v_rover)*F_r
    
    # scalar in -> scalar out
    if om.ndim == 0 and th.ndim == 0:
        return float(np.asarray(Frr).reshape(()))
    return Frr.astype(float)
#############################################################################################
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