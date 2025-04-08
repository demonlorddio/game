import pygame
import random
import time
import sys

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
gif_frames2 = load_gif_to_frames('undyne2.gif')
current_frame = 0
frame_rate = 40# milliseconds per frame
last_update = 30#pygame.time.get_ticks()
hp = 20
max_hp = 20
undyne_max_hp = 400
undyne_hp=400
# Load images
heart_image = pygame.image.load('heart.png')
heart_image = pygame.transform.scale(heart_image, (30, 20))
heart_cursor_image = pygame.transform.scale(heart_image, (30,20))

arrow_up_image = pygame.transform.scale((pygame.image.load('arrow_up.png')),(15,30))
arrow_down_image = pygame.transform.scale((pygame.image.load('arrow_down.png')),(15,30))
arrow_left_image = pygame.transform.scale((pygame.image.load('arrow_left.png')),(30,15))
arrow_right_image = pygame.transform.scale((pygame.image.load('arrow_right.png')),(30,15))
frame_width = 55  # Width of each frame
frame_height = 309# Height of each frame
num_frames = 6  # Total number of frames in the sprite sheet
attack_bar_image = pygame.image.load("attack bar.png")
sprites=pygame.image.load("damage_sprites.png")
damage_frames = []
damage_sprites = pygame.transform.scale(sprites,(330,309))
for i in range(6):
    frame = damage_sprites.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
    damage_frames.append(frame)
numbers = pygame.image.load("numbers.png")
numbers_image=pygame.transform.scale(numbers, (421,49))

undertale_music = pygame.mixer.Sound('bgm.mp3')
undertale_music.play(-1)

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW=(255,255,0)

# Define heart position
heart_rect = heart_image.get_rect(center=(width/2, height/2))

font = pygame.font.Font('undertale.ttf', 74)
small_font = pygame.font.Font('undertale.ttf', 36)
item_font=pygame.font.Font('undertale.ttf', 50)
text_font = pygame.font.Font('undertale.ttf', 20)
num_width = 42
num_height = 49

numbers = []
for i in range(10):
    num_rect = pygame.Rect(i * num_width, 0, num_width, num_height)
    numbers.append(numbers_image.subsurface(num_rect))
def draw_damage_number(surface, damage, x, y):
    damage_str = str(damage)
    for i, char in enumerate(damage_str):
        if char.isdigit():  # Only process digits
            num_img = numbers[int(char)]
            surface.blit(num_img, (x + i * num_width, y))
            
