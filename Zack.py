import os
import sys
import subprocess
import time

# Changing dir to digi
os.chdir("/home/digi")

# Function to check and install missing libraries
def ensure_library_installed(library):
    try:
        __import__(library)
    except ImportError:
        print(f"{library} not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", library])

# Ensure required libraries are installed
ensure_library_installed("pygame")

# Import libraries after ensuring installation
import pygame

# Initialize Pygame
pygame.init()

# Get display info for full screen
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h

# Set up the screen to full screen mode
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("DTG by Zos Computer")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Ball properties
ball_radius = 50
ball_y = screen_height // 2
ball_x1 = screen_width // 3  # First ball's position
ball_x2 = 2 * screen_width // 3  # Second ball's position

# Timing control
last_toggle_time = time.time()
toggle_interval = 20  # Seconds
off_duration = 0.1  # Seconds
balls_visible = True

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle ball visibility toggling
    current_time = time.time()
    if balls_visible and current_time - last_toggle_time >= toggle_interval:
        balls_visible = False
        last_toggle_time = current_time
    elif not balls_visible and current_time - last_toggle_time >= off_duration:
        balls_visible = True
        last_toggle_time = current_time

    # Clear the screen
    screen.fill(BLACK)

    # Draw the balls if visible
    if balls_visible:
        pygame.draw.circle(screen, WHITE, (ball_x1, ball_y), ball_radius)
        pygame.draw.circle(screen, WHITE, (ball_x2, ball_y), ball_radius)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
