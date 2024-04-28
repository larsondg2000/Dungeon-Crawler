import random
import pygame
import math
import constants


class Weapon:
    def __init__(self, image, arrow_image):
        self.original_image = image
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.arrow_image = arrow_image
        self.fired = False
        self.last_shot = pygame.time.get_ticks()

    def update(self, player):
        shot_cooldown = 300
        arrow = None

        self.rect.center = player.rect.center

        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - self.rect.centerx
        y_dist = -(pos[1] - self.rect.centery)
        self.angle = math.degrees(math.atan2(y_dist, x_dist))

        # Get mouse clicks 0 -> left click, 2-> right click
        if pygame.mouse.get_pressed()[0] and self.fired is False and (
                pygame.time.get_ticks() - self.last_shot) >= shot_cooldown:
            arrow = Arrow(self.arrow_image, self.rect.centerx, self.rect.centery, self.angle)
            self.fired = True
            self.last_shot = pygame.time.get_ticks()

        # reset firing trigger to false
        if not pygame.mouse.get_pressed()[0]:
            self.fired = False

        return arrow

    def draw(self, surface):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        surface.blit(self.image,
                     ((self.rect.centerx - int(self.image.get_width() / 2)),
                      (self.rect.centery - int(self.image.get_height() / 2))))


class Arrow(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # calculate horizontal and vertical speeds based on angle
        self.dx = math.cos(math.radians(self.angle)) * constants.ARROW_SPEED
        self.dy = -(math.sin(math.radians(self.angle)) * constants.ARROW_SPEED)

    def update(self, screen_scroll, obstacle_tiles, enemy_list):
        # reset variables
        damage = 0
        damage_pos = None
        # reposition based on speed
        self.rect.x += screen_scroll[0] + self.dx
        self.rect.y += screen_scroll[1] + self.dy

        # Check for collision with walls
        for obstacle in obstacle_tiles:
            if obstacle[1].colliderect(self.rect):
                self.kill()

        # check if arrow is off-screen
        if (self.rect.right < 0
                or self.rect.left > constants.SCREEN_WIDTH
                or self.rect.bottom < 0
                or self.rect.top > constants.SCREEN_HEIGHT):
            self.kill()

        # Check collision between arrow and enemy
        for enemy in enemy_list:
            if enemy.rect.colliderect(self.rect) and enemy.alive:
                damage = 10 + random.randint(-5, 5)
                damage_pos = enemy.rect
                enemy.health -= damage
                enemy.hit = True
                self.kill()
                break
        return damage, damage_pos

    def draw(self, surface):
        surface.blit(self.image,
                     ((self.rect.centerx - int(self.image.get_width() / 2)),
                      (self.rect.centery - int(self.image.get_height() / 2))))


class FireBall(pygame.sprite.Sprite):
    def __init__(self, image, x, y, target_x, target_y):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        x_dist = target_x - x
        y_dist = -(target_y - y)
        self.angle = math.degrees(math.atan2(y_dist, x_dist))
        self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # calculate horizontal and vertical speeds based on angle
        self.dx = math.cos(math.radians(self.angle)) * constants.FIREBALL_SPEED
        self.dy = -(math.sin(math.radians(self.angle)) * constants.FIREBALL_SPEED)

    def update(self, screen_scroll, player):

        # reposition based on speed
        self.rect.x += screen_scroll[0] + self.dx
        self.rect.y += screen_scroll[1] + self.dy

        # check if fireball is off-screen
        if (self.rect.right < 0
                or self.rect.left > constants.SCREEN_WIDTH
                or self.rect.bottom < 0
                or self.rect.top > constants.SCREEN_HEIGHT):
            self.kill()
        # check fireball collision with player
        if player.rect.colliderect(self.rect) and player.hit == False:
            player.hit = True
            player.last_hit = pygame.time.get_ticks()
            player.health -= 5
            self.kill()


    def draw(self, surface):
        surface.blit(self.image,
                     ((self.rect.centerx - int(self.image.get_width() / 2)),
                      (self.rect.centery - int(self.image.get_height() / 2))))
