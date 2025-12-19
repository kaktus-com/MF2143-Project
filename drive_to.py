from XRPLib.differential_drive import DifferentialDrive
import time

drivetrain = DifferentialDrive.get_default_differential_drive()

LINEUP_TURN_SPEED = 12.0
DRIVE_SPEED = 20.0
BASKET_X_TARGET = 0.4
BASKET_X_DEADZONE = 0.02
BASKET_Y_TARGET = 0.82
BASKET_Y_DEADZONE = 0.02
TARGET_X_TARGET = 0.7
TARGET_X_DEADZONE = 0.02
TARGET_Y_TARGET = 0.8
TARGET_Y_DEADZONE = 0.05


def drive_to(x_center, y_center, width, height):
    global drivetrain

    if width == 0 and height == 0:
        X_TOLERANCE = 0.05
        Y_TOLERANCE = 0.05

        if x_center < -X_TOLERANCE:
            drivetrain.set_speed(-LINEUP_TURN_SPEED, LINEUP_TURN_SPEED)
            return

        if x_center > X_TOLERANCE:
            drivetrain.set_speed(LINEUP_TURN_SPEED, -LINEUP_TURN_SPEED)
            return

        if y_center < -Y_TOLERANCE:
            drivetrain.set_speed(DRIVE_SPEED, DRIVE_SPEED)
            return

        if y_center > Y_TOLERANCE:
            drivetrain.set_speed(-DRIVE_SPEED, -DRIVE_SPEED)
            return

        drivetrain.set_speed(0, 0)
        return

    x_done = False
    drive_to.wait_counter = getattr(drive_to, "wait_counter", 0)

    if x_center < (BASKET_X_TARGET - BASKET_X_DEADZONE):
        drivetrain.set_speed(-LINEUP_TURN_SPEED, LINEUP_TURN_SPEED)
        return

    elif x_center > (BASKET_X_TARGET + BASKET_X_DEADZONE):
        drivetrain.set_speed(LINEUP_TURN_SPEED, -LINEUP_TURN_SPEED)
        return

    else:
        drivetrain.set_speed(0.0, 0.0)
        x_done = True

    if x_done:
        if y_center < (BASKET_Y_TARGET - BASKET_Y_DEADZONE):
            drivetrain.set_speed(DRIVE_SPEED, DRIVE_SPEED)
            drive_to.wait_counter = 0
            return

        elif y_center > (BASKET_Y_TARGET + BASKET_Y_DEADZONE):
            drivetrain.set_speed(-DRIVE_SPEED, -DRIVE_SPEED)
            drive_to.wait_counter = 0
            return

        else:
            drive_to.wait_counter += 1
            if drive_to.wait_counter >= 5:
                drivetrain.set_speed(0.0, 0.0)
                time.sleep(1.0)
            return


def drive_to_pad(x_center, y_center, width, height, current_state):
    global drivetrain

    # Keep a small wait counter like drive_to
    drive_to_pad.wait_counter = getattr(drive_to_pad, "wait_counter", 0)

    x_done = False

    # ---------- X ALIGNMENT ----------
    if x_center < (TARGET_X_TARGET - TARGET_X_DEADZONE):
        drivetrain.set_speed(-LINEUP_TURN_SPEED, LINEUP_TURN_SPEED)
        return

    elif x_center > (TARGET_X_TARGET + TARGET_X_DEADZONE):
        drivetrain.set_speed(LINEUP_TURN_SPEED, -LINEUP_TURN_SPEED)
        return

    else:
        drivetrain.set_speed(0.0, 0.0)
        x_done = True

    # ---------- DRIVE FORWARD ----------
    if x_done:
        if y_center < (TARGET_Y_TARGET - TARGET_Y_DEADZONE):
            drivetrain.set_speed(DRIVE_SPEED, DRIVE_SPEED)
            drive_to_pad.wait_counter = 0
            return

        elif y_center > (TARGET_Y_TARGET + TARGET_Y_DEADZONE):
            drivetrain.set_speed(-DRIVE_SPEED, -DRIVE_SPEED)
            drive_to_pad.wait_counter = 0
            return

        else:
            # In target zone → stop after stable frames
            drive_to_pad.wait_counter += 1
            if drive_to_pad.wait_counter >= 5:
                drivetrain.set_speed(0.0, 0.0)
                time.sleep(1.0)
            return

    current_state = 2
