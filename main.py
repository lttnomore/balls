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
    global mouse_position
    commons.screen.fill((50, 50, 50))
    entities.draw_all()
    trajectory = Trajectory()
    trajectory.draw_line(mouse_position)

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
                x = (mouse_position[0] - commons.screen_w // 2)
                y = mouse_position[1]
                direction = Vector(x, y)
                entities.balls.append(Ball(Vector(commons.screen_w // 2, 16), vector.normalize(direction) * 1000))
            elif event.button == pygame.BUTTON_RIGHT:
                entities.pins.append(Pin(Vector(mouse_position[0], mouse_position[1])))
    update()
    draw()
    pygame.display.flip()
    commons.delta_time = 0.001 * clock.tick(144)

pygame.quit()
