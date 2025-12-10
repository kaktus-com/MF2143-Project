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

def get_bboxes(uart):

    # Read UART line
    line = uart.readline()

    # Debug: Show raw UART bytes
    print("UART RAW:", line)

    if line is None:
        print("UART returned None")
        return (None, None, None)

    # Try to decode JSON
    try:
        decoded = line.decode("utf-8")
        print("UART DECODED:", decoded)

        bboxes = json.loads(decoded)
        print("PARSED JSON:", bboxes)

    except Exception as e:
        print("JSON ERROR:", e)
        return (None, None, None)

    bbox_arrow = None
    bbox_basket = None
    bbox_pad = None

    # Iterate through detections
    for bbox in bboxes["bboxes"]:
        print("FOUND BBOX:", bbox)

        if bbox["id"] == 1:
            if bbox_arrow is None or bbox["score"] > bbox_arrow["score"]:
                bbox_arrow = bbox
                print("UPDATED ARROW:", bbox_arrow)

        elif bbox["id"] == 2:
            if bbox_basket is None or bbox["score"] > bbox_basket["score"]:
                bbox_basket = bbox
                print("UPDATED BASKET:", bbox_basket)

        elif bbox["id"] == 3:
            if bbox_pad is None or bbox["score"] > bbox_pad["score"]:
                bbox_pad = bbox
                print("UPDATED PAD:", bbox_pad)

    print("FINAL SELECTED:", bbox_arrow, bbox_basket, bbox_pad)
    return (bbox_arrow, bbox_basket, bbox_pad)

while True:
    bbox_arrow, bbox_basket, bbox_pad = get_bboxes(uart)