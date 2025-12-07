import math

def update_coordinates(speed, turn_effort, dt, pos):
    print("reached coordinate update")
    angular_velocity = turn_effort * 0.5

    # Update heading
    pos[2] += angular_velocity * dt
    pos[2] %= 2 * math.pi

    # Update x, y
    distance = speed * dt
    pos[0] += distance * math.cos(pos[2])
    pos[1] += distance * math.sin(pos[2])
