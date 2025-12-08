import time
from turn import turn, drivetrain
from XRPLib.rangefinder import Rangefinder

# Rangefinder instance used for distance reads
rangefinder = Rangefinder.get_default_rangefinder()

SCAN_STEP = 45        # degrees per scan step
DRIVE_SPEED = 0.7
MOVE_DISTANCE = 20   # cm every call
MINIMAL_DISTANCE_TO_WALL_FORWARD = 20  # cm


def forward(cm):
    drivetrain.straight(cm, DRIVE_SPEED)
    time.sleep(2)  # wait for movement to complete

def get_distance():
    # single read from the rangefinder (in cm)
    return rangefinder.distance()


# =====================================================
# 360 deg SCAN FUNCTION
# =====================================================
# --- incremental scan state -------------------------------------------------
# The scanning is done across multiple calls to `scan_turn_move()`.
# Each call performs a single `SCAN_STEP` read+turn. After a full 360 deg is
# sampled the state machine will decide the best heading and perform
# orientation + forward movement across subsequent calls.

# Precomputed scan angles and state
_SCAN_ANGLES = list(range(0, 360, SCAN_STEP))
scan_readings = {}        # angle -> distance
scan_index = 0            # next index into _SCAN_ANGLES to read
scan_mode = "scanning"   # one of: scanning, orienting, checking
pending_turn_amount = 0.0 # degrees to turn when orienting

def reset_scan_state():
    global scan_readings, scan_index, scan_mode, pending_turn_amount
    scan_readings = {}
    scan_index = 0
    scan_mode = "scanning"
    pending_turn_amount = 0.0





# =====================================================
# Helper: decide orientation after full 360 scan
# =====================================================
def _decide_turn_from_readings():
    """Return shortest turn amount (deg) to orient so closest wall is on the RIGHT."""
    if not scan_readings:
        return 0.0
    # pick the angle with the smallest distance
    closest_angle = min(scan_readings.items(), key=lambda kv: kv[1])[0]
    print(f"Closest wall: angle {closest_angle} deg, dist {scan_readings[closest_angle]} cm")
    # compute desired robot heading to have wall on right
    desired_angle = (closest_angle - 90) % 360
    turn_amount = desired_angle
    if turn_amount > 180:
        turn_amount -= 360
    return turn_amount


# =====================================================
# MOVE EXACTLY 20 CM
# =====================================================
def move_30cm():
    print(f"Moving forward {MOVE_DISTANCE} cm")
    forward(MOVE_DISTANCE)


# =====================================================
# MAIN FUNCTION (CALL THIS REPEATEDLY)
# =====================================================
def scan_turn_move():
    """Called repeatedly. Performs one scan-step (45deg) per call while
    in `scanning` mode. After a full 360 is sampled the function moves
    through `orienting` -> `checking` states to orient and move forward.
    """
    global scan_index, scan_mode, pending_turn_amount

    # --- SCANNING: one read + turn per call -----------------------------
    if scan_mode == "scanning":
        if scan_index < len(_SCAN_ANGLES):
            angle = _SCAN_ANGLES[scan_index]
            d = get_distance()
            scan_readings[angle] = d
            print(f"Scanned angle {angle} deg, dist={d} cm")
            # rotate to next step
            turn(SCAN_STEP)
            scan_index += 1

        if scan_index >= len(_SCAN_ANGLES):
            # finished full 360
            scan_mode = "orienting"
            pending_turn_amount = _decide_turn_from_readings()
            print(f"Full 360 scanned -- will orient {pending_turn_amount} deg next call")
        return

    # --- ORIENTING: rotate to chosen heading ---------------------------
    if scan_mode == "orienting":
        print(f"Orienting {pending_turn_amount} deg to position wall on right")
        turn(pending_turn_amount)
        time.sleep(1)
        scan_mode = "checking"
        return

    # --- CHECKING: verify forward free space, otherwise turn left 90 deg ---
    if scan_mode == "checking":
        distance_ahead = get_distance()
        print(f"Distance ahead: {distance_ahead} cm")
        if distance_ahead < MINIMAL_DISTANCE_TO_WALL_FORWARD:
            print(f"Not enough space ahead ({distance_ahead}<{MINIMAL_DISTANCE_TO_WALL_FORWARD}), turning left 90 deg")
            turn(-90)
            time.sleep(0.5)
            return
        # We have enough space -- move forward and then reset
        move_30cm()
        reset_scan_state()
        return

