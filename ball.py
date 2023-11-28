import images
import commons
import pygame
import vector

from vector import Vector
from enum import Enum
from pygame.locals import *
from pygame.sprite import Sprite, Group


class BallType(Enum):
    DEFAULT = 0


class Ball(Sprite):
    all = Group()
    def __init__(self, position: Vector, velocity: Vector = Vector(0, 0), radius: float = 8,
                 ball_type: BallType = BallType.DEFAULT, image: pygame.Surface = None):
        super().__init__()
        self.position = vector.copy(position)
        self.velocity = vector.copy(velocity)

        self.radius = radius
        self.diameter = radius * 2.0
        self.image = image
        if self.image is None:
            self.image = images.ball_default
        self.rect = self.image.get_rect(center=self.position.make_int_tuple())
        self.alive = True

    def update(self):
        if not self.alive:
            self.kill()
        else:
            self.rect = self.image.get_rect(center=self.position.make_int_tuple())
            self.velocity.y += commons.delta_time * commons.gravity
            self.check_screen_collisions()
            self.position += self.velocity * commons.delta_time

    def check_screen_collisions(self):
        if self.position.y >= commons.screen_h - self.radius * 1.05:
            # self.position.y = commons.screen_h - self.radius
            self.alive = False
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
