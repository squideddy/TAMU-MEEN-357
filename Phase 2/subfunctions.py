
from asyncio import events
import numpy as np
import math as m

# PART 1 SUBFUNCTIONS BELOW 
############################################################################################################
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
        if omega.ndim > 1:
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
    
    if isinstance(omega, np.ndarray) and len(omega.shape) > 1:
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
############################################################################################################




# PART 2 SUBFUNCTIONS BELOW
############################################################################################################

def motorW(v,rover): # v is 1D array translational velocity, rover is dictionary, calling will be w = motorW(v,rover) and returns motor speed [rad/s]
    """
    Computes the motor speed [rad/s] given the translational velocity [m/s] and rover dictionary.
    """
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

############################################################################################################

def rover_dynamics(t, y, rover, planet, experiment): 
    """
    Compute state derivative for the rover.
      y[0] = velocity [m/s]
      y[1] = position [m]
    Returns:
      dydt[0] = acceleration [m/s^2]
      dydt[1] = velocity [m/s]
    """
    from scipy.interpolate import interp1d

    # validate y
    y_arr = np.asarray(y, dtype=float).reshape(-1)
    if y_arr.size != 2:
        raise Exception("Error: y must be a 1D array-like with two elements: [velocity, position].")
    v, x = float(y_arr[0]), float(y_arr[1])

    # validate dicts
    if not isinstance(rover, dict):
        raise Exception("Error: 'rover' must be a dictionary.")
    if not isinstance(planet, dict):
        raise Exception("Error: 'planet' must be a dictionary.")
    if not isinstance(experiment, dict):
        raise Exception("Error: 'experiment' must be a dictionary.")

    # get experiment data
    try:
        alpha_dist = np.asarray(experiment['alpha_dist'], dtype=float)
        alpha_deg  = np.asarray(experiment['alpha_deg'],  dtype=float)
    except KeyError as e:
        raise Exception(f"Error: experiment missing key {e!s} ('alpha_dist' and 'alpha_deg' required).")

    if alpha_dist.ndim != 1 or alpha_deg.ndim != 1 or alpha_dist.size != alpha_deg.size:
        raise Exception("Error: alpha_dist and alpha_deg must be 1D arrays of equal length.")

    # Rolling resistance coefficient
    if 'Crr' not in experiment:
        raise Exception("Error: experiment must include 'Crr' (rolling resistance coefficient).")
    Crr = float(experiment['Crr'])
    if Crr <= 0:
        raise Exception("Error: 'Crr' must be a positive scalar.")

    # terrain angle at current position (degrees)
    alpha_fun = interp1d(alpha_dist, alpha_deg, kind='cubic', fill_value='extrapolate')
    terrain_angle_deg = float(alpha_fun(x))

    # dynamics: compute motor speed, forces, acceleration
    omega = motorW(v, rover)  # [rad/s], uses your get_gear_ratio & wheel radius
    F     = F_net(omega, terrain_angle_deg, rover, planet, Crr)  # net force [N]
    m     = get_mass(rover)  # [kg]
    a     = F / m            # [m/s^2]

    # derivative of state
    return np.array([a, v], dtype=float)

############################################################################################################

def mechpower(v, rover): #computes the mechanical power output of the rover's drive system given velocity v [m/s] and rover dictionary
    """
    Computes the mechanical power output of the rover's drive system given velocity v [m/s] and rover dictionary.
    """
    if not isinstance(v, (int, float, np.ndarray)):
        raise Exception("Error: 'v' must be a scalar or 1D numpy array of numbers.")
    elif isinstance(v, np.ndarray) and v.ndim > 1:
        raise Exception("Error: 'v' must be a 1D numpy array of numbers.")
    if not isinstance(rover, dict):
        raise Exception("Error: 'rover' must be a dictionary.")
    # retrieving torque and motor speed to compute mechanical power
    torque_motor = tau_dcmotor(motorW(v, rover), rover['wheel_assembly']['motor'])
    motorw = motorW(v, rover) # rad/sec
    #compute mechanical power
    P_mech = torque_motor * motorw 
    return P_mech # [W] for one wheel

