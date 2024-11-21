import pygame
import sys
import random
import heapq
import time
import json

# Initialize Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up display with additional space for scores and options
scale_factor = 1
base_game_width, base_game_height = 400, 400  # Base game area
game_area_width, game_area_height = base_game_width * scale_factor, base_game_height * scale_factor
scoreboard_width, options_width = 200, 200
width = game_area_width + scoreboard_width + options_width
height = game_area_height
# Game area settings
game_width, game_height = base_game_width, base_game_height  # Define game dimensions
cell_size = 25  # Size of each square (16x16 grid)

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Smart Snake")
clock = pygame.time.Clock()

# Game area settings
cell_size = 25  # Size of each square (16x16 grid)

# Load images
snake_image = pygame.image.load("C:/Users/Asus/Downloads/1F7E9_color.png")
food_image = pygame.image.load("C:/Users/Asus/Downloads/1F34F_color.png")

# Resize images to match the new cell size
snake_image = pygame.transform.scale(snake_image, (cell_size, cell_size))
food_image = pygame.transform.scale(food_image, (cell_size, cell_size))

# Snake settings
snake_pos = [[100, 50], [75, 50], [50, 50]]

# Initialize scores
score = 0
scores = []

# Autopilot mode
autopilot = True

# Sample Scores
players_scores = [("Player 1", 10), ("Player 2", 15), ("Player 3", 8)]  # Sample data

# Function to draw scoreboard
def draw_scoreboard():
    pygame.draw.rect(win, BLACK, (game_area_width, 0, scoreboard_width, height))
    score_title = font.render('Scoreboard', True, WHITE)
    win.blit(score_title, (game_area_width + 10, 10))
    y_offset = 40
    for player, score in players_scores:
        score_text = font.render(f"{player}: {score}", True, WHITE)
        win.blit(score_text, (game_area_width + 10, y_offset))
        y_offset += 30

# Function to draw key options
def draw_options():
    pygame.draw.rect(win, BLACK, (game_area_width + scoreboard_width, 0, options_width, height))
    options_title = font.render('Options', True, WHITE)
    win.blit(options_title, (game_area_width + scoreboard_width + 10, 10))
    options_texts = [
        "P: Pause/Resume",
        "S: Save Game",
        "L: Load Game",
        "A: Toggle Autopilot",
        "Q: Quit"
    ]
    y_offset = 40
    for text in options_texts:
        option_text = font.render(text, True, WHITE)
        win.blit(option_text, (game_area_width + scoreboard_width + 10, y_offset))
        y_offset += 30

def toggle_autopilot():
    global autopilot
    autopilot = not autopilot

# Function to save the game state
def save_game(snake_pos, food_pos, direction, score):
    game_state = {
        'snake_pos': snake_pos,
        'food_pos': food_pos,
        'direction': direction,
        'score': score
    }
    with open('savegame.json', 'w') as save_file:
        json.dump(game_state, save_file)

# Function to load the game state
def load_game():
    with open('savegame.json', 'r') as save_file:
        game_state = json.load(save_file)
    return game_state['snake_pos'], game_state['food_pos'], game_state['direction'], game_state['score']

# Function to display the score
def show_score(score, font):
    score_surface = font.render(f'Score: {score}', True, WHITE)
    win.blit(score_surface, (10, 10))



# Food settings

import random

import random

