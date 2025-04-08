import pygame
import random

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Load the Toriel sprite
toriel_dying_image = pygame.image.load("toriel_dying.png").convert_alpha()
toriel_dying_image = pygame.transform.scale(toriel_dying_image, (200, 200))
toriel_rect = toriel_dying_image.get_rect(topleft=(325, 225))

# Load the heart sprite
toriel_heart_image = pygame.image.load("toriel_heart.png").convert_alpha()
toriel_heart_image = pygame.transform.scale(toriel_heart_image,(30,20))
heart_rect = toriel_heart_image.get_rect(center=toriel_rect.center)

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

# Function to animate the heart breaking
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
        (heart_image.subsurface(pygame.Rect(0, 0, heart_rect.width // 2, heart_rect.height)), heart_rect.topleft),
        (heart_image.subsurface(pygame.Rect(heart_rect.width // 2, 0, heart_rect.width // 2, heart_rect.height)), (heart_rect.centerx, heart_rect.top))
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
                "vy": random.uniform(-1, 2),
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
def toriel_death_animation(screen, toriel_dying_image, rect, heart_image, heart_rect):
    particles = create_particles(rect, 3000)
    for i in range(255, 0, -5):
        screen.fill((0, 0, 0))
        toriel_dying_image.set_alpha(i)
        screen.blit(toriel_dying_image, rect.topleft)
        screen.blit(heart_image, heart_rect.topleft)
        for particle in particles:
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]
            if particle["alpha"] > 0:
                particle["alpha"] -= 2
        
        draw_particles(screen, particles)
        pygame.display.flip()
        clock.tick(30)

    # Heart breaking animation
    heart_break_animation(screen, toriel_heart_image, heart_rect)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((0, 0, 0))
    screen.blit(toriel_dying_image, toriel_rect.topleft)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_z]:
        toriel_death_animation(screen, toriel_dying_image, toriel_rect, toriel_heart_image, heart_rect)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
