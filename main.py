import commons
import pygame
import vector
import states
import entities

from ball import Ball
from vector import Vector
from states import GameState, PlayState, MenuState


def update():
    entities.update_balls()


def draw():
    commons.screen.fill((50, 50, 50))
    entities.draw_balls()


pygame.init()

commons.screen = pygame.display.set_mode((commons.screen_w, commons.screen_h))

pygame.display.set_caption("Balls")
app_running = True
clock = pygame.time.Clock()

mouse_position = (0, 0)

while app_running:
    mouse_position = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            app_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                app_running = False
            elif event.key == pygame.K_r:
                entities.delete_balls()
        elif event.type == pygame.KEYUP:
            pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                x = (mouse_position[0] - commons.screen_w // 2) / commons.screen_w
                y = mouse_position[1] / commons.screen_h
                direction = Vector(x, y)
                entities.balls.append(Ball(Vector(commons.screen_w // 2, 0), vector.normalize(direction) * 1000))

    update()
    draw()

    pygame.display.flip()
    commons.delta_time = 0.001 * clock.tick(144)

pygame.quit()
