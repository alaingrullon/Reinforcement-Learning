def reward_function(params):
    '''
    All wheels on track, spped min threshold, distance from center / marker
    Resulted in 66% (10.03s), 57% (08.23s), 74% (12.4s)
    '''
    
    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    all_wheels_on_track = params['all_wheels_on_track']
    steering = abs(params['steering_angle'])
    ABS_STEERING_THRESHOLD = 15
    speed = params['speed']
    SPEED_MIN_THRESHOLD = 1
    SPEED_MAX_THRESHOLD = 3

    # Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    
    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward = 1.0
    elif distance_from_center <= marker_2:
        reward = 0.7
    elif distance_from_center <= marker_3:
        reward = 0.2
    else:
        reward = 1e-3  # likely crashed/ close to off track
    
    # Penalize if the car goes off track
    if not all_wheels_on_track:
	    reward = 1e-3
    
    # Penalize if the car goes too slow
    elif speed <= SPEED_MIN_THRESHOLD:
        reward = reward + 0.7
    
    # Penalize if the car goes too fast
    elif speed >= SPEED_MAX_THRESHOLD:
        reward = reward + 0.5
    # Highest reward if the car stays on track and goes steady
    else:
        reward = reward + 1.0

    if steering > ABS_STEERING_THRESHOLD and speed >= SPEED_MAX_THRESHOLD:
        reward *= 0.4
    elif steering > ABS_STEERING_THRESHOLD and speed <= SPEED_MAX_THRESHOLD and speed <= SPEED_MIN_THRESHOLD:
        reward *= 0.6
    elif steering > ABS_STEERING_THRESHOLD and speed <= SPEED_MIN_THRESHOLD:
        reward *= 0.8
    
    return float(reward)