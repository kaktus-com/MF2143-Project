import time 
from time import sleep
from machine import UART, Pin
from XRPLib.differential_drive import DifferentialDrive
import find_stuff
from XRPLib.servo import Servo
from XRPLib.imu import IMU

differentialDrive = DifferentialDrive.get_default_differential_drive()
imu = IMU()

SERVO_PORT = 2

differentialDrive = DifferentialDrive.get_default_differential_drive()
servo = Servo.get_default_servo(SERVO_PORT)

def driveStraight(speed, duration):
    target_heading = imu.get_yaw()   # save current direction
    kP = 0.02                        # tuning constant

    start_time = time.time()
    while time.time() - start_time < duration:
        error = target_heading - imu.get_yaw()
        correction = kP * error

        differentialDrive.arcade(speed, correction)
        sleep(0.02)

    drive.arcade(0, 0)  # stop


driveStraight(0.5, 10)
sleep(100)
