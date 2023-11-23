import commons
import vector
import pygame

from entities import pins
from vector import Vector


class Trajectory:
    def __init__(self):
        self.start = Vector(commons.screen_w // 2, 16)
        self.end = Vector(commons.screen_w // 2, 16)
        self.velocity = None

    def reset(self):
        self.start = Vector(commons.screen_w // 2, 16)
        self.end = Vector(commons.screen_w // 2, 16)
        self.velocity = None

    def draw_line(self, mouse_position):
        direction = Vector(mouse_position[0] - commons.screen_w // 2, mouse_position[1])
        self.velocity = vector.normalize(direction) * 1000
        self.start = vector.copy(self.end)

        iteration = 0
        max_iterations = 1000

        while iteration < max_iterations:
            self.velocity.y += commons.time_step * commons.gravity
            self.check_screen_collisions()
            self.check_hit()
            self.end += self.velocity * commons.time_step

            pygame.draw.line(commons.screen, (255, 0, 0), self.start.make_int_tuple(), self.end.make_int_tuple(), 2)
            self.start = vector.copy(self.end)
            iteration += 1


    def check_screen_collisions(self):
        if self.end.y >= commons.screen_h - 8 * 1.05:
            self.end.y = commons.screen_h - 8
        elif self.end.y < 8:
            self.end.y = 8

        if self.end.x < 8:
            self.end.x = 8
        elif self.end.x > commons.screen_w - 8:
            self.end.x = commons.screen_w - 8

        if self.end.x <= 8 or self.end.x >= commons.screen_w - 8:
            self.velocity.x = -self.velocity.x * 0.8
        if self.end.y <= 8 or self.end.y >= commons.screen_h - 8:
            self.velocity.y = -self.velocity.y * 0.7
            self.velocity.x *= 0.995

    def check_hit(self):
        for j in range(len(pins) - 1, -1, -1):
            distance = vector.dist(self.end, pins[j].position)
            if distance <= (8 + pins[j].radius):
                relative_velocity = - self.velocity
                normal = vector.normalize(pins[j].position - self.end)

                impulse = 2 * vector.dot(relative_velocity, normal) / (1 / 8)

                impulse *= commons.restitution

                self.velocity += impulse * normal / (1 / 8)

                overlap = 8 + pins[j].radius - distance

                correction = commons.correction_factor * vector.length(relative_velocity) * commons.time_step
                correction_vector = normal * (overlap + correction) / 2

                self.end -= correction_vector
                break
                # balls[j].position += correction_vector