def battenergy(t,v,rover): #computes the total battery energy consumed over time t [s] given velocity v [m/s] and rover dictionary
    """
    Computes the total battery energy consumed over time t [s] 
    given velocity v [m/s] and rover dictionary.
    """

  # (a) Validate t and v
    if not isinstance(t, np.ndarray):
        raise Exception("Error: 't' must be a NumPy array.")
    if not isinstance(v, np.ndarray):
        raise Exception("Error: 'v' must be a NumPy array.")
    if t.ndim != 1 or v.ndim != 1:
        raise Exception("Error: 't' and 'v' must both be 1D vectors.")
    if t.size != v.size:
        raise Exception("Error: 't' and 'v' must have the same length.")
    if not np.issubdtype(t.dtype, np.number) or not np.issubdtype(v.dtype, np.number):
        raise Exception("Error: 't' and 'v' must contain numeric values only.")

    # (b) Validate rover
    if not isinstance(rover, dict):
        raise Exception("Error: 'rover' must be a dictionary.")

   
    P_mech = mechpower(v, rover) # [W] 
    omega = motorW(v, rover)
    tau = tau_dcmotor(omega, rover['wheel_assembly']['motor'])

    #efficiency interpolation function for torque
    effcy_tau = rover['wheel_assembly']['motor']['efficiency']['effcy_tau']
    effcy_vals = rover['wheel_assembly']['motor']['efficiency']['effcy']
    effcy_fun = sp.interp1d(effcy_tau, effcy_vals, kind='cubic', fill_value="extrapolate")
    eta = effcy_fun(tau)

    # Integrate electrical power over time to get battery energy consumed
    # Electrical power input to all six motors
    P_elec = np.where(eta<= 1e-9, 0, P_mech / eta) * 6 # [W]
    E_batt = np.trapz(P_elec, t)  # [J]

    return E_batt

def end_of_mission_event(end_event):
    """
    Defines an event that terminates the mission simulation. Mission is over
    when rover reaches a certain distance, has moved for a maximum simulation
    time or has reached a minimum velocity.
    """
    mission_distance = end_event['max_distance']
    mission_max_time = end_event['max_time']
    mission_min_velocity = end_event['min_velocity']
    # Assume that y[1] is the distance traveled
    distance_left = lambda t,y: mission_distance - y[1]
    distance_left.terminal = True
    time_left = lambda t,y: mission_max_time - t
    time_left.terminal = True
    velocity_threshold = lambda t,y: y[0] - mission_min_velocity
    velocity_threshold.terminal = True
    velocity_threshold.direction = -1
    # terminal indicates whether any of the conditions can lead to the
    # termination of the ODE solver. In this case all conditions can terminate
    # the simulation independently.
    # direction indicates whether the direction along which the different
    # conditions is reached matters or does not matter. In this case, only
    # the direction in which the velocity treshold is arrived at matters
    # (negative)
    events = [distance_left, time_left, velocity_threshold]
    return events



def simulate_rover(rover, planet, experiment, end_event): 
    """
    Main function that integrates the trajectory of a rover
    solves the IVP for the rover dynamics over the specified time range
    Returns time array, velocity array, position array.
    """
    from scipy.integrate import solve_ivp

    # validate dicts
    if not isinstance(rover, dict):
        raise Exception("Error: 'rover' must be a dictionary.")
    if not isinstance(planet, dict):
        raise Exception("Error: 'planet' must be a dictionary.")
    if not isinstance(experiment, dict):
        raise Exception("Error: 'experiment' must be a dictionary.")
    if not isinstance(end_event, dict):
        raise Exception("Error: 'end_event' must be a dictionary.")

    # get experiment data
    # should populate the telemetry dictionary in rover
    
    try:
        time_range = np.asarray(experiment['time_range'], dtype=float)
        initial_conditions = np.asarray(experiment['initial_conditions'], dtype=float)
    except KeyError as e:
        raise Exception(f"Error: experiment missing key {e!s} ('time_range' and 'initial_conditions' required).")
    if time_range.ndim != 1 or time_range.size != 2:
        raise Exception("Error: time_range must be a 1D array of length 2.")
    if initial_conditions.ndim != 1 or initial_conditions.size != 2:
        raise Exception("Error: initial_conditions must be a 1D array of length 2.")
    # define end of mission events
    events = end_of_mission_event(end_event)
    # integrate equations of motion
    sol = solve_ivp(fun=lambda t,y: rover_dynamics(t,y,rover,planet,experiment),
                    t_span=(time_range[0], time_range[1]),
                    y0=initial_conditions,
                    method='BDF',
                    events=events,
                    max_step=1.0)
    
    # store telemetry data
    rover['telemetry']['time'] = sol.t
    rover['telemetry']['velocity'] = sol.y[0,:]
    rover['telemetry']['position'] = sol.y[1,:]
    rover['telemetry']['completion_time'] = sol.t[-1]
    rover['telemetry']['distance_traveled'] = sol.y[1,-1] - initial_conditions[1]
    rover['telemetry']['max_velocity'] = np.max(sol.y[0,:])
    rover['telemetry']['average_velocity'] = rover['telemetry']['distance_traveled']/ rover['telemetry']['completion_time'] if rover['telemetry']['completion_time'] > 0 else 0.0
    rover['telemetry']['power'] = mechpower(sol.y[0,:], rover)
    rover['telemetry']['battery_energy'] = battenergy(sol.t, sol.y[0,:], rover)
    rover['telemetry']['energy_per_distance'] = (rover['telemetry']['battery_energy']/ rover['telemetry']['distance_traveled']) 
    return rover['telemetry']



