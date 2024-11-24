
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
            'body': pygame.image.load("pics/1F7E9_color.png")
        }
    },
    'food': {
        'easy': pygame.image.load("pics/1F34F_color.png"),
        'medium': pygame.image.load("pics/1F34F_color.png"),
        'hard': pygame.image.load("pics/1F34F_color.png")
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


def draw_options():
    pygame.draw.rect(
        win, BLACK, (0, config['game_area']['base_height'], width, config['display']['options_width']))
    options_title = font.render('Options', True, WHITE)
    win.blit(options_title, (10, config['game_area']['base_height'] + 10))

    # Add more options as needed
    option1 = font.render('P: Pause/Resume', True, WHITE)
    win.blit(option1, (10, config['game_area']['base_height'] + 50))

    option2 = font.render('Q: Quit', True, WHITE)
    win.blit(option2, (10, config['game_area']['base_height'] + 90))

    option3 = font.render('S: Save Game', True, WHITE)
    win.blit(option3, (10, config['game_area']['base_height'] + 130))

    option4 = font.render('L: Load Game', True, WHITE)
    win.blit(option4, (10, config['game_area']['base_height'] + 170))

    option5 = font.render('A: Toggle Autopilot', True, WHITE)
    win.blit(option5, (10, config['game_area']['base_height'] + 210))

    option6 = font.render('M: Main Menu', True, WHITE)
    win.blit(option6, (10, config['game_area']['base_height'] + 250))


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
        self.load_game()

    def load_game(self):
        snake_pos, food_pos, direction, score, high_score = self.load_game_from_file(
            self.username)
        if snake_pos:
            self.snake.snake_pos = snake_pos
            self.food.position = food_pos
            self.snake.direction = direction
            self.score = score
            self.high_score = high_score

    def save_game(self):
        self.save_game_to_file(self.snake.snake_pos, self.food.position,
                               self.snake.direction, self.score, self.username)

    def load_game_from_file(self, username):
        try:
            with open('savegame.json', 'r') as save_file:
                data = json.load(save_file)
            if username in data:
                return data[username]['snake_pos'], data[username]['food_pos'], data[username]['direction'], data[username]['score'], data[username]['high_score']
            else:
                return None, None, None, 0, 0
        except FileNotFoundError:
            return None, None, None, 0, 0

    def save_game_to_file(self, snake_pos, food_pos, direction, score, username):
        try:
            with open('savegame.json', 'r') as save_file:
                data = json.load(save_file)
        except FileNotFoundError:
            data = {}

        if username not in data or score > data[username]['high_score']:
            data[username] = {'snake_pos': snake_pos, 'food_pos': food_pos,
                              'direction': direction, 'score': score, 'high_score': score}
        else:
            data[username].update(
                {'snake_pos': snake_pos, 'food_pos': food_pos, 'direction': direction, 'score': score})

        with open('savegame.json', 'w') as save_file:
            json.dump(data, save_file)

    def draw_scoreboard(self):
        pygame.draw.rect(
            win, BLACK, (config['game_area']['base_width'], 0, config['display']['scoreboard_width'], height))
        score_title = font.render('Scoreboard', True, WHITE)
        win.blit(score_title, (config['game_area']['base_width'] + 10, 10))
        current_score_text = font.render(f"Score: {self.score}", True, WHITE)
        win.blit(current_score_text,
                 (config['game_area']['base_width'] + 10, 50))
        high_score_text = font.render(f"High Score {self.username}: {
                                      self.high_score}", True, WHITE)
        win.blit(high_score_text, (config['game_area']['base_width'] + 10, 90))

    def run(self):
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
                    elif event.key == pygame.K_s:
                        self.save_game()
                    elif event.key == pygame.K_l:
                        self.load_game()
                    elif event.key == pygame.K_a:
                        self.autopilot = not self.autopilot
                    elif event.key == pygame.K_m:
                        main_menu()
                        return

            if not paused:
                self.snake.move(self.autopilot, self.food.position)
                if self.snake.check_collision(self.walls, self.blocks):
                    running = False
                    print(f"Game Over! Your score: {self.score}")

                if self.snake.snake_pos[0] == self.food.position:
                    self.food.position = self.food.handle_collision(
                        self.snake.snake_pos, self.blocks)
                    self.score += 1
                    if self.score > self.high_score:
                        self.high_score = self.score
                else:
                    self.snake.snake_pos.pop()

            win.fill(BLACK)
            self.snake.draw(win)
            self.food.draw(win)
            self.draw_scoreboard()
            draw_options()

            pygame.display.update()
            clock.tick(config['snake']['speed'])


class Snake:
    def __init__(self):
        self.snake_pos = config['snake']['start_pos']
        self.direction = RIGHT

    def move(self, autopilot, food_pos):
        if autopilot:
            path = Navigate.dijkstra(
                self.snake_pos, food_pos, config['game_area']['base_width'], config['game_area']['base_height'], config['game_area']['cell_size'])
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
    def __init__(self):
        self.position = self.generate_food_position(
            [], config['game_area']['base_width'], config['game_area']['base_height'], config['game_area']['cell_size'])

    def handle_collision(self, snake_pos, blocks):
        global score
        if self.position == self.generate_poison_food_position(snake_pos, config['game_area']['base_width'], config['game_area']['base_height'], config['game_area']['cell_size']):
            score -= 1  # Decrease score for poison food
        else:
            score += 1  # Increase score for normal food
            if config['game_modes']['blocks']:
                block = self.generate_blocks(snake_pos)
                if block:
                    blocks.append(block)
            if config['game_modes']['poison food']:
                self.position = self.generate_poison_food_position(
                    snake_pos, config['game_area']['base_width'], config['game_area']['base_height'], config['game_area']['cell_size'])
            else:
                self.position = self.generate_food_position(
                    snake_pos, config['game_area']['base_width'], config['game_area']['base_height'], config['game_area']['cell_size'])
        return self.position

    def draw(self, surface):
        # Change as needed for mode
        surface.blit(config['food']['easy'],
                     (self.position[0], self.position[1]))

    @staticmethod
    def generate_food_position(snake_pos, game_width, game_height, cell_size):
        food_pos = [random.randrange(1, game_width // cell_size) * cell_size,
                    random.randrange(1, game_height // cell_size) * cell_size]
        while food_pos in snake_pos:
            food_pos = [random.randrange(1, game_width // cell_size) * cell_size,
                        random.randrange(1, game_height // cell_size) * cell_size]
        return food_pos

    @staticmethod
    def generate_poison_food_position(snake_pos, game_width, game_height, cell_size):
        poison_food_pos = [random.randrange(1, game_width // cell_size) * cell_size,
                           random.randrange(1, game_height // cell_size) * cell_size]
        while poison_food_pos in snake_pos:
            poison_food_pos = [random.randrange(1, game_width // cell_size) * cell_size,
                               random.randrange(1, game_height // cell_size) * cell_size]
        return poison_food_pos

    @staticmethod
    def generate_blocks(snake_pos, probability=0.1):
        if random.random() < probability:
            block_pos = [random.randrange(1, config['game_area']['base_width'] // config['game_area']['cell_size']) * config['game_area']['cell_size'],
                         random.randrange(1, config['game_area']['base_height'] // config['game_area']['cell_size']) * config['game_area']['cell_size']]
            while block_pos in snake_pos:
                block_pos = [random.randrange(1, config['game_area']['base_width'] // config['game_area']['cell_size']) * config['game_area']['cell_size'],
                             random.randrange(1, config['game_area']['base_height'] // config['game_area']['cell_size']) * config['game_area']['cell_size']]
            return block_pos
        return None


class Navigate:
    @staticmethod
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
                    game_options(username)
                    login_active = False
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
                    game_options(username)
                    sign_up_active = False
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
    # Logic to check credentials from a stored file/database
    try:
        with open('users.json', 'r') as user_file:
            users = json.load(user_file)
        if username in users:
            return True
        return False
    except FileNotFoundError:
        return False


def register_user(username):
    # Logic to register user in a stored file/database
    try:
        with open('users.json', 'r') as user_file:
            users = json.load(user_file)
    except FileNotFoundError:
        users = {}

    if username not in users:
        users[username] = None
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
                    view_high_scores(username)
                if event.key == pygame.K_4:
                    main_menu()
                    options_active = False


def view_high_scores(username):
    high_scores_active = True
    while high_scores_active:
        win.fill(BLACK)
        draw_text('HIGH SCORES', font, WHITE, win, width // 2, height // 4)
        try:
            with open('savegame.json', 'r') as save_file:
                data = json.load(save_file)
            if username in data:
                high_score_text = f"High Score for {
                    username}: {data[username]['high_score']}"
            else:
                high_score_text = "No high score available for this user."
        except FileNotFoundError:
            high_score_text = "No high score available."
        draw_text(high_score_text, font, WHITE, win, width // 2, height // 2)
        draw_text('Press any key to return', font, WHITE,
                  win, width // 2, height // 2 + 40)
        draw_text('Press Alt+M to return to menu', font,
                  WHITE, win, width // 2, height // 2 + 80)
        pygame.display.update()

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


if __name__ == "snakegame":
    pygame.init()
    width, height = config['game_area']['base_width'] + \
        config['display']['scoreboard_width'], config['game_area']['base_height']
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Smart Snake")
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()

    main_menu()
