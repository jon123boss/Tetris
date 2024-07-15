import pygame
import sys

WINDOW_SIZE = (800, 600)
WINDOW_TITLE = "Tetris"

def initialize_pygame():
    """Initialize Pygame and create the game window."""
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption(WINDOW_TITLE)
    return screen

def draw_window(screen):
    """Draw the game window."""
    screen.fill((0, 0, 0))
    pygame.display.update()

def handle_events():
    """Handle user input and events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True

def update_game():
    """Update the game state."""

    pass

def main_loop():
    """Main loop of the game."""
    screen = initialize_pygame()
    running = True

    while running:
        running = handle_events()
        update_game()
        draw_window(screen)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_loop()