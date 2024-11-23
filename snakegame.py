import pygame
import sys
import random
import heapq
import json

# Initialize Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Game configuration
config = {
    'game_area': {
        'scale_factor': 1,
        'base_width': 400,
        'base_height': 400,
        'cell_size': 25
    },
    'display': {
        'scoreboard_width': 200,
        'options_width': 200
    },
    'snake': {
        'start_pos': [[100, 50], [75, 50], [50, 50]],
        'speed': 15,
        'images': {
            'head': {
                'up': pygame.image.load("C:/Users/Mohammadi/Downloads/Telegram Desktop/photo_4_2024-11-23_20-53-02.jpg"),
                'down': pygame.image.load("C:/Users/Mohammadi/Downloads/Telegram Desktop/photo_3_2024-11-23_20-53-02.jpg"),
                'left': pygame.image.load("C:/Users/Mohammadi/Downloads/Telegram Desktop/photo_2_2024-11-23_20-53-02.jpg"),
                'right': pygame.image.load("C:/Users/Mohammadi/Downloads/Telegram Desktop/photo_1_2024-11-23_20-53-02.jpg")
            },
            'body': pygame.image.load("C:/Users/Mohammadi/Downloads/Telegram Desktop/photo_4_2024-11-23_20-53-02.jpg")
        }
    },
    'food': {
        'easy': pygame.image.load("C:/Users/Mohammadi/Downloads/Telegram Desktop/photo_4_2024-11-23_20-53-02.jpg"),
        'medium': pygame.image.load("C:/Users/Mohammadi/Downloads/Telegram Desktop/photo_4_2024-11-23_20-53-02.jpg"),
        'hard': pygame.image.load("C:/Users/Mohammadi/Downloads/Telegram Desktop/photo_4_2024-11-23_20-53-02.jpg")
    },
    'game_modes': {
        'autopilot': True,
        'walls': False,
        'blocks': False,
        'poison food': False
    }
}

# Resize images to match the cell size
for key in config['snake']['images']['head']:
    config['snake']['images']['head'][key] = pygame.transform.scale(config['snake']['images']['head'][key], (
        # Enlarge the snake head
        config['game_area']['cell_size'], config['game_area']['cell_size']))
config['snake']['images']['body'] = pygame.transform.scale(
    config['snake']['images']['body'], (config['game_area']['cell_size'], config['game_area']['cell_size']))
for key in config['food']:
    config['food'][key] = pygame.transform.scale(
        config['food'][key], (config['game_area']['cell_size'], config['game_area']['cell_size']))


# Set up display with additional space for scores and options
game_area_width = config['game_area']['base_width'] * \
    config['game_area']['scale_factor']
game_area_height = config['game_area']['base_height'] * \
    config['game_area']['scale_factor']
scoreboard_width = config['display']['scoreboard_width']
options_width = config['display']['options_width']
width = game_area_width + scoreboard_width + options_width
height = game_area_height
cell_size = config['game_area']['cell_size']

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Smart Snake")
clock = pygame.time.Clock()


# Snake settings
snake_pos = config['snake']['start_pos']

# Initialize scores
score = 0
scores = []

# Autopilot mode
autopilot = config['game_modes']['autopilot']

# Sample Scores
players_scores = [("Player 1", 10), ("Player 2", 15),
                  ("Player 3", 8)]  # Sample data

# Font setup
font = pygame.font.Font(None, 36)

