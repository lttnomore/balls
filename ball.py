import numpy as np
import images
import commons
from enum import Enum
from collisions import check_hit, check_screen_collisions
from pygame.locals import *
from pygame.sprite import Sprite, Group

class BallType(Enum):
    DEFAULT = 0

class Ball(Sprite):
    all = Group()

    def __init__(self, position, velocity=np.array([0, 0]), radius=8,
                 ball_type=BallType.DEFAULT, image=None):
        super().__init__()
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)

        self.radius = radius
        self.diameter = radius * 2.0
        self.image = image if image is not None else images.ball_default
        self.rect = self.image.get_rect(center=self.position.astype(int))
        self.alive = True

    def update(self):
        if not self.alive:
            self.kill()
        else:
            check_hit(self, False)
            self.rect = self.image.get_rect(center=self.position.astype(int))
            self.velocity[1] += commons.delta_time * commons.gravity
            check_screen_collisions(self)
            self.position += self.velocity * commons.delta_time
