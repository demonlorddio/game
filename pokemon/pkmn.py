import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN
import time
import os
import sys
import random
import math
pygame.init()
pygame.font.init()
fps=30
#color
wt=(255,255,255)
bl=(0,0,0)
green = (0, 255, 0)
red = (255, 0, 0)

WIDTH,HEIGHT=900,500
screen = pygame.display.set_mode((1300,700))
fade = pygame.Surface((1300, 700))
fade.fill(bl)
eny=pygame.Rect(900,200,300,400)
me=pygame.Rect(100,325,400,200)
pygame.display.set_caption("POKEMON!")
font = pygame.font.Font((os.path.join('img','font.ttf')), 74)
font2 = pygame.font.Font((os.path.join('img','font.ttf')), 40)
health = 100
max_health = 100
health_bar_width = 100
health_bar_height = 7

# Draw Charmander's health bar
ch_health = 100  # Example health value for Charmander
ch_max_health = 100
ch_health_bar_width = 100
ch_health_bar_height = 7
ch_x = 1110  # Adjust position as needed
ch_y = 430  # Adjust position as needed
intro=pygame.image.load('img/intro_bg.png')
intro_bg=pygame.transform.scale(intro,(1300,700))
start=pygame.image.load('img/start.png')
bg=pygame.image.load(os.path.join('img','background.png'))
bg_img=pygame.transform.scale(bg,(1300,700))
pika=pygame.image.load(os.path.join('img','pikachu.png'))
pika_img=pygame.transform.scale(pika,(150,200))
text_png=pygame.image.load(os.path.join('img','text.png'))
text_img=pygame.transform.scale(text_png,(875,175))
me_box_img=pygame.image.load(os.path.join('img','box_me.png'))
eny_box_img=pygame.image.load(os.path.join('img','box_eny.png'))

pokemon_data = {
    'charmander': {'health': 100, 'max_health': 100, 'image':pygame.transform.scale(pygame.image.load(os.path.join('img','charmander.png')), (200, 350)), 'x': 1110, 'y': 430, 'health_bar_width': 100, 'health_bar_height': 7},
    'bulbasaur': {'health': 100, 'max_health': 100, 'image':pygame.transform.scale( pygame.image.load(os.path.join('img','bulbasaur.png')),(200,350)), 'x': 1110, 'y': 430, 'health_bar_width': 100, 'health_bar_height': 7},
    'squirtle': {'health': 100, 'max_health': 100, 'image': pygame.transform.scale(pygame.image.load(os.path.join('img','squirtle.png')),(200,350)), 'x': 1110, 'y': 430, 'health_bar_width': 100, 'health_bar_height': 7}
}
selected_pokemon = 'charmander'

text1 =["A wild Pikachu appeared!"]
text2=["What should",f"{selected_pokemon} do?"]

words = ['fight', 'bag', 'pokemon', 'run']
wordsf=['scratch','ember','metal claw','flamethrower']

positions = [(900, 500), (1150,500), (900, 550), (1150,550)]
positionsf = [(600, 500), (900,500), (600, 550), (900,550)]
scratch=pygame.image.load(os.path.join('img','scratch.png'))
ember_img=pygame.image.load(os.path.join('img','ember.png'))
metal_claw = pygame.image.load(os.path.join('img','metal_claw.png'))
flamethrower_img = pygame.image.load(os.path.join('img','flamethrower.png'))
flamethrower=pygame.transform.scale(flamethrower_img,(WIDTH/2,HEIGHT/2))
ember=pygame.transform.scale(ember_img,(WIDTH/2,HEIGHT/2))
metal_claw_img = pygame.image.load(os.path.join('img','metal_claw.png'))
metal_claw=pygame.transform.scale(metal_claw_img,(WIDTH/2,HEIGHT/2))
thunderbolt_img = pygame.image.load(os.path.join('img','Thunderbolt.png'))
thunderbolt=pygame.transform.scale(thunderbolt_img,(WIDTH/2,HEIGHT/2))
thunder_img = pygame.image.load(os.path.join('img','Thunder.png'))
thunder=pygame.transform.scale(thunder_img,(WIDTH/2,HEIGHT/2))  
thundershock_img = pygame.image.load(os.path.join('img','thundershock.png'))
thundershock=pygame.transform.scale(thundershock_img,(WIDTH/2,HEIGHT/2))
iron_img = pygame.image.load(os.path.join('img','iron tail.png'))
iron_tail=pygame.transform.scale(iron_img,(WIDTH/2,HEIGHT/2))

