SERVO_PICKUP = 12.0
SERVO_CARRY = 40.0
MAX_EFFORT = 0.5
PICKUP_DISTANCE = 18.0
PICKUP_INCREMENTS = 10

def pick_up():
    # Deploy arm
            servo.set_angle(SERVO_PICKUP)
            
            # Drive forward to pick up basket
            drivetrain.straight(
                distance=PICKUP_DISTANCE,
                max_effort=MAX_EFFORT,
            )
            
            # Pick up basket (somewhat slowly)
            period = 1 / PICKUP_INCREMENTS
            for i in range(PICKUP_INCREMENTS):
                servo.set_angle(
                    ((SERVO_CARRY - SERVO_PICKUP) * (period * i)) + SERVO_PICKUP
                )
                time.sleep(period)
            servo.set_angle(SERVO_CARRY)
            time.sleep(1.0)
            
            # Continue to state 3
            print("Searching for target...")
            current_state = 3
            continue