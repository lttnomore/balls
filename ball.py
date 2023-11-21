import images
import commons
import pygame
import vector

from vector import Vector
from enum import Enum
from pygame.locals import *


class BallType(Enum):
    DEFAULT = 0

class Ball:
    def __init__(self, position: Vector, velocity: Vector = Vector(0, 0), radius: float = 8,
                 ball_type: BallType = BallType.DEFAULT, image: pygame.Surface = None):
        self.position = vector.copy(position)
        self.velocity = vector.copy(velocity)

        self.radius = radius
        self.diameter = radius * 2.0

        self.image = image
        if self.image is None:
            self.image = images.ball_default
        self.bounding_box = Rect(0, 0, 1, 1)
        self.alive = True

    def update(self):
        self.velocity.y += commons.delta_time * commons.gravity
        self.check_screen_collisions()
        self.position += self.velocity * commons.delta_time

    def draw(self):
        top_left_position = self.position - self.radius
        commons.screen.blit(self.image, top_left_position.make_int_tuple())

    def check_screen_collisions(self):
        if self.position.y >= commons.screen_h - self.radius * 1.05:
            self.position.y = commons.screen_h - self.radius
            #self.alive = False
        elif self.position.y < self.radius:
            self.position.y = self.radius

        if self.position.x < self.radius:
            self.position.x = self.radius
        elif self.position.x > commons.screen_w - self.radius:
            self.position.x = commons.screen_w - self.radius

        if self.position.x <= self.radius or self.position.x >= commons.screen_w - self.radius:
            self.velocity.x = -self.velocity.x * 0.8
        if self.position.y <= self.radius or self.position.y >= commons.screen_h - self.radius:
            self.velocity.y = -self.velocity.y * 0.7
            self.velocity.x *= 0.995
