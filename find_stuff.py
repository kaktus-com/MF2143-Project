from machine import UART, Pin
import ujson as json

UART_BAUDRATE = 115200

uart = UART(
    0,
    baudrate=UART_BAUDRATE,
    tx=Pin(0),
    rx=Pin(1),
    timeout=200,
)

uart_buffer = ""

def get_bboxes(uart):
    global uart_buffer

    line = uart.read()

    if line is None:
        return (None, None, None)

    try:
        uart_buffer += line.decode("utf-8")
    except:
        uart_buffer = ""
        return (None, None, None)

    if "}" not in uart_buffer:
        return (None, None, None)

    try:
        json_str, uart_buffer = uart_buffer.split("}\r\n", 1)
        json_str += "}"
    except:
        uart_buffer = ""
        return (None, None, None)

    try:
        data = json.loads(json_str)
    except:
        uart_buffer = ""
        return (None, None, None)

    bbox_arrow = None
    bbox_basket = None
    bbox_pad = None

    for bbox in data["bboxes"]:

        if bbox["id"] in (2, 5):
            if bbox_pad is None or bbox["score"] > bbox_pad["score"]:
                bbox_pad = bbox

        elif bbox["id"] in (1, 4):
            if bbox_basket is None or bbox["score"] > bbox_basket["score"]:
                bbox_basket = bbox

        elif bbox["id"] == 3:
            if bbox_arrow is None or bbox["score"] > bbox_arrow["score"]:
                bbox_arrow = bbox

    return (bbox_arrow, bbox_basket, bbox_pad)
