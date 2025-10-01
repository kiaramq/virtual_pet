import pygame, sys, time

# initialize
pygame.init()
screen = pygame.display.set_mode((400, 400))

# load full sprite sheet
sprite_sheet = pygame.image.load('spritesheet_black.png').convert_alpha()

# possible to cut out each frame from the sheet with this function
def get_sprite(sheet, x, y, width, height):
    # extracts a single sprite from the sheet
    image = pygame.Surface((width, height), pygame.SRCALPHA)  
    image.blit(sheet, (0, 0), (x, y, width, height))  
    return image

