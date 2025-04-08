import pygame
import sys
import random
import time
import math
# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 1300, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Undertale-inspired Game")

attack_bar_length = 200
attack_bar_height = 25
attack_bar_x = (width - attack_bar_length) // 2
attack_bar_y = height - 500
attack_phase = False
attack_start_time = 0
attack_duration = 2  # Attack phase duration in seconds
# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
slider_speed = 10
slider_direction = 1
slider_position = 0
clock=pygame.time.Clock()
# Fonts
font = pygame.font.Font('undertale.ttf', 74)
small_font = pygame.font.Font('undertale.ttf', 36)
item_font=pygame.font.Font('undertale.ttf', 50)
text_font = pygame.font.Font('undertale.ttf', 20)

# items
items = {
    "Monster Candy": 10,
    "Spider Donut": 12,
    "Butterscotch Pie": 20,
    "Snowman Piece": 15
}

# Quantities of items
item_quantities = {
    "Monster Candy": 3,
    "Spider Donut": 2,
    "Butterscotch Pie": 1,
    "Snowman Piece": 2
}



# Load images
heart_image = pygame.image.load("heart.png")
heart_image = pygame.transform.scale(heart_image, (30,20))
# Load heart cursor image
heart_cursor_image = pygame.transform.scale(heart_image, (15,10))

