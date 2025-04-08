import pygame
from ffpyplayer.player import MediaPlayer

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rhythm Game with Video Background")

# Load video using ffpyplayer
video_path = 'diti.avi'
player = MediaPlayer(video_path)

# Function to update the video frame
def update_video_frame(player, surface):
    frame, val = player.get_frame()
    if val == 'eof':
        player.seek(0, relative=False)
        frame, val = player.get_frame()
    if frame is not None:
        img, t = frame
        img = pygame.surfarray.make_surface(img.to_bytearray()[..., ::-1].transpose(1, 0, 2))
        surface.blit(img, (0, 0))
