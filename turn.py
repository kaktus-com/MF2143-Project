def turn(drivetrain, degrees):
    """
    Very hacky way of turning: simply measure one encoder until it reaches a set
    point. This is because drivetrain.turn() is bugged and enter a forever loop
    of turning. Warning: this function is not very accurate!
    """
    
    # Get starting positions
    left_start = drivetrain.left_motor.get_position()
    right_start = drivetrain.right_motor.get_position()
    
    # Set direction and speed
    if degrees == 0.0:
        return
    elif degrees > 0.0:
        drivetrain.set_speed(
            left_speed=SEARCH_TURN_SPEED,
            right_speed=-SEARCH_TURN_SPEED
        )
        target_pos = (degrees / 360) * WHEEL_ROT_PER_ROBOT_ROT
    elif degrees < 0.0:
        drivetrain.set_speed(
            left_speed=-SEARCH_TURN_SPEED,
            right_speed=SEARCH_TURN_SPEED
        )
        target_pos = -(degrees / 360) * WHEEL_ROT_PER_ROBOT_ROT
        
    # Turn until desired position
    while True:
        left_pos = drivetrain.left_motor.get_position()
        right_pos = drivetrain.right_motor.get_position()
        if (abs(left_pos - left_start) >= target_pos) or \
            (abs(right_pos - right_start) >= target_pos):
            break

    drivetrain.set_speed(left_speed=0.0, right_speed=0.0)