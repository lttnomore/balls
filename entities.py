import numpy as np
from ball import Ball
import vector
import commons
from collisions import check_balls_collisions
from pin import Pin

@staticmethod
def update_balls():
    check_balls_collisions(list(Ball.all))
    Ball.all.update()

@staticmethod
def update_pins():
    Pin.all.update()


@staticmethod
def draw_all():
    Pin.all.draw(commons.screen)
    Ball.all.draw(commons.screen)

@staticmethod
def delete_balls():
    for ball in Ball.all:
        ball.kill()

@staticmethod
def delete_pins():
    for pin in Pin.all:
        pin.kill()


@staticmethod
def add_pin():
    new_pin = Pin(np.random.rand(2) * np.array([760.0, 520.0]) + np.array([100.0, 100.0]))
    Pin.all.add(new_pin)
