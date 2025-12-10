import time
from XRPLib.board import Board
from XRPLib.reflectance import Reflectance
from XRPLib.rangefinder import Rangefinder
from XRPLib.differential_drive import DifferentialDrive
import coordinates

board = Board.get_default_board()
rangefinder = Rangefinder.get_default_rangefinder()
reflectance = Reflectance.get_default_reflectance()
differentialDrive = DifferentialDrive.get_default_differential_drive()

def follow():
    forward = 0.4
    K = 1.0
    cycle = 0

    while True:
        left  = reflectance.get_left()
        right = reflectance.get_right()

        turn_effort = (left - right) * K
        differentialDrive.arcade(forward, turn_effort)
        time.sleep(0.01)

        cycle += 1
        if cycle < 50:
            continue
        cycle = 0   # reset
        left_l  = reflectance.get_left()
        right_l = reflectance.get_right()
        
        if left_l > 0.65 or right_l > 0.65:
            continue

        # WIGGLE LEFT
        differentialDrive.arcade(0.0, -0.4)
        time.sleep(0.1)
        left_l  = reflectance.get_left()
        right_l = reflectance.get_right()

        if left_l > 0.65 or right_l > 0.65:
            continue

        # WIGGLE RIGHT
        differentialDrive.arcade(0.0, 0.4)
        time.sleep(0.1)
        left_r  = reflectance.get_left()
        right_r = reflectance.get_right()

        if left_r > 0.65 or right_r > 0.65:
            continue

        print("line is over, stopping")
        break

    differentialDrive.stop()

def follow_steps(steps):
    forward = 0.4

    # --- Normal line following for N steps ---
    for _ in range(steps):
        left  = reflectance.get_left()
        right = reflectance.get_right()
        turn_effort = (left - right)
        differentialDrive.arcade(forward, turn_effort)
        time.sleep(0.01)

    # Stop before scanning
    differentialDrive.stop()
    time.sleep(0.05)

    # Refresh reflectance readings
    left  = reflectance.get_left()
    right = reflectance.get_right()

    # --- If line is still strong, no scan needed ---
    if left > 0.65 or right > 0.65:
        return

    # --- LOOK AROUND PHASE ---

    # 1. Wiggle LEFT
    differentialDrive.arcade(0.0, -0.4)
    time.sleep(0.12)
    left_check  = reflectance.get_left()
    right_check = reflectance.get_right()
    if left_check > 0.65 or right_check > 0.65:
        differentialDrive.stop()
        return

    # 2. Wiggle RIGHT
    differentialDrive.arcade(0.0, 0.4)
    time.sleep(0.12)
    left_check  = reflectance.get_left()
    right_check = reflectance.get_right()
    if left_check > 0.65 or right_check > 0.65:
        differentialDrive.stop()
        return

    # 3. Try moving slightly forward
    differentialDrive.arcade(0.25, 0.0)
    time.sleep(0.15)
    left_check  = reflectance.get_left()
    right_check = reflectance.get_right()
    if left_check > 0.65 or right_check > 0.65:
        differentialDrive.stop()
        return

    # If all scans failed, just stop normally
    differentialDrive.stop()




