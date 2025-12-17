import time
from machine import UART, Pin
from XRPLib.differential_drive import DifferentialDrive
import find_stuff

UART_BAUDRATE = 115200

uart = UART(
    0,
    baudrate=UART_BAUDRATE,
    tx=Pin(0),
    rx=Pin(1),
    timeout=200,
)
drivetrain = DifferentialDrive.get_default_differential_drive()


def read_coral():
    """Read one frame of bboxes from Coral."""
    return find_stuff.get_bboxes(uart)


def main():
    print("STEP 3: Gentle movement + Coral read test")

    while True:
        bbox_arrow, bbox_basket, bbox_pad = read_coral()
        print("CORAL:", bbox_arrow, bbox_basket, bbox_pad)

        drivetrain.set_speed(4, 4)
        time.sleep(1.0)

        drivetrain.set_speed(0, 0)
        time.sleep(1.0)


main()