heart_rect = heart_image.get_rect()
broken_heart_image = pygame.image.load("broken_heart.png")
broken_heart_image = pygame.transform.scale(broken_heart_image, (30,20))
broken_heart_rect = heart_image.get_rect()
heart_rect.center = (width // 2, height-150)



attack_bar_image = pygame.image.load("attack bar.png")

# Load Toriel image
toriel_image = pygame.image.load("toriel.png")
toriel_image = pygame.transform.scale(toriel_image, (200, 200))
toriel_hurt_image = pygame.image.load("toriel_hurt.png")
toriel_hurt_image = pygame.transform.scale(toriel_hurt_image, (200, 200))
toriel_defeat_image = pygame.image.load("toriel defeat.png")
toriel_defeat_image = pygame.transform.scale(toriel_defeat_image, (200, 200))
toriel_betrayed_image = pygame.image.load("toriel_betrayed.png")
toriel_betrayed_image = pygame.transform.scale(toriel_betrayed_image, (200, 200))
toriel_dying_image = pygame.image.load("toriel_dying.png").convert_alpha()
toriel_dying_image = pygame.transform.scale(toriel_dying_image,(180,150))
toriel_rect = toriel_dying_image.get_rect(topleft=(560, 100))
toriel_heart_image = pygame.image.load("toriel_heart.png").convert_alpha()
toriel_heart_image = pygame.transform.scale(toriel_heart_image,(30,20))
toriel_heart_rect = toriel_heart_image.get_rect(center=toriel_rect.center)
toriel_broken_heart=pygame.image.load("broken_toriel_heart.png").convert_alpha()
toriel_broken_heart_image = pygame.transform.scale(toriel_broken_heart,(30,20))
toriel_heart_rect = toriel_heart_image.get_rect(center=toriel_rect.center)
sprites=pygame.image.load("damage_sprites.png")
damage_sprites = pygame.transform.scale(sprites,(330,309))
background_image = pygame.image.load("background.png")
background=pygame.transform.scale(background_image, (200, 200))
numbers = pygame.image.load("numbers.png")
numbers_image=pygame.transform.scale(numbers, (421,49))
# Load text bubble image
text_bubble_image = pygame.image.load("text bubble.png").convert_alpha()
text_bubble_image=pygame.transform.scale(text_bubble_image, (300, 150))

# Position of text bubble
text_bubble_rect = text_bubble_image.get_rect(midleft=(width // 2 + toriel_image.get_width() // 2 + 20, 100))

# Load sounds
pygame.mixer.music.load("bgm.mp3")  # Background music
damage_sound = pygame.mixer.Sound("damage.mp3")
attack_sound = pygame.mixer.Sound("attack.mp3")
heal_sound = pygame.mixer.Sound("heal.mp3")
talk=pygame.mixer.Sound("talk.mp3")
pygame.mixer.music.play(-1)  # Play backgro und music on loop

dialogues = {
    "defeat": [
        ["URGH..."],
        ["you are stronger...", "than i thought..."],
        ["listen to me,", "small one ..."],
        ["if u go beyond", "this door,"],
        ["keep walking as,", "far as you can ..."],
        ["eventually you will","reach an exit..."],
        ["...","...."],
        ["asgore","i will not let asgore","take your soul..."],
        ["his plan","cannot be allowed","to succeed..."],
        ["......."],
        ["be good...","wont you?...."],
        ["M Y  C H I L D ....."]
    ]
}

spare_dialogues = {
    "spare": [
        ["......"],
        ["......",'.....'],
        ["......",'......','......'],
        ["......?"],
        ['what are you doing?'],
        ['attack','or run','away'],
        ['what are','you ','proving','this way?'],
        ['fight me','or','leave!'],
        ['stop it!'],
        ['stop' ,'looking ','at me','that way'],
        ['go away!'],
        ["......"],
        ["......",'.....'],
        ['I know you want','to go home, but...'],
        ['but please','go upstairs now'],
        ['I promise I will','take good care','of you here.'],
        ['I know we',"don't have much, but..."],
        ['we can have a','good life here.'],
        ['why are you making','it so difficult'],
        ['please,','go upstairs'],
        ['..........'],
        ['ha .. ha...'],
        ['pathetic, is it not?','I cannot save even','a single child'],
        ['......']
    ],
    "final": [
        ["No, I understand"],
        ["you would just be ", "unhappy trapped",'down here'],
        ['the ruins are very ','small once you','get used to them'],
        ['it would not be','right for you to ','grow up in a ','place like this.'],
        ['my expectations...','my lonleliness...','my fear...'],
        ['for you, my child','I put them aside']
    ],
    "pacifist":[
        ['if you truely wish to','leave the ruins...'],
        ['i will not stop you'],
        ['however, when you','leave...'],
        ['please do no come','back.'],
        ['i hope you understand'],
        ['goodbye, my child.']
    ]
}
betrayal_dialogues={
    'betrayed':[
        ['Y O U . . .'],
        ['. . . at my most','vulnerable','moment . . .'],
        ["To think I was","worried you", "wouldn't fit", "in out there . . ."],
        ['Eheheheheh ! ! !','you really are','no different than','them!'],
        ['H a . . . H a . . .']
        ]
    }
current_spare_index = 0 # Track the current spare dialogue
# Modify the hitbox size
heart_rect.width = 45
heart_rect.height = 30
broken_heart_rect.width = 45
broken_heart_rect.height = 30
# Define the dimensions and number of frames in the sprite sheet
frame_width = 55  # Width of each frame
frame_height = 309# Height of each frame
num_frames = 5  # Total number of frames in the sprite sheet
damage_frames = []
damage_frames = []
for i in range(num_frames):
    frame = damage_sprites.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
    damage_frames.append(frame)


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


# Game variables
heart_speed = 10
hp = 20
max_hp = 20
toriel_hp = 100
dodging_time = 5  # Time in seconds to dodge bullets

# Obstacles (bullets)
#bullet_size = 10
bullets = []
green_bullets = []

# Function to draw text
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)



def draw_text_animated(surface, font, text, x, y, delay=50):
    words = text.split(' ')
    current_x = x
    if betrayed :
        screen.blit(toriel_betrayed_image, (width // 2 - toriel_image.get_width() // 2, 50))
    else:
        screen.blit(toriel_defeat_image, (width // 2 - toriel_image.get_width() // 2, 50)) if toriel_hp<=0 else screen.blit(toriel_image, (width // 2 - toriel_image.get_width() // 2, 50))
    for word in words:
        clock.tick(10)
        color = (255, 0, 0) if word.lower() == 'asgore' else (0, 0, 0)
        for i in range(len(word)):
            current_text = word[:i + 1]
            text_surf = font.render(current_text, True, color)
            text_rect = text_surf.get_rect(topleft=(current_x, y))
            surface.blit(text_surf, text_rect)
            pygame.display.update(text_rect)
            time.sleep(delay / 1000) if word !=' ' else  time.sleep(delay / 500)
            # Add your sound playing code here for each letter
            talk.play()
        current_x += text_surf.get_width() + font.size(' ')[0]

def display_dialogues(dialogues):
    for dialogue in dialogues:
        clock.tick(10)
        screen.fill(black)
        screen.blit(text_bubble_image,text_bubble_rect)

        y_offset = 50  # Adjust the y position as needed
        for i, text in enumerate(dialogue):
            draw_text_animated(screen, text_font, text, 850, y_offset + i * 30)  # Correct the function call
            pygame.display.flip()
            pygame.time.wait(1000)  # Wait between lines
        pygame.time.wait(1000)  # Wait between dialogues
    pygame.display.flip()

def show_defeat_dialogues():
    display_dialogues(dialogues["defeat"])
    fade_away_effect()
    draw_text("You won!", font, (255, 140, 0), screen, width // 2, height // 2)
    draw_text("Neutral Ending", font, (255, 140, 0), screen, width // 2, (height // 2)+100)
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

# Function to create dust particles
def create_particles(rect, num_particles):
    particles = []
    for _ in range(num_particles):
        x = random.randint(rect.left, rect.right)
        y = random.randint(rect.top, rect.bottom)
        initial_alpha = 255 - int(255 * (y - rect.top) / rect.height)  # Initial alpha based on vertical position
        particle = {
            "x": x,
            "y": y,
            "vx": random.uniform(-0.5, 0.5),
            "vy": random.uniform(-1, -2),
            "alpha": initial_alpha
        }
        particles.append(particle)
    return particles
# Function to draw particles
def draw_particles(screen, particles):
    for particle in particles:
        if particle["alpha"] > 0:
            particle_surface = pygame.Surface((2, 2), pygame.SRCALPHA)
            particle_alpha = max(0, min(255, particle["alpha"]))  # Clamp alpha value
            pygame.draw.circle(particle_surface, (255, 255, 255, particle_alpha), (1, 1), 2)
            screen.blit(particle_surface, (int(particle["x"]), int(particle["y"])))

def heart_break_animation(screen, heart_image, heart_rect):
    # Shake the heart
    shake_amplitude = 5
    shake_duration = 30  # Number of frames to shake
    for _ in range(shake_duration):
        screen.fill((0, 0, 0))
        dx = random.randint(-shake_amplitude, shake_amplitude)
        dy = random.randint(-shake_amplitude, shake_amplitude)
        screen.blit(heart_image, (heart_rect.x + dx, heart_rect.y + dy))
        pygame.display.flip()
        clock.tick(30)
    
    # Split the heart into two
    split_pieces = [
        (toriel_broken_heart_image.subsurface(pygame.Rect(0, 0, heart_rect.width // 2, heart_rect.height)), heart_rect.topleft),
        (toriel_broken_heart_image.subsurface(pygame.Rect(heart_rect.width // 2, 0, heart_rect.width // 2, heart_rect.height)), (heart_rect.centerx, heart_rect.top))
    ]
    
    for _ in range(30):  # Number of frames to animate splitting
        screen.fill((0, 0, 0))
        for piece, pos in split_pieces:
            screen.blit(piece, pos)
        pygame.display.flip()
        clock.tick(30)
    
    # Break the heart into six pieces and fall
    fall_pieces = []
    for piece, pos in split_pieces:
        for _ in range(3):
            fall_pieces.append({
                "surface": piece.subsurface(pygame.Rect(random.randint(0, piece.get_width() // 2), random.randint(0, piece.get_height() // 2), piece.get_width() // 2, piece.get_height() // 2)),
                "x": pos[0],
                "y": pos[1],
                "vx": random.uniform(-1, 1),
                "vy": random.uniform(-1, 50),
                "rotation": random.uniform(-5, 5),
                "rotation_speed": random.uniform(-1, 1)
                #"alpha": 255
            })
    
    for i in range(255, 0, -5):
        screen.fill((0, 0, 0))
        for particle in fall_pieces:
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]
            particle["vy"] += 0.1  # Gravity effect
            particle["rotation"] += particle["rotation_speed"]
            particle_surface = pygame.transform.rotate(pygame.transform.scale(particle["surface"], (24,8)), particle["rotation"])
            screen.blit(particle_surface, (int(particle["x"]), int(particle["y"])))
        
        pygame.display.flip()
        clock.tick(30)
# Toriel death animation function
def toriel_death_animation(screen, toriel_dying_image, rect):
    particles = create_particles(rect, 3000)
    for i in range(255, 0, -5):
        screen.fill((0, 0, 0))
        toriel_dying_image.set_alpha(i)
        screen.blit(toriel_dying_image, rect.topleft)
        
        for particle in particles:
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]
            if particle["alpha"] > 0:
                particle["alpha"] -= 1
        
        draw_particles(screen, particles)
        pygame.display.flip()
        clock.tick(30)
    heart_break_animation(screen, toriel_heart_image, toriel_heart_rect)
def fade_away_effect():
    fade_surface = pygame.Surface((width, height))
    fade_surface.fill(black)
    toriel_death_animation(screen, toriel_dying_image, toriel_rect)
    for alpha in range(0, 300):  # Adjust the range for fade duration
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.wait(20)  # Adjust the delay for fade speed
        
# Load bullet images
bullet_png = pygame.image.load("bullet.png").convert_alpha()
green_bullet_png = pygame.image.load("green_bullet.png").convert_alpha()
bullet_image = pygame.transform.scale(bullet_png, (20,30))
green_bullet_image = pygame.transform.scale(green_bullet_png, (20,30))

# Function to create bullets
def create_bullets(num_bullets):
#    bullet_size = random.randint(10,20)
    for _ in range(num_bullets):
        bullet_rect = bullet_image.get_rect(center=(random.randint(50, width-50), random.randint(height-315, height-115)))
        corner = random.choice(['top-left', 'top-right', 'bottom-left', 'bottom-right'])
        if corner == 'top-left':
            x, y = 50, height-(random.randint(200,400))
        elif corner == 'top-right':
            x, y =  width-(random.randint(50,1000)), height-(random.randint(200,400))
        elif corner == 'bottom-left':
            x, y = 50, height - 315
        else:
            x, y = width - (random.randint(50,1000)), height - 315

        dx = random.choice([4, 5]) * random.uniform(1.5, 2.5)
        dy = random.choice([4, 5]) * random.uniform(1.5, 2.5)
        bullets.append({"rect": bullet_rect, "dx": dx, "dy": dy, "image": bullet_image})
# Function to create green bullets (healing)
def create_green_bullets(num_bullets):
    for _ in range(num_bullets):
        green_bullet_rect = green_bullet_image.get_rect(center=(random.randint(50, width-50), random.randint(height-315, height-115)))
        green_bullet_rect.width=10
        green_bullet_rect.height=10

        corner = random.choice(['top-left', 'top-right', 'bottom-left', 'bottom-right'])
        if corner == 'top-left':
            x, y = 50, height-(random.randint(200,400))
        elif corner == 'top-right':
            x, y =50, height - 315
        elif corner == 'bottom-left':
            x, y = width-(random.randint(50,1000)), height-(random.randint(200,400))
        else:
            x, y = width - (random.randint(50,1000)), height - 315

        dx = random.choice([-1, 1]) * random.uniform(0.5, 1.5)
        dy = random.choice([-1, 1]) * random.uniform(0.5, 1.5)
        green_bullets.append({"rect": green_bullet_rect, "dx": dx, "dy": dy, "image": green_bullet_image})
# Function to draw health bar
def draw_health_bar(hp, max_hp, x, y, color, surface):
    bar_length = 200
    bar_height = 25
    fill = (hp / max_hp) * bar_length
    border_color = white

    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surface, color, fill_rect)
    pygame.draw.rect(surface, border_color, outline_rect, 2)
    draw_text(f"    {int(hp)}/{max_hp}", small_font, white, surface, x + bar_length + 45, y+15)

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
    pygame.draw.rect(screen, white, cursor_rect)

def play_damage_animation(surface, x, y):
    for frame in damage_frames:
        screen.fill(black)
        screen.blit(toriel_image, (width // 2 - toriel_image.get_width() // 2, 50))

        surface.blit(frame, (x, y))
        pygame.display.flip()
        pygame.time.wait(100)  # Adjust the delay for animation speed
def color_flash(color):
    original_screen = screen.copy()
    for _ in range(3):
        screen.fill(color)
        pygame.display.flip()
        pygame.time.wait(100)
        screen.blit(original_screen, (0, 0))
        pygame.display.flip()
        pygame.time.wait(100)


def create_wave_bullets(num_bullets, amplitude=50, frequency=1):
    for i in range(num_bullets):
        x = 500 + i * 40
        y = height - 200
        dx = 2
        bullets.append({"rect": pygame.Rect(x, y, bullet_size, bullet_size), "dx": dx, "dy": 0, "angle": frequency * i, "amplitude": amplitude, "frequency": frequency})

def update_wave_bullets():
    for bullet in bullets:
        if "frequency" in bullet:
            bullet["rect"].x += bullet["dx"]
            bullet["angle"] += bullet["frequency"]
            bullet["rect"].y = height - 400 + bullet["amplitude"] * math.sin(bullet["angle"])
betrayed=False
def shake_screen(damage):
    global betrayed
    original_position = screen.get_rect().topleft
    for _ in range(10):
        offset_x = random.randint(-10, 10)
        offset_xa = random.randint(-15, 15)
        offset_y = random.randint(-5, 5)
        # Draw the updated game state here
        screen.blit(heart_image, heart_rect)
        for bullet in bullets:
            pygame.draw.rect(screen, white, bullet["rect"])
        for green_bullet in green_bullets:
            pygame.draw.rect(screen, green, green_bullet["rect"])
        draw_health_bar(hp, max_hp, 550, height - 60, yellow, screen)
        screen.fill(black)
        if toriel_hp<=0 and not betrayed:
            pygame.mixer.music.pause()
            screen.blit(toriel_defeat_image, (width // 2 - toriel_defeat_image.get_width() // 2+offset_xa , 50 ))  # Apply shake to Toriel image
            pygame.display.flip()
            #pygame.time.wait(3000)
            
        elif betrayed:
            pygame.mixer.music.pause()
            screen.blit(toriel_betrayed_image, (width // 2 - toriel_defeat_image.get_width() // 2+offset_xa , 50 ))
            pygame.display.flip()
            pygame.time.wait(3000)
        else:
            screen.blit(toriel_hurt_image, (width // 2 - toriel_hurt_image.get_width() // 2+offset_x , 50 ))  # Apply shake to Toriel image
        draw_health_bar(toriel_hp, 100, 550+offset_x, height - 550, red, screen)

        # Draw damage number during the shake
        draw_damage_number(screen, int(damage), 675+offset_x , 180)
        pygame.display.flip()
        pygame.time.wait(50)
    #screen.fill(red)  # Restore background after shaking
    # Redraw everything in its original position after the shake
    screen.blit(heart_image, heart_rect)
    pygame.display.flip()



def create_rotating_bullets(num_bullets, center_x, center_y, radius, angle_step=10):
    for angle in range(0, 360, int(360 / num_bullets)):
        rad_angle = math.radians(angle)
        x = center_x + int(radius * math.cos(rad_angle))
        y = center_y + int(radius * math.sin(rad_angle))
        bullets.append({"rect": pygame.Rect(x, y, bullet_size, bullet_size), "angle": rad_angle, "center_x": center_x, "center_y": center_y, "radius": radius, "angle_step": math.radians(angle_step)})

def update_rotating_bullets():
    for bullet in bullets:
        if "angle_step" in bullet:
            bullet["angle"] += bullet["angle_step"]
            bullet["rect"].x = bullet["center_x"] + int(bullet["radius"] * math.cos(bullet["angle"]))
            bullet["rect"].y = bullet["center_y"] + int(bullet["radius"] * math.sin(bullet["angle"]))

def items_phase():
    global hp
    flattened_items = flatten_items(items,item_quantities)
    pages = paginate_items(flattened_items)
    current_page=0
    selected_option = 0
    running = True

    while running:
        screen.fill(black)
        
        # Display Toriel image
        screen.blit(toriel_image, (width // 2 - toriel_image.get_width() // 2, 50))
        play_area = pygame.Rect(50, height - 400, width - 100, 300)
        pygame.draw.rect(screen, white, play_area, 2)
        box_width = 150
        box_height = 50
        spacing_x = 250
        spacing_y=20
        columns =2
        
        for i, option in enumerate(pages[current_page]):
            col = i % columns
            row = i // columns
            x = 150+ col * (box_width + spacing_x)
            y = height - 400 + row * (box_height + spacing_y)
            #pygame.draw.rect(screen, (255, 255, 255), (x, y, box_width, box_height), 2)  # White border
            draw_text_left_aligned(screen, item_font, f'* {option}', (255, 255, 255), x + 10, y + box_height // 4)
            if i == selected_option:
                screen.blit(heart_cursor_image, ((x - heart_cursor_image.get_width()), y + 25+box_height // 4))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 2) % len(pages[current_page])
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 2) % len(pages[current_page])
                elif event.key == pygame.K_LEFT:
                    selected_option = (selected_option - 1) % len(pages[current_page])
                elif event.key == pygame.K_RIGHT:
                    selected_option = (selected_option + 1) % len(pages[current_page])
                elif event.key == pygame.K_PAGEUP:
                    current_page = (current_page - 1) % len(pages)
                    selected_option = 0
                elif event.key == pygame.K_PAGEDOWN:
                    current_page = (current_page + 1) % len(pages)
                    selected_option = 0
                elif event.key == pygame.K_RETURN:
                    flattened_items = flatten_items(items,item_quantities)
                    item = pages[current_page][selected_option]
                    heal_amount = items[item]
                    hp = min(hp + heal_amount, max_hp)
                    display_item_message(item, heal_amount)
                    item_quantities[item] -= 1
                    if item_quantities[item] == 0:
                        del item_quantities[item]
                    return "used"

def flatten_items(items, item_quantities):
    flattened_items = []
    for item, quantity in item_quantities.items():
        flattened_items.extend([item] * quantity)
    return flattened_items


def draw_text_left_aligned(surface, font, text, color, x, y):
    """Draws text starting from the left side."""
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(topleft=(x, y))
    surface.blit(textobj, textrect)
        
def paginate_items(items, items_per_page=4):
    pages = [items[i:i + items_per_page] for i in range(0, len(items), items_per_page)]
    return pages

                
def display_item_message(item, heal_amount):
    if True:
        screen.fill(black)
        play_area = pygame.Rect(50, height - 400, width - 100, 300)
        pygame.draw.rect(screen, white, play_area, 2)

        # Display Toriel image
        screen.blit(toriel_image, (width // 2 - toriel_image.get_width() // 2, 50))
        pygame.display.flip()

        message1 = f"* You ate the {item}."
        message2 = f"* You recovered {heal_amount} HP."
        draw_text(message1, small_font, (255, 255, 255), screen, 350, height // 2 - 20)
        draw_text(message2, small_font, (255, 255, 255), screen, 350, height // 2 + 20)
        pygame.display.flip()
        pygame.time.wait(2000)

def mercy_phase():
    options = ["SPARE", "FLEE"]
    selected_option = 0
    running = True

    while running:
        screen.fill(black)
        clock.tick(60)
        # Display Toriel image
        screen.blit(toriel_image, (width // 2 - toriel_image.get_width() // 2, 50))
        play_area = pygame.Rect(50, height - 400, width - 100, 300)
        pygame.draw.rect(screen, white, play_area, 2)
        box_width = 150
        box_height = 50
        spacing = 50
        for i, option in enumerate(options):
            x = 50
            y = height - 400 + i * (box_height + spacing)
            #pygame.draw.rect(screen, (255, 255, 255), (x, y, box_width, box_height), 2)  # White border
            draw_text(option, small_font, (255, 255, 255), screen, x + box_width // 2, y + box_height // 2)
            if i == selected_option:
                screen.blit(heart_cursor_image, ((x - heart_cursor_image.get_width())+25, y + box_height // 4))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if options[selected_option] == "SPARE":
                        return "spare"
                    elif options[selected_option] == "FLEE":
                        return "flee"

# When Toriel takes damage
def attack_toriel():
    global toriel_hp
    bar_length = 200
    print(slider_position)
    distance_from_center = (265-slider_position)
    if distance_from_center<0:
        distance_from_center*=-1
    damage = 20-(distance_from_center//10)
    #damage+=100  # for testing purpose
    print(distance_from_center,damage)
    if damage<=0:
        damage*=-1
        damage+=1
    toriel_hp -= damage  # Ensure minimum damage is 1
     #color_flash(red)  # Flash red screen effect
    attack_sound.play()
    play_damage_animation(screen, 650, 10)
    shake_screen(damage)
    if toriel_hp<=0:
        show_defeat_dialogues()
def dodge_phase():
    global hp
    dodging_start_time = time.time()
    while time.time() - dodging_start_time < dodging_time:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        
        keys = pygame.key.get_pressed()

        # Update bullet positions and check for collisions
        for bullet in bullets:
            if "angle" in bullet:
                update_rotating_bullets()
            elif "frequency" in bullet:
                update_wave_bullets()
            else:
                bullet["rect"].x += bullet["dx"]
                bullet["rect"].y += bullet["dy"]
                if bullet["rect"].left < 50 or bullet["rect"].right > width - 50:
                    bullet["dx"] *= -1
                if bullet["rect"].top < height - 400 or bullet["rect"].bottom > height - 115:
                    bullet["dy"] *= -1
                if heart_rect.colliderect(bullet["rect"]):
                    hp -= 1
                    damage_sound.play()
                    bullets.remove(bullet)
                    create_bullets(1)
                    if hp<=0:
                        game_over()
                    break

        screen.fill(black)
        play_area = pygame.Rect(50, height - 400, width - 100, 300)
        pygame.draw.rect(screen, white, play_area, 2)

        if keys[pygame.K_LEFT] and heart_rect.left > play_area.left:
            heart_rect.x -= heart_speed
        if keys[pygame.K_RIGHT] and heart_rect.right < play_area.right:
            heart_rect.x += heart_speed
        if keys[pygame.K_UP] and heart_rect.top > play_area.top:
            heart_rect.y -= heart_speed
        if keys[pygame.K_DOWN] and heart_rect.bottom < play_area.bottom:
            heart_rect.y += heart_speed

        screen.blit(heart_image, heart_rect)

        for bullet in bullets:
            screen.blit(bullet["image"], bullet["rect"])
        for green_bullet in green_bullets:
            screen.blit(green_bullet["image"], green_bullet["rect"])

        for green_bullet in green_bullets:
            green_bullet["rect"].x += green_bullet["dx"]
            green_bullet["rect"].y += green_bullet["dy"]
            if green_bullet["rect"].left < 50 or green_bullet["rect"].right > width - 50:
                green_bullet["dx"] *= -1
            if green_bullet["rect"].top < height - 315 or green_bullet["rect"].bottom > height - 115:
                green_bullet["dy"] *= -1
            if heart_rect.colliderect(green_bullet["rect"]):
                hp = min(hp + 1, max_hp)
                heal_sound.play()
                green_bullets.remove(green_bullet)
                create_green_bullets(1)
                break

        draw_health_bar(hp, max_hp, 550, height - 60, yellow, screen)
        draw_health_bar(toriel_hp, 100, 550, height - 450, red, screen)
        screen.blit(toriel_image, (width // 2 - toriel_image.get_width() // 2, 50))
        pygame.display.flip()
        pygame.time.Clock().tick(30)
    
        
    return True

def choice_phase(txt):
   # global txt
    options = ["FIGHT", "ACT", "ITEM", "MERCY"]
    selected_option = 0
    running = True

    while running:
        screen.fill(black)
        clock.tick(60)
        draw_health_bar(hp, max_hp, 550, height - 160, yellow, screen)
        draw_text('frisk',small_font,(255,255,255),screen,500,height-150)
        draw_health_bar(toriel_hp, 100, 550, height - 450, red, screen)
        draw_text('toriel',small_font,(255,255,255),screen,500,height-440)
        draw_text_left_aligned(screen,small_font,txt,(255,255,255),100,height-350)
        # Display Toriel image
        screen.blit(toriel_image, (width // 2 - toriel_image.get_width() // 2, 50))
        play_area = pygame.Rect(50, height - 400, width - 100, 200)
        pygame.draw.rect(screen, white, play_area, 2)
        box_width = 150  # Width of each option box
        box_height = 50  # Height of each option box
        spacing = 100     # Space between boxes
        
        for i, option in enumerate(options):
            x = 600 - (box_width + spacing) * 1.5 + i * (box_width + spacing)
            y = height - 100  # Position menu near the bottom of the screen
            if i == selected_option:
                pygame.draw.rect(screen, (255, 255, 0), (x, y, box_width, box_height), 2)  # Highlight in yellow
                draw_text(option, font, (255, 255, 0), screen, x + box_width // 2, y + box_height // 2)
            else:
                pygame.draw.rect(screen, (255, 140, 0), (x, y, box_width, box_height), 2)  # Orange box
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
                elif event.key == pygame.K_RETURN:
                    if options[selected_option] == "ACT":
                        return act_menu()

                    return options[selected_option]

def act_menu():
    options = ["TORIEL", "TALK"]
    selected_option = 0
    running = True

    while running:
        screen.fill(black)
        play_area = pygame.Rect(50, height - 400, width - 100, 300)
        pygame.draw.rect(screen, white, play_area, 2)

        # Display Toriel image
        screen.blit(toriel_image, (width // 2 - toriel_image.get_width() // 2, 50))

        box_width = 200
        box_height = 50
        spacing = 10

        for i, option in enumerate(options):
            x = 50
            y = height - 400 + i * (box_height + spacing)
            #pygame.draw.rect(screen, (255, 255, 255), (x, y, box_width, box_height), 2)  # White border
            draw_text(option, small_font, (255, 255, 255), screen, x + box_width // 2, y + box_height // 2)
            if i == selected_option:
                screen.blit(heart_cursor_image, ((x - heart_cursor_image.get_width())+25, y + box_height // 4))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if options[selected_option] == "TORIEL":
                        display_toriel_stats()
                        return
                    elif options[selected_option] == "TALK":
                        #talk_to_toriel()

                        
                        pass

def display_toriel_stats():
    screen.fill(black)
            # Display Toriel image
    screen.blit(toriel_image, (width // 2 - toriel_image.get_width() // 2, 50))
    play_area = pygame.Rect(50, height - 400, width - 100, 300)
    pygame.draw.rect(screen, white, play_area, 2)
    draw_text("* TORIEL - ATK 80 DEF 80", small_font, white, screen, 250, height // 2)
    draw_text("* Knows best for you.", small_font, white, screen, 250, height // 2 + 40)
    pygame.display.flip()
    pygame.time.wait(3000)  # Display stats for 3 seconds


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)



def attack_phase():
    attack_start_time = time.time()
    while time.time() - attack_start_time < attack_duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        
        keys = pygame.key.get_pressed()
        screen.fill(black)

        screen.blit(toriel_image, (width // 2 - toriel_image.get_width() // 2, 50))
        draw_health_bar(hp, max_hp, 550, height - 60, yellow, screen)
        draw_health_bar(toriel_hp, 100, 550, height - 450, red, screen)

        if keys[pygame.K_SPACE]:
            attack_toriel()
            return
            slider_position, slider_direction=0,1
            if toriel_hp <= 0:
                draw_text("You won!", font, white, screen, width // 2 - 100, height // 2)
                pygame.display.flip()
                pygame.time.wait(2000)
                return "win"

        draw_text("Press SPACE to attack!", small_font, white, screen, width // 2 - 100, height - 400)
        slider_position=0
        slider_direction=1
        draw_attack_bar()
        pygame.display.flip()
        pygame.time.Clock().tick(30)

    return "continue"
   
def retry_game():
    global hp, toriel_hp, bullets, green_bullets, heart_rect, running

    # Reset game state
    hp = max_hp
    toriel_hp = 100
    bullets = []
    green_bullets = []
    create_bullets(10)
    create_green_bullets(5)
    heart_rect = heart_image.get_rect(center=(width // 2, height - 200))
    pygame.mixer.music.pause()
    pygame.mixer.music.load("bgm.mp3")  # Background music
    pygame.mixer.music.play(-1)
    # Restart the game loop
    #dodging_pase=True
    running = True
    


def game_over_screen():
    global running
    pygame.mixer.music.load("game over.mp3")  # Background music
    pygame.mixer.music.play(-1)  # Play backgro und music on loop
    options = ["RETRY", "GIVE UP"]
    selected_option = 0
    running = True

    while running:
        screen.fill(black)
        

        # Display Game Over message
        draw_text("GAME OVER", font, white, screen, width // 2, height // 3)
        draw_text("You cannot give up just yet...", small_font, white, screen, width // 2, height // 2)

        box_width = 200  # Width of each option box
        box_height = 50  # Height of each option box
        spacing = 100     # Space between boxes

        for i, option in enumerate(options):
            x = width // 2 - (box_width + spacing) + i * (box_width + spacing)
            y = height - 100  # Position menu near the bottom of the screen
            if i == selected_option:
                pygame.draw.rect(screen, (255, 255, 0), (x, y, box_width, box_height), 2)  # Highlight in yellow
                draw_text(f" {option}", font, (255, 255, 0), screen, x + box_width // 2, y + box_height // 2)
            else:
                pygame.draw.rect(screen, (255, 140, 0), (x, y, box_width, box_height), 2)  # Orange box
                draw_text(option, font, (255, 140, 0), screen, x + box_width // 2, y + box_height // 2)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_RIGHT:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if options[selected_option] == "RETRY":
                        retry_game()
                        return
                    elif options[selected_option] == "GIVE UP":
                        pygame.time.wait(1000)
                        pygame.quit()
                        sys.exit()
                        return


def game_over():
    global running

    # Pause the music
    pygame.mixer.music.pause()

    # Set screen to black
    screen.fill(black)

    # Display heart at its last position
    screen.blit(broken_heart_image, heart_rect)
    pygame.display.flip()
    pygame.time.wait(1000)  # Wait for a second

    # Heart break animation
    for _ in range(30):  # Adjust the range for animation duration
        heart_rect.y += 20  # Falling speed
        screen.fill(black)
        screen.blit(broken_heart_image, heart_rect)
        pygame.display.flip()
        pygame.time.wait(50)  # Adjust the speed of falling

    # Game Over Screen
    game_over_screen()

def final_decision():
    global running,toriel_hp

    while running:
        txt='* ...........'
        choice = choice_phase(txt)
        if choice == "FIGHT":
            # Trigger betrayal ending
            betrayed=True
            damage=999
            toriel_hp-=999
            play_damage_animation(screen, 650, 10)
            attack_sound.play()
            for _ in range(10):
                offset_xa = random.randint(-15, 15)
                pygame.mixer.music.pause()
                
                screen.fill(black)
                screen.blit(toriel_betrayed_image, (width // 2 - toriel_defeat_image.get_width() // 2+offset_xa , 50 ))
                draw_health_bar(toriel_hp, 100, 550+offset_xa, height - 550, red, screen)
                draw_damage_number(screen, int(damage), 675+offset_xa , 180)
                pygame.display.flip()
                pygame.time.wait(100)
                
            pygame.time.wait(300)
                
            display_dialogues((betrayal_dialogues['betrayed']))
            
            pygame.display.flip()
            fade_away_effect()
            draw_text("You got the betrayal ending...", font, (255, 0, 0), screen, width // 2, height // 2)
            pygame.time.wait(3000)
            pygame.quit()
            sys.exit()
        elif choice == "MERCY":
            result = mercy_phase()
            if result == "spare":
                show_pacifist_ending()
                running = False

def show_pacifist_ending():
    display_dialogues(spare_dialogues['final'])
    pygame.mixer.music.load('fallen_down.mp3')
    pygame.mixer.music.play(-1)
    display_dialogues(spare_dialogues['pacifist'])
    draw_text("You won with a pacifist ending!", font, (0, 0, 255), screen, width // 2, height // 2)
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

running = True
clock = pygame.time.Clock()
create_bullets(10)
create_green_bullets(5)
dodging_time = 10  # Example dodge time in seconds
attack_duration = 5  # Example attack duration in seconds

def main_game_loop():
    global running,current_spare_index,hp
    #current_spare_index=24 #change for testing purpose
    while running:
        if hp <= 0:
            game_over()
            break
        txt=random.choice(['* Toriel blocks the way!','* Toriel looks through you.','* Toriel takes a deep breath.','* Toriel prepares a magical attack.','* Toriel is acting aloof'])
        if current_spare_index>11:
            txt='* ..........'
            pygame.mixer.music.pause()
        choice = choice_phase(txt)
        

        #choice = choice_phase()
        if choice == "FIGHT":
            result = attack_phase()
            if result == "win":
                #show_defeat_dialogues()
                running = False  # Exit the game loop
                break
        elif choice == "ACT":
            act_phase()
        elif choice == "ITEM":
            result = items_phase()
            #if result == "used":
                
        elif choice == "MERCY":
            result=mercy_phase()
            if result=='spare':   
                
                if current_spare_index<len(spare_dialogues['spare']):
                    display_dialogues([spare_dialogues['spare'][current_spare_index]])
                    current_spare_index+=1
                    if current_spare_index>11:
                        pygame.mixer.music.pause()
                        continue
                    
                    if not dodge_phase():
                        break
                else:
                    #display_dialogues(spare_dialogues['final'])
                    final_decision()
                    #running==False
                    
            elif result =='flee':
                draw_text("You fled away!", font, (255, 140, 0), screen, width // 2, height // 2 + 160)
                pygame.display.flip()
                pygame.time.wait(2000)
                pygame.quit()
                sys.exit()
        #show_defeat_dialogues()
        if toriel_hp <= 0:
            #show_defeat_dialogues()
            running = False
            
        if not dodge_phase():
            break
    pygame.quit()
    sys.exit()

# Start the game
main_game_loop()
