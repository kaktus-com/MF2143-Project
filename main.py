import time
import json
import sys
import os
import follow_line
import drive_to
import pressure_pad
from machine import UART, Pin
from XRPLib.differential_drive import DifferentialDrive
from XRPLib.servo import Servo

#configure connection
uart = UART(
    0,
    baudrate=UART_BAUDRATE,
    tx=Pin(0),
    rx=Pin(1),
    timeout=200,
)

# Magical empirical constant to perform degrees of robot rotation using
WHEEL_ROT_PER_ROBOT_ROT = 2.42

# Configure encoded motors and servo
drivetrain = DifferentialDrive.get_default_differential_drive()
servo = Servo.get_default_servo(SERVO_PORT)

current_state = 0
current_position = [0.0, 0.0, 0.0]

while True:
        
    # --- CHECK FOR STOP COMMAND ---
    if uart.any():
        data = uart.readline()
        print(data)
        if data:
            try:
                cmd = data.decode().strip().upper()
                print("Received:", cmd)

                if cmd == "STOP":
                    drivetrain.set_speed(0.0, 0.0)
                    print("Robot STOPPED!")
                    continue   # <-- robot freezes until next command

            except Exception as e:
                print("UART decode error:", e)
    # --------------------------------

    print(current_state)
        
    if current_state == 0:
            
        follow_line.follow(current_position)
        current_state = 1
            
        # check pressure pad
        pad = pressure_pad.get_pressure_pad()
        if pad is not None:
            print("Pressure pad was detected")
            drivetrain.set_speed(0.0, 0.0)
            current_state = 1
            continue
        
    follow_line.follow_line(position)
        
    if current_state == 1:
            
        drive_to.drive_to(10, 10, 0, 0)
        current_state = 2
            
        pad = pressure_pad.get_pressure_pad()
        if pad is None:
            print("Pressure pad is lost")
            current_state = 0
            continue
            
        width = pad["xmax"] - pad["xmin"]
        height = pad["ymax"] - pad["ymin"]
        x_center = pad["xmin"] + (width / 2.0)
        y_center = pad["ymin"] + (height / 2.0)
            
        print(f"Lining up pressure pad: ({x_center:.3f}, {y_center:.3f})")

        drive_to.drive_to(x_center, y_center, width, height)
            
    if current_state == 2:
        drive_to.drive_to(position[0], position[1])
        follow_line.follow_line(current_position)

main()        