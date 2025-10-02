import pygame
import sys
import time

# initialize pygame
pygame.init()

# game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

# initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Virtual Pet")
clock = pygame.time.Clock()

# load font
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

import os

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
    def __init__(self):
        # pet stats (0-100)
        self.hunger = 50
        self.happiness = 50
        self.energy = 50
        # time tracking for stat decay
        self.last_update = time.time()
    
    def update(self):
        """Update pet stats over time"""
        current_time = time.time()
        time_passed = current_time - self.last_update
        
        # decay stats over time (every 5 seconds)
        if time_passed > 5:
            self.hunger = max(0, self.hunger - 2)
            self.energy = max(0, self.energy - 1)
            
            # happiness depends on other stats
            if self.hunger < 20 or self.energy < 20:
                self.happiness = max(0, self.happiness - 3)
            elif self.hunger > 80 and self.energy > 80:
                self.happiness = min(100, self.happiness + 1)
            
            self.last_update = current_time
    
    def feed(self):
        """Feed the pet"""
        self.hunger = min(100, self.hunger + 25)
        self.happiness = min(100, self.happiness + 10)
        if self.energy < 100:
            self.energy = min(100, self.energy + 5)
    
    def play(self):
        """Play with the pet"""
        if self.energy > 20:
            self.happiness = min(100, self.happiness + 20)
            self.energy = max(0, self.energy - 15)
            self.hunger = max(0, self.hunger - 10)
    
    def sleep(self):
        """Let the pet sleep"""
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
    """Draw the user interface with emotion image"""
    # Emotion image above bars
    emotion_img = get_emotion_image(pet.happiness)
    img_rect = emotion_img.get_rect(center=(SCREEN_WIDTH // 2, 60))
    screen.blit(emotion_img, img_rect)

    # title
    title_text = font.render("Virtual Pet", True, BLACK)
    screen.blit(title_text, (10, 10))
    
    # stats
    stats_y = 120
    bar_width = 200
    bar_height = 20
    
    # hunger bar
    hunger_text = small_font.render("Hunger:", True, BLACK)
    screen.blit(hunger_text, (10, stats_y))
    draw_stat_bar(screen, 80, stats_y, bar_width, bar_height, pet.hunger, 100, GREEN)
    
    # happiness bar
    happiness_text = small_font.render("Happiness:", True, BLACK)
    screen.blit(happiness_text, (10, stats_y + 30))
    draw_stat_bar(screen, 80, stats_y + 30, bar_width, bar_height, pet.happiness, 100, BLUE)
    
    # energy bar
    energy_text = small_font.render("Energy:", True, BLACK)
    screen.blit(energy_text, (10, stats_y + 60))
    draw_stat_bar(screen, 80, stats_y + 60, bar_width, bar_height, pet.energy, 100, RED)
    
    # instructions
    instructions = [
        "Controls:",
        "F - Feed pet",
        "P - Play with pet", 
        "S - Put pet to sleep",
        "ESC - Quit"
    ]
    
    for i, instruction in enumerate(instructions):
        instruction_text = small_font.render(instruction, True, BLACK)
        screen.blit(instruction_text, (SCREEN_WIDTH - 200, 120 + i * 25))

def main():
    """Main game loop"""
    pet = VirtualPet()
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

if __name__ == "__main__":
    main()
