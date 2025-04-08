import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1300, 650
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Visual Novel Game")

# Colors
background_color = (255, 255, 255)
text_color = (0, 0, 0)

# Fonts
font = pygame.font.Font(None, 36)
name_font = pygame.font.Font(None, 40)

# Load images
background_image = pygame.image.load("background.png")
character_images = {
    "character1": {
        "neutral": pygame.transform.scale(pygame.image.load("neutral.png"), (400, 400)),
        "happy": pygame.transform.scale(pygame.image.load("happy.png"), (400, 400))
    },
    "character2": {
        "neutral": pygame.transform.scale(pygame.image.load("neutral.png"), (400, 400)),
        "sad": pygame.transform.scale(pygame.image.load("sad.png"), (400, 400))
    },
}

textbox_image = pygame.transform.scale(pygame.image.load("textbox.png"), (1200, 200))

# Load music and sound effects
#pygame.mixer.music.load("background_music.ogg")
#pygame.mixer.music.play(-1)  # Loop music

# Dialogue with choices
dialogue = [
    {"name": "Character1", "expression": "neutral", "text": "Welcome to the visual novel game!"},
    {"name": "Character2", "expression": "neutral", "text": "This is the first scene of the story."},
    {"name": "Character1", "expression": "happy", "text": "You can use the space bar to progress through the dialogue."},
    {"name": "Character2", "expression": "sad", "text": "Enjoy the story and the game!"},
    {"name": "Character1", "expression": "happy", "text": "would you us to call u a name?"},
    {"name": "", "expression": "", "text": "Do you like the game so far?", "choices": ["Yes", "No"]},
    {"name": "character1", "expression": "neutral", "text": "now, enjoy the story"}
]

# Variables to keep track of dialogue progression
current_dialogue_index = 0
in_choice = False
current_choice = 0

def draw_text(text, position, font, color):
    words = text.split(' ')
    lines = []
    current_line = []

    for word in words:
        current_line.append(word)
        # Check the width of the line with the new word
        if font.size(' '.join(current_line))[0] > textbox_image.get_width() - 40:
            current_line.pop()
            lines.append(' '.join(current_line))
            current_line = [word]

    lines.append(' '.join(current_line))

    for i, line in enumerate(lines):
        rendered_text = font.render(line, True, color)
        screen.blit(rendered_text, (position[0], position[1] + i * 30))

def draw_choice(choices, current_choice):
    base_y = height - 70
    for i, choice in enumerate(choices):
        color = (0, 255, 0) if i == current_choice else (255, 255, 0)
        draw_text(f"{i + 1}. {choice}", (100, base_y + i * 30 -50), font, color)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.KEYDOWN:
            if not in_choice:
                if event.key == pygame.K_SPACE:
                    current_dialogue_index += 1
                    if current_dialogue_index >= len(dialogue):
                        current_dialogue_index = len(dialogue) - 1  # Stay at the last dialogue entry
                    if "choices" in dialogue[current_dialogue_index]:
                        in_choice = True
            else:
                if event.key == pygame.K_UP:
                    current_choice = (current_choice - 1) % len(dialogue[current_dialogue_index]["choices"])
                elif event.key == pygame.K_DOWN:
                    current_choice = (current_choice + 1) % len(dialogue[current_dialogue_index]["choices"])
                elif event.key == pygame.K_RETURN:
                    # Implement choice handling logic here
                    print(f"Selected choice: {dialogue[current_dialogue_index]['choices'][current_choice]}")
                    in_choice = False
                    current_dialogue_index += 1

    # Clear the screen
    screen.fill(background_color)

    # Draw the background
    screen.blit(background_image, (0, 0))

    # Draw the current dialogue
    if current_dialogue_index < len(dialogue):
        current_dialogue = dialogue[current_dialogue_index]
        if "expression" in current_dialogue:
            character_name = current_dialogue["name"]
            expression = current_dialogue["expression"]
            if character_name:
                character_image = character_images[character_name.lower()][expression]
                screen.blit(character_image, (width // 2 - character_image.get_width() // 2, height - character_image.get_height() - 150))

        # Draw the textbox
        screen.blit(textbox_image, (50, height - 200))

        # Draw the character name
        if "name" in current_dialogue and current_dialogue["name"]:
            draw_text(current_dialogue["name"], (100, height - 170), name_font, text_color)

        # Draw the dialogue or choices
        if "choices" in current_dialogue and in_choice:
            draw_choice(current_dialogue["choices"], current_choice)
        elif "text" in current_dialogue:
            draw_text(current_dialogue["text"], (100, height - 100), font, text_color)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
