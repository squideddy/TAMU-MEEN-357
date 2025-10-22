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
def F_net(omega, terrain_angle, rover, planet, Crr):
    """
    Compute net force acting on rover in direction of motion.
    """

    # --- validate inputs ---
    om = np.asarray(omega)
    th = np.asarray(terrain_angle)

    # must be scalar or 1-D vector
    if om.ndim > 1 or th.ndim > 1:
        raise Exception("Error: omega and terrain_angle must be scalars or 1-D vectors.")

    # sizes must match (or one scalar)
    if om.size != 1 and th.size != 1 and om.size != th.size:
        raise Exception("Error: omega and terrain_angle must be the same length or one scalar.")

    # terrain angle check
    if not np.all((-75.0 <= th) & (th <= 75.0)):
        raise Exception("Error: terrain_angle values must be between -75 and 75 degrees.")

    # dict checks
    if not isinstance(rover, dict):
        raise Exception("Error: rover must be a dictionary.")
    if not isinstance(planet, dict):
        raise Exception("Error: planet must be a dictionary.")

    # Crr check
    if not isinstance(Crr, (int, float)) or Crr <= 0:
        raise Exception("Error: Crr must be a positive scalar.")

    # --- compute forces ---
    F_drive_u   = F_drive(om, rover)
    F_g_u       = F_gravity(th, rover, planet)
    F_rolling_u = F_rolling(om, th, rover, planet, Crr)

    return F_drive_u + F_g_u + F_rolling_u

############################################################################################################
def basic_bisection(fun, x1=0 , xu=2, err_max =1e-6, iter_max = 1000):
    # INitializaiton

    # actual number of iterations
    numIter = 0

    done = False

    err_est = np.nan
    root = np.nan
    range = xu - x1


    if fun(xu) == 0:
            root = xu
            done = True
            err_est = 0
    
    elif fun(x1) == 0:
            root = x1
            done = True
            err_est = 0

    # create a bisector
    while not done:
        numIter += 1

        # find the bisector
        average = (x1 + xu) / 2

        # evaluate the function at the bisector
        if fun(average) * fun(x1) < 0:
            xu = average
            if err_est < err_max or numIter == iter_max:
                done = True
                err_est = range / (2 ** numIter)
                root = average

        else:
            x1 = average
            if err_est < err_max or numIter == iter_max:
                done = True
                err_est = range / (2 ** numIter)
                root = average
    return root

def motorW(v,rover): # v is 1D array translational velocity, rover is dictionary, calling will be w = motorW(v,rover) and returns motor speed [rad/s]
     # Check numeric / array type
    if not isinstance(v, (int, float, np.ndarray)):
        raise Exception("Error: 'v' must be a scalar or 1D numpy array of numbers.")
    # Check type
    if not isinstance(rover, dict):
        raise Exception("Error: 'rover' must be a dictionary.")
    #Calculating motor angular velocity
    r = rover['wheel_assembly']['wheel']['radius']              # [m]
    Ng = get_gear_ratio(rover['wheel_assembly']['speed_reducer'])

    # Compute
    v_arr = np.asarray(v, dtype=float)
    w_motor = (v_arr / r) * Ng   # [rad/s]
    return w_motor if np.ndim(v) == 0 else w_motor
