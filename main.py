import pygame
import sys
import random

# Constants
WINDOW_SIZE = (300, 600)
WINDOW_TITLE = "Tetris"
GRID_SIZE = (10, 20)  # Columns, Rows
CELL_SIZE = 30
GRAVITY_SPEED = 500  # Time in milliseconds for tetromino to move down automatically

# Colors
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

# Tetromino shapes
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


def draw_tetromino(screen, shape_key, tetromino, offset):
    """Draw the tetromino on the screen."""
    off_x, off_y = offset
    color = COLORS[shape_key]
    for y, row in enumerate(tetromino):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, color,
                                 ((x + off_x) * CELL_SIZE, (y + off_y) * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, BLACK,
                                 ((x + off_x) * CELL_SIZE, (y + off_y) * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)


def handle_events():
    """Handle user input and events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True


def move_tetromino(tetromino, offset, direction, grid):
    """Move the tetromino in the specified direction if possible."""
    shape, (off_x, off_y) = tetromino
    if direction == 'left':
        new_x = off_x - 1
        if is_valid_move(shape, (new_x, off_y), grid):
            return shape, (new_x, off_y)
    elif direction == 'right':
        new_x = off_x + 1
        if is_valid_move(shape, (new_x, off_y), grid):
            return shape, (new_x, off_y)
    elif direction == 'down':
        new_y = off_y + 1
        if is_valid_move(shape, (off_x, new_y), grid):
            return shape, (off_x, new_y)
    elif direction == 'rotate':
        rotated_shape = rotate_tetromino(shape)
        if is_valid_move(rotated_shape, (off_x, off_y), grid):
            return rotated_shape, (off_x, off_y)
    return tetromino


def rotate_tetromino(shape):
    """Rotate the tetromino shape."""
    return [[shape[y][x] for y in range(len(shape))] for x in range(len(shape[0]) - 1, -1, -1)]


def is_valid_move(shape, offset, grid):
    """Check if the tetromino move is valid within the grid."""
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                new_x, new_y = x + off_x, y + off_y
                if new_x < 0 or new_x >= GRID_SIZE[0] or new_y >= GRID_SIZE[1] or (
                        new_y >= 0 and grid[new_y][new_x] != 0):
                    return False
    return True


def update_game(tetromino, grid, last_time):
    """Update the game state."""
    current_time = pygame.time.get_ticks()
    if current_time - last_time > GRAVITY_SPEED:
        tetromino = move_tetromino(tetromino, tetromino[1], 'down', grid)
        last_time = current_time

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        tetromino = move_tetromino(tetromino, tetromino[1], 'left', grid)
    if keys[pygame.K_RIGHT]:
        tetromino = move_tetromino(tetromino, tetromino[1], 'right', grid)
    if keys[pygame.K_DOWN]:
        tetromino = move_tetromino(tetromino, tetromino[1], 'down', grid)
    if keys[pygame.K_UP]:
        tetromino = move_tetromino(tetromino, tetromino[1], 'rotate', grid)
    return tetromino, last_time


def create_grid():
    """Create a 2D array to represent the grid."""
    return [[0 for _ in range(GRID_SIZE[0])] for _ in range(GRID_SIZE[1])]


def get_random_tetromino():
    """Return a random tetromino shape."""
    shape_key = random.choice(list(TETROMINOS.keys()))
    return shape_key, TETROMINOS[shape_key], (3, 0)  # Start in the middle of the grid horizontally


def main_loop():
    """Main loop of the game."""
    screen = initialize_pygame()
    grid = create_grid()
    shape_key, tetromino_shape, tetromino_offset = get_random_tetromino()
    tetromino = (tetromino_shape, tetromino_offset)
    last_time = pygame.time.get_ticks()
    running = True

    while running:
        running = handle_events()
        tetromino, last_time = update_game(tetromino, grid, last_time)
        draw_grid(screen, grid)
        draw_tetromino(screen, shape_key, tetromino[0], tetromino[1])
        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main_loop()
