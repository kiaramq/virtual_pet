import pygame
import sys
import time
import os

# initialize pygame
pygame.init()

# game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# colors (color-hex.com)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (186,255,201)
PINK = (255,179,186)
BLUE = (186,225,255)
GRAY = (128, 128, 128)

# initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Virtual Pet")
clock = pygame.time.Clock()

# load welcome background
WELCOME_BG = pygame.image.load(os.path.join("assets", "backgrounds", "welcome.png"))
WELCOME_BG = pygame.transform.scale(WELCOME_BG, (SCREEN_WIDTH, SCREEN_HEIGHT)) # scale to fit screen

# Define the size of a single frame in the spritesheet.
DOG_FRAME_WIDTH = 15  
DOG_FRAME_HEIGHT = 20  

# load font
WELCOME_FONT = pygame.font.Font("assets/fonts/semiboldbaloo.ttf", 48)
FONT = pygame.font.Font("assets/fonts/regularbaloo.ttf", 36)
SMALL_FONT = pygame.font.Font("assets/fonts/regularbaloo.ttf", 24)

# Load puppy spritesheets
DOG_SPRITES_PATH = os.path.join("assets", "dogs")
DOG_SPRITES = {
    "black": pygame.image.load(os.path.join(DOG_SPRITES_PATH, "spritesheet_black.png")),
    "brown": pygame.image.load(os.path.join(DOG_SPRITES_PATH, "spritesheet_brown.png")),
    "white": pygame.image.load(os.path.join(DOG_SPRITES_PATH, "spritesheet_white.png")),
}

# Helper to get a scaled intro puppy image (first frame of spritesheet)
def get_intro_puppy_image(color, scale_factor=10):
    sheet = DOG_SPRITES[color]
    frame = pygame.Surface((DOG_FRAME_WIDTH, DOG_FRAME_HEIGHT), pygame.SRCALPHA)
    frame.blit(sheet, (0, 0), (0, 0, DOG_FRAME_WIDTH, DOG_FRAME_HEIGHT))
    return pygame.transform.scale(frame, (DOG_FRAME_WIDTH * scale_factor, DOG_FRAME_HEIGHT * scale_factor))

INTRO_PUPPY_SCALE = 10
INTRO_PUPPY_IMAGES = {
    "black": get_intro_puppy_image("black", INTRO_PUPPY_SCALE),
    "brown": get_intro_puppy_image("brown", INTRO_PUPPY_SCALE),
    "white": get_intro_puppy_image("white", INTRO_PUPPY_SCALE),
}

def show_intro_and_choose_color(screen, font):
    intro_running = True
    chosen_color = None
    while intro_running:
        screen.blit(WELCOME_BG, (0, 0))
        title = WELCOME_FONT.render("Welcome to Virtual Pet!", True, (0, 0, 0))
        prompt = FONT.render("Choose your puppy:", True, (0, 0, 0))
        screen.blit(title, (200, 100))
        screen.blit(prompt, (200, 160))

        # Draw puppy images in a row with borders
        puppy_colors = ["black", "brown", "white"]
        spacing = 60 + DOG_FRAME_WIDTH * INTRO_PUPPY_SCALE  # space between images
        total_width = (len(puppy_colors) - 1) * spacing + (DOG_FRAME_WIDTH * INTRO_PUPPY_SCALE)
        start_x = (SCREEN_WIDTH - total_width) // 2
        y = 220
        for i, color in enumerate(puppy_colors):
            img = INTRO_PUPPY_IMAGES[color]
            img_rect = img.get_rect()
            img_rect.topleft = (start_x + i * spacing, y)
            screen.blit(img, img_rect)
            # Draw border (black, 4px thick)
            pygame.draw.rect(screen, (0,0,0), img_rect, 4)
            # Draw label below each puppy
            label = FONT.render(f"{i+1} - {color.capitalize()}", True, (0,0,0))
            label_rect = label.get_rect(center=(img_rect.centerx, img_rect.bottom + 25))
            screen.blit(label, label_rect)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    chosen_color = "black"
                    intro_running = False
                elif event.key == pygame.K_2:
                    chosen_color = "brown"
                    intro_running = False
                elif event.key == pygame.K_3:
                    chosen_color = "white"
                    intro_running = False
    return chosen_color

# load emotion images
EMOTION_PATH = os.path.join("assets", "Emotes", "left")
EMOTION_IMAGES = {
    "very_happy": pygame.image.load(os.path.join(EMOTION_PATH, "veryHappyEmote.png")),
    "happy": pygame.image.load(os.path.join(EMOTION_PATH, "happyEmote.png")),
    "neutral": pygame.image.load(os.path.join(EMOTION_PATH, "neutralEmote.png")),
    "bored": pygame.image.load(os.path.join(EMOTION_PATH, "boredEmote.png")),
    "sad": pygame.image.load(os.path.join(EMOTION_PATH, "sadEmote.png")),
    "angry": pygame.image.load(os.path.join(EMOTION_PATH, "angryEmote.png")),
    "worried": pygame.image.load(os.path.join(EMOTION_PATH, "worriedEmote.png")),
}

