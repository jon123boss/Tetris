import pygame
import random
import os
import json

pygame.init()

WINDOW_SIZE = (300, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Tetris")

SCORE_PER_LINE = [0, 100, 300, 500, 800]  # Single, double, triple, Tetris
score = 0  # Initialize the score
high_score = 0  # Initialize high score

GRID_WIDTH = 10
GRID_HEIGHT = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]]
]

STARTING_LEVEL = 1
LINES_PER_LEVEL = 10  # Number of lines to clear per level increase
FALL_SPEED = 500  # Initial fall speed in milliseconds
SPEED_INCREASE = 50  # Fall speed increase per level in milliseconds

current_level = STARTING_LEVEL
lines_cleared_total = 0  # Track total lines cleared across the game

def load_high_score():
    global high_score
    if os.path.exists('highscore.json'):
        with open('highscore.json', 'r') as f:
            data = json.load(f)
            high_score = data.get('high_score', 0)

def save_high_score():
    global high_score
    with open('highscore.json', 'w') as f:
        json.dump({'high_score': high_score}, f)

def new_tetromino():
    shape = random.choice(SHAPES)
    return shape, [0, GRID_WIDTH // 2 - len(shape[0]) // 2]

def valid_position(grid, shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                if x + off_x < 0 or x + off_x >= GRID_WIDTH or y + off_y >= GRID_HEIGHT or grid[y + off_y][x + off_x]:
                    return False
    return True

def join_matrixes(grid, shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                grid[y + off_y][x + off_x] = cell
    return grid

def clear_lines(grid):
    lines_to_clear = []
    for i, row in enumerate(grid):
        if all(row):
            lines_to_clear.append(i)

    lines_cleared = len(lines_to_clear)
    if lines_cleared > 0:
        global score, high_score, lines_cleared_total, current_level
        lines_cleared_total += lines_cleared
        score += SCORE_PER_LINE[lines_cleared]  # Update the score based on lines cleared
        high_score = max(high_score, score)  # Update the high score if current score is higher

        # Check if level should increase
        if lines_cleared_total // LINES_PER_LEVEL >= current_level:
            current_level += 1
            # Increase speed
            new_speed = max(FALL_SPEED - (current_level - 1) * SPEED_INCREASE, 50)  # Ensure speed doesn't drop below 50ms
            print(f"Level {current_level}, Speed: {new_speed}ms")

    # Remove cleared lines and add new empty lines at the top
    for i in lines_to_clear:
        del grid[i]
        grid.insert(0, [0 for _ in range(GRID_WIDTH)])

    return lines_cleared

def draw_score(screen):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    level_text = font.render(f"Level: {current_level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 50))
    screen.blit(level_text, (10, 90))

def draw_grid(screen, grid):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell:
                color = get_color(cell)
                pygame.draw.rect(screen, color, (x * 30, y * 30, 30, 30), 0)
                pygame.draw.rect(screen, BLACK, (x * 30, y * 30, 30, 30), 1)

def draw_tetromino(screen, shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                color = get_color(cell)
                pygame.draw.rect(screen, color, ((x + off_x) * 30, (y + off_y) * 30, 30, 30), 0)
                pygame.draw.rect(screen, BLACK, ((x + off_x) * 30, (y + off_y) * 30, 30, 30), 1)

def get_color(value):
    colors = [BLACK, BLUE, RED, GREEN, YELLOW, ORANGE, PURPLE]
    return colors[value]

def start_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 36)
    title_text = font.render("Tetris", True, WHITE)
    start_text = font.render("Press Space to Start", True, WHITE)
    screen.blit(title_text, (WINDOW_SIZE[0] // 2 - title_text.get_width() // 2, 200))
    screen.blit(start_text, (WINDOW_SIZE[0] // 2 - start_text.get_width() // 2, 300))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

def game_over_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 36)
    game_over_text = font.render("Game Over", True, RED)
    score_text = font.render(f"Score: {score}", True, WHITE)
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(game_over_text, (WINDOW_SIZE[0] // 2 - game_over_text.get_width() // 2, 200))
    screen.blit(score_text, (WINDOW_SIZE[0] // 2 - score_text.get_width() // 2, 300))
    screen.blit(high_score_text, (WINDOW_SIZE[0] // 2 - high_score_text.get_width() // 2, 350))
    pygame.display.flip()
    pygame.time.wait(3000)

def main_loop():
    global score, current_level, lines_cleared_total
    start_screen()

    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    shape, offset = new_tetromino()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = FALL_SPEED  # Initial fall speed

    load_high_score()

    running = True
    paused = False
    while running:
        if not paused:
            fall_time += clock.get_rawtime()
            clock.tick()

            if fall_time >= fall_speed:
                fall_time = 0
                offset[1] += 1  # Move the tetromino down vertically
                if not valid_position(grid, shape, offset):
                    offset[1] -= 1
                    grid = join_matrixes(grid, shape, offset)
                    lines_cleared = clear_lines(grid)
                    shape, offset = new_tetromino()
                    if not valid_position(grid, shape, offset):
                        game_over_screen()
                        running = False
                        save_high_score()

                    # Adjust fall speed based on level
                    fall_speed = max(FALL_SPEED - (current_level - 1) * SPEED_INCREASE, 50)  # Ensure speed doesn't drop below 50ms

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    save_high_score()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        offset[0] -= 1
                        if not valid_position(grid, shape, offset):
                            offset[0] += 1
                    elif event.key == pygame.K_RIGHT:
                        offset[0] += 1
                        if not valid_position(grid, shape, offset):
                            offset[0] -= 1
                    elif event.key == pygame.K_DOWN:
                        offset[1] += 1
                        if not valid_position(grid, shape, offset):
                            offset[1] -= 1
                    elif event.key == pygame.K_UP:
                        shape = [list(row) for row in zip(*shape[::-1])]
                        if not valid_position(grid, shape, offset):
                            shape = [list(row) for row in zip(*shape)][::-1]
                    elif event.key == pygame.K_SPACE:
                        paused = not paused

            screen.fill(BLACK)
            draw_grid(screen, grid)
            draw_tetromino(screen, shape, offset)
            draw_score(screen)
            pygame.display.flip()
        else:
            # Draw pause screen
            font = pygame.font.Font(None, 36)
            pause_text = font.render("Paused", True, WHITE)
            screen.blit(pause_text, (WINDOW_SIZE[0] // 2 - pause_text.get_width() // 2, WINDOW_SIZE[1] // 2))
            pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main_loop()