# Define the player's Pokémon party
party_bg =pygame.transform.scale( pygame.image.load(os.path.join('img', 'party_bg.png')),(1300,700))  # Replace with your party menu background image
pokemon_icons = {
    'charmander': pygame.image.load(os.path.join('img', 'icon004.png')),
    'bulbasaur': pygame.image.load(os.path.join('img', 'icon001.png')),
    'squirtle': pygame.image.load(os.path.join('img', 'icon007.png'))
}
pokemon_party = ['charmander', 'bulbasaur', 'squirtle']
current_pokemon_index = 0

# audio files
#intro_bgm=pygame.mixer.Sound('bgm/intro_bgm.wav')
#opening=pygame.mixer.Sound('bgm/opening.mp3')
# Categories and items
categories = {
    'items': {
        'potion': 3,
        'super potion': 2,
        'hyper potion': 1
    },
    'key items': {
        'bike': 1,
        'town map': 1,
        'fishing rod': 1
    },
    'pokeballs': {
        'pokeball': 5,
        'greatball': 3,
        'ultraball': 2,
        'masterball': 1
    }
}

catch_probabilities = {
    'pokeball': 0.3,  # 30% catch rate
    'greatball': 0.5,  # 50% catch rate
    'ultraball': 0.7,  # 70% catch rate
    'masterball': 1.0  # 100% catch rate
}

item_descriptions = {
    'potion': 'Restores 20 HP of a Pokémon.',
    'super potion': 'Restores 50 HP of a Pokémon.',
    'hyper potion': 'Restores 200 HP of a Pokémon.',
    'bike': 'A folding bicycle that allows fast travel.',
    'town map': 'A map of the region. It shows your present location.',
    'fishing rod': 'A tool used to fish for wild Pokémon.',
    'pokeball': 'A device for catching wild Pokémon.',
    'greatball': 'A good, high-performance Poké Ball.',
    'ultraball': 'An ultra-high performance Poké Ball.',
    'masterball': 'The best BALL with the ultimate performance.'
}

# Background and Item images
bag_bg = pygame.image.load(os.path.join('img', 'bag.png'))
bag_bg=pygame.transform.scale(bag_bg,(1300,700))
item_images = {
    'potion': pygame.image.load(os.path.join('img', 'POTION.png')),
    'super potion': pygame.image.load(os.path.join('img', 'SUPERPOTION.png')),
    'hyper potion': pygame.image.load(os.path.join('img', 'HYPERPOTION.png')),
    'bike': pygame.image.load(os.path.join('img', 'BICYCLE.png')),
    'town map': pygame.image.load(os.path.join('img', 'TOWNMAP.png')),
    'fishing rod': pygame.image.load(os.path.join('img', 'OLDROD.png')),
    'pokeball': pygame.image.load(os.path.join('img', 'POKEBALL.png')),
    'greatball': pygame.image.load(os.path.join('img', 'GREATBALL.png')),
    'ultraball': pygame.image.load(os.path.join('img', 'ULTRABALL.png')),
    'masterball': pygame.image.load(os.path.join('img', 'MASTERBALL.png')),
}
# Load sprite sheets for different balls
pokeball_throw_sheet = pygame.image.load(os.path.join('img', 'pokeball_throw.png'))
greatball_throw_sheet = pygame.image.load(os.path.join('img', 'greatball_throw.png'))
ultraball_throw_sheet = pygame.image.load(os.path.join('img', 'ultraball_throw.png'))
masterball_throw_sheet = pygame.image.load(os.path.join('img', 'masterball_throw.png'))

