from XRPLib import *
import time

from turn import turn, drivetrain
from search_around import forward
from pick_up import pick_up

# ============================
# CONSTANTS
# ============================

WORD_A = "go"
WORD_B = "left"
WORD_C = "down"

TIME_FROM_LAST_VOICE_DETECTION_THRESHOLD = 60   # seconds


# ============================
# GLOBAL STATE
# ============================

is_first_word_detected = False
is_second_word_detected = False
is_third_word_detected = False

first_word = None
second_word = None
third_word = None

servo_motor_moved_degrees = 0
time_of_last_word = 0.0  # timestamp of last detected word


# ============================
# XRPLIB DEVICES
# ============================

uart = UART(1, baudrate=115200)       # Voice module UART
servo_one = Servo(0)                  # Change port if needed
word = ""


# ============================
# UART COMMAND HANDLER
# ============================

def get_command():
    """
    Reads UART characters until a space/newline/':' ends a word.
    Returns one lowercase command word.
    """
    global word

    while uart.any():
        ch = uart.read(1).decode("utf-8", "ignore")

        if ch in [' ', '\n', ':']:
            cmd = word.strip().lower()
            word = ""
            return cmd

        word += ch

    return None


# ============================
# SERVO HELPERS
# ============================

def servo_down(deg):
    global servo_motor_moved_degrees
    servo_motor_moved_degrees += deg
    servo_one.setAngle(servo_motor_moved_degrees)


def servo_reset():
    global servo_motor_moved_degrees
    servo_one.setAngle(0)
    servo_motor_moved_degrees = 0


# ============================
# ACTIONS
# ============================

def action_AA():
    print("Action: (A, A)")
    turn(45)

def action_AB():
    print("Action: (A, B)")
    turn(-45)

def action_AC():
    print("Action: (A, C)")
    forward(20)

def action_BA():
    print("Action: (B, A)")
    forward(-20)

def action_BB():
    print("Action: (B, B)")
    forward(50)

def action_BC():
    print("Action: (B, C)")
    pick_up()

def action_CA():
    print("Action: (C, A)")
    # example: set state for line search
    print("State change: search for line (state 2)")

def action_CB():
    print("Action: (C, B)")
    print("State change: search for bucket (state 5)")

def action_CC():
    print("Action: (C, C)")
    print("State change: search for arrow (state 7)")


ACTION_TABLE = {
    (WORD_A, WORD_A): action_AA,
    (WORD_A, WORD_B): action_AB,
    (WORD_A, WORD_C): action_AC,
    (WORD_B, WORD_A): action_BA,
    (WORD_B, WORD_B): action_BB,
    (WORD_B, WORD_C): action_BC,
    (WORD_C, WORD_A): action_CA,
    (WORD_C, WORD_B): action_CB,
    (WORD_C, WORD_C): action_CC,
}


# ============================
# WORD PROCESSING
# ============================

def handle_detected_word(word):
    global is_first_word_detected, is_second_word_detected, is_third_word_detected
    global first_word, second_word, third_word
    global time_of_last_word

    # XRPLib time (ms → seconds)
    time_of_last_word = run_time() / 1000.0

    # FIRST WORD
    if not is_first_word_detected:
        first_word = word
        is_first_word_detected = True
        print("First word detected:", first_word)
        return

    # SECOND WORD
    if not is_second_word_detected:
        if word != first_word:
            servo_down(10)
        second_word = word
        is_second_word_detected = True
        print("Second word detected:", second_word)
        return

    # THIRD WORD
    if not is_third_word_detected:
        if word != first_word:
            servo_down(10)
        third_word = word
        is_third_word_detected = True
        print("Third word detected:", third_word)
        execute_final_action()


# ============================
# FINAL EVALUATION
# ============================

def execute_final_action():
    global is_first_word_detected, is_second_word_detected, is_third_word_detected
    global first_word, second_word, third_word

    print("Three words collected. Running action...")

    servo_reset()

    pair = (second_word, third_word)
    action = ACTION_TABLE.get(pair, action_CC)
    action()

    # Reset state
    is_first_word_detected = False
    is_second_word_detected = False
    is_third_word_detected = False
    first_word = None
    second_word = None
    third_word = None


# ============================
# TIMEOUT HANDLING
# ============================

def tick_time_voice_commands():
    global time_of_last_word
    global is_first_word_detected, is_second_word_detected, is_third_word_detected
    global first_word, second_word, third_word

    if time_of_last_word == 0.0:
        return

    current = run_time() / 1000.0
    elapsed = current - time_of_last_word

    if elapsed > TIME_FROM_LAST_VOICE_DETECTION_THRESHOLD:
        print("Timeout: resetting state.")
        servo_reset()
        is_first_word_detected = False
        is_second_word_detected = False
        is_third_word_detected = False
        first_word = None
        second_word = None
        third_word = None
        time_of_last_word = 0.0


# ============================
# MAIN LOOP
# ============================

print("XRPLib Voice Command System Ready.")

while True:
    tick_time_voice_commands()
    w = get_command()
    if w:
        handle_detected_word(w)
