import time

SCAN_STEP = 2        # degrees per scan step
TURN_SPEED = 0.6
DRIVE_SPEED = 0.7

MOVE_DISTANCE = 30   # cm every call

def turn(angle):
    drivetrain.turn(angle, TURN_SPEED)

def forward(cm):
    drivetrain.straight(cm, DRIVE_SPEED)

def get_distance():
    return range_sensor.distance()


# =====================================================
# 360° SCAN FUNCTION
# =====================================================
def scan_360():
    readings = []

    for angle in range(0, 360, SCAN_STEP):
        d = get_distance()
        readings.append((angle, d))
        turn(SCAN_STEP)
        time.sleep(0.03)

    return readings


# =====================================================
# TURN SO WALL IS ON THE RIGHT SIDE
# =====================================================
def orient_wall_right():
    print("Scanning 360°…")
    readings = scan_360()

    # Get angle of closest wall
    closest_angle, closest_distance = min(readings, key=lambda x: x[1])
    print(f"Closest wall: angle {closest_angle}°, dist {closest_distance} cm")

    # To keep wall on the RIGHT:
    # Desired heading = closest_angle - 90° (mod 360)
    desired_angle = (closest_angle - 90) % 360

    # Pick shortest turning direction
    turn_amount = desired_angle
    if turn_amount > 180:
        turn_amount -= 360

    print(f"Turning {turn_amount}° so wall stays on right.")
    turn(turn_amount)
    time.sleep(0.1)


# =====================================================
# MOVE EXACTLY 30 CM
# =====================================================
def move_30cm():
    print("Moving forward 30 cm...")
    forward(MOVE_DISTANCE)
    time.sleep(0.1)


# =====================================================
# MAIN FUNCTION (CALL THIS REPEATEDLY)
# =====================================================
def scan_turn_move():
    orient_wall_right()
    move_30cm()
