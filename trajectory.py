import pygame
from pygame.locals import *
import numpy as np
import commons
from collisions import check_screen_collisions, check_hit
import cProfile
from pin import Pin

class Trajectory:
    def __init__(self, ball, max_points=commons.trajectory_points):
        self.ball = ball
        self.max_points = max_points
        self.points = self.calculate_trajectory()
        self.rendered_surface = pygame.Surface(commons.screen.get_size(), pygame.SRCALPHA)

    # def update(self):
    #     if len(self.points) < self.max_points:
    #         predicted_positions = self.calculate_trajectory()
    #         self.points.extend(predicted_positions)

    def draw(self):
        if len(self.points) > 1:
            pygame.draw.aalines(commons.screen, (0, 0, 255), False, self.points, 4)
            commons.screen.blit(self.rendered_surface, (0, 0))

    def calculate_trajectory(self):
        positions = [np.copy(self.ball.position)]

        for _ in range(self.max_points - 1):
            check_hit(self.ball, True)
            self.ball.velocity[1] += commons.delta_time * commons.gravity
            check_screen_collisions(self.ball)
            self.ball.position += self.ball.velocity * commons.delta_time
            positions.append(np.copy(self.ball.position))
        return [(int(pos[0]), int(pos[1])) for pos in positions]
