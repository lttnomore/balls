import numpy as np
import images
import pygame
from enum import Enum
from pygame.locals import *
from pygame.sprite import Sprite, Group

class PinType(Enum):
    DEFAULT = 0

class Pin(Sprite):
    all = Group()

    def __init__(self, position, radius=8, pin_type=PinType.DEFAULT, image=None):
        super().__init__()
        self.position = np.array(position, dtype=float)
        self.velocity = np.array([0, 0], dtype=float)
        self.radius = radius
        self.diameter = radius * 2.0

        self.image = image if image is not None else images.ball_default
        self.rect = self.image.get_rect(center=self.position.astype(int))
        self.alive = True

    def update(self):
        if not self.alive:
            self.kill()
