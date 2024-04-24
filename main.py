import pygame

import constants
from character import Character
from weapon import Weapon

pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Crawler")

# Create clock for maintaining frame rate
clock = pygame.time.Clock()

# Define player movement variables
moving_left = False
moving_right = False
moving_up = False
moving_down = False

# define font
font = pygame.font.Font("assets/fonts/AtariClassic.ttf", 20)


# helper function to scale image
def scale_image(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w * scale, h * scale))


# Load Player health images
heart_empty = scale_image(pygame.image.load("assets/images/items/heart_empty.png").convert_alpha(),
                          constants.ITEM_SCALE)
heart_half = scale_image(pygame.image.load("assets/images/items/heart_half.png").convert_alpha(),
                         constants.ITEM_SCALE)
heart_full = scale_image(pygame.image.load("assets/images/items/heart_full.png").convert_alpha(),
                         constants.ITEM_SCALE)

# weapon images
bow_image = scale_image(pygame.image.load("assets/images/weapons/bow.png").convert_alpha(), constants.WEAPONS_SCALE)
arrow_image = scale_image(pygame.image.load("assets/images/weapons/arrow.png").convert_alpha(), constants.WEAPONS_SCALE)

# load character images
mob_animations = []
mob_types = ['elf', 'imp', 'skeleton', 'goblin', 'muddy', 'tiny_zombie', 'big_demon']
animation_types = ["idle", "run"]

for mob in mob_types:
    animation_list = []
    for animation in animation_types:
        # reset temp list of images
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f"assets/images/characters/{mob}/{animation}/{i}.png").convert_alpha()
            img = scale_image(img, constants.SCALE)
            temp_list.append(img)
        animation_list.append(temp_list)
    mob_animations.append(animation_list)


# Game info function
def draw_info():
    # Draw panel at the top for info display
    pygame.draw.rect(screen, constants.PANEL, (0, 0, constants.SCREEN_WIDTH, 50))
    pygame.draw.line(screen, constants.WHITE, (0, 50), (constants.SCREEN_WIDTH, 50))

    # display hearts for health
    half_heart_drawn = False
    for idx in range(5):
        if player.health >= ((idx + 1) * 20):
            screen.blit(heart_full, (10 + idx * 50, 0))
        elif player.health % 20 > 0 and half_heart_drawn is False:
            screen.blit(heart_half, (10 + idx * 50, 0))
            half_heart_drawn = True
        else:
            screen.blit(heart_empty, (10 + idx * 50, 0))


# damage text class
class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        # Move damage text up
        self.rect.y -= 1
        # delete counter after a few seconds
        self.counter += 1
        if self.counter > 30:
            self.kill()


# Create player
player = Character(100, 100, 100, mob_animations, 0)

# Create enemy
enemy = Character(200, 300, 100, mob_animations, 1)

# Create player weapon
bow = Weapon(bow_image, arrow_image)

# Create empty enemy list
enemy_list = []
enemy_list.append(enemy)

# Create sprite groups
damage_text_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()

# Main game loop
run = True
while run:

    # Control frame rate
    clock.tick(constants.FPS)

    screen.fill(constants.BG)

    # calculate player movement
    dx = 0
    dy = 0

    if moving_right is True:
        dx = constants.SPEED
    if moving_left is True:
        dx = -constants.SPEED
    if moving_up is True:
        dy = -constants.SPEED
    if moving_down is True:
        dy = constants.SPEED

    # move player
    player.move(dx, dy)

    # iterate through enemy list6
    for enemy in enemy_list:
        enemy.update()

    # update player
    player.update()
    arrow = bow.update(player)
    if arrow:
        arrow_group.add(arrow)
    for arrow in arrow_group:
        damage, damage_pos = arrow.update(enemy_list)
        if damage:
            damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), constants.RED)
            damage_text_group.add(damage_text)
    damage_text_group.update()

    # Draw player
    for enemy in enemy_list:
        enemy.draw(screen)
    player.draw(screen)
    bow.draw(screen)
    for arrow in arrow_group:
        arrow.draw(screen)
    damage_text_group.draw(screen)
    draw_info()

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # Take keyboard inputs
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_w:
                moving_up = True
            if event.key == pygame.K_s:
                moving_down = True

        # Release button
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_w:
                moving_up = False
            if event.key == pygame.K_s:
                moving_down = False

    pygame.display.update()

pygame.quit()
