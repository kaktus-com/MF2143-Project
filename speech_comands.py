import xrp
import time

# ============================
# CONSTANTS
# ============================

WORD_A = "WORD_A"
WORD_B = "WORD_B"
WORD_C = "WORD_C"

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
# SERVO HELPERS
# ============================

def servo_down(deg):
    """Move servo further down by deg degrees (accumulates)."""
    global servo_motor_moved_degrees
    servo_motor_moved_degrees += deg
    servo_one.set_angle(servo_motor_moved_degrees)

def servo_reset():
    """Return servo to initial (0°) position and reset counter."""
    global servo_motor_moved_degrees
    servo_one.set_angle(0)
    servo_motor_moved_degrees = 0


# ============================
# ACTIONS: 9 UNIQUE ACTIONS
# ============================

def action_AA(): print("Action: (A, A)")
def action_AB(): print("Action: (A, B)")
def action_AC(): print("Action: (A, C)")
def action_BA(): print("Action: (B, A)")
def action_BB(): print("Action: (B, B)")
def action_BC(): print("Action: (B, C)")
def action_CA(): print("Action: (C, A)")
def action_CB(): print("Action: (C, B)")
def action_CC(): print("Action: (C, C)")


# Map (second_word, third_word) -> function
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
# MAIN WORD HANDLER
# ============================

def handle_detected_word(word):
    global is_first_word_detected, is_second_word_detected, is_third_word_detected
    global first_word, second_word, third_word
    global time_of_last_word

    # Record timestamp of word detection
    time_of_last_word = xrp.time()  # XRP library time

    # FIRST WORD
    if not is_first_word_detected:
        first_word = word
        is_first_word_detected = True
        print("First word detected:", first_word)
        return

    # SECOND WORD
    if is_first_word_detected and not is_second_word_detected:
        if word != first_word:
            servo_down(10)
        second_word = word
        is_second_word_detected = True
        print("Second word detected:", second_word)
        return

    # THIRD WORD
    if is_first_word_detected and is_second_word_detected and not is_third_word_detected:
        if word != first_word:
            servo_down(10)
        third_word = word
        is_third_word_detected = True
        print("Third word detected:", third_word)

        execute_final_action()
        return


# ============================
# EVALUATION & RESET
# ============================

def execute_final_action():
    """Reset servo first, pick action for (second_word, third_word), call it, then reset state."""
    global is_first_word_detected, is_second_word_detected, is_third_word_detected
    global first_word, second_word, third_word

    print("Three words collected. Preparing to execute action...")

    # Reset servo to initial position BEFORE executing any action
    servo_reset()

    pair = (second_word, third_word)
    action = ACTION_TABLE.get(pair, action_CC)  # fallback if unknown pair

    # Call the chosen action
    action()

    # Reset all state
    is_first_word_detected = False
    is_second_word_detected = False
    is_third_word_detected = False
    first_word = None
    second_word = None
    third_word = None


# ============================
# TIMEOUT / TICK FUNCTION
# ============================

def tick_time_voice_commands():
    global time_of_last_word
    global is_first_word_detected, is_second_word_detected, is_third_word_detected
    global first_word, second_word, third_word

    if time_of_last_word == 0.0:
        return  # no word detected yet

    elapsed = xrp.time() - time_of_last_word

    if elapsed > TIME_FROM_LAST_VOICE_DETECTION_THRESHOLD:
        print("Timeout exceeded: resetting state and servo.")
        servo_reset()
        is_first_word_detected = False
        is_second_word_detected = False
        is_third_word_detected = False
        first_word = None
        second_word = None
        third_word = None
        time_of_last_word = 0.0


# ============================
# Example usage snippet
# ============================

# while True:
#     tick_time_voice_commands()
#     w = voice_get_word()  # replace with your voice detection function
#     if w:
#         handle_detected_word(w)
