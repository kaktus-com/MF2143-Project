import time
from time import sleep
from XRPLib.board import Board
from XRPLib.reflectance import Reflectance
from XRPLib.rangefinder import Rangefinder
from XRPLib.differential_drive import DifferentialDrive
import find_stuff
from machine import UART, Pin

UART_BAUDRATE = 115200
WHEEL_ROT_PER_ROBOT_ROT = 2.42
SEARCH_TURN_SPEED = 20.0

board = Board.get_default_board()
rangefinder = Rangefinder.get_default_rangefinder()
reflectance = Reflectance.get_default_reflectance()
differentialDrive = DifferentialDrive.get_default_differential_drive()

uart = UART(
    0,
    baudrate=UART_BAUDRATE,
    tx=Pin(0),
    rx=Pin(1),
    timeout=50,
)

# drive straight for a set time period (defualt 1 second)
def drive_straight(drive_time: float = 1):
    drivetrain.set_effort(0.8, 0.8)
    time.sleep(drive_time)
    drivetrain.stop()

def turn_robot(degrees):
    if degrees == 0:
        return

    left_start  = differentialDrive.left_motor.get_position()
    right_start = differentialDrive.right_motor.get_position()

    target_rot = abs(degrees) / 360.0 * WHEEL_ROT_PER_ROBOT_ROT

    if degrees > 0:
        differentialDrive.set_speed(SEARCH_TURN_SPEED, -SEARCH_TURN_SPEED)
    else:
        differentialDrive.set_speed(-SEARCH_TURN_SPEED, SEARCH_TURN_SPEED)

    while True:
        left_rot  = abs(differentialDrive.left_motor.get_position() - left_start)
        right_rot = abs(differentialDrive.right_motor.get_position() - right_start)

        if max(left_rot, right_rot) >= target_rot:
            break

        time.sleep(0.01)

    differentialDrive.set_speed(0.0, 0.0)
    time.sleep(0.1)


def follow():
    forward = 0.3
    K = 1.0
    LINE_THRESH = 0.8

    while True:
        left = reflectance.get_left()
        right = reflectance.get_right()
        

        if left > LINE_THRESH or right > LINE_THRESH:
            turn_effort = (left - right) * K
            differentialDrive.arcade(forward, turn_effort)
            time.sleep(0.01)
            continue

        differentialDrive.stop()
        time.sleep(0.05)

        differentialDrive.turn(-5, 0.5)
        time.sleep(0.12)
        differentialDrive.stop()
        
        left = reflectance.get_left()
        right = reflectance.get_right()
        print(left, right)

        if left > LINE_THRESH or right > LINE_THRESH:
            continue

        differentialDrive.turn(5, 0.5)
        time.sleep(0.12)
        differentialDrive.stop()
        
        left = reflectance.get_left()
        right = reflectance.get_right()
        print(left, right)

        if left > LINE_THRESH or right > LINE_THRESH:
            continue

        break

    differentialDrive.stop()
    return


def follow_steps(steps):
    global uart
    count = 0
    while count < steps:
        left = reflectance.get_left()
        right = reflectance.get_right()

        diff = left - right
        turn_effort = diff * 0.5

        differentialDrive.arcade(0.3, turn_effort)
        sleep(0.2)
        count += 1

    differentialDrive.stop()
    sleep(0.1)

    print("turn left")
    differentialDrive.turn(90,0.5)
    differentialDrive.straight(0.5, 0.4)
    sleep(1)
