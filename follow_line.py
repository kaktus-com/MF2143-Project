from XRPLib.board import Board
from XRPLib.reflectance import Reflectance
from XRPLib.rangefinder import Rangefinder
from XRPLib.differential_drive import DifferentialDrive

turn_effort = None
board = Board.get_default_board()
rangefinder = Rangefinder.get_default_rangefinder()
reflectance = Reflectance.get_default_reflectance()
differentialDrive = DifferentialDrive.get_default_differential_drive()

def follow_line():
    while not (rangefinder.distance()) < 15:
        turn_effort = (reflectance.get_left()) - (reflectance.get_right())
        differentialDrive.arcade(0.4, turn_effort)
    differentialDrive.stop()    

follow_line()