def draw_health_bar(hp, max_hp, x, y, color, surface):
    bar_length = 200
    bar_height = 25
    fill = (hp / max_hp) * bar_length
    border_color = WHITE

    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surface, color, fill_rect)
    pygame.draw.rect(surface, border_color, outline_rect, 2)
    draw_text(f"    {int(hp)}/{max_hp}", small_font, WHITE, surface, x + bar_length + 45, y+15)
    
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
        self.speed = 2#random.randint(2,3)
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
slider_speed = 10
slider_direction = 1
slider_position = 0
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
def choice_phase():
    global current_frame, last_update
    
    options = ["FIGHT", "ACT","ITEM","MERCY"]
    selected_option = 0
    running = True

    while running:
        now = pygame.time.get_ticks()
        if now - last_update > frame_rate:
            last_update = now
            current_frame = (current_frame + 1) % len(gif_frames)
        
        screen.fill(BLACK)
        screen.blit(gif_frames2[current_frame], (width/2-100, 20))
        clock.tick(60)
        draw_text( '.....',  font,WHITE,screen,100, height - 350)
        
        # Display the play area
        
        play_area = pygame.Rect(50, height - 400, width - 100, 200)
        pygame.draw.rect(screen, WHITE, play_area, 2)

        box_width = 200  # Width of each option box
        box_height = 100  # Height of each option box
        spacing = 150     # Space between boxes
        
        for i, option in enumerate(options):
            x = 500 - (box_width + spacing) * 1.5 + i * (box_width + spacing)
            y = height - 200  # Position menu near the bottom of the screen
            if i == selected_option:
                pygame.draw.rect(screen, (255, 255, 0), (x+60, y+30, box_width, box_height), 2)  # Highlight in yellow
                draw_text(option, font, (255, 255, 0), screen, x + box_width // 2, y + box_height // 2)
            else:
                pygame.draw.rect(screen, (255, 140, 0), (x+60, y+30, box_width, box_height), 2)  # Orange box
                draw_text(option, font, (255, 140, 0), screen, x + box_width // 2, y + box_height // 2)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_RIGHT:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_z:
                    return options[selected_option]

def attack_phase():
    global undyne_hp,current_frame, last_update
    attack_duration=5
    attack_start_time = time.time()
    while time.time() - attack_start_time < attack_duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        now = pygame.time.get_ticks()
        if now - last_update > frame_rate:
            last_update = now
            current_frame = (current_frame + 1) % len(gif_frames)
        
        keys = pygame.key.get_pressed()
        screen.fill(BLACK)

        screen.blit(gif_frames2[current_frame], (width/2-100, 20))
        draw_health_bar(hp, max_hp, 550, height - 60, YELLOW, screen)
        draw_health_bar(undyne_hp, undyne_max_hp, 550, height - 450, RED, screen)
        if keys[pygame.K_SPACE]:
            attack_undyne()
            return
            slider_position, slider_direction=0,1
            if undyne_hp <= 0:
                draw_text("You won!", font, WHITE, screen, width // 2 - 100, height // 2)
                pygame.display.flip()
                pygame.time.wait(2000)
                return "win"

        draw_text("Press SPACE to attack!", small_font, WHITE, screen, width // 2 - 100, height - 400)
        slider_position=0
        slider_direction=1
        draw_attack_bar()
        pygame.display.flip()
        pygame.time.Clock().tick(30)

    return "continue"
def draw_attack_bar():
    global slider_position, slider_direction

    bar_length = 550
    bar_height = 75
    attack_bar_x = 300
    attack_bar_y = height - 300
    slider_position += slider_direction * slider_speed
    if slider_position < 0 or slider_position > bar_length:
        slider_direction *= -1

    cursor_x = attack_bar_x + slider_position
    cursor_rect = pygame.Rect(cursor_x, attack_bar_y  , 10, bar_height + 20)

    screen.blit(attack_bar_image, (attack_bar_x, attack_bar_y))
    pygame.draw.rect(screen, WHITE, cursor_rect)

def attack_undyne():
    global undyne_hp,current_frame, last_update, last_arrow_time
    bar_length = 200
    #print(slider_position)
    distance_from_center = (265-slider_position)
    if distance_from_center<0:
        distance_from_center*=-1
    damage = 40-(distance_from_center//10)
    #damage+=100  # for testing purpose
    #print(distance_from_center,damage)
    if damage<=0:
        damage*=-1
        damage+=1
    undyne_hp -= damage  # Ensure minimum damage is 1
    play_damage_animation(screen, 650, 10)
    shake_screen(damage)
    if undyne_hp<=0:
        #show_defeat_dialogues()
        pygame.quit()
        sys.exit()

def play_damage_animation(surface, x, y):
    global undyne_hp,current_frame, last_update
    for frame in damage_frames:
        now = pygame.time.get_ticks()
        if now - last_update > frame_rate:
            last_update = now
            current_frame = (current_frame + 1) % len(gif_frames)
        screen.fill(BLACK)
        screen.blit(gif_frames2[current_frame], (width/2-100, 20))
        surface.blit(frame, (x, y))
        pygame.display.flip()
        pygame.time.wait(100)  # Adjust the delay for animation speed
def shake_screen(damage):
    global undyne_hp,current_frame, last_update, last_arrow_time
    original_position = screen.get_rect().topleft
    for _ in range(10):
        now = pygame.time.get_ticks()
        if now - last_update > frame_rate:
            last_update = now
            current_frame = (current_frame + 1) % len(gif_frames)
        offset_x = random.randint(-10, 10)
        offset_xa = random.randint(-15, 15)
        offset_y = random.randint(-5, 5)
        # Draw the updated game state here
        screen.blit(heart_image, heart_rect)
        
        draw_health_bar(hp, max_hp, 550, height - 60, YELLOW, screen)
        screen.fill(BLACK)
        screen.blit(gif_frames2[current_frame], (width/2-100+offset_xa, 20))  # Apply shake to Toriel image
        draw_health_bar(undyne_hp, undyne_max_hp, 550+offset_x, height - 550, RED, screen)

        # Draw damage number during the shake
        draw_damage_number(screen, int(damage), 675+offset_x , 180)
        pygame.display.flip()
        pygame.time.wait(50)
    #screen.fill(red)  # Restore background after shaking
    # Redraw everything in its original position after the shake
    screen.blit(heart_image, heart_rect)
    pygame.display.flip()        
def mercy_phase():
    options = ["SPARE", "FLEE"]
    selected_option = 0
    running = True
    global current_frame, last_update
    while running:
        now = pygame.time.get_ticks()
        if now - last_update > frame_rate:
            last_update = now
            current_frame = (current_frame + 1) % len(gif_frames)
        screen.fill(BLACK)
        clock.tick(60)
        # Display Toriel image
        screen.blit(gif_frames2[current_frame], (width/2-100, 20))
        play_area = pygame.Rect(50, height - 400, width - 100, 300)
        pygame.draw.rect(screen, WHITE, play_area, 2)
        box_width = 150
        box_height = 50
        spacing = 50
        for i, option in enumerate(options):
            x = 50
            y = height - 400 + i * (box_height + spacing)
            #pygame.draw.rect(screen, (255, 255, 255), (x, y, box_width, box_height), 2)  # White border
            draw_text(option, small_font, (255, 255, 255), screen, x + box_width // 2, y + box_height // 2)
            if i == selected_option:
                screen.blit(heart_cursor_image, ((x - heart_cursor_image.get_width())+50, y + box_height // 4+25))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_x:
                    return choice_phase()
                elif event.key == pygame.K_z:
                    if options[selected_option] == "SPARE":
                        return "spare"
                    elif options[selected_option] == "FLEE":
                        heart_cursor_rect=heart_cursor_image.get_rect()
                        heart_cursor_rect.x=55
                        heart_cursor_rect.y=412
                        for _ in range(30):  # Adjust the range for animation duration
                            
                            heart_cursor_rect.width=100
                            heart_cursor_rect.height=525
                            heart_cursor_rect.x -= 3  # Falling speed
                            screen.fill(BLACK)
                            draw_text('* escaped',small_font,(255,255,255),screen,300,500)
                            screen.blit(gif_frames2[current_frame], (width/2-100, 20))
                            play_area = pygame.Rect(50, height - 400, width - 100, 300)
                            pygame.draw.rect(screen, WHITE, play_area, 2)
                            box_width = 150
                            box_height = 50
                            spacing = 50
                            for i, option in enumerate(options):
                                x = 50
                                y = height - 400 + i * (box_height + spacing)
                                draw_text(option, small_font, (255, 255, 255), screen, x + box_width // 2, y + box_height // 2)
                            screen.blit(heart_cursor_image, heart_cursor_rect)
                            pygame.display.flip()
                            pygame.time.wait(50)  # Adjust the speed of falling
                        pygame.quit()
                        sys.exit()
# Main game loop
running = True
last_arrow_time = time.time()
def dodging_phase():
    dodging_start_time = time.time()
    dodging_time = random.randint(5,10)
    while time.time() - dodging_start_time < dodging_time:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        global current_frame, last_update, last_arrow_time, hp

        now = pygame.time.get_ticks()
        if now - last_update > frame_rate:
            last_update = now
            current_frame = (current_frame + 1) % len(gif_frames)

        current_time = time.time()
        if current_time - last_arrow_time > random.uniform(0.5, 1):  # Create a new arrow every 0.5 to 1 second
            create_arrows()
            last_arrow_time = current_time

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            global line_rect, line1x, line1y, line2x, line2y
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
                
            elif heart_rect.colliderect(arrow.rect):
                arrow.kill()
                
                hp-=1
                if hp<=0:
                    pygame.quit()
                    sys.exit()
                # You'll get damage
        
        # Draw everything
        screen.fill(BLACK)
        screen.blit(gif_frames[current_frame], (width/2-100, 20))
        play_area = pygame.Rect(width/2-50, height/2-50 , 100, 100)
        draw_health_bar(hp, max_hp, 550, height - 60, YELLOW, screen)
        pygame.draw.rect(screen, WHITE, play_area, 2)
        screen.blit(heart_image, heart_rect)
        draw_shield_lines(screen, heart_rect, line1x, line1y, line2x, line2y)
        all_sprites.draw(screen)
        pygame.display.flip()
    
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    result = choice_phase()
    if result=="MERCY":
        mercy_phase()
    elif result=='FIGHT':
        attack_phase()
    dodging_phase()



pygame.quit()