def get_emotion_image(happiness):
    if happiness >= 85:
        return EMOTION_IMAGES["very_happy"]
    elif happiness >= 65:
        return EMOTION_IMAGES["happy"]
    elif happiness >= 45:
        return EMOTION_IMAGES["neutral"]
    elif happiness >= 30:
        return EMOTION_IMAGES["bored"]
    elif happiness >= 15:
        return EMOTION_IMAGES["sad"]
    elif happiness >= 5:
        return EMOTION_IMAGES["worried"]
    else:
        return EMOTION_IMAGES["angry"]

class VirtualPet:
    def __init__(self, puppy_color):
        # pet stats (0-100)
        self.hunger = 50
        self.happiness = 50
        self.energy = 50
        self.last_update = time.time()
        self.puppy_color = puppy_color
        self.spritesheet = DOG_SPRITES[puppy_color]

    def get_idle_frame(self):
        # Return the first frame (top-left) of the spritesheet as the idle pose
        frame = pygame.Surface((DOG_FRAME_WIDTH, DOG_FRAME_HEIGHT), pygame.SRCALPHA)
        frame.blit(self.spritesheet, (0, 0), (0, 0, DOG_FRAME_WIDTH, DOG_FRAME_HEIGHT))
        # Scale up 10x using nearest neighbor for crisp pixel art
        scale_factor = 10  # much bigger
        scaled_frame = pygame.transform.scale(frame, (DOG_FRAME_WIDTH * scale_factor, DOG_FRAME_HEIGHT * scale_factor))
        return scaled_frame
    def update(self):
        current_time = time.time()
        time_passed = current_time - self.last_update
        if time_passed > 5:
            self.hunger = max(0, self.hunger - 2)
            self.energy = max(0, self.energy - 1)
            if self.hunger < 20 or self.energy < 20:
                self.happiness = max(0, self.happiness - 3)
            elif self.hunger > 80 and self.energy > 80:
                self.happiness = min(100, self.happiness + 1)
            self.last_update = current_time
    def feed(self):
        self.hunger = min(100, self.hunger + 25)
        self.happiness = min(100, self.happiness + 10)
        if self.energy < 100:
            self.energy = min(100, self.energy + 5)
    def play(self):
        if self.energy > 20:
            self.happiness = min(100, self.happiness + 20)
            self.energy = max(0, self.energy - 15)
            self.hunger = max(0, self.hunger - 10)
    def sleep(self):
        self.energy = min(100, self.energy + 30)
        self.happiness = min(100, self.happiness + 5)

def draw_stat_bar(screen, x, y, width, height, value, max_value, color):
    """draw a stat bar"""
    # background
    pygame.draw.rect(screen, GRAY, (x, y, width, height))
    # fill
    fill_width = int((value / max_value) * width)
    pygame.draw.rect(screen, color, (x, y, fill_width, height))
    # border
    pygame.draw.rect(screen, BLACK, (x, y, width, height), 2)

def draw_ui(screen, pet):
    """Draw the user interface with emotion image and puppy sprite"""
    # Draw puppy idle frame (centered horizontally, lower on the screen)
    idle_frame = pet.get_idle_frame()
    sprite_rect = idle_frame.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 120))
    screen.blit(idle_frame, sprite_rect)

    # Emotion image above bars
    emotion_img = get_emotion_image(pet.happiness)
    img_rect = emotion_img.get_rect(center=(SCREEN_WIDTH // 2, 60))
    screen.blit(emotion_img, img_rect)

    # title
    title_text = FONT.render("Virtual Pet", True, BLACK)
    screen.blit(title_text, (10, 10))

    # stats
    stats_y = 320
    bar_width = 200
    bar_height = 20

    # hunger bar
    hunger_text = SMALL_FONT.render("Hunger:", True, BLACK)
    screen.blit(hunger_text, (10, stats_y))
    draw_stat_bar(screen, 80, stats_y, bar_width, bar_height, pet.hunger, 100, GREEN)

    # happiness bar
    happiness_text = SMALL_FONT.render("Happiness:", True, BLACK)
    screen.blit(happiness_text, (10, stats_y + 30))
    draw_stat_bar(screen, 80, stats_y + 30, bar_width, bar_height, pet.happiness, 100, BLUE)

    # energy bar
    energy_text = SMALL_FONT.render("Energy:", True, BLACK)
    screen.blit(energy_text, (10, stats_y + 60))
    draw_stat_bar(screen, 80, stats_y + 60, bar_width, bar_height, pet.energy, 100, PINK)

    # instructions
    instructions = [
        "Controls:",
        "F - Feed pet",
        "P - Play with pet", 
        "S - Put pet to sleep",
        "ESC - Quit"
    ]

    for i, instruction in enumerate(instructions):
        instruction_text = SMALL_FONT.render(instruction, True, BLACK)
        screen.blit(instruction_text, (SCREEN_WIDTH - 200, 120 + i * 25))

def main():
    # Show intro and get puppy color
    chosen_color = show_intro_and_choose_color(screen, FONT)
    pet = VirtualPet(chosen_color)
    running = True
    while running:
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_f:
                    pet.feed()
                elif event.key == pygame.K_p:
                    pet.play()
                elif event.key == pygame.K_s:
                    pet.sleep()
        # update pet
        pet.update()
        # draw everything
        screen.fill(WHITE)
        draw_ui(screen, pet)
        # update display
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
    sys.exit()

# Entry point
if __name__ == "__main__":
    main()
