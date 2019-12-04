from config import *
from visual_control import convert_vel_to_PWM

dist_traveled_straight, dist_turned = 0, 0
need_to_square = True
pwm = convert_vel_to_PWM(TURN_SPEED_LIMIT)

# TODO Account for moving start
# TODO Account for tilted start
# Go Straight and then maybe turn, then return
# returns l_motor r_motor, done
def open_compute_motor_values(prev_hug, traversal_type, delta_l_encoder, delta_r_encoder):
    global dist_traveled_straight, dist_turned, need_to_square, pwm
    
    if need_to_square:
        need_to_square = False
        if prev_hug:
            return pwm, 0, False
        else:
            return 0, pwm, False

    # set parameters
    # TODO convert to 2, 0, 1
    if traversal_type == "straight":
        straight_goal = STRAIGHT_DIST
        turn_goal = 0

    if traversal_type == "left":
        straight_goal = LEFT_TURN_DIST
        turn_goal = QUARTER_TURN
    
    if traversal_type == "right":
        straight_goal = DIST_FROM_STOP_LINE
        turn_goal = QUARTER_TURN

    # update distances traveled
    if dist_traveled_straight < straight_goal:
        dist_traveled_straight += ((delta_l_encoder + delta_r_encoder) / 2) * CM_PER_TICK
    else:
        # one of these should be zero
        dist_turned += (delta_l_encoder + delta_r_encoder) * CM_PER_TICK
    

    # if we haven't gone straight far enough go straight
    if dist_traveled_straight < straight_goal:
        return pwm, pwm, False
    
    # if we have gone straight far enough turn
    if dist_turned < turn_goal:
        if traversal_type == "left":
            return pwm, 0, False
        else:
            return 0, pwm, False
    else:
        # reset globals and pass control
        dist_traveled_straight, dist_turned = 0, 0
        need_to_square = True
        return pwm, pwm, True