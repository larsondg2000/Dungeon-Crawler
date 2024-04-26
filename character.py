import pygame
import constants
import math


class Character:
    def __init__(self, x, y, health, mob_animations, char_type):
        self.char_type = char_type
        self.score = 0
        self.flip = False
        self.frame_index = 0
        self.action = 0   # 0: idle 1: running animations
        self.update_time = pygame.time.get_ticks()
        self.running = False
        self.health = health
        self.alive = True
        self.animation_list = mob_animations[char_type]

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(0, 0, constants.TILE_SIZE, constants.TILE_SIZE)
        self.rect.center = (x, y)

    def move(self, dx, dy):
        self.running = False

        if dx != 0 or dy != 0:
            self.running = True

        # sets character image flip
        if dx > 0:
            self.flip = False
        if dx < 0:
            self.flip = True
        # control diagonal speed
        if dx != 0 and dy != 0:
            dx = dx * (math.sqrt(2)/2)
            dy = dy * (math.sqrt(2) / 2)

        self.rect.x += dx
        self.rect.y += dy

    def update(self):
        # check if character has died
        if self.health <= 0:
            self.health = 0
            self.alive = False

        # check action player is performing
        if self.running is True:
            self.update_action(1)
        else:
            self.update_action(0)

        animation_cooldown = 70
        # handle animation
        # update image
        self.image = self.animation_list[self.action][self.frame_index]
        # check update time
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        # check if animation list has finished
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        # check if new action is different
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        if self.char_type == 0:
            surface.blit(flipped_image, (self.rect.x, self.rect.y - constants.SCALE * constants.OFFSET))
        else:
            surface.blit(flipped_image, self.rect)
        pygame.draw.rect(surface, constants.RED, self.rect, 1)
