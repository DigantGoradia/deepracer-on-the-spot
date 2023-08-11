import math

def reward_function(params):
    # Constants
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    speed = params['speed']
    progress = params['progress']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    abs_steering = abs(params['steering_angle'])
    on_track = params['all_wheels_on_track']

    # Fast Waypoints on track
    fast_waypoints = [138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]

    # Give higher reward for staying on the track and penalize for going off-track
    if distance_from_center <= track_width / 2:
        reward = 1.0
    else:
        reward = 1e-3

    #on track?
    if on_track:
        reward += 1
    else:
        reward += 1e-3

    # Reward the car for higher speed
    reward += speed

    # Calculate the direction of the previous waypoint
    prev_point = waypoints[closest_waypoints[0]]
    next_point = waypoints[closest_waypoints[1]]

    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    track_direction = math.degrees(track_direction)

    # Calculate the difference between the car's heading and the direction to the next waypoint
    heading_diff = abs(track_direction - heading)

    # Reward the car for heading alignment with the track
    if heading_diff < 10.0:
        reward += 0.5
    else:
        reward = 1e-3
        # Calculate the progress percentage
    track_len = len(waypoints)
    progress_percentage = progress / (track_len - 1)

    # Reward the car for making progress on the track
    reward += progress_percentage * 10.0

    #Prevent Zig-Zag
    ABS_STEERING_THRESHOLD=15
    if abs_steering > ABS_STEERING_THRESHOLD:
        reward *= 0.5

    return float(reward)