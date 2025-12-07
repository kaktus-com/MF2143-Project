from XRPLib.differential_drive import DifferentialDrive
drivetrain = DifferentialDrive.get_default_differential_drive()

LINEUP_TURN_SPEED = 12.0        # Drive speed when lining up object
DRIVE_SPEED = 20.0
BASKET_X_TARGET = 0.4           # Where the basket X should be for pickup
BASKET_X_DEADZONE = 0.02        # Basket center X can be lined up +/- this val
BASKET_Y_TARGET = 0.82          # Where the basket Y should be for pickup
BASKET_Y_DEADZONE = 0.02        # Basket center Y can be lined up +/- this val
TARGET_X_TARGET = 0.36          # Where the target X should be for dropoff
TARGET_X_DEADZONE = 0.02        # Target center X can be lined up +/- this val
TARGET_Y_TARGET = 0.8           # Where the target Y should be for dropoff
TARGET_Y_DEADZONE = 0.05  

def drive_to(x_center, y_center, width, height):
    global drivetrain
    if width == 0 and height == 0:
        print("Driving to coordinates:", x_center, y_center)

        X_TOLERANCE = 0.05
        Y_TOLERANCE = 0.05

        # Turn left/right based on x
        if x_center < -X_TOLERANCE:
            drivetrain.set_speed(-LINEUP_TURN_SPEED, LINEUP_TURN_SPEED)
            return

        if x_center > X_TOLERANCE:
            drivetrain.set_speed(LINEUP_TURN_SPEED, -LINEUP_TURN_SPEED)
            return

        # Drive forward/backward based on y
        if y_center < -Y_TOLERANCE:
            drivetrain.set_speed(DRIVE_SPEED, DRIVE_SPEED)
            return

        if y_center > Y_TOLERANCE:
            drivetrain.set_speed(-DRIVE_SPEED, -DRIVE_SPEED)
            return

        # When both X and Y are within tolerance:
        drivetrain.set_speed(0, 0)
        print("Reached target coordinates")
        return

    # Case when width and height are provided (e.g., lining up with basket)
    x_done = False
    wait_counter = 0

    if x_center < (BASKET_X_TARGET - BASKET_X_DEADZONE):
        drivetrain.set_speed(-LINEUP_TURN_SPEED, LINEUP_TURN_SPEED)
    elif x_center > (BASKET_X_TARGET + BASKET_X_DEADZONE):
        drivetrain.set_speed(LINEUP_TURN_SPEED, -LINEUP_TURN_SPEED)
    else:
        drivetrain.set_speed(0.0, 0.0)
        x_done = True

    # If X is lined up, line up Y
    if x_done:
        if y_center < (BASKET_Y_TARGET - BASKET_Y_DEADZONE):
            drivetrain.set_speed(DRIVE_SPEED, DRIVE_SPEED)
            wait_counter = 0
        elif y_center > (BASKET_Y_TARGET + BASKET_Y_DEADZONE):
            drivetrain.set_speed(-DRIVE_SPEED, -DRIVE_SPEED)
            wait_counter = 0
        else:
            wait_counter += 1
            if wait_counter >= 5:
                print(f"Getting basket: ({x_center:.3f}, {y_center:.3f})")
                drivetrain.set_speed(0.0, 0.0)
                time.sleep(1.0)
                # current_state = 2  # You should change state in main loop, not inside drive_to
