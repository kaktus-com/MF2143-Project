import time
import json
import sys
import os
import follow_line
import drive_to
import find_stuff
from machine import UART, Pin
from XRPLib.differential_drive import DifferentialDrive
from XRPLib.servo import Servo

SERVO_PORT = 1
UART_BAUDRATE = 115200

uart = UART(
    0,
    baudrate=UART_BAUDRATE,
    tx=Pin(0),
    rx=Pin(1),
    timeout=200,
)

differentialDrive = DifferentialDrive.get_default_differential_drive()
servo = Servo.get_default_servo(SERVO_PORT)

current_state = 0

def main():
    
    global current_state
    global current_position
    global drivetrain
    global uart
    global servo

    while True:
        bbox_arrow, bbox_basket, bbox_pad = find_stuff.get_bboxes(uart)
        
        if current_state == -1:
            drivetrain.set_speed(0.0, 0.0)
            continue

        elif current_state == 0:

            # normal line following
            follow_line.follow_steps(10)
            # if pressure pad is detected
            if bbox_pad is not None:
                print("Pressure pad detected")
                drivetrain.set_speed(0.0, 0.0)
                current_state = 1
                continue
            
            differentialDrive.turn(90,0.8)
            sleep(1)
            continue

        elif current_state == 1:
            
            if bbox_pad is None:
                print("Pressure pad lost")
                current_state = 0
                continue
            
            width = bbox_pad["xmax"] - bbox_pad["xmin"]
            height = bbox_pad["ymax"] - bbox_pad["ymin"]
            x_center = bbox_pad["xmin"] + width / 2.0
            y_center = bbox_pad["ymin"] + height / 2.0
    
            print(f"Lining up: ({x_center:.3f}, {y_center:.3f})")
            drive_to.drive_to_pad(x_center, y_center, width, height)
            x_center = x_center - 2 * x_center
            y_center = y_center - 2 * y_center
            drive_to.drive_to_pad(x_center, y_center, width, height)
            
            time.sleep(2) # stand on the pressure pad for 2 seconds

            print("pressure pad activated, moves back to line")
            current_state = 2
            continue
main()

