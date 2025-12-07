import time
from XRPLib.board import Board
from XRPLib.reflectance import Reflectance
from XRPLib.rangefinder import Rangefinder
from XRPLib.differential_drive import DifferentialDrive
import coordinates

board = Board.get_default_board()
rangefinder = Rangefinder.get_default_rangefinder()
reflectance = Reflectance.get_default_reflectance()
differentialDrive = DifferentialDrive.get_default_differential_drive()

def follow(pos):
    max_steps = 5
    previous_time = time.ticks_ms()
    steps = 0

    while rangefinder.distance() >= 15 and steps < max_steps:
        turn_effort = reflectance.get_left() - reflectance.get_right()
        differentialDrive.arcade(0.4, turn_effort)
        steps += 1 

        now = time.ticks_ms()
        dt = time.ticks_diff(now, previous_time) / 1000.0
        previous_time = now

        # update coordinates
        coordinates.update_coordinates(0.4, turn_effort, dt, pos)
        print(pos)

    differentialDrive.stop()
    print(f"Followed line for {steps} steps. Current position: {pos}")
