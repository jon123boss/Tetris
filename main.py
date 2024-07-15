import pygame
import sys
import random

WINDOW_SIZE = (300, 600)
WINDOW_TITLE = "Tetris"
GRID_SIZE = (10, 20)
CELL_SIZE = 30

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = {
    'I': (0, 255, 255),
    'O': (255, 255, 0),
    'T': (128, 0, 128),
    'S': (0, 255, 0),
    'Z': (255, 0, 0),
    'J': (0, 0, 255),
    'L': (255, 165, 0),
}

TETROMINOS = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'Z': [[1, 1, 0], [0, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]],
    'L': [[0, 0, 1], [1, 1, 1]],
}

def initialize_pygame():
    """Initialize Pygame and create the game window."""
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption(WINDOW_TITLE)
    return screen

def draw_grid(screen, grid):
    """Draw the grid on the screen."""
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            color = WHITE if grid[y][x] == 0 else COLORS[grid[y][x]]
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def draw_tetromino(screen, tetromino, offset):
    """Draw the tetromino on the screen."""
    shape, (off_x, off_y) = tetromino, offset
    color = COLORS[shape[0]]
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, color, ((x + off_x) * CELL_SIZE, (y + off_y) * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, BLACK, ((x + off_x) * CELL_SIZE, (y + off_y) * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def handle_events():
    """Handle user input and events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True

def update_game():
    """Update the game state."""
    pass

def create_grid():
    """Create a 2D array to represent the grid."""
    return [[0 for _ in range(GRID_SIZE[0])] for _ in range(GRID_SIZE[1])]

def get_random_tetromino():
    """Return a random tetromino shape."""
    shape = random.choice(list(TETROMINOS.keys()))
    return TETROMINOS[shape], (shape, 3, 0)

def main_loop():
    """Main loop of the game."""
    screen = initialize_pygame()
    grid = create_grid()
    tetromino_shape, tetromino_info = get_random_tetromino()
    running = True

    while running:
        running = handle_events()
        update_game()
        draw_grid(screen, grid)
        draw_tetromino(screen, tetromino_shape, (tetromino_info[1], tetromino_info[2]))
        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_loop()