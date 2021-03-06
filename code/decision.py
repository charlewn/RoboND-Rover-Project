import numpy as np
from pprint import pprint

# This is where you can build a decision tree for determining throttle, brake and steer 
# commands based on the output of the perception_step() function

def decision_step(Rover):

    # Implement conditionals to decide what to do given perception data
    # Here you're all set up with some basic functionality but you'll need to
    # improve on this decision tree to do a good job of navigating autonomously!
    print('----rovering----')
    print(Rover)
    # Example:
    # Check if we have vision data to make decisions with

    """
    speed = 0.7073 position = [101.469, 85.5209] 
    throttle = 0.2 steer_angle = 15.0 near_sample: 0 
    picking_up: 0 sending pickup: False total 
    time: 4.925782203674316 samples remaining: 6 samples found: 0
    """

    """
    Stuck:
    speed = 0.0 position = [99.7821, 76.0712] 
    throttle = 0.4 steer_angle = -15.0 
    near_sample: 0 picking_up: 0 
    sending pickup: False total time: 121.9631609916687 
    samples remaining: 6 samples found: 0

    """

    if Rover.nav_angles is not None:
        # Check for Rover.mode status
        if Rover.mode == 'forward': 
            # Check the extent of navigable terrain
            if len(Rover.nav_angles) >= Rover.stop_forward:  
                # If mode is forward, navigable terrain looks good 
                # and velocity is below max, then throttle 
                if Rover.vel < Rover.max_vel:
                    # Set throttle value to throttle setting
                    Rover.throttle = Rover.throttle_set
                else: # Else coast
                    Rover.throttle = 0
                Rover.brake = 0
                # Set steering to average angle clipped to the range +/- 15
                # print(np.clip(np.mean(Rover.nav_angles * 180/np.pi), -10, 10))
                Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -30, 30)
            # If there's a lack of navigable terrain pixels then go to 'stop' mode
            elif len(Rover.nav_angles) < Rover.stop_forward:
                    # Set mode to "stop" and hit the brakes!
                    Rover.throttle = 0
                    # Set brake to stored brake value
                    Rover.brake = Rover.brake_set
                    Rover.steer = 0
                    Rover.mode = 'stop'

        # If we're already in "stop" mode then make different decisions
        elif Rover.mode == 'stop':
            # If we're in stop mode but still moving keep braking
            if Rover.vel > 0.2:
                Rover.throttle = 0
                Rover.brake = Rover.brake_set
                Rover.steer = 0
            # If we're not moving (vel < 0.2) then do something else
            elif Rover.vel <= 0.2:
                # Now we're stopped and we have vision data to see if there's a path forward
                if len(Rover.nav_angles) < Rover.go_forward:
                    Rover.throttle = 0
                    # Release the brake to allow turning
                    Rover.brake = 0
                    # Turn range is +/- 15 degrees, when stopped the next line will induce 4-wheel turning
                    Rover.steer = -30 # Could be more clever here about which way to turn
                # If we're stopped but see sufficient navigable terrain in front then go!
                if len(Rover.nav_angles) >= Rover.go_forward:
                    # Set throttle back to stored value
                    Rover.throttle = Rover.throttle_set
                    # Release the brake
                    Rover.brake = 0
                    
                    # Set steer to mean angle minus an offset for following walls
                    steering_offset = 10

                    steering_angle = np.mean(Rover.nav_angles * 180/np.pi) - steering_offset

                    Rover.steer = np.clip(steering_angle, -30, 30)

                    Rover.mode = 'forward'
    # Just to make the rover do something 
    # even if no modifications have been made to the code
    else:
        Rover.throttle = Rover.throttle_set
        Rover.steer = 0
        Rover.brake = 0
        
    # If in a state where want to pickup a rock send pickup command
    if Rover.near_sample and not Rover.picking_up:
        Rover.throttle = 0
        Rover.brake = Rover.brake_set # need to brake_set to pick up
        Rover.steer = 0
        if Rover.vel == 0 and Rover.near_sample:
            Rover.send_pickup = True
    # this is not picking up
    # if Rover.near_sample and Rover.vel == 0 and not Rover.picking_up:
    #    Rover.send_pickup = True
    
    return Rover

