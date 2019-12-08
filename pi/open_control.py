from config import *
from visual_control import convert_vel_to_PWM

dist_traveled_straight, dist_turned, dist_second_straight = 0, 0, 0
need_to_square = True
pwm = convert_vel_to_PWM(TURN_SPEED_LIMIT)
# pwm_high = pwm * 1.05

# TODO Account for moving start
# TODO Account for tilted start
# Go Straight and then maybe turn, then return
# returns l_motor r_motor, done
def open_compute_motor_values(prev_hug, traversal_type, delta_l_encoder, delta_r_encoder, ping_distance):
    # If we encounter an obstruction VERY close in the intersection, 
    # we stop right away without bothering to match speed
    if(ping_distance < PING_MIN_INTERSECTION and ping_distance > 0):
        return 0, 0, False

    global dist_traveled_straight, dist_turned, dist_second_straight, need_to_square, pwm, pwm_high
    
    # if need_to_square:
    #     need_to_square = False
    #     if prev_hug:
    #         return pwm, 0, False
    #     else:
    #         return 0, pwm, False

    # set parameters
    # TODO convert to 2, 0, 1
    if traversal_type == TURN_S:
        straight_goal = STRAIGHT_DIST
        turn_goal = 0
        second_straight_goal = 0

    if traversal_type == TURN_L:
        straight_goal = LEFT_TURN_DIST
        turn_goal = LEFT_TURN
        second_straight_goal = LEFT_SECOND_STRAIGHT_DIST
    
    if traversal_type == TURN_R:
        straight_goal = DIST_FROM_STOP_LINE
        turn_goal = RIGHT_TURN
        second_straight_goal = 0

    # update distances traveled
    if dist_traveled_straight < straight_goal:
        dist_traveled_straight += ((delta_l_encoder + delta_r_encoder) / 2) * CM_PER_TICK
    else:# dist_turned < turn_goal:
        # one of these should be zero
        dist_turned += (delta_l_encoder + delta_r_encoder) * CM_PER_TICK
    # else:
    #     dist_second_straight += ((delta_l_encoder + delta_r_encoder) / 2) * CM_PER_TICK

    # if we haven't gone straight far enough go straight
    if dist_traveled_straight < straight_goal:
        # if delta_l_encoder >
        return pwm, pwm, False
    
    # if we have gone straight far enough turn
    if dist_turned < turn_goal:
        if traversal_type == TURN_L:
            return pwm, 0, False
        else:
            return 0, pwm, False
    # if dist_second_straight < second_straight_goal:
    #     return pwm, pwm, False
    else:
        # reset globals and pass control
        dist_traveled_straight, dist_turned, second_straight_goal = 0, 0, 0
        need_to_square = True
        return pwm, pwm, True
