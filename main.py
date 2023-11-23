import commons
import pygame
import vector
import states
import entities

from pin import Pin
from ball import Ball
from vector import Vector
from trajectory import Trajectory
from states import GameState, PlayState, MenuState

def update():
    entities.update_balls()
    entities.update_pins()

def draw():
    global mouse_position
    global trajectory
    commons.screen.fill((50, 50, 50))
    entities.draw_all()
    trajectory.reset()
    trajectory.draw_line(mouse_position)

def clear():
    entities.delete_balls()
    entities.delete_pins()


pygame.init()

commons.screen = pygame.display.set_mode((commons.screen_w, commons.screen_h))

pygame.display.set_caption("Balls")
app_running = True
clock = pygame.time.Clock()
mouse_position = (0, 0)
trajectory = Trajectory()
while app_running:
    mouse_position = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            app_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                app_running = False
            elif event.key == pygame.K_r:
                clear()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                circle_following_mouse = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                direction = Vector(mouse_position[0] - commons.screen_w // 2, mouse_position[1])
                entities.balls.append(Ball(Vector(commons.screen_w // 2, 16), vector.normalize(direction) * 1000))
            elif event.button == pygame.BUTTON_RIGHT:
                entities.pins.append(Pin(Vector(mouse_position[0], mouse_position[1])))
    update()
    draw()
    pygame.display.flip()
    commons.delta_time = 0.001 * clock.tick(144)

pygame.quit()
