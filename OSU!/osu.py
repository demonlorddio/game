import pygame
import json
import os

# Initialize Pygame
pygame.init()

# Set up display
width, height = 1300, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Osu! Rhythm Game")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Function to draw text
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

# Function to load level data
def load_level_data(filename):
    with open(filename, 'r') as f:
        level_data = json.load(f)
    return level_data

# Main game loop
def main():
    running = True
    while running:
        screen.fill(BLACK)
        font = pygame.font.SysFont(None, 72)
        draw_text("Osu!", font, WHITE, screen, width // 2, height // 4)
        
        font = pygame.font.SysFont(None, 36)
        draw_text("1. Play Mode", font, WHITE, screen, width // 2, height // 2)
        draw_text("2. Builder Mode", font, WHITE, screen, width // 2, height // 2 + 40)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    select_level()
                    running = False
                elif event.key == pygame.K_2:
                    os.system('python builder_mode.py')
                    running = False

    pygame.quit()

# Function to select level
def select_level():
    levels = [f for f in os.listdir('levels') if f.endswith('.json')]
    selected_level = None
    running = True
    while running:
        screen.fill(BLACK)
        font = pygame.font.SysFont(None, 48)
        draw_text("Select Level", font, WHITE, screen, width // 2, height // 4)
        
        font = pygame.font.SysFont(None, 36)
        for i, level in enumerate(levels):
            draw_text(f"{i+1}. {level}", font, WHITE, screen, width // 2, height // 2 + i * 40)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif pygame.K_1 <= event.key <= pygame.K_9:
                    index = event.key - pygame.K_1
                    if index < len(levels):
                        selected_level = levels[index]
                        running = False

    if selected_level:
        os.system(f'python play_mode.py levels/{selected_level}')

if __name__ == "__main__":
    main()
