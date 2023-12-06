import commons
import pygame
import numpy as np
from ball import Ball
from trajectory import Trajectory
from pin import Pin
import entities
import time
import cProfile


def update():
    entities.update_balls()
    entities.update_pins()


def draw():
    commons.screen.fill((50, 50, 50))
    entities.draw_all()


def clear():
    entities.delete_balls()
    entities.delete_pins()


pygame.init()
commons.screen = pygame.display.set_mode((commons.screen_w, commons.screen_h))
font = pygame.font.Font(None, 36)
pygame.display.set_caption("Balls")
app_running = True
clock = pygame.time.Clock()
prev_time = pygame.time.get_ticks()
mouse_position = (0, 0)
trajectory = Trajectory(Ball(np.array([commons.screen_w // 2, 16], dtype=float), np.array([0, 0], dtype=float) * 1000))

while app_running:
    profiler = cProfile.Profile()
    profiler.enable()
    start_time = time.time()
    prev_mouse_position = mouse_position
    mouse_position = pygame.mouse.get_pos()
    direction = np.array([mouse_position[0] - commons.screen_w // 2, mouse_position[1]], dtype=float)

    ball_position = np.array([commons.screen_w // 2, 16], dtype=float)
    ball_velocity = direction / np.linalg.norm(direction) * 1000
    # trajectory = Trajectory(Ball(ball_position, ball_velocity))

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
                for _ in range(20):
                    entities.add_pin()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                Ball.all.add(Ball(np.array([commons.screen_w // 2, 16], dtype=float),
                                  direction / np.linalg.norm(direction) * 1000))
            elif event.button == pygame.BUTTON_RIGHT:
                Pin.all.add(Pin(np.array([mouse_position[0], mouse_position[1]], dtype=float)))

    update()
    draw()

    # trajectory.draw()

    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
    delta_time_text = font.render(f"Delta Time: {commons.delta_time:.6f}", True, (255, 255, 255))
    balls = font.render(f"Balls: {len(Ball.all)}", True, (255, 255, 255))
    pins = font.render(f"Pins: {len(Pin.all)}", True, (255, 255, 255))

    commons.screen.blit(fps_text, (10, 10))
    commons.screen.blit(delta_time_text, (10, 50))
    commons.screen.blit(balls, (10, 90))
    commons.screen.blit(pins, (10, 130))

    pygame.display.flip()
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - prev_time
    commons.delta_time = round((1 - commons.alpha) * commons.delta_time + commons.alpha * (elapsed_time / 1000.0), 3)
    prev_time = current_time
    clock.tick(commons.fps)
    profiler.disable()
    # commons.delta_time = 0.001 * clock.tick(commons.fps)

pygame.quit()
profiler.print_stats()
