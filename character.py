import pygame
import constants
import math


class Character:
    def __init__(self, x, y, health, mob_animations, char_type, boss, size):
        self.char_type = char_type
        self.boss = boss
        self.score = 0
        self.flip = False
        self.frame_index = 0
        self.action = 0  # 0: idle 1: running animations
        self.update_time = pygame.time.get_ticks()
        self.running = False
        self.health = health
        self.alive = True
        self.animation_list = mob_animations[char_type]
        self.hit = False
        self.last_hit = pygame.time.get_ticks()
        self.stunned = False

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(0, 0, constants.TILE_SIZE * size, constants.TILE_SIZE * size)
        self.rect.center = (x, y)

    def move(self, dx, dy, obstacle_tiles):
        screen_scroll = [0, 0]
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
            dx = dx * (math.sqrt(2) / 2)
            dy = dy * (math.sqrt(2) / 2)

        # Check for collision in x direction
        self.rect.x += dx
        for obstacle in obstacle_tiles:
            if obstacle[1].colliderect(self.rect):
                if dx > 0:
                    self.rect.right = obstacle[1].left
                if dx < 0:
                    self.rect.left = obstacle[1].right

        self.rect.y += dy
        for obstacle in obstacle_tiles:
            if obstacle[1].colliderect(self.rect):
                if dy > 0:
                    self.rect.bottom = obstacle[1].top
                if dy < 0:
                    self.rect.top = obstacle[1].bottom

        # check if its player
        if self.char_type == 0:
            # Left and right
            if self.rect.right > (constants.SCREEN_WIDTH - constants.SCROLL_THRESH):
                screen_scroll[0] = (constants.SCREEN_WIDTH - constants.SCROLL_THRESH) - self.rect.right
                self.rect.right = constants.SCREEN_WIDTH - constants.SCROLL_THRESH
            if self.rect.left < constants.SCROLL_THRESH:
                screen_scroll[0] = constants.SCROLL_THRESH - self.rect.left
                self.rect.left = constants.SCROLL_THRESH
            # Up and down
            if self.rect.bottom > (constants.SCREEN_HEIGHT - constants.SCROLL_THRESH):
                screen_scroll[1] = (constants.SCREEN_HEIGHT - constants.SCROLL_THRESH) - self.rect.bottom
                self.rect.bottom = constants.SCREEN_HEIGHT - constants.SCROLL_THRESH
            if self.rect.top < constants.SCROLL_THRESH:
                screen_scroll[1] = constants.SCROLL_THRESH - self.rect.top
                self.rect.top = constants.SCROLL_THRESH

        return screen_scroll

    def ai(self, player, obstacle_tiles, screen_scroll):
        clipped_line = ()
        stun_cooldown = 100
        ai_dx = 0
        ai_dy = 0

        # reposition mob
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        # Create los from enemy to player
        line_of_site = ((self.rect.centerx, self.rect.centery), (player.rect.centerx, player.rect.centery))

        # Check if los passes through obstacle tile
        for obstacle in obstacle_tiles:
            if obstacle[1].clipline(line_of_site):
                clipped_line = obstacle[1].clipline(line_of_site)
        # Check distance to player
        dist = math.sqrt(((self.rect.centerx - player.rect.centerx) ** 2) +
                         ((self.rect.centery - player.rect.centery) ** 2))
        if not clipped_line and dist > constants.RANGE:
            # calculate enemy movement based on player position
            if self.rect.centerx > player.rect.centerx:
                ai_dx = -constants.ENEMY_SPEED
            if self.rect.centerx < player.rect.centerx:
                ai_dx = constants.ENEMY_SPEED
            if self.rect.centery > player.rect.centery:
                ai_dy = -constants.ENEMY_SPEED
            if self.rect.centery < player.rect.centery:
                ai_dy = constants.ENEMY_SPEED

        if self.alive:
            if not self.stunned:
                self.move(ai_dx, ai_dy, obstacle_tiles)
                # Attack player
                if dist < constants.ATTACK_RANGE and player.hit == False:
                    player.health -= 10
                    player.hit = True
                    player.last_hit = pygame.time.get_ticks()

            # Check if enemy is hit
            if self.hit is True:
                self.hit = False
                self.last_hit = pygame.time.get_ticks()
                self.stunned = True
                self.running = False
                self.update_action(0)

            if pygame.time.get_ticks() - self.last_hit > stun_cooldown:
                self.stunned = False

    def update(self):
        # check if character has died
        if self.health <= 0:
            self.health = 0
            self.alive = False

        # Timer to reset player taking hit
        hit_cooldown = 1000
        if self.char_type == 0:
            if self.hit is True and (pygame.time.get_ticks() - self.last_hit) > hit_cooldown:
                self.hit = False

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