def load_animation_frames(folder):
    frames = []
    for filename in sorted(os.listdir(folder)):
        if filename.endswith('.png'):  # Assuming all frames are in PNG format
            frame = pygame.transform.scale(pygame.image.load((os.path.join(folder, filename))),(1300,700))
            frames.append(frame)
    return frames

# Load frames from the folder
animation_frames = load_animation_frames(os.path.join( 'intro'))
def display_intro_animation(frames, frame_duration=0.05):
    for frame in frames:
        
        screen.blit(frame, (0, 0))  # Draw frame at the top-left corner
        pygame.display.update()
        time.sleep(frame_duration)
        


def extract_frames(sheet, frame_width, frame_height):
    frames = []
    sheet_width, sheet_height = sheet.get_size()
    for y in range(sheet_height // frame_height):
        for x in range(sheet_width // frame_width):
            frame = sheet.subsurface(pygame.Rect(x * frame_width, y * frame_height, frame_width, frame_height))
            frames.append(frame)
    return frames

def bag_menu():
    clock = pygame.time.Clock()
    selected_item_index = 0
    selected_category_index = 0
    categories_list = list(categories.keys())
    menu_open = True
    desc_disp=False
    screen.blit(bag_bg, (0, 0))
    while menu_open:
        
        
        # Get the current category and items
        current_category = categories_list[selected_category_index]
        current_items = categories[current_category]
        
        # Draw items
        y_offset = 50
        for index, (item, quantity) in enumerate(current_items.items()):
            color = bl if index != selected_item_index else red
            draw_text(current_category,font,bl,screen,50,320)
            draw_text(f"{item} x{quantity}", font, color, screen, 550, y_offset)
            y_offset += 50
        
        # Draw item image and description
        selected_item = list(current_items.keys())[selected_item_index]
        item_image = item_images[selected_item]
        screen.blit(item_image, (55, 600))  # Position item image on the left
        description = item_descriptions[selected_item]
        #pygame.draw.rect(screen, wt, pygame.Rect(150, 200, 700, 125))
        if not desc_disp:
            display_text_one_by_one([description], font2, bl, screen, 500, 550, delay=0.01, line_spacing=20)
            desc_disp=True
        
        pygame.display.update()
        clock.tick(fps)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                desc_disp=False
                screen.blit(bag_bg, (0, 0))
                #pygame.draw.rect(screen, wt, pygame.Rect(55, 600, 50, 50))
                #pygame.draw.rect(screen, wt, pygame.Rect(500, 50, 600, 350))
                if event.key == pygame.K_UP:
                    selected_item_index = (selected_item_index - 1) % len(current_items)
                elif event.key == pygame.K_DOWN:
                    selected_item_index = (selected_item_index + 1) % len(current_items)
                elif event.key == pygame.K_LEFT:
                    selected_category_index = (selected_category_index - 1) % len(categories_list)
                    selected_item_index = 0  # Reset item selection when changing categories
                elif event.key == pygame.K_RIGHT:
                    selected_category_index = (selected_category_index + 1) % len(categories_list)
                    selected_item_index = 0  # Reset item selection when changing categories
                elif event.key == pygame.K_RETURN:
                    selected_item = list(current_items.keys())[selected_item_index]
                    if selected_item.endswith('ball'):
                        attempt_catch(selected_item, pika_img, eny)
                        menu_open=False
                        
                    # Perform action with the selected item (currently just closes the menu)
                    print(f"Selected {selected_item} from {current_category}")
                    menu_open = False
                elif event.key == pygame.K_x:
                    menu_open = False

import math

def pokeball_throw_animation(ball_frames, target_img, target_rect,x_radius,y_radius,center_x,center_y):
    clock=pygame.time.Clock()
    # Elliptical throw animation
    #x_radius = 500  # Radius along x-axis
    #y_radius = 75   # Radius along y-axis
    #center_x, center_y = 450, 250  # Center of the ellipse
    num_steps = 50  # Number of steps in the animation
    num_frames = len(ball_frames) # Number of frames in the sprite sheet

    for i in range(num_steps):
        clock.tick(fps)
        screen.fill(wt)
        screen.blit(bg_img, (0, 0))
        screen.blit(target_img, target_rect)
        
        # Calculate the x and y positions using parametric equations of an ellipse
        theta = (i / num_steps) * math.pi  # Angle in radians
        ball_x = center_x - x_radius * math.cos(theta)
        ball_y = center_y - y_radius * math.sin(theta)
        #get the current frama
        current_frame = ball_frames[i % num_frames]
        screen.blit(current_frame, (ball_x, ball_y))
        screen.blit(pokemon_data[selected_pokemon]['image'], (me.x, me.y))
        pygame.display.update()
        time.sleep(0.03)

    # Pikachu goes white and enters Pokéball
    for i in range(5):
        clock.tick(fps)
        screen.fill(wt)
        screen.blit(bg_img, (0, 0))
        screen.blit(pokemon_data[selected_pokemon]['image'], (me.x, me.y))
        if i % 2 == 0:
            screen.blit(target_img, target_rect)
        pygame.display.update()
        time.sleep(0.1)
    fall_distance = 100 # How much the Pokémon falls down
    fall_speed = 5  # Falling speed
    for _ in range(fall_distance // fall_speed):
        clock.tick(fps)
        ball_y += fall_speed
        screen.fill(wt)
        screen.blit(bg_img, (0, 0))
        #screen.blit(pika_img, (eny.x, eny.y))  # Draw opponent Pokémon
        screen.blit(pokemon_data[selected_pokemon]['image'], (me.x, me.y))    # Draw player's Pokémon
        screen.blit(current_frame, (ball_x, ball_y))
        pygame.display.update()
        time.sleep(0.03)
    # Pokéball wiggle
    wiggle_offsets = [(-5, 0), (5, 0), (0, 0), (-5, 0), (5, 0), (0, 0)]  # Wiggle pattern
    for offset in wiggle_offsets:
        clock.tick(fps)
        screen.fill(wt)
        screen.blit(bg_img, (0, 0))
        screen.blit(pokemon_data[selected_pokemon]['image'], (me.x, me.y))
        wiggle_ball = current_frame #pygame.transform.rotate(ball_img, 0)  # No rotation, just position wiggle
        ball_rect = wiggle_ball.get_rect(center=(target_rect.x + 100 + offset[0], ball_y))
        screen.blit(wiggle_ball, ball_rect)
        pygame.display.update()
        time.sleep(0.2)


def attempt_catch(ball_type, target_img, target_rect):
    # Extract frames from the sprite sheet based on ball type
    if ball_type == 'pokeball':
        ball_frames = extract_frames(pokeball_throw_sheet, frame_width=32, frame_height=64)
    elif ball_type == 'greatball':
        ball_frames = extract_frames(greatball_throw_sheet, frame_width=32, frame_height=64)
    elif ball_type == 'ultraball':
        ball_frames = extract_frames(ultraball_throw_sheet, frame_width=32, frame_height=64)
    elif ball_type == 'masterball':
        ball_frames = extract_frames(masterball_throw_sheet, frame_width=32, frame_height=64)
    
    display_text_one_by_one([f'You used a {ball_type}'], font, bl, screen, 475, 500)
    
    pokeball_throw_animation(ball_frames, target_img, target_rect,500,75,450,250)
    
    if random.random() <= catch_probabilities[ball_type]:
        display_text_one_by_one(['Congratulations!', 'You caught Pikachu!'], font, bl, screen, 475, 500,)
    else:
        display_text_one_by_one(['Oh no!', 'Pikachu broke free!'], font, bl, screen, 475,500)
        # Pikachu comes back
        screen.fill(wt)
        screen.blit(bg_img, (0, 0))
        screen.blit(target_img, target_rect)
        pygame.display.update()
def pokemon_menu():
    global current_pokemon_index
    clock = pygame.time.Clock()
    selected_pokemon_index = 0
    menu_open = True
    grid_columns = 2
    grid_rows = 3
    icon_size = 64  # Adjust icon size if necessary
    grid_spacing_x = 550  # Space between grid items
    grid_spacing_y = 100
    prev_poke=pokemon_party[current_pokemon_index]
    
    while menu_open:
        screen.blit(party_bg, (0, 0))  # Draw party background

        # Draw Pokémon party with icons in 2x6 grid
        for index, pokemon in enumerate(pokemon_party):
            row = index // grid_columns
            col = index % grid_columns
            x = 50 + col * (icon_size + grid_spacing_x)
            y = 50 + row * (icon_size + grid_spacing_y)

            color = bl if index != selected_pokemon_index else red
            icon = pokemon_icons[pokemon]
            screen.blit(icon, (x, y))  # Draw Pokémon icon
            draw_text(f"{pokemon}", font, color, screen, x + icon_size + 10, y)
            #draw_text(f"{pokemon['current_hp']}/{pokemon['max_hp']} HP", font, color, screen, x + icon_size + 10, y + 20)
        
        draw_text('CANCEL', font, bl, screen, 50, grid_rows * (icon_size + grid_spacing_y))  # Cancel option

        pygame.display.update()
        clock.tick(fps)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_pokemon_index = (selected_pokemon_index - grid_columns) % (len(pokemon_party) + 1)
                elif event.key == pygame.K_DOWN:
                    selected_pokemon_index = (selected_pokemon_index + grid_columns) % (len(pokemon_party) + 1)
                elif event.key == pygame.K_LEFT:
                    selected_pokemon_index = (selected_pokemon_index - 1) % (len(pokemon_party) + 1)
                elif event.key == pygame.K_RIGHT:
                    selected_pokemon_index = (selected_pokemon_index + 1) % (len(pokemon_party) + 1)
                elif event.key == pygame.K_RETURN:
                    if selected_pokemon_index < len(pokemon_party):
                        # Switch to the selected Pokémon
                        
                        current_pokemon_index = selected_pokemon_index
                        switch_pokemon_animation(prev_poke,me)
                    menu_open = False
                elif event.key == pygame.K_x:
                    menu_open = False


def switch_pokemon_animation(prev_poke,me):
    #global me
    print(prev_poke)
    old_poke=pokemon_data[prev_poke]['image']
    current_pokemon = pokemon_party[current_pokemon_index]
    #print(current_pokemon)
    old_pokemon = me  # Assume `me` is the current Pokémon Rect for simplicity
    #color(eny,old_pokemon)
    screen.blit(bg_img, (0, 0))
    screen.blit(old_poke, old_pokemon)
    screen.blit(pika_img,eny)
    display_text_one_by_one([f'{prev_poke}, come back'], font, bl, screen, 475,500)
    # Old Pokémon goes back
    
    for i in range(50):
        screen.fill(wt)
        screen.blit(bg_img, (0, 0))
        old_pokemon.x -= 50
        screen.blit(old_poke, old_pokemon)
        pygame.display.update()
        screen.blit(pika_img,eny)
        time.sleep(0.05)
    display_text_one_by_one([f'go, {current_pokemon}'], font, bl, screen, 475,500)
    # New Pokémon comes out from Pokéball
    selected_pokemon=current_pokemon
    ball_frames = extract_frames(pokeball_throw_sheet, frame_width=32, frame_height=64)
    pokeball_throw_animation(ball_frames, pokemon_data[selected_pokemon]['image'], old_pokemon,250,200,0,550)
    
    # Update current Pokémon image and rect
    
    me.y=750
    # New Pokémon appears
    for i in range(8):
        me.x=200
        #screen.fill(wt)
        screen.blit(bg_img, (0, 0))
        me.y -= 50
        #print(me)
        screen.blit(pokemon_data[selected_pokemon]['image'], me)
        pygame.display.update()
        time.sleep(0.05)

def attack_animation(sprite, rows, cols, frame_delay, x_offset, y_offset):
    frames = []
    FRAME_WIDTH = sprite.get_width() // cols  # Adjust based on your sprite sheet
    FRAME_HEIGHT = sprite.get_height() // rows  # Adjust based on your sprite sheet
    for row in range(rows):
        for col in range(cols):
            frame = sprite.subsurface(pygame.Rect(col * FRAME_WIDTH, row * FRAME_HEIGHT, FRAME_WIDTH, FRAME_HEIGHT))
            frames.append(frame)
    
    current_frame = 0
    last_update = pygame.time.get_ticks()
    animation_done = False

    while not animation_done:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        now = pygame.time.get_ticks()
        if now - last_update > frame_delay:
            current_frame += 1
            last_update = now
            if current_frame >= len(frames):
                animation_done = True
                screen.blit(pika_img,(eny.x,eny.y))
        
        # Display current frame if animation is not done
        if not animation_done:
            screen.blit(frames[current_frame], (eny.x + x_offset, eny.y + y_offset))
        
        pygame.display.update()

def fade_in(surface, screen, duration):
    

    clock = pygame.time.Clock()
    alpha = 255
    fade.set_alpha(alpha)
    start_time = time.time()

    while alpha > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        elapsed_time = time.time() - start_time
        alpha = max(255 - (elapsed_time / duration) * 255, 0)
        fade.set_alpha(alpha)

        screen.fill(wt)  
        screen.blit(fade, (0, 0))
        pygame.display.flip()
        clock.tick(60)
def fade_out(surface, screen, duration):
    clock = pygame.time.Clock()
    alpha = 255
    fade.set_alpha(alpha)
    start_time = time.time()

    while alpha > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        elapsed_time = time.time() - start_time
        alpha = max(255,  (elapsed_time / duration) * 255, 0)
        fade.set_alpha(alpha)

        screen.fill(bl)
        screen.blit(fade, (255, 255))
        pygame.display.flip()
        clock.tick(60)


def draw_health_bar(surface, x, y, health, max_health, width, height, bar_color=green, bg_color=red):
    # Calculate health bar width based on current health
    current_width = (health / max_health) * width
    # Draw health bar background (red)
    pygame.draw.rect(surface, bg_color, (x, y, width, height))
    # Draw health bar (green) over the background
    pygame.draw.rect(surface, bar_color, (x, y, current_width, height))




def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def display_text_one_by_one(text_list, font, color, surface, x, y, delay=0.05, line_spacing=40):
    screen.blit(text_img, (415, 475))
    #pygame.draw.rect(surface, wt, pygame.Rect(450, 500, 800, 125))
    y_offset = y
    for text in text_list:
        for i in range(len(text) + 1):
            text_surface = font.render(text[:i], True, color)
            surface.blit(text_surface, (x, y_offset))
            pygame.display.update()
            time.sleep(delay)
        y_offset += line_spacing  # Move to the next line

def damage_decrease(surface, pokemon_img, pokemon_rect, current_health, damage, max_health, health_bar_x, health_bar_y, health_bar_width, health_bar_height, blink_color=wt, blink_duration=0.1, decrease_speed=2):
    new_health = max(0, current_health - damage)
    frames = 3  # Number of blinking frames
    original_color = surface.copy()
    
    # Blinking effect
    for _ in range(frames):
        screen.blit(surface, (0, 0))
        pygame.display.update()
        time.sleep(blink_duration)
        screen.blit(pokemon_img, pokemon_rect)
        pygame.display.update()
        time.sleep(blink_duration)
    
    # Slowly decrease the health bar
    while current_health > new_health:
        current_health -= decrease_speed
        current_health = max(new_health, current_health)
        draw_health_bar(surface, health_bar_x, health_bar_y, current_health, max_health, health_bar_width, health_bar_height)
        pygame.display.update()
        time.sleep(0.05)

    # Ensure the final health bar reflects the exact new health
    draw_health_bar(surface, health_bar_x, health_bar_y, new_health, max_health, health_bar_width, health_bar_height)
    pygame.display.update()


def color(eny, me):
    global health,ch_health
    screen.fill(wt)
    screen.blit(bg_img, (0, 0))
    screen.blit(pika_img, (eny.x, eny.y))
    screen.blit(pokemon_data[selected_pokemon]['image'], (me.x, me.y))

    #screen.blit(text_img, (415, 475))
    screen.blit(me_box_img, (975, 390))
    screen.blit(eny_box_img, (150, 200))

    draw_text('pikachu', font2, bl, screen, 170, 200)
    draw_health_bar(screen, 268, 240, health, max_health, health_bar_width, health_bar_height)

    
    
    selected_data = pokemon_data[selected_pokemon]
    draw_health_bar(screen, selected_data['x'], selected_data['y'], selected_data['health'], selected_data['max_health'], selected_data['health_bar_width'], selected_data['health_bar_height'])

    draw_text(selected_pokemon, font2, bl, screen,1020, 390)  # Adjust position as needed

    pygame.display.update()

def run():
    run = ['you got away safely']
    display_text_one_by_one(run, font, bl, screen, 475, 500)
    keys = pygame.key.get_pressed()
    time.sleep(1)
    pygame.quit()
    sys.exit()

def draw_cursor(surface, position, color, size=10):
    points = [(position[0] + size , position[1]+size+2*size), (position[0] , position[1]+2*size), (position[0], position[1] + 2*size+2*size)]
    pygame.draw.polygon(surface, color, points)

def select():
    clock=pygame.time.Clock()
    current_position=0
    choice=True
    cursor_color = bl
    cursor_positions = [pos for pos in positions]
    while choice:
        pygame.display.update()
        clock.tick(fps)
        pygame.draw.rect(screen, wt, pygame.Rect(850, 500, 400, 125))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    current_position = (current_position + 2) % len(cursor_positions)
                elif event.key == pygame.K_UP:
                    current_position = (current_position - 2) % len(cursor_positions)
                elif event.key == pygame.K_LEFT:
                    current_position = (current_position - 1) % len(cursor_positions)
                elif event.key == pygame.K_RIGHT:
                    current_position = (current_position + 1) % len(cursor_positions)
                elif event.key == pygame.K_RETURN:
                    word = words[current_position]
                    print(f'You selected {word}')
                    if word == 'fight':
                        fight()
                        choice = False
                    elif word == 'run':
                        run()
                    elif word=='bag':
                        bag_menu()
                    elif word=='pokemon':
                        pokemon_menu()
                    return
        
        for i, pos in enumerate(cursor_positions):
            draw_text(words[i], font, bl, screen, *pos)
        
        draw_cursor(screen, (cursor_positions[current_position][0] - 20, cursor_positions[current_position][1] + 10), cursor_color)
        
        pygame.display.update()
        clock.tick(fps)

def faint(pokemon_img, pokemon_rect, pokemon_name):
    # Fainting animation (fall down effect)
    fall_distance = 1000  # How much the Pokémon falls down
    fall_speed = 50      # Falling speed
    for _ in range(fall_distance // fall_speed):
        pokemon_rect.y += fall_speed
        screen.fill(wt)
        screen.blit(bg_img, (0, 0))
        screen.blit(pika_img, (eny.x, eny.y))  # Draw opponent Pokémon
        screen.blit(pokemon_data[selected_pokemon]['image'], (me.x, me.y))   # Draw player's Pokémon
        color(eny,me)
        if pokemon_name == 'pikachu':
            screen.blit(pokemon_img, pokemon_rect)
        else:
            screen.blit(pika_img, eny)  # Draw Pikachu if Charmander faints
        pygame.display.update()
        time.sleep(0.05)
    
    # Display faint message
    faint_message = [f'{pokemon_name} fainted']
    display_text_one_by_one(faint_message, font, bl, screen, 475, 500)

def fight():
    global health,ch_health,ch_damage
    pygame.draw.rect(screen, wt, pygame.Rect(450, 500, 800, 125))
    clock=pygame.time.Clock()
    current_position=0
    cursor_color = bl
    cursor_positionsf = [pos for pos in positionsf]
    move=True
    while move:
        pygame.display.update()
        clock.tick(fps)
        pygame.draw.rect(screen, wt, pygame.Rect(450, 500, 800, 125))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    current_position = (current_position + 2) % len(cursor_positionsf)
                elif event.key == pygame.K_UP:
                    current_position = (current_position - 2) % len(cursor_positionsf)
                elif event.key == pygame.K_LEFT:
                    current_position = (current_position - 1) % len(cursor_positionsf)
                elif event.key == pygame.K_RIGHT:
                    current_position = (current_position + 1) % len(cursor_positionsf)
                elif event.key == pygame.K_RETURN:
                    word = wordsf[current_position]
                    attack=[f'{selected_pokemon} used {word}']
                    display_text_one_by_one(attack, font, bl, screen, 475, 500)
                    if word=='scratch':
                        print('hi')
                        attack_animation(scratch, 1, 5, 100, -55, 0)
                        health_decrease_amount = 10
                        print(health)
                    elif word =='ember':
                        attack_animation(ember, 3, 5, 100, 10, 75)

                        health_decrease_amount = 20
                        print(health)
                    elif word == 'flamethrower':
                        attack_animation(flamethrower, 3, 5, 100, 0, 75)

                        health_decrease_amount = 40
                        print(health)
                    elif word=="metal claw":
                        attack_animation(metal_claw, 3, 5, 100, 0, 75)

                        health_decrease_amount = 30
                        
                        print(health)
                    move=False
                    damage_decrease(screen, pika_img, eny, health, health_decrease_amount, max_health, 268, 240, health_bar_width, health_bar_height)
                    health = max(0, health - health_decrease_amount)
                    if health<=0:
                        faint(pika_img,eny,'pikachu')
                        return
                    # Pikachu's counterattack
                    pikachu_attacks = ['thundershock', 'thunder', 'iron tail', 'thunderbolt']
                    #pikachu_attacks = [ 'iron tail']
                    random_attack = random.choice(pikachu_attacks)
                    counter_attack = [f'pikachu used {random_attack}']
                    display_text_one_by_one(counter_attack, font, bl, screen,475, 500)
                    if random_attack == 'thundershock':
                        attack_animation(thundershock, 3, 5, 100, -730, 350)  # Use an existing animation or add a new one
                        ch_damage = 10
                    elif random_attack == 'iron tail':
                        attack_animation(iron_tail, 1, 2, 100, -750, 190)
                        ch_damage = 20
                    elif random_attack == 'thunderbolt':
                        attack_animation(thunderbolt, 2, 5, 100, -730,350)
                        ch_damage = 30
                    elif random_attack == 'thunder':
                        attack_animation(thunder, 2, 5, 100, -730, 350)
                        ch_damage = 40
                        
                    damage_decrease(screen, pokemon_data[selected_pokemon]['image'], me, ch_health, ch_damage, ch_max_health, 1110, 430, ch_health_bar_width, ch_health_bar_height)
                    ch_health = max(0, ch_health - ch_damage)
                    if ch_health<=0:
                        faint(pokemon_data[selected_pokemon]['image'],me,selected_pokemon)
                        return
                    print(ch_health)
        for i, pos in enumerate(cursor_positionsf):
            draw_text(wordsf[i], font, bl, screen, *pos)
        draw_cursor(screen, (cursor_positionsf[current_position][0] - 20, cursor_positionsf[current_position][1] + 10), cursor_color)

    pygame.time.wait(2000)
clock = pygame.time.Clock()
def main():
    global ch_health
    
    fade_in(fade, screen, 1)
    #opening.play(-1)
    #screen.blit(start,(50,0))	    run = True
    color(eny, me)
    text_displayed = False
    if not text_displayed:
        display_text_one_by_one(text1, font, bl, screen, 475, 500)
        text_displayed = True
    run=True
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z]:
            #pygame.draw.rect(screen, wt, pygame.Rect(50, 350, 800, 125))
            text_displayed = False
            if not text_displayed:
                display_text_one_by_one(text2, font, bl, screen, 475, 500)
                text_displayed = True
        if keys[pygame.K_z]:
            select()
            color(eny,me)
            
    pygame.quit()
    sys.exit()
if True:
    #intro_bgm.play()
    display_intro_animation(animation_frames)
    #opening.play(-1)
    #screen.fill(bl)
    #starting=True
    #while starting:
    #    clock.tick(12)
    #    screen.blit(start,(0,0))
    #    keys = pygame.key.get_pressed()
     #   if keys[pygame.K_z]:
     #       opening.stop()
     #       starting=False
    main()