# Define the directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Initialize the food position
food_pos = [random.randrange(1, game_area_width // cell_size) * cell_size,
            random.randrange(1, game_area_height // cell_size) * cell_size]

# Define the directions for Dijkstra's algorithm
directions = [UP, DOWN, LEFT, RIGHT]

# Function to draw text


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

# Function to display the main menu


def main_menu():
    menu = True
    while menu:
        win.fill(BLACK)
        draw_text('SMART SNAKE', font, WHITE, win, width // 2, height // 4)
        draw_text('1. New Game', font, WHITE, win,
                  width // 2, height // 2 - 40)
        draw_text('2. Load Game', font, WHITE, win, width // 2, height // 2)
        draw_text('3. Quit', font, WHITE, win, width // 2, height // 2 + 40)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    mode_menu()
                    menu = False
                if event.key == pygame.K_2:
                    load_game()
                    game_loop()
                    menu = False
                if event.key == pygame.K_3:
                    pygame.quit()
                    sys.exit()

# Function to display the mode selection menu


def mode_menu():
    selecting_mode = True
    while selecting_mode:
        win.fill(BLACK)
        draw_text('SELECT MODE', font, WHITE, win, width // 2, height // 4)
        draw_text('1. Slow', font, WHITE, win, width // 2, height // 2 - 40)
        draw_text('2. Mid', font, WHITE, win, width // 2, height // 2)
        draw_text('3. Fast', font, WHITE, win, width // 2, height // 2 + 40)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    config['snake']['speed'] = 10
                    selecting_mode = False
                if event.key == pygame.K_2:
                    config['snake']['speed'] = 15
                    selecting_mode = False
                if event.key == pygame.K_3:
                    config['snake']['speed'] = 20
                    selecting_mode = False

    game_loop()

# Function to draw scoreboard


def draw_scoreboard():
    pygame.draw.rect(win, BLACK, (game_area_width,
                     0, scoreboard_width, height))
    score_title = font.render('Scoreboard', True, WHITE)
    win.blit(score_title, (game_area_width + 10, 10))
    y_offset = 40
    for player, score in players_scores:
        score_text = font.render(f"{player}: {score}", True, WHITE)
        win.blit(score_text, (game_area_width + 10, y_offset))
        y_offset += 30

# Function to draw key options


def draw_options():
    pygame.draw.rect(win, BLACK, (game_area_width +
                     scoreboard_width, 0, options_width, height))
    options_title = font.render('Options', True, WHITE)
    win.blit(options_title, (game_area_width + scoreboard_width + 10, 10))
    options_texts = [
        "P: Pause/Resume",
        "S: Save Game",
        "A: Toggle Autopilot",
        "M: Main Menu",  # Added option for Main Menu
        "Q: Quit"
    ]
    y_offset = 40
    for text in options_texts:
        option_text = font.render(text, True, WHITE)
        win.blit(option_text, (game_area_width +
                 scoreboard_width + 10, y_offset))
        y_offset += 30


def loading_screen():
    loading = True
    bar_y = height // 2  # Position the bar in the middle of the screen
    # Start the snake off the screen to the left
    load_snake_pos = [[-cell_size, bar_y]]
    load_direction = RIGHT
    load_text = "Smart Snake"
    text_progress = [" "] * len(load_text)  # Initialize the text as spaces
    total_text_length = len(load_text) * cell_size
    # Calculate starting x position to center the text
    start_x = (width - total_text_length) // 2

    while loading and " " in text_progress:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        next_pos = [load_snake_pos[0][0] + load_direction[0]
                    * cell_size, load_snake_pos[0][1]]

        # Update the grid and text as the tail of the snake passes
        if start_x <= load_snake_pos[-1][0] < start_x + total_text_length:
            text_progress[(load_snake_pos[-1][0] - start_x) //
                          cell_size] = load_text[(load_snake_pos[-1][0] - start_x) // cell_size]

        load_snake_pos.insert(0, list(next_pos))
        load_snake_pos.pop()

        win.fill(BLACK)
        for pos in load_snake_pos:
            win.blit(config['snake']['images']['head']['up'],
                     (pos[0], pos[1]))  # Draw the enlarged head

        # Draw the grid and text
        for i, letter in enumerate(text_progress):
            letter_surface = font.render(letter, True, WHITE)
            win.blit(letter_surface, (start_x + i *
                     cell_size + cell_size // 4, bar_y))

        pygame.display.update()
        clock.tick(10)

        if next_pos[0] >= start_x + total_text_length:
            loading = False

    # Final pause to allow the full title to be visible
    pygame.time.delay(1500)


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

# Function to check for collisions


def check_collision(snake_pos, next_pos):
    if next_pos in snake_pos:
        return True
    return False

# Enhanced Dijkstra's algorithm to avoid the snake's body


def dijkstra(snake_pos, food_pos, game_width, game_height, cell_size):
    queue = [(0, snake_pos[0])]
    visited = set()
    came_from = {tuple(snake_pos[0]): None}
    snake_set = set(map(tuple, snake_pos))

    while queue:
        current_cost, current_node = heapq.heappop(queue)
        visited.add(tuple(current_node))

        if current_node == food_pos:
            break

        for direction in directions:
            neighbor = [current_node[0] + direction[0] * cell_size,
                        current_node[1] + direction[1] * cell_size]
            neighbor[0] = (neighbor[0] + game_width) % game_width
            neighbor[1] = (neighbor[1] + game_height) % game_height

            if tuple(neighbor) not in visited and tuple(neighbor) not in snake_set:
                heapq.heappush(queue, (current_cost + 1, neighbor))
                visited.add(tuple(neighbor))
                came_from[tuple(neighbor)] = current_node

    path = []
    step = food_pos
    while step:
        path.append(step)
        step = came_from.get(tuple(step))

    return path[::-1]


# Function to wander safely if no path found
def wander(snake_pos, game_width, game_height, cell_size):
    possible_moves = [UP, DOWN, LEFT, RIGHT]
    random.shuffle(possible_moves)
    for move in possible_moves:
        next_pos = [snake_pos[0][0] + move[0] * cell_size,
                    snake_pos[0][1] + move[1] * cell_size]
        next_pos[0] = (next_pos[0] + game_width) % game_width
        next_pos[1] = (next_pos[1] + game_height) % game_height

        if next_pos not in snake_pos:
            return next_pos
    return snake_pos[0]

# Function to generate a new food position that is not inside the snake's body


def generate_food_position(snake_pos, game_width, game_height, cell_size):
    while True:
        food_pos = [random.randrange(1, game_width // cell_size) * cell_size,
                    random.randrange(1, game_height // cell_size) * cell_size]
        if food_pos not in snake_pos:
            return food_pos

# Main game loop with pause functionality, optimized collision logic, and wrap-around for both autopilot and manual modes


def game_loop():
    global snake_pos, food_pos, direction, score, autopilot

    running = True
    paused = False
    direction = RIGHT
    autopilot = config['game_modes']['autopilot']

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_s:
                    save_game(snake_pos, food_pos, direction, score)
                elif event.key == pygame.K_l:
                    snake_pos, food_pos, direction, score = load_game()
                elif event.key == pygame.K_a:
                    toggle_autopilot()
                elif event.key == pygame.K_m:
                    main_menu()  # Return to main menu
                    return

        if not paused:
            if autopilot:
                path = dijkstra(snake_pos, food_pos, config['game_area']['base_width'],
                                config['game_area']['base_height'], config['game_area']['cell_size'])
                if path and len(path) > 1:
                    next_pos = path[1]
                    if next_pos[0] > snake_pos[0][0]:
                        direction = RIGHT
                    elif next_pos[0] < snake_pos[0][0]:
                        direction = LEFT
                    elif next_pos[1] > snake_pos[0][1]:
                        direction = DOWN
                    elif next_pos[1] < snake_pos[0][1]:
                        direction = UP
                else:
                    next_pos = wander(snake_pos, config['game_area']['base_width'],
                                      config['game_area']['base_height'], config['game_area']['cell_size'])
            else:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP] and direction != DOWN:
                    direction = UP
                elif keys[pygame.K_DOWN] and direction != UP:
                    direction = DOWN
                elif keys[pygame.K_LEFT] and direction != RIGHT:
                    direction = LEFT
                elif keys[pygame.K_RIGHT] and direction != LEFT:
                    direction = RIGHT
                next_pos = [snake_pos[0][0] + direction[0] * config['game_area']['cell_size'],
                            snake_pos[0][1] + direction[1] * config['game_area']['cell_size']]

            # Wrap around logic for both autopilot and manual modes
            next_pos[0] = (next_pos[0] + config['game_area']
                           ['base_width']) % config['game_area']['base_width']
            next_pos[1] = (next_pos[1] + config['game_area']
                           ['base_height']) % config['game_area']['base_height']

            if next_pos == food_pos:
                score += 10
                snake_pos.insert(0, list(next_pos))
                food_pos = generate_food_position(
                    snake_pos, config['game_area']['base_width'], config['game_area']['base_height'], config['game_area']['cell_size'])
            else:
                if check_collision(snake_pos, next_pos):
                    running = False
                    print(f"Game Over! Your score: {score}")
                else:
                    snake_pos.insert(0, list(next_pos))
                    snake_pos.pop()

        # Clear the screen before drawing

        win.fill(BLACK)
        for pos in snake_pos:
            if pos == snake_pos[0]:
                head_img = config['snake']['images']['head'][{
                    UP: 'up', DOWN: 'down', LEFT: 'left', RIGHT: 'right'}[direction]]
                win.blit(head_img, (pos[0], pos[1]))
            else:
                win.blit(config['snake']['images']['body'],
                         (pos[0], pos[1]))  # Draw the body

        win.blit(config['food']['easy'], (food_pos[0], food_pos[1]))
        show_score(score, font)
        draw_scoreboard()
        draw_options()

        pygame.display.update()
        clock.tick(config['snake']['speed'])


# Update the main function to call the loading screen
def main():
    loading_screen()
    main_menu()


# Start the game by calling the main function
if __name__ == "__main__":
    main()
