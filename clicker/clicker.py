import pygame
import sys
import json

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Professional Clicker Game")

# Colors
background_color = (30, 30, 30)
text_color = (255, 255, 255)
button_color = (50, 50, 200)
button_hover_color = (100, 100, 250)

# Load the images for the gallery
image_filenames = ["cool.png", "mario.png", "sans.png"]
images = [pygame.image.load(filename) for filename in image_filenames]
current_image_index = 0

# Load sound files for the sound gallery
sound_filenames = ["coin.mp3", "yahoo.mp3", "sans.mp3","beeb.mp3"]
sounds = [pygame.mixer.Sound(filename) for filename in sound_filenames]
current_sound_index = 0

# Fonts
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 36)

# Game variables
clicks = 0
click_multiplier = 1
small_image = pygame.transform.scale(images[current_image_index], (images[current_image_index].get_rect().width // 2, images[current_image_index].get_rect().height // 2))
animation_counter = 0

# Button variables
start_button_rect = pygame.Rect((width // 2 - 100, height // 2 - 25, 200, 50))
upgrade_button_rect = pygame.Rect((width // 2 - 100, height // 2 + 50, 200, 50))
save_button_rect = pygame.Rect((width // 2 - 100, height // 2 + 125, 200, 50))
load_button_rect = pygame.Rect((width // 2 - 100, height // 2 + 200, 200, 50))
achievement_text = ""
image_select_button_rect = pygame.Rect((width // 2 - 100, height // 2 - 100, 200, 50))
sound_select_button_rect = pygame.Rect((width // 2 - 100, height // 2 - 175, 200, 50))

# Function to draw buttons
def draw_button(rect, text):
    mouse_pos = pygame.mouse.get_pos()
    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, button_hover_color, rect)
    else:
        pygame.draw.rect(screen, button_color, rect)
    button_text = button_font.render(text, True, text_color)
    screen.blit(button_text, (rect.x + 50, rect.y + 10))

# Function to save the game state
def save_game():
    game_data = {
        "clicks": clicks,
        "click_multiplier": click_multiplier
    }
    with open("savefile.json", "w") as f:
        json.dump(game_data, f)
    global achievement_text
    achievement_text = "Game Saved!"

# Function to load the game state
def load_game():
    global clicks, click_multiplier, achievement_text
    try:
        with open("savefile.json", "r") as f:
            game_data = json.load(f)
            clicks = game_data["clicks"]
            click_multiplier = game_data["click_multiplier"]
        achievement_text = "Game Loaded!"
    except FileNotFoundError:
        achievement_text = "No Save File Found!"

# Gallery menu to select images
def gallery_menu():
    global current_image_index
    selecting_image = True
    while selecting_image:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_image_index = (current_image_index - 1) % len(images)
                elif event.key == pygame.K_RIGHT:
                    current_image_index = (current_image_index + 1) % len(images)
                elif event.key == pygame.K_RETURN:
                    selecting_image = False

        screen.fill(background_color)
        screen.blit(images[current_image_index], images[current_image_index].get_rect(center=(width // 2, height // 2 - 50)))
        instructions = small_font.render("Use LEFT and RIGHT arrows to select, ENTER to confirm", True, text_color)
        screen.blit(instructions, (width // 2 - instructions.get_width() // 2, height - 100))
        pygame.display.flip()

# Gallery menu to select sounds
def sound_gallery_menu():
    global current_sound_index
    selecting_sound = True
    while selecting_sound:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_sound_index = (current_sound_index - 1) % len(sounds)
                elif event.key == pygame.K_RIGHT:
                    current_sound_index = (current_sound_index + 1) % len(sounds)
                elif event.key == pygame.K_RETURN:
                    selecting_sound = False
                elif event.key == pygame.K_p:
                    sounds[current_sound_index].play()

        screen.fill(background_color)
        instructions = small_font.render("Use LEFT and RIGHT arrows to select, ENTER to confirm, P to play", True, text_color)
        current_sound_text = small_font.render(f"Current Sound: {sound_filenames[current_sound_index]}", True, text_color)
        screen.blit(instructions, (width // 2 - instructions.get_width() // 2, height - 150))
        screen.blit(current_sound_text, (width // 2 - current_sound_text.get_width() // 2, height - 100))
        pygame.display.flip()

# Main menu
def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    return
                elif upgrade_button_rect.collidepoint(event.pos):
                    global clicks, click_multiplier, achievement_text
                    if clicks >= 10:
                        clicks -= 10
                        click_multiplier += 1
                        achievement_text = f"Upgrade Purchased! Multiplier: {click_multiplier}"
                    else:
                        achievement_text = "Not Enough Clicks!"
                elif save_button_rect.collidepoint(event.pos):
                    save_game()
                elif load_button_rect.collidepoint(event.pos):
                    load_game()
                elif image_select_button_rect.collidepoint(event.pos):
                    gallery_menu()
                    reset_image()
                elif sound_select_button_rect.collidepoint(event.pos):
                    sound_gallery_menu()

        screen.fill(background_color)
        draw_button(start_button_rect, "START")
        draw_button(upgrade_button_rect, "UPGRADE")
        draw_button(save_button_rect, "SAVE")
        draw_button(load_button_rect, "LOAD")
        draw_button(image_select_button_rect, "GALLERY")
        draw_button(sound_select_button_rect, "SOUND")

        if achievement_text:
            achievement_display = small_font.render(achievement_text, True, text_color)
            screen.blit(achievement_display, (width // 2 - achievement_display.get_width() // 2, height // 2 - 100))

        # Draw the title
        title_text = font.render("CLICKER GAME", True, text_color)
        screen.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 4))

        pygame.display.flip()

def reset_image():
    global image_rect, small_image
    small_image = pygame.transform.scale(images[current_image_index], (images[current_image_index].get_rect().width // 2, images[current_image_index].get_rect().height // 2))
    image_rect = images[current_image_index].get_rect(center=(width // 2, height // 2))

# Pause menu to return to the main menu
def pause_menu():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False
                    return
                elif event.key == pygame.K_m:
                    paused = False
                    main_menu()

        screen.fill(background_color)
        instructions = small_font.render("Press ESC to resume or M to return to menu", True, text_color)
        screen.blit(instructions, (width // 2 - instructions.get_width() // 2, height // 2 - 50))
        pygame.display.flip()

# Main game loop
running = True
main_menu()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if image_rect.collidepoint(event.pos):
                clicks += click_multiplier
                sounds[current_sound_index].play()  # Play the selected sound
                animation_counter = 5  # Set animation duration
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause_menu()

    screen.fill(background_color)
    if animation_counter > 0:
        screen.blit(small_image, small_image.get_rect(center=image_rect.center))
        animation_counter -= 1
    else:
        screen.blit(images[current_image_index], image_rect)

    score_text = font.render(f"Clicks: {clicks}", True, text_color)
    screen.blit(score_text, (width // 2 - score_text.get_width() // 2, 50))

    pygame.display.flip()

pygame.quit()
sys.exit()
