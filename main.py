import time
import json
import sys
import follow_line

from machine import UART, Pin

from XRPLib.differential_drive import DifferentialDrive
from XRPLib.servo import Servo

# Settings
SERVO_PORT = 1
UART_BAUDRATE = 115200
RESTART_WAIT = 5.0              # How long to wait for Coral Micro to boot (sec)
SEARCH_TURN_SPEED = 20.0        # Drive speed when searching
LINEUP_TURN_SPEED = 12.0        # Drive speed when lining up object
DRIVE_SPEED = 20.0              # Drive speed when not bound by distance
MAX_EFFORT = 0.5                # Drive speed when driving by distance
BASKET_X_TARGET = 0.4           # Where the basket X should be for pickup
BASKET_X_DEADZONE = 0.02        # Basket center X can be lined up +/- this val
BASKET_Y_TARGET = 0.82          # Where the basket Y should be for pickup
BASKET_Y_DEADZONE = 0.02        # Basket center Y can be lined up +/- this val
TARGET_X_TARGET = 0.36          # Where the target X should be for dropoff
TARGET_X_DEADZONE = 0.02        # Target center X can be lined up +/- this val
TARGET_Y_TARGET = 0.8           # Where the target Y should be for dropoff
TARGET_Y_DEADZONE = 0.05        # Target center Y can be lined up +/- this val
SERVO_HOME = 180.0              # Arm in the collapsed position (degrees)
SERVO_PICKUP = 12.0             # Arm in the pickup position (degrees)
SERVO_CARRY = 40.0              # Arm in the carry basket position (degrees)
PICKUP_INCREMENTS = 10          # Perform servo lift in increments
PICKUP_DISTANCE = 18.0          # How far to drive backwards to get basket (cm)
DROPOFF_DISTANCE = 15.0         # How far to drive backwards to drop off (cm)
VICTORY_TURN_DEGREES = 90.0     # How far to dance
NUM_VICTORY_TURNS = 2           # How many back and forth turns to do

# Magical empirical constant to perform degrees of robot rotation using
# encoder raw output (warning: not accurate)
WHEEL_ROT_PER_ROBOT_ROT = 2.42

# Configure encoded motors and servo
drivetrain = DifferentialDrive.get_default_differential_drive()
servo = Servo.get_default_servo(SERVO_PORT)

# State machine
# 0: Follow the line
# 1: Drive towards the pressure pad
# 2: Look for the opening
# 3: Go to the opening
# 4: Look for the busket in the room
# 5: Drive towards the basket
# 6: Pick up the basket
# 7: Look for the arrow
# 8: Go to the arrow
# 9: Follow the line
# 10: Stop
current_state = 0

def main():
    global uart
    global drivetrain
    global servo
    global current_state
    
    # Setup
    servo.set_angle(SERVO_HOME)
    drivetrain.set_speed(
        left_speed=0.0,
        right_speed=0.0,
    )
    wait_counter = 0

    # Wait for Coral Micro to start running
    print("Waiting for Coral Micro to boot...")
    time.sleep(RESTART_WAIT)
    print("Go!")
    
    while True:
        
        if current_state == 0:
            
            #if the pressure pad is detected
            if pressure_pad:
                print("Pressure pad was detected")
                drivetrain.set_speed(
                    left_speed=0.0,
                    right_speed=0.0,
                )
                current_state = 1
                continue
        
        #if the pressure pad is not detected it follows the line for 5cm
        follow_line.follow_line()
        
        if current_state == 1:
            
            #if the basket is lost
            if pressure_pad is None:
                print("Pressure pad is lost")
                current_state = 0
                continue
            
            width = pressure_pad["xmax"] - pressure_pad["xmin"]
            height = pressure_pad["ymax"] - pressure_pad["ymin"]
            x_center = pressure_pad["xmin"] + (width / 2.0)
            y_center = pressure_pad["ymin"] + (height / 2.0)
            
            # Print debug string
            print(f"Lining up pressure pad: ({x_center:.3f}, {y_center:.3f})")
            
            drive_to(x_center, y_center, width, height)
    
