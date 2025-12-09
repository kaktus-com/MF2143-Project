from XRPLib.differential_drive import DifferentialDrive
from machine import UART, Pin
drivetrain = DifferentialDrive.get_default_differential_drive()
word = ""
ch = ""

def get_command(uart, current_state):
    global word

    while uart.any():
        ch = uart.read(1).decode('utf-8', 'ignore')

        if ch in [' ', '\n', ':']:
            cmd = word.strip().lower()
            word = "" 


            return current_state

        word += ch

    return current_state


