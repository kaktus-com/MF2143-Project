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
import voice_commands
import search_around

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
drivetrain = DifferentialDrive.get_default_differential_drive()
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

            # if pressure pad is detected
            if bbox_pad is not None:
                print("Pressure pad detected")
                drivetrain.set_speed(0.0, 0.0)
                current_state = 1
                continue

            # normal line following
            follow_line.follow_steps(10)
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

        elif current_state == 2:
            
            #if search_for_line() == 1:
            #    print ("line found")
            #    current_state = 3
            #    continue
            
            drive_to.drive_to_pad(x_center, y_center, width, height)
            current_state = 3
            continue
        
        elif current_state == 3:
        
            follow_line.follow()
            current_state = 4
        
        elif current_state == 4:
            
            if bbox_basket is not None:
                print("Basket detected")
                drivetrain.set_speed(0, 0)
                current_state = 5
                continue
            
            search_around.scan_turn_move() 
            continue
            
        elif current_state == 5:
            
            if bbox_basket is None:
                print("basket is lost")
                current_state = 4
                continue
            
            width = basket["xmax"] - basket["xmin"]
            height = basket["ymax"] - basket["ymin"]
            x_center = basket["xmin"] + width / 2.0
            y_center = basket["ymin"] + height / 2.0
            
            print(f"Lining up: ({x_center:.3f}, {y_center:.3f})")
            drive_to.drive_to(x_center, y_center, width, height)
            
            current_state = 6
            continue
        
        elif current_state == 6:

            pick_up.pick_up() # we need to check if pick up was successfull
            print("Basket picked up")
            time.sleep(2) # wait for 2 seconds after picking up the basket
            
            current_state = 7
            continue
        
        elif current_state == 7:
            drivetrain.set_speed(0, 0)
        #    
        #    arrow = find_stuff.get_arrow() # code to write when we have the model
        #    if arrow is not None:
        #        print("Arrow detected")
        #        drivetrain.set_speed(0, 0)
        #        current_state = 8
        #        continue
        #    
        #   search_around.scan_turn_move() # the same comment as before
        #    continue
            
        #elif current_state == 8:

        #    arrow = find_stuff.get_arrow()
        #    if arrow is None:
        #        print("arrow is lost, return to previous stage")
        #        current_state = 7
        #        continue
            
        #    width = arrow["xmax"] - arrow["xmin"] #TODO: code is repeated, make a function in find_stuff
        #    height = arrow["ymax"] - arrow["ymin"]
        #    x_center = arrow["xmin"] + width / 2.0
        #    y_center = arrow["ymin"] + height / 2.0
            
        #    print(f"Lining up: ({x_center:.3f}, {y_center:.3f})")
        #    drive_to.drive_to(x_center, y_center)
        #    print("moving to arrow")
        #    time.sleep(2) # wait for 2 seconds after moving to the arrow
            
        #    current_state = 9
        #    continue
        
        #elif current_state == 9:
        #    follow_line.follow() # question, how good is the line following?
            
main()

