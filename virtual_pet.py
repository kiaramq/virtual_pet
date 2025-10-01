import pygame, sys, time

# initialize
pygame.init()
screen = pygame.display.set_mode((400, 400))

hunger = 100
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Feed pet
                hunger = min(hunger + 20, 100)

    # bar decreases over time
    hunger -= 0.05
    if hunger <= 0:
        pet_state = "sad"
    else:
        pet_state = "happy"

    # background + pet + hunger bar
    screen.fill((200,200,200))
    pygame.draw.rect(screen, (255,0,0), (50,50, hunger*3, 20))  # hunger bar
    pygame.display.flip()
    clock.tick(30)
