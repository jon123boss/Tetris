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
        global score, high_score
        score += SCORE_PER_LINE[lines_cleared]  # Update the score based on lines cleared
        high_score = max(high_score, score)  # Update the high score if current score is higher
        for i in lines_to_clear:
            del grid[i]
            grid.insert(0, [0 for _ in range(len(grid[0]))])  # Add a new empty row at the top

    return lines_cleared


def draw_score(screen):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 50))


def draw_grid(screen, grid):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, WHITE, (x * 30, y * 30, 30, 30), 0)
                pygame.draw.rect(screen, GREY, (x * 30, y * 30, 30, 30), 1)


def draw_tetromino(screen, shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, WHITE, ((x + off_x) * 30, (y + off_y) * 30, 30, 30), 0)
                pygame.draw.rect(screen, GREY, ((x + off_x) * 30, (y + off_y) * 30, 30, 30), 1)


def game_over(grid):
    for cell in grid[0]:
        if cell:
            return True
    return False


def main_loop():
    global score
    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    shape, offset = new_tetromino()
    clock = pygame.time.Clock()
    fall_time = 0

    load_high_score()

    running = True
    while running:
        fall_speed = 500  # Milliseconds - adjust this value to change fall speed
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time >= fall_speed:
            fall_time = 0
            offset[1] += 1  # Move the tetromino down vertically
            if not valid_position(grid, shape, offset):
                offset[1] -= 1
                grid = join_matrixes(grid, shape, offset)
                clear_lines(grid)
                shape, offset = new_tetromino()
                if not valid_position(grid, shape, offset):
                    running = False
                    save_high_score()

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

        screen.fill(BLACK)
        draw_grid(screen, grid)
        draw_tetromino(screen, shape, offset)
        draw_score(screen)
        pygame.display.flip()

    # Game Over Screen
    font = pygame.font.Font(None, 72)
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2))
    screen.blit(game_over_text, game_over_rect)
    pygame.display.flip()
    pygame.time.wait(3000)

    pygame.quit()



if __name__ == "__main__":
    main_loop()
