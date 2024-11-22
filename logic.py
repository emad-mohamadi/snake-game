from keyboard import add_hotkey, remove_all_hotkeys
from display import Screen, Window, welcome, sleep, borders, message, format, toggle, intensity, apple_prizes
from json import load, dump
from random import choice

class Game:
    pressed_key = None
    score = 0
    data_path = "data.json"
    username = None
    record_broken = False
    obstacle = True

    def __init__(self, size=16, wall=False, autopilot=False, show_path=True, step_time=15):
        self.size = size
        self.wall = wall
        self.step_time = step_time
        self.autopilot = autopilot
        self.show_path = show_path
        return

    def switch(self, code):
        match code:
            case 1:
                return self.main_menu()
            case 2:
                return self.start()
            case 3:
                return self.login_menu()
            case 4:
                return self.signin_menu()
            case 5:
                return self.pause_menu()
            case 6:
                return self.run()

        return 0

    def signin_menu(self):
        screen = Screen()
        win = Window(size=[18, 6])
        win.set_header(title="Sign-up")
        win.set_border()

        add_hotkey("enter", self.press_key, args=["enter"], suppress=True)
        add_hotkey("backspace", self.press_key,
                   args=["backspace"], suppress=True)
        add_hotkey("shift+l", self.press_key, args=["L"], suppress=True)
        add_hotkey("esc", self.press_key, args=["Q"], suppress=True)
        for i in range(97, 123):
            add_hotkey(chr(i), self.press_key, args=[chr(i)], suppress=True)

        typed = ""
        while True:
            win.text = []
            win.add_text(text="username:", pos=["m", 2])
            win.add_text(text=typed+"_", pos=["m", 3])
            win.add_text(text="Login", pos=["l", 5])
            win.add_text(text="Quit", pos=["l", 6])
            win.add_text(text="L", pos=["r", 5], format=format["underlined"])
            win.add_text(text="esc", pos=["r", 6], format=format["underlined"])
            screen.add_window(win)
            screen.show()
            match self.pressed_key:
                case "enter":
                    self.pressed_key = None
                    self.load_data(self.data_path)
                    if typed not in self.data:
                        if len(typed) > 3:
                            self.username = typed
                            self.data[self.username] = {
                                "True": {"hs": 0, "ml": 3},
                                "False": {"hs": 0, "ml": 3}
                            }
                            self.save_data(self.data_path)
                            message([f"welcome {typed}"], 1.5,
                                    form=format["fore"]["green"])
                            code = 1
                        else:
                            message(
                                [f"username is too short"], 2.5, form=format["fore"]["red"])
                            code = 4
                    else:
                        message(
                            [f"username '{typed}' already exists"], 2.5, form=format["fore"]["red"])
                        code = 4
                    break
                case "L":
                    self.pressed_key = None
                    code = 3
                    break
                case "Q":
                    self.pressed_key = None
                    code = 0
                    break
                case "backspace":
                    self.pressed_key = None
                    typed = typed[:-1]
                case _:
                    if self.pressed_key and len(typed) < 10:
                        typed += self.pressed_key
                        self.pressed_key = None

            sleep(self.step_time/100)
            screen.clear()
            win.set_pos(("m", "m"))
            win.set_header(title="Sign-up")
        remove_all_hotkeys()
        return code

    def login_menu(self):
        screen = Screen()
        win = Window(size=[18, 6])
        win.set_header(title="Login")
        win.set_border()

        add_hotkey("enter", self.press_key, args=["enter"], suppress=True)
        add_hotkey("backspace", self.press_key,
                   args=["backspace"], suppress=True)
        add_hotkey("shift+s", self.press_key, args=["S"], suppress=True)
        add_hotkey("esc", self.press_key, args=["Q"], suppress=True)
        for i in range(97, 123):
            add_hotkey(chr(i), self.press_key, args=[chr(i)], suppress=True)

        typed = ""
        while True:
            win.text = []
            win.add_text(text="username:", pos=["m", 2])
            win.add_text(text=typed+"_", pos=["m", 3])
            win.add_text(text="Sign up", pos=["l", 5])
            win.add_text(text="Quit", pos=["l", 6])
            win.add_text(text="S", pos=["r", 5], format=format["underlined"])
            win.add_text(text="esc", pos=["r", 6], format=format["underlined"])
            screen.add_window(win)
            match self.pressed_key:
                case "enter":
                    self.pressed_key = None
                    self.load_data(self.data_path)
                    if typed in self.data:
                        self.username = typed
                        message([f"welcome {typed}"], 1.5,
                                form=format["fore"]["green"])
                        code = 1
                    else:
                        message(
                            [f"username '{typed}' not found"], 2.5, form=format["fore"]["red"])
                        code = 3
                    break
                case "S":
                    self.pressed_key = None
                    code = 4
                    break
                case "Q":
                    self.pressed_key = None
                    code = 0
                    break
                case "backspace":
                    self.pressed_key = None
                    typed = typed[:-1]
                case _:
                    if self.pressed_key and len(typed) < 10:
                        typed += self.pressed_key
                        self.pressed_key = None

            screen.show()
            screen.clear()
            sleep(self.step_time/100)
            win.set_pos(("m", "m"))
            win.set_header(title="Login")
        remove_all_hotkeys()
        return code

    def main_menu(self):
        screen = Screen()
        win = Window(size=[25, 10])
        win.set_header(title="Menu")
        win.set_border(*borders["rounded"])

        add_hotkey("w", self.press_key, args=["w"], suppress=True)
        add_hotkey("l", self.press_key, args=["l"], suppress=True)
        add_hotkey("s", self.press_key, args=["s"], suppress=True)
        add_hotkey("a", self.press_key, args=["a"], suppress=True)
        add_hotkey("p", self.press_key, args=["p"], suppress=True)
        add_hotkey("enter", self.press_key, args=["enter"], suppress=True)
        add_hotkey("esc", self.press_key, args=["esc"], suppress=True)
        add_hotkey("backspace", self.press_key, args=["bs"], suppress=True)
        while True:
            win.text = []
            # if saved:
            win.add_text(text="Wall", pos=["l", 2])
            win.add_text(text="Size", pos=["l", 3])
            win.add_text(text="Speed", pos=["l", 4])
            win.add_text(text="AutoPilot", pos=["l", 5])
            win.add_text(text="ShowPath", pos=["l", 6])
            win.add_text(text="├"+"─"*win.size[0]+"┤", pos=["m", 7])
            win.add_text(text="Start", pos=["l", 8])
            win.add_text(text="Logout", pos=["l", 9])
            win.add_text(text="Exit", pos=["l", 10])

            win.add_text(text=toggle[self.wall], pos=["nr", 2], format=format["bold"] +
                         format["fore"]["green"] if self.wall else format["bold"]+format["fore"]["red"])
            win.add_text(text=intensity[self.size], pos=[
                         "nr", 3], format=format["bold"]+format["fore"]["blue"])
            win.add_text(text=intensity[self.step_time], pos=[
                         "nr", 4], format=format["bold"]+format["fore"]["blue"])
            win.add_text(text=toggle[self.autopilot], pos=["nr", 5], format=format["bold"] +
                         format["fore"]["green"] if self.autopilot else format["bold"]+format["fore"]["red"])
            win.add_text(text=toggle[self.show_path], pos=["nr", 6], format=format["bold"] +
                         format["fore"]["green"] if self.show_path else format["bold"]+format["fore"]["red"])

            win.add_text(text="w", pos=["r", 2], format=format["underlined"])
            win.add_text(text="l", pos=["r", 3], format=format["underlined"])
            win.add_text(text="s", pos=["r", 4], format=format["underlined"])
            win.add_text(text="a", pos=["r", 5], format=format["underlined"])
            win.add_text(text="p", pos=["r", 6], format=format["underlined"])
            win.add_text(text="ENTER", pos=[
                         "r", 8], format=format["underlined"])
            win.add_text(text="backspace", pos=[
                         "r", 9], format=format["underlined"])
            win.add_text(text="esc", pos=["r", 10],
                         format=format["underlined"])

            screen.add_window(win)
            match self.pressed_key:
                case "w":
                    self.wall = not self.wall
                    self.pressed_key = None
                case "l":
                    self.size = self.size + 8 if self.size != 32 else 16
                    self.pressed_key = None
                case "s":
                    self.step_time = self.step_time - 10 if self.step_time != 5 else 25
                    self.pressed_key = None
                case "a":
                    self.autopilot = not self.autopilot
                    self.pressed_key = None
                case "p":
                    self.show_path = not self.show_path
                    self.pressed_key = None
                case "enter":
                    self.pressed_key = None
                    code = 2
                    break
                case "bs":
                    self.pressed_key = None
                    code = 3
                    break
                case "esc":
                    self.pressed_key = None
                    code = 0
                    break
            screen.show()
            screen.clear()
            sleep(self.step_time/100)
            win.set_pos(("m", "m"))
            win.set_header(title="Menu")
        remove_all_hotkeys()
        return code

    def pause_menu(self):
        screen = Screen()
        win = Window(size=[28, 9])
        win.set_header(title=" Paused ")
        win.set_border()

        add_hotkey("enter", self.press_key, args=["r"], suppress=True)
        add_hotkey("n", self.press_key, args=["n"], suppress=True)
        add_hotkey("esc", self.press_key, args=["q"], suppress=True)
        add_hotkey("backspace", self.press_key, args=["m"], suppress=True)
        add_hotkey("a", self.press_key, args=["a"], suppress=True)
        add_hotkey("s", self.press_key, args=["s"], suppress=True)
        add_hotkey("p", self.press_key, args=["p"], suppress=True)
        # self.save_game()

        while True:
            win.text = []
            win.add_text(text="Resume", pos=["l", 6])
            win.add_text(text="New Game", pos=["l", 7])
            win.add_text(text="Back to Menu", pos=["l", 8])
            win.add_text(text="Quit", pos=["l", 9])
            win.add_text(text="AutoPilot", pos=["l", 2])
            win.add_text(text="ShowPath", pos=["l", 3])
            win.add_text(text="Speed", pos=["l", 4])
            win.add_text(text="├"+"─"*win.size[0]+"┤", pos=["m", 5])

            win.add_text(text=toggle[self.autopilot], pos=["nr", 2], format=format["bold"] +
                         format["fore"]["green"] if self.autopilot else format["bold"]+format["fore"]["red"])
            win.add_text(text=toggle[self.show_path], pos=["nr", 3], format=format["bold"] +
                         format["fore"]["green"] if self.show_path else format["bold"]+format["fore"]["red"])
            win.add_text(text=intensity[self.step_time], pos=[
                         "nr", 4], format=format["bold"] + format["fore"]["blue"])

            win.add_text(text="Enter", pos=[
                         "r", 6], format=format["underlined"])
            win.add_text(text="n", pos=["r", 7], format=format["underlined"])
            win.add_text(text="backspace", pos=[
                         "r", 8], format=format["underlined"])
            win.add_text(text="esc", pos=["r", 9], format=format["underlined"])
            win.add_text(text="a", pos=["r", 2], format=format["underlined"])
            win.add_text(text="p", pos=["r", 3], format=format["underlined"])
            win.add_text(text="s", pos=["r", 4], format=format["underlined"])

            screen.add_window(win)
            match self.pressed_key:
                case "r":
                    self.pressed_key = None
                    code = 6
                    break
                case "n":
                    self.pressed_key = None
                    code = 2
                    # Here we should set up a new game
                    # by initializing some parameters in 'self.run'
                    # again.
                    break
                case "m":
                    self.pressed_key = None
                    code = 1
                    break
                case "q":
                    self.pressed_key = None
                    code = 0
                    break
                case "a":
                    self.autopilot = not self.autopilot
                    self.get_direction()
                    self.pressed_key = None
                case "p":
                    self.show_path = not self.show_path
                    self.pressed_key = None
                case "s":
                    self.step_time = self.step_time - 10 if self.step_time != 5 else 25
                    self.pressed_key = None
            sleep(self.step_time/100)
            screen.show()
            screen.clear()
            win.set_pos(("m", "m"))
            win.set_header(title="Paused")
        remove_all_hotkeys()
        return code

    def press_key(self, key):
        self.pressed_key = key
        return

    def get_direction(self):
        self.direction = (self.snake_body[-1][0]-self.snake_body[-2]
                          [0], self.snake_body[-1][1]-self.snake_body[-2][1])
        return

    def set_direction(self, dir):
        if dir == "up":
            self.direction = (-1, 0) if self.direction != (1, 0) else (1, 0)
        elif dir == "down":
            self.direction = (1, 0) if self.direction != (-1, 0) else (-1, 0)
        elif dir == "right":
            self.direction = (0, 1) if self.direction != (0, -1) else (0, -1)
        elif dir == "left":
            self.direction = (0, -1) if self.direction != (0, 1) else (0, 1)
        return

    def load_data(self, data_path):
        with open(data_path, "r") as file:
            self.data = load(file)
        return

    def save_data(self, data_path):
        with open(data_path, "w") as file:
            dump(self.data, file, indent=4)
        return

    def game_over(self):
        self.window.set_border(format=format["fore"]["red"]+format["bold"])
        scr = Screen()
        scr.add_window(self.window)
        scr.show()
        scr.clear()
        sleep(2)

        phrase = "Your score:"
        if self.record_broken:
            self.record_broken = False
            phrase = "New high score:"
        message_text = ["", phrase, "", str(self.score)]
        message(message_text, header=" Game Over ",
                time=3.0, form=format["fore"]["red"]+format["bold"], border=borders["rounded"])
        self.save_data(self.data_path)
        return

    def start(self):
        self.score = 0
        self.direction = (0, 1)
        game_size = self.size
        if self.wall:
            game_size += 2
        win = Window((game_size*2, game_size))
        win.show_path = self.show_path
        win.set_board(game_size)
        if self.wall:
            win.board.set(*[(0, i) for i in range(game_size)])
            win.board.set(*[(i, 0) for i in range(game_size)])
            win.board.set(*[(game_size-1, i) for i in range(game_size)])
            win.board.set(*[(i, game_size-1) for i in range(game_size)])
            win.set_border(*borders["no-border"])
        else:
            win.set_border(*borders["dotted"])

        self.snake_body = [(1, 1), (1, 2), (1, 3)]
        win.board.set(self.snake_body[0], value=1)
        win.board.set(self.snake_body[1], value=2)
        win.board.set(self.snake_body[2], value=3)

        win.apple, win.apple_code = win.board.drop_apple()

        self.window = win
        return self.run()

    def shrink(self, times=1):
        for _ in range(times):
            if len(self.snake_body) > 3:
                self.window.board.minus(*self.snake_body)
                self.snake_body.pop(0)
        return

    def make_obstacle(self):
        if self.obstacle and choice([0, 0, 0, 1]):
            self.window.board.set(self.window.board.drop_apple()[0], value=-1)
        return

    def run(self):
        self.load_data(self.data_path)

        add_hotkey("esc", self.press_key, args=["esc"], suppress=True)
        if not self.autopilot:
            add_hotkey("up", self.set_direction, args=["up"], suppress=True)
            add_hotkey("down", self.set_direction,
                       args=["down"], suppress=True)
            add_hotkey("right", self.set_direction,
                       args=["right"], suppress=True)
            add_hotkey("left", self.set_direction,
                       args=["left"], suppress=True)

        win = self.window
        win.show_path = self.show_path

        scr = Screen()
        while True:
            scr.clear()
            win.set_header(title=str(self.score)+" " +
                           str(self.data[self.username][str(self.wall)]["hs"]))
            win.set_pos(("m", "m"))
            if self.pressed_key == "esc":
                self.save_data(self.data_path)
                self.pressed_key = None
                return 5

            if self.autopilot:
                sleep(self.step_time/100)
                if not win.paused:
                    steps = win.board.find_path(self.snake_body[-1], win.apple)
                    if not steps:
                        self.game_over()
                        break
                    win.path = steps
                    next_step = steps[-1]
                scr.add_window(win)
                scr.show()
            else:
                win.path = win.board.find_path(self.snake_body[-1], win.apple)
                scr.add_window(win)
                scr.show()
                sleep(self.step_time/100)
                if not win.paused:
                    next_step = (win.board.fix(
                        self.snake_body[-1][0]+self.direction[0]), win.board.fix(self.snake_body[-1][1]+self.direction[1]))
                    if win.board.is_blocked(next_step):
                        self.game_over()
                        break

            if not win.paused:
                if next_step == win.apple:
                    self.score += apple_prizes[win.apple_code][0]
                    if self.data[self.username][str(self.wall)]["hs"] < self.score:
                        self.data[self.username][str(
                            self.wall)]["hs"] = self.score
                        self.record_broken = True
                    self.shrink(times=apple_prizes[win.apple_code][1])
                    win.apple, win.apple_code = win.board.drop_apple()
                    self.make_obstacle()
                else:
                    # win.board.set(self.snake_body.pop(0), value=0)
                    self.shrink()
                self.snake_body.append(next_step)
                win.board.set(next_step, value=len(self.snake_body))

                self.data[self.username][str(self.wall)]["ml"] = max(len(self.snake_body),
                                                                     self.data[self.username][str(self.wall)]["ml"])

        return 1


# snake = Game(step_time=0.1)
# # snake.run()
# snake.menu()
