THRESHOLD = 1500  # adjust for your robot

def on_line():
    left = robot.left_line_sensor.read()
    right = robot.right_line_sensor.read()
    return (left < THRESHOLD) or (right < THRESHOLD)

def search_for_line():
    sweep_angle = 20    # degrees
    max_sweep = 120     # do not rotate endlessly

    # Move forward while looking for the line
    robot.set_motor_power(0.15, 0.15)
    for _ in range(200):   # adjust distance if needed
        if on_line():
            robot.stop()
            center_on_line()
            return
        time.sleep(0.02)
    
    robot.stop()

    # If forward search fails, begin sweeping pattern
    angle = sweep_angle
    direction = 1

    while angle <= max_sweep:
        # Rotate to one side
        robot.turn_degrees(direction * angle)

        # Move forward slowly and check for line
        robot.set_motor_power(0.1, 0.1)
        for _ in range(150):
            if on_line():
                robot.stop()
                center_on_line()
                return
            time.sleep(0.02)
        robot.stop()

        # Reverse rotation
        robot.turn_degrees(-direction * angle)

        # Increase sweep
        direction *= -1
        angle += sweep_angle

    # If we reach here, something is wrong (line too far or lost)
    print("Line not found!")

search_for_line()