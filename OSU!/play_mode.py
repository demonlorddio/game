import pygame
import time
import json
import numpy as np
import os

# Initialize Pygame
pygame.init()

# Set up display
width, height = 1300, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Osu! Play Mode")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

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

# Function to draw a shrinking ring
def draw_ring(screen, x, y, time_elapsed, total_time, color=GREEN):
    max_radius = 80
    min_radius = 50
    radius = max_radius - (max_radius - min_radius) * (time_elapsed / total_time)
    pygame.draw.circle(screen, color, (x, y), int(radius), 2)

# Function to check if a point is inside a circle
def is_inside_circle(point, center, radius):
    return np.linalg.norm(np.array(point) - np.array(center)) <= radius

# Function to calculate score based on distance from circle
def calculate_score(distance, circle_radius):
    if distance <= circle_radius * 1.1:
        return 300
    elif distance <= circle_radius * 1.5:
        return 100
    else:
        return 50

# Function to load level data
def load_level_data(filename):
    with open(filename, 'r') as f:
        level_data = json.load(f)
    return level_data

# Function to list saved levels
def list_levels(levels_dir):
    levels = [f for f in os.listdir(levels_dir) if f.endswith('.json')]
    return levels

# Function to display level selection screen
def select_level(levels):
    font = pygame.font.SysFont(None, 48)
    selected = 0
    while True:
        screen.fill(BLACK)
        for i, level in enumerate(levels):
            color = GREEN if i == selected else WHITE
            draw_text(level, font, color, screen, width // 2, 100 + i * 60)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(levels)
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(levels)
                if event.key == pygame.K_RETURN:
                    return levels[selected]

# Main play mode function
def play_game(level_file):
    level_data = load_level_data(level_file)
    circles = level_data["circles"]
    bg_image = level_data["bg_image"]
    bgm = level_data["bgm"]
    
    #pygame.mixer.music.load(f'bgm/{bgm}')
    #pygame.mixer.music.play()
    
    bg = pygame.image.load(f'backgrounds/{bg_image}')
    bg = pygame.transform.scale(bg, (width, height))
    
    start_time = time.time()
    score = 0
    circle_radius = 50
    circle_display_time = 3.0

    playing = True
    while playing:
        screen.blit(bg, (0, 0))
        current_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    playing = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for circle in circles:
                    if is_inside_circle(event.pos, (circle["x"], circle["y"]), circle_radius * 1.5):
                        distance = np.linalg.norm(np.array(event.pos) - np.array((circle["x"], circle["y"])))
                        score += calculate_score(distance, circle_radius)
                        circles.remove(circle)
                        break

        for i, circle in enumerate(circles):
            show_time = circle["time"] - circle_display_time
            hide_time = circle["time"] + 0.5
            if show_time <= current_time <= hide_time:
                time_elapsed = current_time - show_time
                draw_circle(screen, circle["x"], circle["y"], circle["order"], circle["color"])
                draw_ring(screen, circle["x"], circle["y"], time_elapsed, circle_display_time)

        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        pygame.time.Clock().tick(60)

if __name__ == "__main__":
    levels_dir = 'levels'
    levels = list_levels(levels_dir)
    if not levels:
        print("No levels found in the 'levels' directory.")
    else:
        selected_level = select_level(levels)
        if selected_level:
            play_game(os.path.join(levels_dir, selected_level))
