import pygame
import sys
import random
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 640, 480
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Font
font = pygame.font.SysFont(None, 36)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def main_menu():
    while True:
        DISPLAYSURF.fill(BLACK)
        draw_text('Snake Game', font, WHITE, DISPLAYSURF, WIDTH // 2 - 80, HEIGHT // 4)
        draw_text('Start', font, WHITE, DISPLAYSURF, WIDTH // 2 - 30, HEIGHT // 2)
        draw_text('Easy', font, WHITE, DISPLAYSURF, WIDTH // 2 - 30, HEIGHT // 2 + 40)
        draw_text('Medium', font, WHITE, DISPLAYSURF, WIDTH // 2 - 30, HEIGHT // 2 + 80)
        draw_text('Hard', font, WHITE, DISPLAYSURF, WIDTH // 2 - 30, HEIGHT // 2 + 120)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if WIDTH // 2 - 30 <= event.pos[0] <= WIDTH // 2 + 30:
                    if HEIGHT // 2 +40 <= event.pos[1] <= HEIGHT // 2 + 76:
                        game_loop(10)
                    if HEIGHT // 2 + 80 <= event.pos[1] <= HEIGHT // 2 + 116:
                        game_loop(20)
                    if HEIGHT // 2 + 120 <= event.pos[1] <= HEIGHT // 2 + 156:
                        game_loop(30)

        pygame.display.update()

def game_loop(speed):
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    direction = 'RIGHT'
    change_to = direction

    food_pos = [random.randrange(1, (WIDTH // 10)) * 10, random.randrange(1, (HEIGHT // 10)) * 10]
    food_spawn = True

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    if direction != 'DOWN':
                        direction = 'UP'
                elif event.key == K_DOWN:
                    if direction != 'UP':
                        direction = 'DOWN'
                elif event.key == K_LEFT:
                    if direction != 'RIGHT':
                        direction = 'LEFT'
                elif event.key == K_RIGHT:
                    if direction != 'LEFT':
                        direction = 'RIGHT'

        if direction == 'UP':
            snake_pos[1] -= 10
        if direction == 'DOWN':
            snake_pos[1] += 10
        if direction == 'LEFT':
            snake_pos[0] -= 10
        if direction == 'RIGHT':
            snake_pos[0] += 10

        snake_body.insert(0, list(snake_pos))
        if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
            food_spawn = False
        else:
            snake_body.pop()

        if not food_spawn:
            food_pos = [random.randrange(1, (WIDTH // 10)) * 10, random.randrange(1, (HEIGHT // 10)) * 10]
        food_spawn = True

        DISPLAYSURF.fill(BLACK)

        for pos in snake_body:
            pygame.draw.rect(DISPLAYSURF, WHITE, pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(DISPLAYSURF, RED, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        if snake_pos[0] < 0 or snake_pos[0] > WIDTH - 10:
            game_over()
        if snake_pos[1] < 0 or snake_pos[1] > HEIGHT - 10:
            game_over()

        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                game_over()

        pygame.display.update()
        pygame.time.Clock().tick(speed)

def game_over():
    while True:
        DISPLAYSURF.fill(WHITE)
        draw_text('Game Over', font, RED, DISPLAYSURF, WIDTH // 2 - 80, HEIGHT // 4)
        draw_text('Restart', font, BLACK, DISPLAYSURF, WIDTH // 2 - 30, HEIGHT // 2)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if WIDTH // 2 - 30 <= event.pos[0] <= WIDTH // 2 + 30:
                    if HEIGHT // 2 <= event.pos[1] <= HEIGHT // 2 + 36:
                        main_menu()

        pygame.display.update()

main_menu()
