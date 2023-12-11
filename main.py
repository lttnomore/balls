import pygame

import commons
from sprites import *
from config import *
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(None, 36)
        self.ball_spritesheet = Spritesheet('resources/images/ball.png')
        self.default_pin_spritesheet = Spritesheet('resources/images/default_pin.png')
        self.refresh_pin_spritesheet = Spritesheet('resources/images/refresh_pin.png')
        self.bomb_pin_spritesheet = Spritesheet('resources/images/bomb_pin.png')
        self.coin_pin_spritesheet = Spritesheet('resources/images/coin_pin.png')
        self.trajectory_spritesheet = Spritesheet('resources/images/trajectory.png')

    def create_tilemap(self, refresh=False):
        refresh_pins = []

        while len(refresh_pins) != 3:
            c = random.randint(0, 410)
            if c not in self.coins_position and c not in refresh_pins:
                refresh_pins.append(c)

        cur = 0
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                if column == 'P':
                    if cur in refresh_pins:
                        Pin(self, j * 16, i * 32, pin_type='refresh')
                    elif cur in self.coins_position:
                        Pin(self, j * 16, i * 32, pin_type='coin', number=cur)
                    elif random.random() < 0.05:
                        Pin(self, j * 16, i * 32, pin_type='bomb')
                    else:
                        Pin(self, j * 16, i * 32)
                    cur += 1

    def new(self):
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.balls = pygame.sprite.LayeredUpdates()
        self.pins = pygame.sprite.LayeredUpdates()
        self.trajectory = pygame.sprite.LayeredUpdates()
        self.coins = 0
        self.total_damage = 0
        self.coins_count = 100
        self.coins_position = []
        while len(self.coins_position) != self.coins_count:
            c = random.randint(0, 410)
            if c not in self.coins_position:
                self.coins_position.append(c)
        self.create_tilemap()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    for _ in range(20):
                        Pin(self, random.random() * 760.0 + 100.0, random.random() * 520.0 + 100.0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                if event.button == pygame.BUTTON_LEFT:
                    self.total_damage = 0
                    direction = pygame.Vector2(mouse_position[0] - WINDOW_WIDTH // 2, mouse_position[1])
                    Ball(self, WINDOW_WIDTH // 2, 16, direction.normalize() * commons.speed)
                elif event.button == pygame.BUTTON_RIGHT:
                    Pin(self, mouse_position[0], mouse_position[1])

    def update(self):
        self.all_sprites.update()
        self.pins.update()

    def draw(self):
        self.screen.fill((50, 50, 50))
        self.calc_trajectory()
        self.calc_dt()
        self.info()
        self.all_sprites.draw(self.screen)
        self.pins.draw(self.screen)
        self.trajectory.draw(self.screen)
        pygame.display.update()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False

    def game_over(self):
        pass

    def intro_screen(self):
        pass

    def info(self):
        fps_text = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, BLACK)
        delta_time_text = self.font.render(f"Delta Time: {commons.delta_time:.6f}", True, BLACK)
        balls = self.font.render(f"Balls: {len(self.balls)}", True, BLACK)
        pins = self.font.render(f"Pins: {len(self.pins)}", True, BLACK)

        self.screen.blit(fps_text, (10, 10))
        self.screen.blit(delta_time_text, (10, 50))
        self.screen.blit(balls, (10, 90))
        self.screen.blit(pins, (10, 130))
        self.screen.blit(self.font.render(f"Coins: {self.coins}", True, BLACK), (800, 10))
        self.screen.blit(self.font.render(f"Damage: {self.total_damage}", True, BLACK), (800, 50))

    def calc_trajectory(self):
        self.trajectory.empty()
        mouse_position = pygame.mouse.get_pos()
        direction = pygame.Vector2(mouse_position[0] - WINDOW_WIDTH // 2, mouse_position[1])
        position = pygame.Vector2(WINDOW_WIDTH // 2, 16)
        velocity = direction.normalize() * commons.speed
        for _ in range(50):
            velocity[1] += commons.delta_time * commons.gravity
            position += velocity * commons.delta_time
            Trajectory(self, position[0], position[1])

    def calc_dt(self):
        elapsed_time = self.clock.tick(FPS)
        current_delta_time = min(0.001 * elapsed_time, 0.1)
        commons.smoothed_delta_time = commons.smoothing_factor * commons.smoothed_delta_time + (
                    1 - commons.smoothing_factor) * current_delta_time
        commons.delta_time = round(commons.smoothed_delta_time, 3)


game = Game()
game.intro_screen()
game.new()
while game.running:
    game.main()
    game.game_over()

pygame.quit()
sys.exit()
