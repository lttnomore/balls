import commons
import numpy as np
from pin import Pin


def check_screen_collisions(ball):
    ball.position[1] = np.clip(ball.position[1], ball.radius, commons.screen_h - ball.radius)

    if ball.position[1] >= commons.screen_h - ball.radius * 1.05:
        ball.position[1] = commons.screen_h - ball.radius
        # ball.alive = False
    elif ball.position[1] < ball.radius:
        ball.position[1] = ball.radius

    if ball.position[0] <= ball.radius:
        ball.position[0] = ball.radius
    elif ball.position[0] >= commons.screen_w - ball.radius:
        ball.position[0] = commons.screen_w - ball.radius

    if ball.position[0] <= ball.radius or ball.position[0] >= commons.screen_w - ball.radius:
        ball.velocity[0] = -ball.velocity[0] * 0.8

    if ball.position[1] <= ball.radius:
        ball.velocity[1] = -ball.velocity[1] * 0.7
        ball.velocity[0] *= 0.995

    if ball.position[1] >= commons.screen_h - ball.radius:
        ball.velocity[1] = -ball.velocity[1] * 0.7
        ball.velocity[0] *= 0.995
def check_hit(ball, trajectory):
    for pin in Pin.all:
        distance = np.linalg.norm(ball.position - pin.position)
        sum_of_radii = ball.radius + pin.radius

        if distance <= sum_of_radii:
            relative_velocity = -ball.velocity
            normal = (pin.position - ball.position) / distance

            impulse = 2 * np.dot(relative_velocity, normal) * ball.radius
            impulse *= commons.restitution

            ball.velocity += impulse * normal * ball.radius

            overlap = ball.radius + pin.radius - distance
            correction = commons.correction_factor * np.linalg.norm(relative_velocity) * commons.delta_time
            correction_vector = normal * (overlap + correction) / 2

            ball.position -= correction_vector
            if not trajectory:
                pin.alive = False
            break

def check_balls_collisions(balls):
    num_balls = len(balls)

    for i in range(num_balls - 1, -1, -1):
        for j in range(i - 1, -1, -1):
            ball_i = balls[i]
            ball_j = balls[j]

            distance = np.linalg.norm(ball_i.position - ball_j.position)
            if distance <= (ball_i.radius + ball_j.radius):
                relative_velocity = ball_j.velocity - ball_i.velocity
                normal = (ball_j.position - ball_i.position) / distance

                impulse = 2 * np.dot(relative_velocity, normal) / (1 / ball_i.radius + 1 / ball_j.radius)
                impulse *= commons.restitution

                ball_i.velocity += impulse * normal / (1 / ball_i.radius)
                ball_j.velocity -= impulse * normal / (1 / ball_j.radius)

                overlap = ball_i.radius + ball_j.radius - distance

                correction = commons.correction_factor * np.linalg.norm(relative_velocity) * commons.delta_time
                correction_vector = normal * (overlap + correction) / 2

                ball_i.position -= correction_vector
                ball_j.position += correction_vector