import time
import json
import sys

from machine import UART, Pin

#configure connection
uart = UART(
    0,
    baudrate=UART_BAUDRATE,
    tx=Pin(0),
    rx=Pin(1),
    timeout=200,
)
