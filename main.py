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
import v
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

current_state = -1

def main():
    
    global current_state
    global current_position
    global drivetrain
    global uart
    global servo

    while board.is_button_pressed():
        pass  # wait for button release to start

    while True:
        speech_commands.tick_time_voice_commands()
        w = speech_commands.get_command()  # replace with your voice detection function
        if w:
            if w == "down" or w == "left" or w == "right":
                speech_commands.handle_detected_word(w)
                current_state = -2
            else: # detection of an object
                find_stuff.object_detected(w)


        
        if current_state == -2: # only voice comands drive
            continue

        if current_state == -1:
            drivetrain.set_speed(0.0, 0.0)
            continue

        elif current_state == 0:

            # if pressure pad is detected
            pad = find_stuff.get_pressure_pad() # havent done the logic for this function
            if pad is not None:
                print("Pressure pad detected")
                drivetrain.set_speed(0, 0)
                current_state = 1
                continue

            # normal line following
            follow_line.follow_steps(10)
            continue

        elif current_state == 1:
            
            pad = find_stuff.get_pressure_pad()
            if pad is None:
                print("Pressure pad lost")
                current_state = 0 # maybe we do a separate function for it
                continue
            
            width = pad["xmax"] - pad["xmin"]
            height = pad["ymax"] - pad["ymin"]
            x_center = pad["xmin"] + width / 2.0
            y_center = pad["ymin"] + height / 2.0
    
            print(f"Lining up: ({x_center:.3f}, {y_center:.3f})")
            drive_to.drive_to(x_center, y_center) #question
            #todo: save cordinats and after standing onm the pad use (drive_to.drive_to(-x_center, -y_center))
            
            time.sleep(2) # stand on the pressure pad for 2 seconds

            print("pressure pad activated, moves back to line")
            current_state = 2

            # todo: drive_to.drive_to(-x_center, -y_center) # drive back to original position
            continue

        elif current_state == 2:
            
            # todo: just use current_state = 3 after driving back to line
            if search_for_line() == 1:
                print ("line found")
                current_state = 3
                continue
            
            continue
        
        elif current_state == 3:
        
            follow_line.follow() #question, what happens if robot stands like 30 deg to the line
            current_state = 4
        
        elif current_state == 4:
            
            basket = find_stuff.get_basket() # code to write when we have the model
            if basket is not None:
                print("Basket detected")
                drivetrain.set_speed(0, 0)
                current_state = 5
                continue
            
            search_around.scan_turn_move() 
            continue
            
        elif current_state == 5:
            
            basket = find_stuff.get_basket()
            if basket is None:
                print("basket is lost")
                current_state = 4
                continue
            
            width = basket["xmax"] - basket["xmin"] # TODO: code is repeated, make a function in find_stuff
            height = basket["ymax"] - basket["ymin"]
            x_center = basket["xmin"] + width / 2.0
            y_center = basket["ymin"] + height / 2.0
            
            print(f"Lining up: ({x_center:.3f}, {y_center:.3f})")
            drive_to.drive_to(x_center, y_center) # question, does it work? dont you need 4 parameters?
            
            current_state = 6
            continue
        
        elif current_state == 6:

            pick_up.pick_up() # we need to check if pick up was successfull
            print("Basket picked up")
            time.sleep(2) # wait for 2 seconds after picking up the basket
            
            current_state = 7
            continue
        
        elif current_state == 7:
            
            arrow = find_stuff.get_arrow() # code to write when we have the model
            if arrow is not None:
                print("Arrow detected")
                drivetrain.set_speed(0, 0)
                current_state = 8
                continue
            
            search_around.scan_turn_move() # the same comment as before
            continue
            
        elif current_state == 8:

            arrow = find_stuff.get_arrow()
            if arrow is None:
                print("arrow is lost, return to previous stage")
                current_state = 7
                continue
            
            width = arrow["xmax"] - arrow["xmin"] #TODO: code is repeated, make a function in find_stuff
            height = arrow["ymax"] - arrow["ymin"]
            x_center = arrow["xmin"] + width / 2.0
            y_center = arrow["ymin"] + height / 2.0
            
            print(f"Lining up: ({x_center:.3f}, {y_center:.3f})")
            drive_to.drive_to(x_center, y_center)
            print("moving to arrow")
            time.sleep(2) # wait for 2 seconds after moving to the arrow
            
            current_state = 9
            continue
        
        elif current_state == 9:
            follow_line.follow() # question, how good is the line following?
            
main()

