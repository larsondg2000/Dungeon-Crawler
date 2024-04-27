import pygame
import csv
import constants
from character import Character
from weapon import Weapon
from items import Item
from world import World

pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Crawler")

# Create clock for maintaining frame rate
clock = pygame.time.Clock()

# Define game variables
level = 1
screen_scroll = [0, 0]

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

# Load coin images
coin_images = []
for x in range(4):
    img = scale_image(pygame.image.load(f"assets/images/items/coin_f{x}.png").convert_alpha(),
                      constants.ITEM_SCALE)
    coin_images.append(img)

# Load potion
red_potion = scale_image(pygame.image.load("assets/images/items/potion_red.png").convert_alpha(),
                         constants.POTION_SCALE)

item_images = []
item_images.append(coin_images)
item_images.append(red_potion)

# weapon images
bow_image = scale_image(pygame.image.load("assets/images/weapons/bow.png").convert_alpha(), constants.WEAPONS_SCALE)
arrow_image = scale_image(pygame.image.load("assets/images/weapons/arrow.png").convert_alpha(), constants.WEAPONS_SCALE)

# Load tile map images
tile_list = []
for x in range(constants.TILE_TYPES):
    tile_image = pygame.image.load(f"assets/images/tiles/{x}.png").convert_alpha()
    tile_image = pygame.transform.scale(tile_image, (constants.TILE_SIZE, constants.TILE_SIZE))
    tile_list.append(tile_image)

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


# function to output text on screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


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
    # Show level
    draw_text("Level: " + str(level), font, constants.WHITE, constants.SCREEN_WIDTH / 2.2, 15)

    # Show score
    draw_text(f"Score {player.score}", font, constants.WHITE, constants.SCREEN_WIDTH - 200, 15)


# Create empy tile list
world_data = []
for row in range(constants.ROW):
    r = [-1] * constants.COLS
    world_data.append(r)

# Load level data and create world
with open(f"levels/level{level}_data.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")

    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

world = World()
world.process_data(world_data, tile_list, item_images, mob_animations)


# damage text class
class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        # reposition based on scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]
        # Move damage text up
        self.rect.y -= 1
        # delete counter after a few seconds
        self.counter += 1
        if self.counter > 30:
            self.kill()


# Create player
player = world.player

# Create player weapon
bow = Weapon(bow_image, arrow_image)

# Create enemy
enemy_list = world.character_list

# Create sprite groups
damage_text_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()

score_coin = Item(constants.SCREEN_WIDTH - 215, 23, 0, coin_images, True)
item_group.add(score_coin)

# add items for level data
for item in world.item_list:
    item_group.add(item)

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
    screen_scroll = player.move(dx, dy)

    # Update world tiles
    world.update(screen_scroll)

    # iterate through enemy list6
    for enemy in enemy_list:
        enemy.update()

    # update player
    player.update()
    arrow = bow.update(player)
    if arrow:
        arrow_group.add(arrow)
    for arrow in arrow_group:
        damage, damage_pos = arrow.update(screen_scroll, enemy_list)
        if damage:
            damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), constants.RED)
            damage_text_group.add(damage_text)
    damage_text_group.update()

    item_group.update(screen_scroll, player)

    # Draw world tiles
    world.draw(screen)

    # Draw player on screen
    for enemy in enemy_list:
        enemy.ai(screen_scroll)
        enemy.draw(screen)
    player.draw(screen)
    bow.draw(screen)
    for arrow in arrow_group:
        arrow.draw(screen)
    damage_text_group.draw(screen)
    item_group.draw(screen)
    draw_info()
    score_coin.draw(screen)

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
