import images
import vector
import pygame
import commons

from vector import Vector
from enum import Enum
from pygame.locals import *
from pygame.sprite import Sprite, Group


class PinType(Enum):
    DEFAULT = 0


class Pin(Sprite):
    all = Group()
    def __init__(self, position: Vector, radius: float = 8, pin_type: PinType = PinType.DEFAULT, image: pygame.Surface = None):
        super().__init__()
        self.position = vector.copy(position)
        self.velocity = Vector(0, 0)
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
