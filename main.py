import pygame
from pygame import Surface

import constants
from character import Character

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


# helper function to scale image
def scale_image(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w * scale, h * scale))


animation_list = []
for i in range(4):
    img = pygame.image.load(f"assets/images/characters/elf/idle/{i}.png").convert_alpha()
    img = scale_image(img, constants.SCALE)
    print(i)
    animation_list.append(img)

# Create player
player = Character(100, 100, animation_list)

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

    # update player
    player.update()

    # Draw player
    player.draw(screen)

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
