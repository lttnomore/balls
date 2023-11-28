import pygame
from pygame.locals import *
import vector
import commons


from pin import Pin

class Trajectory:
    def __init__(self, ball, max_points=commons.trajectory_points):
        self.ball = ball
        self.max_points = max_points
        self.points = []


    def update(self):
        predicted_positions = self.calculate_trajectory()
        self.points.extend(predicted_positions)
        if len(self.points) > self.max_points:
            self.points = self.points[-self.max_points:]

    def draw(self):
        for i in range(len(self.points) - 1):
            start_pos = self.points[i].make_int_tuple()
            end_pos = self.points[i + 1].make_int_tuple()
            pygame.draw.aaline(commons.screen, (0, 0, 255), start_pos, end_pos, 4)

    def calculate_trajectory(self):
        positions = []

        for _ in range(self.max_points):
            positions.append(vector.copy(self.ball.position))
            max_collision_distance = (self.ball.radius + 8) * 1.5
            for pin in Pin.all:
                distance_squared = vector.dist_sqr(self.ball.position, pin.position)
                if distance_squared <= max_collision_distance ** 2:
                    sum_of_radii = self.ball.radius + pin.radius
                    if distance_squared <= sum_of_radii ** 2:
                        relative_velocity = -self.ball.velocity
                        normal = vector.normalize(pin.position - self.ball.position)

                        impulse = 2 * vector.dot(relative_velocity, normal) / (1 / self.ball.radius)
                        impulse *= commons.restitution

                        self.ball.velocity += impulse * normal / (1 / self.ball.radius)

                        overlap = sum_of_radii - distance_squared ** 0.5
                        correction = commons.correction_factor * vector.length(relative_velocity) * commons.delta_time
                        correction_vector = normal * (overlap + correction) / 2

                        self.ball.position -= correction_vector
                        break
            self.ball.velocity.y += commons.delta_time * commons.gravity
            self.ball.position += self.ball.velocity * commons.delta_time
        return positions
