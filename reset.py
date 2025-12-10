from XRPLib.differential_drive import DifferentialDrive
from XRPLib.servo import Servo
import sys
import time

print("RESET: Stopping robot...")

# Stop motors
drivetrain = DifferentialDrive.get_default_differential_drive()
drivetrain.set_speed(0.0, 0.0)
time.sleep(0.1)

# Optional servo reset
try:
    servo = Servo.get_default_servo(1)
    servo.set_position(0.5)  # center position
except:
    pass

print("Robot stopped.")
sys.exit()