def generate_food(snake_pos, game_width, game_height, cell_size):
    snake_set = set(map(tuple, snake_pos))  # Convert snake positions to a set of tuples for quick look-up

    while True:
        food_x = random.randint(0, game_width // cell_size - 1) * cell_size
        food_y = random.randint(0, game_height // cell_size - 1) * cell_size
        food_pos = (food_x, food_y)

        # Check if the food position overlaps with the snake's body using the set
        if food_pos not in snake_set:
            return food_pos



# Initialize food_pos at the start
food_pos = generate_food(snake_pos, game_width, game_height, cell_size)
food_spawn = True

pygame.font.init()
font = pygame.font.SysFont('Arial', 25)

def draw_food(food_pos, scale_factor):
    scaled_food = pygame.transform.scale(food_image, (cell_size * scale_factor, cell_size * scale_factor))
    win.blit(scaled_food, (food_pos[0] * scale_factor, food_pos[1] * scale_factor))

def draw_snake(snake_pos, scale_factor):
    scaled_snake = pygame.transform.scale(snake_image, (cell_size * scale_factor, cell_size * scale_factor))
    for pos in snake_pos:
        win.blit(scaled_snake, (pos[0] * scale_factor, pos[1] * scale_factor))

def game_over(snake_pos, grid):
    head_x, head_y = snake_pos[0]
    directions = [
        (0, -cell_size),   # UP
        (0, cell_size),    # DOWN
        (-cell_size, 0),   # LEFT
        (cell_size, 0)     # RIGHT
    ]
    
    for direction in directions:
        new_x, new_y = head_x + direction[0], head_y + direction[1]
        if 0 <= new_x < len(grid[0]) * cell_size and 0 <= new_y < len(grid) * cell_size:
            if grid[new_y // cell_size][new_x // cell_size] == 0:
                return False  # There's a free neighbor, not game over

    return True  # No free neighbors, game over


def create_grid(snake_pos, food_pos, game_width, game_height, cell_size):
    grid = [[0 for _ in range(game_width // cell_size)] for _ in range(game_height // cell_size)]
    
    # Mark the snake on the grid
    for x, y in snake_pos:
        grid[y // cell_size][x // cell_size] = 1
    
    # Mark the food on the grid if it's defined
    if food_pos:
        fx, fy = food_pos[0] // cell_size, food_pos[1] // cell_size
        grid[fy][fx] = 2
    
    return grid


def dijkstra(grid, start, target):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    width, height = len(grid[0]), len(grid)
    distance = { (i, j): float('inf') for i in range(height) for j in range(width) }
    previous = { (i, j): None for i in range(height) for j in range(width) }
    queue = [(0, start)]
    distance[start] = 0

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_node == target:
            break

        for direction in directions:
            neighbor = (current_node[0] + direction[0], current_node[1] + direction[1])
            if 0 <= neighbor[0] < height and 0 <= neighbor[1] < width:
                if grid[neighbor[0]][neighbor[1]] == 1:
                    continue
                new_distance = current_distance + 1
                if new_distance < distance[neighbor]:
                    distance[neighbor] = new_distance
                    previous[neighbor] = current_node
                    heapq.heappush(queue, (new_distance, neighbor))

    path = []
    node = target
    while node:
        path.append(node)
        node = previous[node]
    path.reverse()
    return path

def get_safe_moves(grid, snake_pos):
    head_x, head_y = snake_pos[0]
    safe_moves = []

    directions = {
        'UP': (head_x, head_y - cell_size),
        'DOWN': (head_x, head_y + cell_size),
        'LEFT': (head_x - cell_size, head_y),
        'RIGHT': (head_x + cell_size, head_y)
    }
    
    for move, (new_x, new_y) in directions.items():
        if 0 <= new_x < len(grid[0]) * cell_size and 0 <= new_y < len(grid) * cell_size:
            if grid[new_y // cell_size][new_x // cell_size] == 0:
                safe_moves.append(move)
    
    return safe_moves
def is_safe_move(grid, snake_pos, move):
    head_x, head_y = snake_pos[0]
    directions = {
        'UP': (head_x, head_y - cell_size),
        'DOWN': (head_x, head_y + cell_size),
        'LEFT': (head_x - cell_size, head_y),
        'RIGHT': (head_x + cell_size, head_y)
    }

    new_head_x, new_head_y = directions[move]

    # Check if the new head position is on the snake's body
    for pos in snake_pos[1:]:  # Exclude the head from the check
        if pos == (new_head_x, new_head_y):
            return False

    return True

def safe_wandering(grid, snake_pos, direction):
    safe_moves = get_safe_moves(grid, snake_pos)
    
    if safe_moves:
        return safe_moves[0]  # Simply take the first safe move
    
    return direction  # If no safe move, keep the current direction
def adaptive_decision(snake_pos, grid, direction):
    safe_moves = get_safe_moves(grid, snake_pos)

    for move in safe_moves:
        if is_safe_move(grid, snake_pos, move):
            return move

    return direction  # If no safe move is found, continue in the current direction

def draw_path(path, scale_factor):
    for cell in path:
        cell_x, cell_y = cell[1] * cell_size, cell[0] * cell_size
        pygame.draw.circle(win, GREEN, (cell_x * scale_factor + cell_size * scale_factor // 2, cell_y * scale_factor + cell_size * scale_factor // 2), cell_size * scale_factor // 4)


def get_next_move(snake_pos, food_pos, game_width, game_height, cell_size):
    grid = create_grid(snake_pos, food_pos, game_width, game_height, cell_size)
    start = (snake_pos[0][1] // cell_size, snake_pos[0][0] // cell_size)
    target = (food_pos[1] // cell_size, food_pos[0] // cell_size)
    path = dijkstra(grid, start, target)
    if not path or len(path) < 2:
        # Backtracking or alternative method here
        return None
    next_cell = path[1]
    head_x, head_y = snake_pos[0]
    next_x, next_y = next_cell[1] * cell_size, next_cell[0] * cell_size
    if next_x > head_x:
        return "RIGHT"
    elif next_x < head_x:
        return "LEFT"
    elif next_y > head_y:
        return "DOWN"
    elif next_y < head_y:
        return "UP"

direction = "RIGHT"
change_to = direction

def change_direction(event, direction):
    if event.key == pygame.K_UP and direction != "DOWN":
        return "UP"
    elif event.key == pygame.K_DOWN and direction != "UP":
        return "DOWN"
    elif event.key == pygame.K_LEFT and direction != "RIGHT":
        return "LEFT"
    elif event.key == pygame.K_RIGHT and direction != "LEFT":
        return "RIGHT"
    return direction

def move_snake(snake_pos, direction):
    head_x, head_y = snake_pos[0]

    # Move snake in the given direction
    if direction == "UP":
        head_y -= cell_size
    elif direction == "DOWN":
        head_y += cell_size
    elif direction == "LEFT":
        head_x -= cell_size
    elif direction == "RIGHT":
        head_x += cell_size

    new_head = [head_x, head_y]

    # Wrap-around logic within game boundaries
    if new_head[0] >= game_width:
        new_head[0] = 0
    elif new_head[0] < 0:
        new_head[0] = game_width - cell_size
    if new_head[1] >= game_height:
        new_head[1] = 0
    elif new_head[1] < 0:
        new_head[1] = game_height - cell_size

    # Check for collision with self (except the new head)
    if new_head in snake_pos[1:]:
        game_over()

    new_snake_pos = [new_head] + snake_pos[:-1]
    return new_snake_pos

def show_score(score, font):
    score_surface = font.render(f'Score: {score}', True, BLACK)
    win.blit(score_surface, (10, 10))  # Position it at the top-left corner

# Initialize score
score = 0

def grow_snake(snake_pos, food_pos):
    global food_spawn, score
    snake_head_x, snake_head_y = snake_pos[0][0], snake_pos[0][1]
    food_x, food_y = food_pos[0], food_pos[1]

    if snake_head_x == food_x and snake_head_y == food_y:
        food_spawn = False
        snake_pos.append(snake_pos[-1])
        score += 1  # Update score
    return snake_pos, food_spawn
def show_menu():
    win.fill(BLACK)
    menu_surface = font.render('Press P to Pause/Resume', True, RED)
    win.blit(menu_surface, (width // 2 - 150, height // 2 - 50))
    pygame.display.update()


def save_game(snake_pos, food_pos, direction, score):
    game_state = {
        'snake_pos': snake_pos,
        'food_pos': food_pos,
        'direction': direction,
        'score': score
    }
    with open('savegame.json', 'w') as save_file:
        json.dump(game_state, save_file)

# Ensure food_pos is correctly defined
if not food_pos:
    food_pos = generate_food(snake_pos, game_width, game_height, cell_size)

# Calculate the path using A* or Dijkstra's Algorithm
path = dijkstra(create_grid(snake_pos, food_pos, game_width, game_height, cell_size), 
                (snake_pos[0][1] // cell_size, snake_pos[0][0] // cell_size), 
                (food_pos[1] // cell_size, food_pos[0] // cell_size))


# Main loop
paused = False
food_pos = generate_food(snake_pos, game_width, game_height, cell_size)  # Initialize food_pos at the start

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
            elif event.key == pygame.K_s:
                save_game(snake_pos, food_pos, direction, score)
            elif event.key == pygame.K_l and not paused:
                snake_pos, food_pos, direction, score = load_game()
            elif event.key == pygame.K_a:
                toggle_autopilot()
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
            elif not autopilot:
                if event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"

    if paused:
        continue

    # Ensure food_pos is initialized and not empty
    if not food_pos:
        food_pos = generate_food(snake_pos, game_width, game_height, cell_size)

    head_x, head_y = snake_pos[0][0] // cell_size, snake_pos[0][1] // cell_size  # Ensure head position
    food_x, food_y = food_pos[0] // cell_size, food_pos[1] // cell_size

    # Calculate the path using Dijkstra's Algorithm
    path = dijkstra(create_grid(snake_pos, food_pos, game_width, game_height, cell_size), 
                    (head_y, head_x), 
                    (food_y, food_x))

    if autopilot:
        if path:
            next_move = get_next_move(snake_pos, food_pos, game_width, game_height, cell_size)
            if next_move and is_safe_move(create_grid(snake_pos, food_pos, game_width, game_height, cell_size), snake_pos, next_move):
                direction = next_move
        else:
            direction = adaptive_decision(snake_pos, create_grid(snake_pos, food_pos, game_width, game_height, cell_size), direction)

    # Move snake
    snake_pos = move_snake(snake_pos, direction)

    # Check if the snake eats the food
    snake_pos, food_spawn = grow_snake(snake_pos, food_pos)
    if not food_spawn:
        food_pos = generate_food(snake_pos, game_width, game_height, cell_size)
        food_spawn = True

    # Check game over condition for autopilot mode
    if autopilot and game_over(snake_pos, create_grid(snake_pos, [], game_width, game_height, cell_size)):
        win.fill(BLACK)
        game_over_surface = font.render('GAME OVER', True, RED)
        win.blit(game_over_surface, (game_width // 2 - 100, game_height // 2 - 50))
        pygame.display.update()
        time.sleep(3)
        pygame.quit()
        sys.exit()

    # Drawing
    win.fill(BLACK)
    pygame.draw.rect(win, WHITE, (0, 0, game_area_width, game_area_height))
    draw_snake(snake_pos, scale_factor)
    draw_food(food_pos, scale_factor)
    show_score(score, font)
    draw_scoreboard()
    draw_options()
    draw_path(path, scale_factor)  # Draw the path in both modes
    pygame.display.update()
    clock.tick(10)
