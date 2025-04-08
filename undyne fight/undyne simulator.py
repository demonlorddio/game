import pygame
import random
import time
import json
DATA_FILE = 'score.json'
def load_data():
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)
scores=load_data()
#print(scores)
def get_user(dodge):
    if scores<dodge:
        scores=dodge
    return scores
# Initialize Pygame
pygame.init()
width,height=1300,700
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
from PIL import Image

def load_gif_to_frames(gif_path):
    gif = Image.open(gif_path)
    frames = []
    try:
        while True:
            frame = gif.copy()
            frame = frame.convert('RGBA')
            pygame_frame = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
            frames.append(pygame_frame)
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass
    return frames

gif_frames = load_gif_to_frames('undyne.gif')
current_frame = 0
frame_rate = 40# milliseconds per frame
last_update = 30#pygame.time.get_ticks()
dodge=0
hit=0
# Load images
heart_image = pygame.image.load('heart.png')
heart_image = pygame.transform.scale(heart_image, (30, 20))
arrow_up_image = pygame.transform.scale((pygame.image.load('arrow_up.png')),(15,30))
arrow_down_image = pygame.transform.scale((pygame.image.load('arrow_down.png')),(15,30))
arrow_left_image = pygame.transform.scale((pygame.image.load('arrow_left.png')),(30,15))
arrow_right_image = pygame.transform.scale((pygame.image.load('arrow_right.png')),(30,15))

#undertale_music = pygame.mixer.Sound('bgm.mp3')
#undertale_music.play(-1)

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Define heart position
heart_rect = heart_image.get_rect(center=(width/2, height/2))

font = pygame.font.Font('undertale.ttf', 74)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)
    
# Define arrow class
class Arrow(pygame.sprite.Sprite):
    def __init__(self, direction):
        super().__init__()
        self.direction = direction
        self.image = arrow_up_image
        self.rect = self.image.get_rect(center=(random.randint(50, 750), random.randint(50, 550)))
        self.speed = random.randint(5,6)
        if self.direction == 'up':
            self.image=arrow_up_image
            self.rect.x = heart_rect.x + 5
            self.rect.y = height
        elif self.direction == 'down':
            self.image=arrow_down_image
            self.rect.x = heart_rect.x + 5
            self.rect.y = 0
        elif self.direction == 'right':
            self.image=arrow_right_image
            self.rect.y = heart_rect.y + 5
            self.rect.x = 0
        elif self.direction == 'left':
            self.image=arrow_left_image
            self.rect.y = heart_rect.y + 5
            self.rect.x = width

    def update(self):
        clock.tick(1200)
        if self.direction == 'up':
            self.rect.y -= self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed
        elif self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'right':
            self.rect.x += self.speed
        
# Create sprite groups
all_sprites = pygame.sprite.Group()
arrows = pygame.sprite.Group()

# Create arrows periodically
def create_arrows():
    arrow = Arrow(random.choice(['up', 'down', 'left', 'right']))
    all_sprites.add(arrow)
    arrows.add(arrow)

# Define shield lines
def draw_shield_lines(screen, heart_rect, line1x, line1y, line2x, line2y):
    pygame.draw.line(screen, BLUE, line1x, line1y, 3)
    pygame.draw.line(screen, BLUE, line2x, line2y, 3)

# Line dimensions
line1_leftx, line1_lefty = (heart_rect.x - 10, heart_rect.y - 10), (heart_rect.x - 10, heart_rect.y + 30)
line2_leftx, line2_lefty = (heart_rect.x, heart_rect.y + 5), (heart_rect.x - 10, heart_rect.y + 32)
lineleft_rect = pygame.Rect((heart_rect.x - 10, heart_rect.y - 10), (1, 40))
line1_upx, line1_upy = (heart_rect.x + 40, heart_rect.y - 20), (heart_rect.x - 10, heart_rect.y - 20)
line2_upx, line2_upy = (heart_rect.x + 5, heart_rect.y), (heart_rect.x - 10, heart_rect.y - 20)
lineup_rect = pygame.Rect((heart_rect.x - 10, heart_rect.y - 20), (40, 1))
line1_rightx, line1_righty = (heart_rect.x + 40, heart_rect.y + 30), (heart_rect.x + 40, heart_rect.y - 20)
line2_rightx, line2_righty = (heart_rect.x + 30, heart_rect.y + 10), (heart_rect.x + 40, heart_rect.y - 20)
lineright_rect = pygame.Rect((heart_rect.x + 40, heart_rect.y - 20), (1, 40))
line1_downx, line1_downy = (heart_rect.x - 10, heart_rect.y + 30), (heart_rect.x + 40, heart_rect.y + 30)
line2_downx, line2_downy = (heart_rect.x + 10, heart_rect.y + 20), (heart_rect.x + 40, heart_rect.y + 30)
linedown_rect = pygame.Rect((heart_rect.x - 10, heart_rect.y + 30), (40, 1))
line1x, line1y = line1_downx, line1_downy
line2x, line2y = line2_downx, line2_downy
line_rect = linedown_rect

# Main game loop
running = True
last_arrow_time = time.time()
while running:
    now = pygame.time.get_ticks()
    if now - last_update > frame_rate:
        last_update = now
        current_frame = (current_frame + 1) % len(gif_frames)

        clock.tick(30)
        current_time = time.time()
        
        if current_time - last_arrow_time > random.uniform(0.5,1):  # Create a new arrow every 0.5 seconds
            create_arrows()
            last_arrow_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        line_rect = lineleft_rect
        line1x, line1y = line1_leftx, line1_lefty
        line2x, line2y = line2_leftx, line2_lefty
    elif keys[pygame.K_RIGHT]:
        line_rect = lineright_rect
        line1x, line1y = line1_rightx, line1_righty
        line2x, line2y = line2_rightx, line2_righty
    elif keys[pygame.K_UP]:
        line_rect = lineup_rect
        line1x, line1y = line1_upx, line1_upy
        line2x, line2y = line2_upx, line2_upy
    elif keys[pygame.K_DOWN]:
        line_rect = linedown_rect
        line1x, line1y = line1_downx, line1_downy
        line2x, line2y = line2_downx, line2_downy

    # Update arrows
    all_sprites.update()
    # Check for collisions with shield
    for arrow in arrows:
        if line_rect.colliderect(arrow.rect):
            arrow.kill()
            dodge+=1
        elif heart_rect.colliderect(arrow.rect):
            arrow.kill()
            hit+=1
            # You'll get damage
            

    # Draw everything
    screen.fill(BLACK)
    screen.blit(gif_frames[current_frame], (width/2-100, 20))
    score_color=WHITE if dodge<=scores else (255,255,0)
    draw_text(f'dodge: {dodge}', font, score_color, screen, 50, height-100)
    draw_text(f'health: {20-hit}', font, (255, 255, 255), screen, width-350, height-100)
    draw_text(f'highscore: {scores}', font, (255, 255, 255), screen, 50, height-500)
    play_area = pygame.Rect(width/2-50, height/2-50 , 100, 100)
    pygame.draw.rect(screen, WHITE, play_area, 2)
    screen.blit(heart_image, heart_rect)
    draw_shield_lines(screen, heart_rect, line1x, line1y, line2x, line2y)
    all_sprites.draw(screen)

    pygame.display.flip()
    if hit==20:
        break
if scores<dodge:
    save_data(dodge)
pygame.quit()
