from ball import Ball
import vector
import commons
balls = []

@staticmethod
def update_balls():
    check_balls_collisions()
    for i in range(len(balls) - 1, -1, -1):
        balls[i].update()
        if not balls[i].alive:
            balls.pop(i)
            # print(len(balls))

@staticmethod
def draw_balls():
    for i in range(len(balls)):
        balls[i].draw()

@staticmethod
def check_balls_collisions():
    for i in range(len(balls) - 1, -1, -1):
        for j in range(i - 1, -1, -1):
            distance = vector.dist(balls[i].position, balls[j].position)
            if distance <= (balls[i].radius + balls[j].radius):
                relative_velocity = balls[j].velocity - balls[i].velocity
                normal = vector.normalize(balls[j].position - balls[i].position)

                impulse = 2 * vector.dot(relative_velocity, normal) / (1 / balls[i].radius + 1 / balls[j].radius)
                restitution = 0.01
                impulse *= restitution

                balls[i].velocity += impulse * normal / (1 / balls[i].radius)
                balls[j].velocity -= impulse * normal / (1 / balls[j].radius)

                overlap = balls[i].radius + balls[j].radius - distance
                correction_factor = 0.15
                correction = correction_factor * vector.length(relative_velocity) * commons.delta_time
                correction_vector = normal * (overlap + correction) / 2

                balls[i].position -= correction_vector
                balls[j].position += correction_vector

@staticmethod
def delete_balls():
    balls.clear()
