import time
from time import sleep
import follow_line
import drive_to
import find_stuff
from machine import UART, Pin
from XRPLib.differential_drive import DifferentialDrive
from XRPLib.servo import Servo
from XRPLib.reflectance import Reflectance
from XRPLib.rangefinder import Rangefinder
from XRPLib.imu import IMU

SERVO_PORT = 2
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
PICKUP_DISTANCE = 12.0          # How far to drive backwards to get basket (cm)
DROPOFF_DISTANCE = 15.0         # How far to drive backwards to drop off (cm)

uart = UART(
    0,
    baudrate=UART_BAUDRATE,
    tx=Pin(0),
    rx=Pin(1),
    timeout=50,
)

reflectance = Reflectance.get_default_reflectance()
rangefinder = Rangefinder.get_default_rangefinder()
differentialDrive = DifferentialDrive.get_default_differential_drive()
servo = Servo.get_default_servo(SERVO_PORT)
imu = IMU()

current_state = 15
bbox_fail_count = 0
angle = 0

def main():
    global current_state
    global bbox_fail_count
    global angle
    
    while True:
        bbox_arrow, bbox_basket, bbox_pad = find_stuff.get_bboxes(uart)
        print("current state:", current_state)
        
        if current_state == -1:
            differentialDrive.stop()
            sleep(0.5)
            continue

        if current_state == 0:       
            follow_line.follow_steps(5)
            #differentialDrive.straight(3, 0.3)
            count = 0
            
            while count < 10:
                bbox_arrow, bbox_basket, bbox_pad = find_stuff.get_bboxes(uart)
                count += 1

                if bbox_pad is not None:
                    differentialDrive.stop()
                    current_state = 1
                    count = 0
                    break
            
            if bbox_pad is not None:
                continue
            
            #differentialDrive.straight(-3, 0.3)
            differentialDrive.turn(-90)
            continue

        if current_state == 1:  
            if bbox_pad is None:
                bbox_fail_count += 1
                print(f"bbox is none ({bbox_fail_count})")

                if bbox_fail_count >= 8:
                    differentialDrive.turn(-90)
                    current_state = 0
                    bbox_fail_count = 0  # reset after switching state

                continue
            else:
                bbox_fail_count = 0  # reset if bbox is valid


            width = bbox_pad["xmax"] - bbox_pad["xmin"]
            height = bbox_pad["ymax"] - bbox_pad["ymin"]
            x_center = (bbox_pad["xmin"] + bbox_pad["xmax"]) / 2
            y_center = (bbox_pad["ymin"] + bbox_pad["ymax"]) / 2

            print("x_center:", x_center, "y_center", y_center)

            if x_center < 0.45:
                differentialDrive.turn(100, 0.3)
                steps = 0
                while steps < 20:
                    left = reflectance.get_left()
                    right = reflectance.get_right()

                    diff = left - right
                    turn_effort = diff * 0.5

                    differentialDrive.arcade(0.3, turn_effort)
                    sleep(0.2)
                    steps += 1

                differentialDrive.stop()
                sleep(0.1)
                differentialDrive.turn(-180, 0.3)
                current_state = 0
                continue
            
            if x_center < 0.54 and x_center > 0.4 and x_center != 0.5:
                
                while bbox_pad is not None:
                    differentialDrive.straight(5, 0.5)
                    bbox_arrow, bbox_basket, bbox_pad = find_stuff.get_bboxes(uart)
                    
                differentialDrive.straight(5, 0.3)
                sleep(0.3)
                differentialDrive.straight(5, 0.3)
                sleep(0.3)
                differentialDrive.straight(5, 0.3)
                sleep(0.3)
                current_state = 2
            
            else:
                differentialDrive.turn(-90)
                sleep(0.5)
                current_state = 0
                continue

        elif current_state == 2:       
            left  = reflectance.get_left()
            right = reflectance.get_right()
            
            if left > 0.8 or right > 0.8:
                differentialDrive.straight(7, 0.3)
                differentialDrive.turn(-85, 0.5)
                current_state = 3
                
            differentialDrive.straight(-2, 0.2)
            sleep(0.4)
            differentialDrive.stop()
            continue

        elif current_state == 3:
            follow_line.follow()
            differentialDrive.stop()
            sleep(0.5)
            differentialDrive.straight(30, 0.3)
            current_state = 4
        
        elif current_state == 4:
            
            dist = rangefinder.distance()
            
            if dist > 15:
                differentialDrive.turn(-5, 0.3)
            elif dist < 15:
                differentialDrive.arcade(5, 0.3)
                
            differentialDrive.straight(4, 0.3)
            
            differentialDrive.turn(90, 0.3)
            
            dist = rangefinder.distance()
            
            if dist < 10:
                current_state = 5
        
            else:
                differentialDrive.turn(-90, 0.3)
                continue
            
        elif current_state == 4.5:
            
            differentialDrive.arcade(0.2, -0.38)
            sleep(1.5)
            differentialDrive.stop()
            differentialDrive.arcade(0.2, 0.4)
            sleep(1.5)
            differentialDrive.stop()
            differentialDrive.straight(-8, 0.3)
            differentialDrive.stop()
            current_state = 5
        
        elif current_state == 5:
            
            count = 0
            differentialDrive.straight(3, 0.3)
            sleep(0.5)
            differentialDrive.stop()
            differentialDrive.turn(90, 0.3)
            sleep(0.5)
            differentialDrive.straight(-1, 0.3)
            sleep(0.3)
            while count < 15:
                bbox_arrow, bbox_basket, bbox_pad = find_stuff.get_bboxes(uart)
                count += 1

                if bbox_basket is not None:
                    differentialDrive.stop()
                    current_state = 6
                    count = 0
                    break
            
            if bbox_basket is not None:
                continue
            
            differentialDrive.turn(-90, 0.3)
            sleep(0.5)
            continue
        
        elif current_state == 6:
            
            if bbox_basket is None:
                bbox_fail_count += 1
                print(f"bbox is none ({bbox_fail_count})")
                sleep(0.5)

                if bbox_fail_count >= 15:
                    differentialDrive.turn(-90, 0.3)
                    current_state = 5
                    bbox_fail_count = 0

                continue
            else:
                bbox_fail_count = 0

            x_center = (bbox_basket["xmin"] + bbox_basket["xmax"]) / 2
            y_center = (bbox_basket["ymin"] + bbox_basket["ymax"]) / 2

            print("x_center:", x_center, "y_center", y_center)

            if x_center < 0.61 and x_center > 0.45:
                current_state = 7
                continue
            
            if x_center < 0.45:
                differentialDrive.turn(-90, 0.3)
                differentialDrive.straight(-18, 0.3)
                current_state = 5
            
            else:
                differentialDrive.turn(-90, 0.3)
                sleep(0.5)
                current_state = 5
                continue
            
        elif current_state ==7:
            
            # Find basket bounding box
            if bbox_basket is None:
                count = 0
            
                while count < 20:
                    bbox_arrow, bbox_basket, bbox_pad = find_stuff.get_bboxes(uart)
                    count += 1

                    if bbox_basket is not None:
                        differentialDrive.stop()
                        count = 0
                        break
                
                if bbox_basket is None:
                    differentialDrive.turn(-90, 0.3)
                    current_state = 5
                    continue
            
            # Get coordinates of basket
            width = bbox_basket["xmax"] - bbox_basket["xmin"]
            height = bbox_basket["ymax"] - bbox_basket["ymin"]
            x_center = bbox_basket["xmin"] + (width / 2.0)
            y_center = bbox_basket["ymin"] + (height / 2.0)
            
            differentialDrive.stop()
            count = 0
            current_state = 8
            continue
            
        elif current_state == 8:
            
            if bbox_basket is None:
                count = 0
            
                while count < 20:
                    bbox_arrow, bbox_basket, bbox_pad = find_stuff.get_bboxes(uart)
                    count += 1

                    if bbox_basket is not None:
                        differentialDrive.stop()
                        count = 0
                        break
                
                if bbox_basket is None:
                    differentialDrive.turn(-90, 0.3)
                    current_state = 5
                    continue
                
            x_center = (bbox_basket["xmin"] + bbox_basket["xmax"]) / 2
            
            servo.set_angle(30)
            
            print(x_center)
            
            if x_center > 0.62:
                differentialDrive.arcade(0.2, -0.1)
                sleep(0.3)
                differentialDrive.stop()
                continue
            
            if x_center < 0.57:
                differentialDrive.arcade(0.2, 0.1)
                sleep(0.3)
                differentialDrive.stop()
                continue
            
            differentialDrive.straight(
                distance=PICKUP_DISTANCE,
                max_effort=0.5,
            )
            
            period = 1 / PICKUP_INCREMENTS
            time.sleep(period)
            servo.set_angle(90)
            time.sleep(1.0)
            
            current_state = 9
            sleep(1)
            continue
    
        elif current_state == 9:
            
            differentialDrive.straight(-10, 0.3)
            if bbox_basket is None:
                count = 0
            
                while count < 20:
                    bbox_arrow, bbox_basket, bbox_pad = find_stuff.get_bboxes(uart)
                    count += 1

                    if bbox_basket is not None:
                        current_state = 8
                        differentialDrive.stop()
                        count = 0
                        break
                
                none_count = 0
                count = 0

            current_state = 10
            continue

        elif current_state == 10:
            
            while True:
                dist = rangefinder.distance()

                if dist > 12:
                    differentialDrive.turn(-90, 0.3)
                    sleep(0.2)
                    differentialDrive.straight(3, 0.3)
                    sleep(0.2)
                    differentialDrive.turn(90, 0.3)
                else:
                    differentialDrive.straight(5, 0.3)
                    differentialDrive.stop()
                    sleep(0.5)
                    current_state = 11
                    break
                
            continue
            
        elif current_state == 11:
            
            differentialDrive.straight(3, 0.3)
            differentialDrive.turn(90, 0.3)
            dist = rangefinder.distance()

            if dist < 5:
                differentialDrive.turn(-90, 0.5)
                differentialDrive.straight(-15, 0.3)
            else:
                differentialDrive.stop()
                sleep(0.5)
                current_state = 12
                continue
        
        elif current_state == 12:
            
            count = 0
            
            while count < 15:
                bbox_arrow, bbox_basket, bbox_pad = find_stuff.get_bboxes(uart)
                count += 1

                if bbox_arrow is not None:
                    differentialDrive.stop()
                    current_state = 13
                    count = 0
                    break
            
            if bbox_arrow is not None:
                continue
            
            differentialDrive.turn(-90, 0.3)
            current_state = 11
            sleep(0.5)
            continue
            
        elif current_state == 13:
            
            if bbox_arrow is None:
                bbox_fail_count += 1
                print(f"bbox is none ({bbox_fail_count})")

                if bbox_fail_count >= 8:
                    differentialDrive.turn(-90, 0.3)
                    current_state = 11
                    bbox_fail_count = 0

                continue
            else:
                bbox_fail_count = 0
                
                x_center = (bbox_arrow["xmin"] + bbox_arrow["xmax"]) / 2
                print(x_center)
            
                if x_center < 0.6 and x_center > 0.4:
                    current_state = 14
                    continue
                
                differentialDrive.turn(-90, 0.3)
                current_state = 11
                
        elif current_state == 14:
            
            if bbox_arrow is None:
                bbox_fail_count += 1
                print(f"bbox is none ({bbox_fail_count})")

                if bbox_fail_count >= 8:
                    differentialDrive.straight(-3, 0.3)
                    bbox_fail_count = 0

                continue
            
            x_center = (bbox_arrow["xmin"] + bbox_arrow["xmax"]) / 2
            
            if bbox_arrow is not None:
                bbox_fail_count = 0
                
                if x_center > 0.53:
                    differentialDrive.arcade(0.3, -0.2)
                    sleep(0.5)
                    differentialDrive.stop()
                    continue
            
                elif x_center < 0.47:
                    differentialDrive.arcade(0.3, 0.2)
                    sleep(0.3)
                    differentialDrive.stop()
                    continue
                
                else:
                    current_state = 15
                    differentialDrive.straight(8, 0.3)
                    continue
    
        elif current_state == 15:
                differentialDrive.straight(3, 0.3)
            
                left  = reflectance.get_left()
                right = reflectance.get_right()
                    
                if left > 0.8 or right > 0.8:
                    follow_line.follow()
                    sleep(0.5)
                    differentialDrive.stop()
                    current_state = 16
                    continue
                
                sleep(0.5)
                differentialDrive.turn(-angle, 0.3)
                sleep(0.3)
                        
                left  = reflectance.get_left()
                right = reflectance.get_right()
                
                differentialDrive.turn(angle, 0.3)
                sleep(0.3)
                differentialDrive.stop()
                    
                if left > 0.8 or right > 0.8:
                    follow_line.follow()
                    sleep(0.5)
                    differentialDrive.stop()
                    current_state = 16
                    continue
                
                differentialDrive.turn(angle, 0.3)
                sleep(0.3)
                
                left  = reflectance.get_left()
                right = reflectance.get_right()
                
                differentialDrive.turn(-angle, 0.3)
                sleep(0.3)
                differentialDrive.stop()
                    
                if left > 0.8 or right > 0.8:
                    follow_line.follow()
                    sleep(0.5)
                    differentialDrive.stop()
                    current_state = 16
                    continue
                
                angle += 1
                
        elif current_state == 16:
            break
main()    