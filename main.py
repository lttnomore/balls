import commons
import pygame
import vector
import states
import entities

from ball import Ball
from vector import Vector
from states import GameState, PlayState, MenuState


def update():
    if not circle_following_mouse:
        entities.update_balls()
    else:
        global circle_velocity
        for ball in entities.balls:
            mouse_pos_vec = Vector(mouse_position[0], mouse_position[1])
            diff_vec = mouse_pos_vec - ball.position
            normalized_direction = vector.normalize(diff_vec)
            circle_velocity += normalized_direction * 1000 * commons.delta_time
            ball.velocity = circle_velocity
            ball.position += circle_velocity * commons.delta_time
            ball.check_screen_collisions()
        entities.check_balls_collisions()

def draw():
    commons.screen.fill((50, 50, 50))
    entities.draw_balls()

pygame.init()

commons.screen = pygame.display.set_mode((commons.screen_w, commons.screen_h))

pygame.display.set_caption("Balls")
app_running = True
clock = pygame.time.Clock()
circle_velocity = Vector(0, 0)
circle_following_mouse = False
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
            elif event.key == pygame.K_SPACE:
                circle_following_mouse = True
                circle_velocity = Vector(0, 0)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                circle_following_mouse = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                x = (mouse_position[0] - commons.screen_w // 2) / commons.screen_w
                y = mouse_position[1] / commons.screen_h
                direction = Vector(x, y)
                entities.balls.append(Ball(Vector(commons.screen_w // 2, 0), vector.normalize(direction) * 1000))
            elif event.button == pygame.BUTTON_RIGHT:
                entities.balls.append(Ball(Vector(mouse_position[0], mouse_position[1])))
    update()
    draw()

    pygame.display.flip()
    commons.delta_time = 0.001 * clock.tick(144)

pygame.quit()
