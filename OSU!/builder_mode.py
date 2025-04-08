import pygame
import time
import json
import random
import os

# Initialize Pygame
pygame.init()

# Set up display
width, height = 1300, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Osu! Builder Mode")

# Define colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, GREEN, BLUE]

# Function to draw text
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

# Function to draw a circle
def draw_circle(screen, x, y, order, color=RED):
    pygame.draw.circle(screen, color, (x, y), 50)
    font = pygame.font.SysFont(None, 48)
    text = font.render(str(order), True, WHITE)
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)

# Save the level data to a file
def save_level_data(filename, circles, bg_image, bgm):
    level_data = {
        "circles": circles,
        "bg_image": bg_image,
        "bgm": bgm
    }
    with open(filename, 'w') as f:
        json.dump(level_data, f)

# Function to select background image and BGM
def select_bg_and_bgm():
    bg_images = [f for f in os.listdir('backgrounds') if f.endswith(('.png', '.jpg'))]
    bgms = [f for f in os.listdir('bgm') if f.endswith('.mp3')]
    selected_bg = None
    selected_bgm = None

    running = True
    while running:
        screen.fill(BLACK)
        font = pygame.font.SysFont(None, 48)
        draw_text("Select Background", font, WHITE, screen, width // 2, height // 4)
        
        font = pygame.font.SysFont(None, 36)
        for i, bg in enumerate(bg_images):
            draw_text(f"{i+1}. {bg}", font, WHITE, screen, width // 2, height // 2 + i * 40)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif pygame.K_1 <= event.key <= pygame.K_9:
                    index = event.key - pygame.K_1
                    if index < len(bg_images):
                        selected_bg = bg_images[index]
                        running = False

    running = True
    while running:
        screen.fill(BLACK)
        font = pygame.font.SysFont(None, 48)
        draw_text("Select BGM", font, WHITE, screen, width // 2, height // 4)
        
        font = pygame.font.SysFont(None, 36)
        for i, bgm in enumerate(bgms):
            draw_text(f"{i+1}. {bgm}", font, WHITE, screen, width // 2, height // 2 + i * 40)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif pygame.K_1 <= event.key <= pygame.K_9:
                    index = event.key - pygame.K_1
                    if index < len(bgms):
                        selected_bgm = bgms[index]
                        running = False

    return selected_bg, selected_bgm

# Main builder mode function
def builder_mode():
    circles = []
    bg_image, bgm = select_bg_and_bgm()
    #pygame.mixer.music.load(f'bgm/{bgm}')
    #pygame.mixer.music.play()
    
    start_time = time.time()
    editing = True
    current_color = random.choice(COLORS)
    color_count = 0
    order = 1

    while editing:
        screen.fill(BLACK)
        current_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                editing = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    level_name = input("Enter level name: ")
                    save_level_data(f'levels/{level_name}.json', circles, bg_image, bgm)
                    editing = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                circle_time = current_time
                circles.append({"time": circle_time, "x": x, "y": y, "order": order, "color": current_color})
                order += 1
                color_count += 1
                if color_count >= random.randint(5, 7):
                    current_color = random.choice(COLORS)
                    color_count = 0
                    order = 1

        for i, circle in enumerate(circles):
            draw_circle(screen, circle["x"], circle["y"], circle["order"], circle["color"])

        pygame.display.flip()
        pygame.time.Clock().tick(60)

if __name__ == "__main__":
    builder_mode()
