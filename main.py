import os
import sys
import subprocess
import datetime
import time

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

# Load the background image and scale it dynamically to fit the screen
try:
    background = pygame.image.load("b1.png")
    bg_width, bg_height = background.get_size()

    # Calculate scaling factor to fill the screen
    scale_x = screen_width / bg_width
    scale_y = screen_height / bg_height
    scale_factor = max(scale_x, scale_y)  # Zoom in until the background fills the screen

    # Resize the background
    new_width = int(bg_width * scale_factor)
    new_height = int(bg_height * scale_factor)
    background = pygame.transform.scale(background, (new_width, new_height))
except pygame.error as e:
    print(f"Error loading image: {e}")
    pygame.quit()
    sys.exit()

# Load the custom font
try:
    font_large = pygame.font.Font("CairoPlay-ExtraLight.ttf", 220)  # Large font for clock
    font_small = pygame.font.Font("CairoPlay-ExtraLight.ttf", 60)   # Smaller font for AM/PM
except FileNotFoundError:
    print("Font file 'CairoPlay-ExtraLight.ttf' not found. Please place it in the same directory.")
    pygame.quit()
    sys.exit()

clock_color = (255, 255, 255)  # White color

# Function to handle fade-in effect
def fade_in(screen, duration):
    black_surface = pygame.Surface((screen_width, screen_height))
    black_surface.fill((0, 0, 0))
    for alpha in range(255, -1, -5):  # Gradually decrease alpha
        black_surface.set_alpha(alpha)
        screen.blit(background, (0, 0))  # Draw the background
        screen.blit(black_surface, (0, 0))  # Overlay the fading black surface
        pygame.display.flip()
        pygame.time.delay(int(duration * 1000 / 51))  # Adjust timing for smooth fade

# Fade-in effect at startup
fade_in(screen, 1)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the background centered
    bg_x = (screen_width - background.get_width()) // 2
    bg_y = (screen_height - background.get_height()) // 2
    screen.blit(background, (bg_x, bg_y))

    # Get the current time in 12-hour format
    current_time = datetime.datetime.now()
    time_12hr = current_time.strftime("%I:%M")  # %I is 12-hour format
    am_pm = current_time.strftime("%p")  # AM or PM

    # Render the clock text
    clock_surface = font_large.render(time_12hr, True, clock_color)
    am_pm_surface = font_small.render(am_pm, True, clock_color)

    # Position the clock text in the middle-left
    clock_position = (screen_width // 12, screen_height // 2 - clock_surface.get_height() // 2)

    # Position AM/PM in the top-right corner of the clock
    am_pm_position = (
        clock_position[0] + clock_surface.get_width() - 20,  # Horizontal position
        clock_position[1] + 50,  # Move AM/PM down by 50 pixels
    )

    # Draw the clock and AM/PM on the screen
    screen.blit(clock_surface, clock_position)
    screen.blit(am_pm_surface, am_pm_position)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
