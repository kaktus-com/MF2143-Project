def drive_to(x_center, y_center, width, height):
    x_done = False
            if x_center < (BASKET_X_TARGET - BASKET_X_DEADZONE):
                drivetrain.set_speed(
                    left_speed=-LINEUP_TURN_SPEED,
                    right_speed=LINEUP_TURN_SPEED,
                )
            elif x_center > (BASKET_X_TARGET + BASKET_X_DEADZONE):
                drivetrain.set_speed(
                    left_speed=LINEUP_TURN_SPEED,
                    right_speed=-LINEUP_TURN_SPEED,
                )
            else:
                drivetrain.set_speed(
                    left_speed=0.0,
                    right_speed=0.0
                )
                x_done = True
                
            # Keep lining up x if needed
            if not x_done:
                continue
                
            # If X is lined up, line up Y
            if y_center < (BASKET_Y_TARGET - BASKET_Y_DEADZONE):
                drivetrain.set_speed(
                    left_speed=DRIVE_SPEED,
                    right_speed=DRIVE_SPEED,
                )
                wait_counter = 0
            elif y_center > (BASKET_Y_TARGET + BASKET_Y_DEADZONE):
                drivetrain.set_speed(
                    left_speed=-DRIVE_SPEED,
                    right_speed=-DRIVE_SPEED,
                )
                wait_counter = 0
            else:
                
                # Make sure basket is lined up 5 times in a row
                wait_counter += 1
                if wait_counter >= 5:
                    print(f"Getting basket: ({x_center:.3f}, {y_center:.3f})")
                    drivetrain.set_speed(
                        left_speed=0.0,
                        right_speed=0.0,
                    )
                    time.sleep(1.0)
                    current_state = 2
                    continue