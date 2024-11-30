import pygame
import sys
import random
import heapq
import json
import copy
# Initialize Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (64, 64, 64)
BLUE = (0, 0, 255)
# Game configuration
config = {
    'game_area': {
        'scale_factor': 1,
        'base_width': 400,
        'base_height': 400,
        'cell_size': 25
    },
    'display': {
        'scoreboard_width': 300,
        'options_width': 200
    },
    'snake': {
        'start_pos': [[100, 50], [75, 50], [50, 50]],
        'speed': 15,
        'images': {
            'head': {
                'up': pygame.image.load("pics/snake-head-up.png"),
                'down': pygame.image.load("pics/snake-head-down.png"),
                'left': pygame.image.load("pics/snake-head-left.png"),
                'right': pygame.image.load("pics/snake-head-right.png")
            },
            'body': pygame.image.load("pics/body.png")
        }
    },
    'food': {
        'easy': pygame.image.load("pics/apple.png"),
        'medium': pygame.image.load("pics/apple.png"),
        'hard': pygame.image.load("pics/apple.png"),
        'blocks': pygame.image.load('pics/block.png'),
    },

    'game_modes': {
        'autopilot': True,
        'walls': True,
        'blocks': True,
        'poison food': False,
        'food count': 3
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

# Font setup
font = pygame.font.SysFont('Lobster', 30)

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


class Game:
    def __init__(self, username):
        self.username = username
        self.score = 0
        self.high_score = 0
        self.snake = Snake()
        self.food = Food()
        self.blocks = []
        self.autopilot = config['game_modes']['autopilot']
        self.walls = config['game_modes']['walls']
        self.poison_food = config['game_modes']['poison food']
        self.food_count = config['game_modes']['food count']
        self.board_size = config['game_area']['base_width']
        self.blocks_on = config['game_modes']['blocks']
        self.draw_path = False
        self.speed = config['snake']['speed']
        self.load_high_score()

    def reset(self):
        self.score = 0
        self.snake = Snake()
        self.food = Food()
        self.blocks = []

    def load_high_score(self):
        try:
            with open('users.json', 'r') as user_file:
                users = json.load(user_file)
            if self.username in users:
                self.high_score = users[self.username].get('high_score', 0)
        except FileNotFoundError:
            self.high_score = 0

    def save_high_score(self):
        # Save the high score for the user in users.json
        try:
            with open('users.json', 'r') as user_file:
                users = json.load(user_file)
        except FileNotFoundError:
            users = {}

        if self.username not in users or self.score > users[self.username]['high_score']:
            users[self.username] = {'high_score': self.score}

        with open('users.json', 'w') as user_file:
            json.dump(users, user_file)

    def drawing_path(self, path):
        if path:
            for (x, y) in path:
                # Calculate the center of the cell for each grid coordinate (x, y)
                pixel_x = x + config['game_area']['cell_size'] // 2
                pixel_y = y + config['game_area']['cell_size'] // 2
                # Draw a circle at each calculated position
                pygame.draw.circle(win, GREEN, (pixel_x, pixel_y), 5)

    def setup_options(self):
        running = True

        while running:
            win.fill(BLACK)
            font = pygame.font.SysFont('Lobster', 30)

            # Title
            title = font.render("Game Options", True, WHITE)
            win.blit(title, (150, 50))

            # Options
            options = [
                f"Food Count: {self.food_count} (LEFT/RIGHT to adjust)",
                f"Autopilot: {
                    'ON' if self.autopilot else 'OFF'} (A to toggle)",
                f"Walls: {'ON' if self.walls else 'OFF'} (W to toggle)",
                f"Blocks: {'ON' if self.blocks_on else 'OFF'} (B to toggle)",
            ]

            for i, option in enumerate(options):
                text = font.render(option, True, WHITE)
                win.blit(text, (50, 150 + i * 50))

            # Instructions
            instructions = font.render("Press ENTER to Start", True, WHITE)
            win.blit(instructions, (100, 450))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        running = False
                    elif event.key == pygame.K_RIGHT and self.food_count < 3:
                        self.food_count += 1
                    elif event.key == pygame.K_LEFT and self.food_count > 1:
                        self.food_count -= 1
                    elif event.key == pygame.K_a:
                        self.autopilot = not self.autopilot
                    elif event.key == pygame.K_w:
                        self.walls = not self.walls
                    elif event.key == pygame.K_b:
                        self.blocks_on = not self.blocks_on
        config['game_modes']['food count'] = self.food_count
        config['game_modes']['walls'] = self.walls

    def draw_scoreboard(self):
        pygame.draw.rect(
            win, BLACK, (config['game_area']['base_width'], 0, config['display']['scoreboard_width'], height))

        # Load the users' scores
        try:
            with open('users.json', 'r') as user_file:
                users = json.load(user_file)
        except FileNotFoundError:
            users = {}

        # Get top 3 scores (including the current user)
        top_scores = sorted(
            [(username, user_data['high_score'])
             for username, user_data in users.items()],
            key=lambda x: x[1], reverse=True
        )[:3]  # Take top 3

        # Render scoreboard information
        font = pygame.font.SysFont('Lobster', 25)

        # Title
        score_title = font.render('Scoreboard', True, WHITE)
        win.blit(score_title, (config['game_area']['base_width'] + 10, 10))

        # Current score and user's high score
        current_score_text = font.render(f"Score: {self.score}", True, WHITE)
        win.blit(current_score_text,
                 (config['game_area']['base_width'] + 10, 40))

        high_score_text = font.render(f"High Score {self.username}: {
                                      self.high_score}", True, WHITE)
        win.blit(high_score_text, (config['game_area']['base_width'] + 10, 70))

        # Display top 3 players
        y_offset = 110  # Starting point for top scores
        for i, (player, score) in enumerate(top_scores):
            player_score_text = font.render(
                f"{i+1}. {player}: {score}", True, WHITE)
            win.blit(player_score_text,
                     (config['game_area']['base_width'] + 10, y_offset + i * 20))

        # Update the display
        pygame.display.update()

    def draw_in_game_options(self):
        pygame.draw.rect(win, BLACK, (config['game_area']['base_width'], height//2,
                         config['display']['scoreboard_width'], config['game_area']['base_height']))

        font = pygame.font.SysFont('Lobster', 25)
        options = [
            f"Autopilot: {'ON' if self.autopilot else 'OFF'} (A to toggle)",
            f"Walls: {'ON' if self.walls else 'OFF'} (W to toggle)",
            f"Blocks: {'ON' if self.blocks_on else 'OFF'} (B to toggle)",
            f"Food Count: {self.food_count}",
            f"draw path: {'on' if self.draw_path else 'off'} (D to toggle)",
            f"speed: {'FAST' if self.speed == 20 else ''}{'MID' if self.speed == 15 else ''}{
                'SLOW' if self.speed == 10 else ''}(S to change)"
        ]

        for i, option in enumerate(options):
            text = font.render(option, True, WHITE)
            win.blit(text, (config['game_area']
                     ['base_width'] + 10, height//2 + (i+1) * 25))

    def run(self):
        self.reset()
        self.setup_options()
        running = True
        paused = False
        loading_screen()
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
                    elif event.key == pygame.K_a:
                        self.autopilot = not self.autopilot
                    elif event.key == pygame.K_w:
                        self.walls = not self.walls
                    elif event.key == pygame.K_b:
                        self.blocks_on = not self.blocks_on
                    elif event.key == pygame.K_d:
                        self.draw_path = not self.draw_path
                    elif event.key == pygame.K_s and self.speed < 20:
                        self.speed += 5
                    elif event.key == pygame.K_s and self.speed == 20:
                        self.speed -= 10
                    elif event.key == pygame.K_m:
                        self.save_high_score()
                        main_menu()
                        return
            config['snake']['speed'] = self.speed

            if not paused:
                self.snake.move(
                    self.autopilot, self.food.position, self.blocks)
                if self.snake.check_collision(self.walls, self.blocks):
                    pygame.time.delay(2000)
                    running = False
                    self.save_high_score()
                    self.show_game_over_screen()

                if self.snake.snake_pos[0] in self.food.position:
                    if config['game_modes']['blocks'] and random.random() < 0.25:
                        self.blocks.append(Food.generate_blocks(snake_pos))
                        if len(self.blocks) > (config['game_area']['base_width']*config['game_area']['base_height'])//20:
                            self.blocks.pop(0)
                    self.food.position.remove(self.snake.snake_pos[0])
                    self.food.generate_food_position(
                        self.snake.snake_pos, self.blocks, config['game_area']['base_width'], config['game_area']['base_height'], cell_size)
                    self.score += 10
                    if self.score > self.high_score:
                        self.high_score = self.score
                else:
                    self.snake.snake_pos.pop()

            win.fill(BLACK)
            if self.draw_path:
                path = Navigate.dijkstra(self.snake.snake_pos, self.food.position, self.blocks,
                                         config['game_area']['base_width'], config['game_area']['base_height'], config['game_area']['cell_size'])
                self.drawing_path(path)
            for block in self.blocks:
                win.blit(config['food']['blocks'], (block[0], block[1]))
            self.snake.draw(win)
            self.food.draw(win)
            self.draw_scoreboard()
            self.draw_in_game_options()

            pygame.display.update()
            clock.tick(config['snake']['speed'])

    def show_game_over_screen(self):
        win.fill(BLACK)
        game_over_text = font.render('GAME OVER', True, WHITE)
        win.blit(game_over_text, (width // 2 - 100, height // 2 - 40))
        score_text = font.render(f'Your Score: {self.score}', True, WHITE)
        win.blit(score_text, (width // 2 - 100, height // 2))
        draw_text('Press any key to return to menu', font,
                  WHITE, win, width // 2, height // 2 + 40)
        pygame.display.update()

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    waiting_for_input = False
                    game_options(self.username)


class Snake:
    def __init__(self):
        self.snake_pos = copy.deepcopy(config['snake']['start_pos'])
        self.direction = RIGHT

    def move(self, autopilot, food_pos, blocks):
        if autopilot:
            path = Navigate.dijkstra(self.snake_pos, food_pos, blocks,
                                     config['game_area']['base_width'], config['game_area']['base_height'], config['game_area']['cell_size'])
            if path and len(path) > 1:
                next_pos = path[1]
                if next_pos[0] > self.snake_pos[0][0]:
                    self.direction = RIGHT
                elif next_pos[0] < self.snake_pos[0][0]:
                    self.direction = LEFT
                elif next_pos[1] > self.snake_pos[0][1]:
                    self.direction = DOWN
                elif next_pos[1] < self.snake_pos[0][1]:
                    self.direction = UP
            else:
                next_pos = Navigate.wander(
                    self.snake_pos, config['game_area']['base_width'], config['game_area']['base_height'], config['game_area']['cell_size'])
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and self.direction != DOWN:
                self.direction = UP
            elif keys[pygame.K_DOWN] and self.direction != UP:
                self.direction = DOWN
            elif keys[pygame.K_LEFT] and self.direction != RIGHT:
                self.direction = LEFT
            elif keys[pygame.K_RIGHT] and self.direction != LEFT:
                self.direction = RIGHT
            next_pos = [self.snake_pos[0][0] + self.direction[0] * config['game_area']['cell_size'],
                        self.snake_pos[0][1] + self.direction[1] * config['game_area']['cell_size']]
        if not config['game_modes']['walls']:
            next_pos[0] = (next_pos[0] + config['game_area']
                           ['base_width']) % config['game_area']['base_width']
            next_pos[1] = (next_pos[1] + config['game_area']
                           ['base_height']) % config['game_area']['base_height']

        self.snake_pos.insert(0, list(next_pos))

    def check_collision(self, walls, blocks):
        if self.snake_pos[0] in self.snake_pos[1:]:
            return True
        if walls:
            if self.snake_pos[0][0] < 0 or self.snake_pos[0][0] >= config['game_area']['base_width']:
                return True
            if self.snake_pos[0][1] < 0 or self.snake_pos[0][1] >= config['game_area']['base_height']:
                return True
        for block in blocks:
            if self.snake_pos[0] == block:
                return True
        return False

    def draw(self, surface):
        for i, pos in enumerate(self.snake_pos):
            if i == 0:
                head_img = config['snake']['images']['head'][{
                    UP: 'up',
                    DOWN: 'down',
                    LEFT: 'left',
                    RIGHT: 'right'
                }[self.direction]]
                surface.blit(head_img, (pos[0], pos[1]))
            else:
                surface.blit(config['snake']['images']
                             ['body'], (pos[0], pos[1]))


class Food:
    position = []

    def __init__(self):
        self.generate_food_position([], [], config['game_area']['base_width'],
                                    config['game_area']['base_height'], config['game_area']['cell_size'])

    def draw(self, surface):
        for pos in self.position:
            # Change as needed for mode
            surface.blit(config['food']['easy'], (pos[0], pos[1]))

    def generate_food_position(self, snake_pos, blocks, game_width, game_height, cell_size):
        while len(self.position) < config['game_modes']['food count']:
            food_pos = [random.randrange(1, game_width // cell_size) * cell_size,
                        random.randrange(1, game_height // cell_size) * cell_size]
            if not (food_pos in snake_pos+blocks+self.position or len([1 for direction in directions if [food_pos[0] + direction[0] * cell_size, food_pos[1] + direction[1] * cell_size] not in blocks]) < 2):
                self.position.append(food_pos)

    @staticmethod
    def generate_blocks(snake_pos):
        block_pos = [random.randrange(1, config['game_area']['base_width'] // config['game_area']['cell_size']) * config['game_area']['cell_size'],
                     random.randrange(1, config['game_area']['base_height'] // config['game_area']['cell_size']) * config['game_area']['cell_size']]
        while block_pos in snake_pos:
            block_pos = [random.randrange(1, config['game_area']['base_width'] // config['game_area']['cell_size']) * config['game_area']['cell_size'],
                         random.randrange(1, config['game_area']['base_height'] // config['game_area']['cell_size']) * config['game_area']['cell_size']]
        return block_pos


class Navigate:
    @staticmethod
    def dijkstra(snake_pos, food_positions, blocks, game_width, game_height, cell_size):

        queue = [(0, snake_pos[0])]
        visited = set()
        came_from = {tuple(snake_pos[0]): None}
        snake_set = set(map(tuple, snake_pos))
        current_node = 0
        while queue:
            current_cost, current_node = heapq.heappop(queue)
            visited.add(tuple(current_node))

            if current_node in food_positions:
                break

            for direction in directions:
                neighbor = [current_node[0] + direction[0] * cell_size,
                            current_node[1] + direction[1] * cell_size]
                if not config['game_modes']['walls']:
                    neighbor[0] = (neighbor[0] + game_width) % game_width
                    neighbor[1] = (neighbor[1] + game_height) % game_height
                if tuple(neighbor) not in visited and tuple(neighbor) not in snake_set:
                    if (0 <= neighbor[0] < game_width and 0 <= neighbor[1] < game_height) and not neighbor in blocks:
                        heapq.heappush(queue, (current_cost + 1, neighbor))
                        visited.add(tuple(neighbor))
                        came_from[tuple(neighbor)] = current_node

        path = []
        step = current_node
        while step:
            path.append(step)
            step = came_from.get(tuple(step))
        return path[::-1]

    @staticmethod
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
# Integrate main menu and game loop with new classes


def login():
    login_active = True
    username = ""

    while login_active:
        win.fill(BLACK)
        draw_text('LOGIN', font, WHITE, win, width // 2, height // 4)
        draw_text(f'Username: {username}', font,
                  WHITE, win, width // 2, height // 2)
        draw_text('Press Enter to submit', font, WHITE,
                  win, width // 2, height // 2 + 40)
        draw_text('Press Alt+M to return to menu', font,
                  WHITE, win, width // 2, height // 2 + 80)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if check_credentials(username):
                        game_options(username)
                        login_active = False
                    else:
                        draw_text("User not found. Please sign up.",
                                  font, RED, win, width // 2, height // 2 + 120)
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif event.key == pygame.K_m and pygame.key.get_mods() & pygame.KMOD_ALT:
                    main_menu()
                    login_active = False
                else:
                    username += event.unicode


def sign_up():
    sign_up_active = True
    username = ""

    while sign_up_active:
        win.fill(BLACK)
        draw_text('SIGN UP', font, WHITE, win, width // 2, height // 4)
        draw_text(f'Username: {username}', font,
                  WHITE, win, width // 2, height // 2)
        draw_text('Press Enter to submit', font, WHITE,
                  win, width // 2, height // 2 + 40)
        draw_text('Press Alt+M to return to menu', font,
                  WHITE, win, width // 2, height // 2 + 80)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if register_user(username):
                        game_options(username)
                        sign_up_active = False
                    else:
                        draw_text("Username already exists.", font,
                                  RED, win, width // 2, height // 2 + 120)
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif event.key == pygame.K_m and pygame.key.get_mods() & pygame.KMOD_ALT:
                    main_menu()
                    sign_up_active = False
                else:
                    username += event.unicode


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


def check_credentials(username):
    try:
        with open('users.json', 'r') as user_file:
            users = json.load(user_file)
        return username in users
    except FileNotFoundError:
        return False


def register_user(username):
    try:
        with open('users.json', 'r') as user_file:
            users = json.load(user_file)
    except FileNotFoundError:
        users = {}

    if username not in users:
        users[username] = {"high_score": 0}
        with open('users.json', 'w') as user_file:
            json.dump(users, user_file)
        return True
    return False


def game_options(username):
    options_active = True
    while options_active:
        win.fill(BLACK)
        draw_text('GAME OPTIONS', font, WHITE, win, width // 2, height // 4)
        draw_text(f'Welcome, {username}', font, WHITE,
                  win, width // 2, height // 2 - 60)
        draw_text('1. New Game', font, WHITE, win,
                  width // 2, height // 2 - 20)
        draw_text('2. Load Game', font, WHITE, win,
                  width // 2, height // 2 + 20)
        draw_text('3. View High Scores', font, WHITE,
                  win, width // 2, height // 2 + 60)
        draw_text('4. Back to Main Menu', font, WHITE,
                  win, width // 2, height // 2 + 100)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game = Game(username)
                    game.run()
                    options_active = False
                if event.key == pygame.K_2:
                    game = Game(username)
                    game.run()
                    options_active = False
                if event.key == pygame.K_3:
                    view_and_save_high_score(username)
                if event.key == pygame.K_4:
                    main_menu()
                    options_active = False


def view_and_save_high_score(username, score=None):
    # View High Scores
    win.fill(BLACK)
    draw_text('HIGH SCORES', font, WHITE, win, width // 2, height // 4)

    try:
        with open('users.json', 'r') as user_file:
            users = json.load(user_file)
    except FileNotFoundError:
        users = {}

    if username in users:
        high_score_text = f"High Score for {
            username}: {users[username]['high_score']}"
    else:
        high_score_text = "No high score available for this user."

    draw_text(high_score_text, font, WHITE, win, width // 2, height // 2)

    if score is not None:  # If score is provided, save it as the new high score.
        # Save High Score (if score is higher than the current one)
        if username in users:
            current_high_score = users[username]["high_score"]
            if score > current_high_score:
                users[username]["high_score"] = score
                with open('users.json', 'w') as user_file:
                    json.dump(users, user_file)
                draw_text(f"New high score: {
                          score}", font, GREEN, win, width // 2, height // 2 + 40)
        else:
            users[username] = {"high_score": score}
            with open('users.json', 'w') as user_file:
                json.dump(users, user_file)
            draw_text(f"New high score: {score}", font,
                      GREEN, win, width // 2, height // 2 + 40)

    draw_text('Press any key to return', font, WHITE,
              win, width // 2, height // 2 + 80)
    draw_text('Press Alt+M to return to menu', font,
              WHITE, win, width // 2, height // 2 + 120)
    pygame.display.update()

    high_scores_active = True
    while high_scores_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m and pygame.key.get_mods() & pygame.KMOD_ALT:
                    high_scores_active = False
                    main_menu()
                else:
                    high_scores_active = False
                    game_options(username)


def main_menu():
    menu = True
    while menu:
        win.fill(BLACK)
        draw_text('SMART SNAKE', font, WHITE, win, width // 2, height // 4)
        draw_text('1. Login', font, WHITE, win, width // 2, height // 2 - 60)
        draw_text('2. Sign Up', font, WHITE, win, width // 2, height // 2 - 20)
        draw_text('3. Play as Guest', font, WHITE,
                  win, width // 2, height // 2 + 20)
        draw_text('4. Quit', font, WHITE, win, width // 2, height // 2 + 60)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    login()
                if event.key == pygame.K_2:
                    sign_up()
                if event.key == pygame.K_3:
                    username = "Guest"
                    game_options(username)
                if event.key == pygame.K_4:
                    pygame.quit()
                    sys.exit()


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)


# Start the game by calling the main function
if __name__ == "pygamesnake":
    pygame.init()
    width, height = config['game_area']['base_width'] + \
        config['display']['scoreboard_width'], config['game_area']['base_height']
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Smart Snake")
    font = pygame.font.SysFont('Lobster', 30)
    clock = pygame.time.Clock()

    main_menu()
