import time
from time import sleep
import json
import sys
import os
import follow_line
import drive_to
import find_stuff
import search_around
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

def drive_straight(drive_time: float = 1):
    differentialDrive.set_effort(0.3, 0.3)
    time.sleep(drive_time)
    differentialDrive.stop()

def main():
    
    global current_state
    global current_position
    global differentialDrive
    global uart
    global servo

    while True:
        bbox_arrow, bbox_basket, bbox_pad = find_stuff.get_bboxes(uart)
        sleep(3.0)
        
        if current_state == -1:
            drivetrain.set_speed(0.0, 0.0)
            continue

        elif current_state == 0:

            differentialDrive.straight(10, 0.3)
            sleep(1)
            differentialDrive.turn(90, 0.7)
            bbox_arrow, bbox_basket, bbox_pad = find_stuff.get_bboxes(uart)
            sleep(1)
            
            if bbox_basket is not None:
                print("Basket pad detected")
                differentialDrive.set_speed(0.0, 0.0)
                current_state = 1
                continue
            
            differentialDrive.turn(-90, 0.7)
            continue

        elif current_state == 1:
            
            if bbox_basket is None:
                print("Basket pad lost")
                current_state = 0
                sleep(1)
                continue
            
            width = bbox_basket["xmax"] - bbox_basket["xmin"]
            height = bbox_basket["ymax"] - bbox_basket["ymin"]
            x_center = bbox_basket["xmin"] + width / 2.0
            y_center = bbox_basket["ymin"] + height / 2.0
    
            print(f"Lining up: ({x_center:.3f}, {y_center:.3f})")
            drive_to.drive_to(x_center, y_center, width, height)
            x_center = x_center - 2 * x_center
            y_center = y_center - 2 * y_center
            drive_to.drive(x_center, y_center, width, height)
            
            time.sleep(2) # stand on the pressure pad for 2 seconds

            print("basket found")
            current_state = 2
            continue
        
        elif current_state == 2:
            sleep(10)
        
while True:
    bbox_arrow, bbox_basket, bbox_pad = find_stuff.get_bboxes(uart)

