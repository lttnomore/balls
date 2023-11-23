from ball import Ball
import vector
import commons


balls = []
pins = []


@staticmethod
def update_balls():
    check_hit()
    check_balls_collisions()
    for i in range(len(balls) - 1, -1, -1):
        balls[i].update()
        if not balls[i].alive:
            balls.pop(i)
            # print(len(balls))

@staticmethod
def update_pins():
    for i in range(len(pins) - 1, -1, -1):
        if not pins[i].alive:
            pins.pop(i)

@staticmethod
def draw_all():
    draw_pins()
    draw_balls()


@staticmethod
def draw_balls():
    for i in range(len(balls)):
        balls[i].draw()

@staticmethod
def draw_pins():
    for i in range(len(pins)):
        pins[i].draw()

@staticmethod
def check_balls_collisions():
    for i in range(len(balls) - 1, -1, -1):
        for j in range(i - 1, -1, -1):
            distance = vector.dist(balls[i].position, balls[j].position)
            if distance <= (balls[i].radius + balls[j].radius):
                relative_velocity = balls[j].velocity - balls[i].velocity
                normal = vector.normalize(balls[j].position - balls[i].position)

                impulse = 2 * vector.dot(relative_velocity, normal) / (1 / balls[i].radius + 1 / balls[j].radius)
                impulse *= commons.restitution

                balls[i].velocity += impulse * normal / (1 / balls[i].radius)
                balls[j].velocity -= impulse * normal / (1 / balls[j].radius)

                overlap = balls[i].radius + balls[j].radius - distance

                correction = commons.correction_factor * vector.length(relative_velocity) * commons.time_step
                correction_vector = normal * (overlap + correction) / 2

                balls[i].position -= correction_vector
                balls[j].position += correction_vector

@staticmethod
def delete_balls():
    balls.clear()

@staticmethod
def delete_pins():
    pins.clear()

@staticmethod
def check_hit():
    for i in range(len(balls) - 1, -1, -1):
        for j in range(len(pins) - 1, -1, -1):
            distance = vector.dist(balls[i].position, pins[j].position)
            if distance <= (balls[i].radius + pins[j].radius):
                relative_velocity = -balls[i].velocity
                normal = vector.normalize(pins[j].position - balls[i].position)

                impulse = 2 * vector.dot(relative_velocity, normal) / (1 / balls[i].radius)
                impulse *= commons.restitution

                balls[i].velocity += impulse * normal / (1 / balls[i].radius)

                overlap = balls[i].radius + pins[j].radius - distance
                correction = commons.correction_factor * vector.length(relative_velocity) * commons.time_step
                correction_vector = normal * (overlap + correction) / 2

                balls[i].position -= correction_vector
                pins[j].alive = False