from ball import Ball
import vector
import commons

from pin import Pin

@staticmethod
def update_balls():
    check_hit()
    #check_balls_collisions()
    Ball.all.update()

@staticmethod
def update_pins():
    Pin.all.update()


@staticmethod
def draw_all():
    Pin.all.draw(commons.screen)
    Ball.all.draw(commons.screen)

@staticmethod
def check_balls_collisions():
    balls = list(Ball.all)
    num_balls = len(balls)

    for i in range(num_balls - 1, -1, -1):
        for j in range(i - 1, -1, -1):
            ball_i = balls[i]
            ball_j = balls[j]

            distance = vector.dist(ball_i.position, ball_j.position)
            if distance <= (ball_i.radius + ball_j.radius):
                relative_velocity = ball_j.velocity - ball_i.velocity
                normal = vector.normalize(ball_j.position - ball_i.position)

                impulse = 2 * vector.dot(relative_velocity, normal) / (1 / ball_i.radius + 1 / ball_j.radius)
                impulse *= commons.restitution

                ball_i.velocity += impulse * normal / (1 / ball_i.radius)
                ball_j.velocity -= impulse * normal / (1 / ball_j.radius)

                overlap = ball_i.radius + ball_j.radius - distance

                correction = commons.correction_factor * vector.length(relative_velocity) * commons.delta_time
                correction_vector = normal * (overlap + correction) / 2

                ball_i.position -= correction_vector
                ball_j.position += correction_vector

@staticmethod
def delete_balls():
    for ball in Ball.all:
        ball.kill()

@staticmethod
def delete_pins():
    for pin in Pin.all:
        pin.kill()

@staticmethod
def check_hit():
    for ball in Ball.all:
        for pin in Pin.all:
            distance = vector.dist(ball.position, pin.position)
            if distance <= ball.radius + pin.radius:
                relative_velocity = -ball.velocity
                normal = vector.normalize(pin.position - ball.position)

                impulse = 2 * vector.dot(relative_velocity, normal) / (1 / ball.radius)
                impulse *= commons.restitution

                ball.velocity += impulse * normal / (1 / ball.radius)

                overlap = ball.radius + pin.radius - distance
                correction = commons.correction_factor * vector.length(relative_velocity) * commons.delta_time
                correction_vector = normal * (overlap + correction) / 2

                ball.position -= correction_vector
                pin.alive = False
                break
            # d = vector.dist(ball.position, pin.position)
            # if d - ball.radius <= pin.radius:
            #     deltanorm = (ball.position - pin.position) / d
            #     ball.position = ball.position + deltanorm * (pin.radius - (d - ball.radius) + 0.1)
            #     ball.velocity = (ball.velocity - deltanorm * (2 * (vector.dot(deltanorm, ball.velocity)))) * 0.695
            #     pin.alive = False

@staticmethod
def add_pin():
    new_pin = Pin(vector.random_vector())
    Pin.all.add(new_pin)