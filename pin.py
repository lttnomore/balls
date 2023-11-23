import images
import vector
import pygame
import commons

from vector import Vector
from enum import Enum
from pygame.locals import *


class PinType(Enum):
    DEFAULT = 0

class Pin:
    def __init__(self, position: Vector, radius: float = 8, pin_type: PinType = PinType.DEFAULT, image: pygame.Surface = None):
        self.position = vector.copy(position)
        self.velocity = Vector(0, 0)

        self.radius = radius
        self.diameter = radius * 2.0

        self.image = image
        if self.image is None:
            self.image = images.ball_default
        self.bounding_box = Rect(0, 0, 1, 1)
        self.alive = True

    def draw(self):
        top_left_position = self.position - self.radius
        commons.screen.blit(self.image, top_left_position.make_int_tuple())
