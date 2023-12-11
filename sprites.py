import pygame
import math
import random

import commons

from config import *

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert_alpha()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite

class Ball(pygame.sprite.Sprite):
    def __init__(self, game, x, y, velocity):
        self.game = game
        self._layer = MAIN_LAYER
        self.groups = self.game.all_sprites, self.game.balls
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.velocity = velocity
        self.position = pygame.Vector2(x, y)
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.radius = TILE_SIZE // 2
        self.mass = self.radius
        self.image = self.game.ball_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.rect.x = self.x
        self.rect.y = self.y

        self.damage = 1
        self.alive = True

    def update(self):
        if not self.alive:
            print(self.game.total_damage)
            self.kill()
        else:
            self.rect = self.image.get_rect(center=self.position)
            self.velocity[1] += commons.delta_time * commons.gravity
            self.collide_pin()
            self.collide_border()
            self.position += self.velocity * commons.delta_time

    def collide_border(self):
        if self.position.y >= WINDOW_HEIGHT - self.radius * 1.05:
            # self.rect.y = WINDOW_HEIGHT - self.radius
            self.alive = False
        elif self.position.y < self.radius:
            self.position.y = self.radius

        if self.position.x <= self.radius:
            self.position.x = self.radius
        elif self.position.x >= WINDOW_WIDTH - self.radius:
            self.position.x = WINDOW_WIDTH - self.radius
        if self.position.x <= self.radius or self.position.x >= WINDOW_WIDTH - self.radius:
            self.velocity[0] = -self.velocity[0] * 0.8

        if self.position.y <= self.radius:
            self.velocity[1] = -self.velocity[1] * 0.7
            self.velocity[0] *= 0.995

        # if self.rect.y >= WINDOW_HEIGHT - self.radius:
        #     self.velocity[1] = -self.velocity[1] * 0.7
        #     self.velocity[0] *= 0.995

    def collide_pin(self):
        hits = pygame.sprite.spritecollide(self, self.game.pins, False, pygame.sprite.collide_circle)
        for pin in hits:

            # normal = pygame.Vector2(pin.rect.center) - self.position
            # normal.normalize_ip()
            # speed_along_normal = pygame.Vector2.dot(self.velocity, normal)
            #
            # if speed_along_normal > 0:
            #     overlap = self.radius + pin.radius - pygame.Vector2(pin.rect.center).distance_to(self.position)
            #     impulse_magnitude = -(1 + commons.elasticity) * speed_along_normal
            #     impulse = impulse_magnitude * normal
            #
            #     total_mass = 1 / self.mass + 1 / pin.mass
            #
            #     self.velocity += impulse * (1 / self.mass / total_mass)

            distance = pygame.Vector2(pin.rect.center).distance_to(self.position)
            relative_velocity = - self.velocity
            normal = (pin.position - self.position) / distance

            impulse = 2 * pygame.Vector2.dot(relative_velocity, normal) * self.radius
            impulse *= commons.restitution
            if pin.pin_type == 'bomb':
                impulse = -200

            self.velocity += impulse * normal * self.radius

            overlap = self.radius + pin.radius - distance
            correction = commons.correction_factor * pygame.Vector2.length(relative_velocity) * commons.delta_time
            correction_vector = normal * (overlap + correction) / 2
            self.position -= correction_vector
            pin.damage = self.damage
            pin.alive = False
            # pin.kill()


class Pin(pygame.sprite.Sprite):
    def __init__(self, game, x, y, pin_type='default', number = -1):
        self.game = game
        self._layer = MAIN_LAYER
        self.groups = self.game.pins
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.position = pygame.Vector2(x, y)
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.radius = TILE_SIZE // 2
        self.mass = self.radius
        self.pin_type = pin_type
        if self.pin_type == 'default':
            self.image = self.game.default_pin_spritesheet.get_sprite(0, 0, self.width, self.height)
        elif self.pin_type == 'refresh':
            self.image = self.game.refresh_pin_spritesheet.get_sprite(0, 0, self.width, self.height)
        elif self.pin_type == 'bomb':
            self.image = self.game.bomb_pin_spritesheet.get_sprite(0, 0, self.width, self.height)
        elif self.pin_type == 'coin':
            self.image = self.game.coin_pin_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.rect = self.image.get_rect(center=(x, y))
        self.alive = True
        self.number = number
        self.damage = 0

    def update(self):
        if not self.alive:
            if self.pin_type == 'refresh':
                self.game.pins.empty()
                self.game.create_tilemap(refresh=True)
            elif self.pin_type == 'coin':
                self.game.coins += 1
                self.game.coins_count -= 1
                if self.number in self.game.coins_position:
                    self.game.coins_position.remove(self.number)
            elif self.pin_type == 'bomb':
                for p in self.game.pins:
                    if pygame.Vector2(self.rect.center).distance_to(p.rect.center) < 75:
                        p.alive = False
                        p.damage = self.damage
            self.kill()
            self.game.total_damage += self.damage
class Trajectory(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = MAIN_LAYER
        self.groups = self.game.trajectory
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = 3
        self.height = 3
        self.radius = TILE_SIZE // 2

        # self.image = pygame.Surface((3, 3), pygame.SRCALPHA)
        # self.image.fill((0, 0, 255))
        self.image = self.game.trajectory_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.rect.x = self.x
        self.rect.y = self.y
