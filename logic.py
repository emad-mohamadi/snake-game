from keyboard import add_hotkey, remove_all_hotkeys
from display import Screen, Window, welcome, sleep, borders, message, format, toggle, intensity, apple_prizes, apple_shapes, apple_colors
from json import load, dump
from random import choice
# from snakegame import main


class Game:
    pressed_key = None
    score = 0
    username = None
    record_broken = False
    obstacle = False
    foods = 1

    def __init__(self, size=16, wall=False, autopilot=False, show_path=True, step_time=15, data_path="data.json"):
        self.size = size
        self.wall = wall
        self.step_time = step_time
        self.autopilot = autopilot
        self.show_path = show_path
        self.data_path = data_path
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
            case 7:
                pass

        return 0

    def signin_menu(self):
        screen = Screen()
        win = Window(size=[25, 7])
        win.set_header(title="Sign-up")
        win.set_border()

        add_hotkey("enter", self.press_key, args=["enter"], suppress=True)
        add_hotkey("backspace", self.press_key,
                   args=["backspace"], suppress=True)
        add_hotkey("shift+l", self.press_key, args=["L"], suppress=True)
        add_hotkey("esc", self.press_key, args=["Q"], suppress=True)
        add_hotkey("ctrl+enter", self.press_key,
                   args=["ctrl+enter"], suppress=True)
        for i in range(97, 123):
            add_hotkey(chr(i), self.press_key, args=[chr(i)], suppress=True)

        typed = ""
        while True:
            win.text = []
            win.add_text(text="username:", pos=["m", 2])
            win.add_text(text=typed+"_", pos=["m", 3])
            win.add_text(text="New Window", pos=["l", 6])
            win.add_text(text="Login", pos=["l", 5])
            win.add_text(text="Quit", pos=["l", 7])

            win.add_text(text="ctrl+enter", pos=["r", 6],
                         format=format["underlined"]+format["dim"])
            win.add_text(text="L", pos=["r", 5],
                         format=format["underlined"]+format["dim"])
            win.add_text(text="esc", pos=["r", 7],
                         format=format["underlined"]+format["dim"])
            screen.add_window(win)
            screen.show()
            match self.pressed_key:
                case "enter":
                    self.pressed_key = None
                    self.load_data()
                    if typed not in self.data:
                        if len(typed) > 3:
                            self.username = typed
                            self.data[self.username] = {
                                "True": {"hs": 0, "ml": 3},
                                "False": {"hs": 0, "ml": 3}
                            }
                            self.save_data()
                            message([f"welcome {typed}"], 1.5,
                                    form=format["fore"]["green"])
                            self.pressed_key = None
                            code = 1
                        else:
                            message(
                                [f"username is too short"], 2.5, form=format["fore"]["red"])
                            self.pressed_key = None
                            code = 4
                    else:
                        message(
                            [f"username '{typed}' already exists"], 2.5, form=format["fore"]["red"])
                        self.pressed_key = None
                        code = 4
                    break
                case "L":
                    self.pressed_key = None
                    code = 3
                    break
                case "ctrl+enter":
                    self.pressed_key = None
                    code = 7
                    break
                case "Q":
                    self.pressed_key = None
                    code = 0
                    break
                case "backspace":
                    self.pressed_key = None
                    typed = typed[:-1]
                case _:
                    if self.pressed_key and len(typed) < 15:
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
        win = Window(size=[25, 7])
        win.set_header(title="Login")
        win.set_border()

        add_hotkey("enter", self.press_key, args=["enter"], suppress=True)
        add_hotkey("backspace", self.press_key,
                   args=["backspace"], suppress=True)
        add_hotkey("shift+s", self.press_key, args=["S"], suppress=True)
        add_hotkey("esc", self.press_key, args=["Q"], suppress=True)
        add_hotkey("ctrl+enter", self.press_key,
                   args=["ctrl+enter"], suppress=True)
        for i in range(97, 123):
            add_hotkey(chr(i), self.press_key, args=[chr(i)], suppress=True)

        typed = ""
        while True:
            win.text = []
            win.add_text(text="username:", pos=["m", 2])
            win.add_text(text=typed+"_", pos=["m", 3])
            win.add_text(text="New Window", pos=["l", 6])
            win.add_text(text="Sign-up", pos=["l", 5])
            win.add_text(text="Quit", pos=["l", 7])

            win.add_text(text="ctrl+enter", pos=["r", 6],
                         format=format["underlined"]+format["dim"])
            win.add_text(text="S", pos=["r", 5],
                         format=format["underlined"]+format["dim"])
            win.add_text(text="esc", pos=["r", 7],
                         format=format["underlined"]+format["dim"])
            screen.add_window(win)
            match self.pressed_key:
                case "enter":
                    self.pressed_key = None
                    self.load_data()
                    if typed in self.data:
                        self.username = typed
                        message([f"welcome {typed}"], 1.5,
                                form=format["fore"]["green"])
                        self.pressed_key = None
                        code = 1
                    else:
                        message(
                            [f"username '{typed}' not found"], 2.5, form=format["fore"]["red"])
                        self.pressed_key = None
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
                case "ctrl+enter":
                    self.pressed_key = None
                    code = 7
                    break
                case "backspace":
                    self.pressed_key = None
                    typed = typed[:-1]
                case _:
                    if self.pressed_key and len(typed) < 15:
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
        win = Window(size=[25, 13])
        win.set_header(title="Menu")
        win.set_border(*borders["rounded"])

        add_hotkey("w", self.press_key, args=["w"], suppress=True)
        add_hotkey("l", self.press_key, args=["l"], suppress=True)
        add_hotkey("o", self.press_key, args=["o"], suppress=True)
        add_hotkey("s", self.press_key, args=["s"], suppress=True)
        add_hotkey("a", self.press_key, args=["a"], suppress=True)
        add_hotkey("p", self.press_key, args=["p"], suppress=True)
        add_hotkey("f", self.press_key, args=["f"], suppress=True)
        add_hotkey("enter", self.press_key, args=["enter"], suppress=True)
        add_hotkey("esc", self.press_key, args=["esc"], suppress=True)
        add_hotkey("backspace", self.press_key, args=["bs"], suppress=True)
        while True:
            win.text = []
            win.add_text(text="User", pos=["l", 1],
                         format=format["italic"]+format["dim"])
            win.add_text(text="├"+"─"*win.size[0]+"┤", pos=["m", 2])
            win.add_text(text="Wall", pos=["l", 3])
            win.add_text(text="Obstacles", pos=["l", 4])
            win.add_text(text="Foods", pos=["l", 5])
            win.add_text(text="Size", pos=["l", 6])
            win.add_text(text="Speed", pos=["l", 7])
            win.add_text(text="AutoPilot", pos=["l", 8])
            win.add_text(text="ShowPath", pos=["l", 9])
            win.add_text(text="├"+"─"*win.size[0]+"┤", pos=["m", 10])
            win.add_text(text="Start", pos=["l", 11])
            win.add_text(text="Logout", pos=["l", 12])
            win.add_text(text="Exit", pos=["l", 13])

            win.add_text(text=self.username, pos=[
                         "r", 1], format=format["italic"]+format["dim"])
            win.add_text(text=toggle[self.wall], pos=["nr", 3], format=format["bold"] +
                         format["fore"]["green"] if self.wall else format["bold"]+format["fore"]["red"])
            win.add_text(text=toggle[self.obstacle], pos=["nr", 4], format=format["bold"] +
                         format["fore"]["green"] if self.obstacle else format["bold"]+format["fore"]["red"])
            win.add_text(text=self.foods*"◉",
                         pos=["nr", 5], format=format["fore"]["red"])
            win.add_text(text=intensity[self.size], pos=[
                         "nr", 6], format=format["bold"]+format["fore"]["blue"])
            win.add_text(text=intensity[self.step_time], pos=[
                         "nr", 7], format=format["bold"]+format["fore"]["blue"])
            win.add_text(text=toggle[self.autopilot], pos=["nr", 8], format=format["bold"] +
                         format["fore"]["green"] if self.autopilot else format["bold"]+format["fore"]["red"])
            win.add_text(text=toggle[self.show_path], pos=["nr", 9], format=format["bold"] +
                         format["fore"]["green"] if self.show_path else format["bold"]+format["fore"]["red"])

            win.add_text(text="w", pos=["r", 3], format=format["underlined"])
            win.add_text(text="o", pos=["r", 4], format=format["underlined"])
            win.add_text(text="f", pos=["r", 5], format=format["underlined"])
            win.add_text(text="l", pos=["r", 6], format=format["underlined"])
            win.add_text(text="s", pos=["r", 7], format=format["underlined"])
            win.add_text(text="a", pos=["r", 8], format=format["underlined"])
            win.add_text(text="p", pos=["r", 9], format=format["underlined"])
            win.add_text(text="ENTER", pos=[
                         "r", 11], format=format["underlined"])
            win.add_text(text="backspace", pos=[
                         "r", 12], format=format["underlined"])
            win.add_text(text="esc", pos=["r", 13],
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
                case "o":
                    self.obstacle = not self.obstacle
                    self.pressed_key = None
                case "f":
                    self.foods += 1 if self.foods is not 3 else -2
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
        win = Window(size=[28, 10])
        win.set_header(title=" Paused ")
        win.set_border()

        self.save_data()

        add_hotkey("enter", self.press_key, args=["r"], suppress=True)
        add_hotkey("n", self.press_key, args=["n"], suppress=True)
        add_hotkey("esc", self.press_key, args=["q"], suppress=True)
        add_hotkey("backspace", self.press_key, args=["m"], suppress=True)
        add_hotkey("a", self.press_key, args=["a"], suppress=True)
        add_hotkey("s", self.press_key, args=["s"], suppress=True)
        add_hotkey("p", self.press_key, args=["p"], suppress=True)
        add_hotkey("o", self.press_key, args=["o"], suppress=True)

        while True:
            win.text = []
            win.add_text(text="Resume", pos=["l", 7])
            win.add_text(text="New Game", pos=["l", 8])
            win.add_text(text="Back to Menu", pos=["l", 9])
            win.add_text(text="Quit", pos=["l", 10])
            win.add_text(text="AutoPilot", pos=["l", 2])
            win.add_text(text="ShowPath", pos=["l", 3])
            win.add_text(text="Obstacles", pos=["l", 4])
            win.add_text(text="Speed", pos=["l", 5])
            win.add_text(text="├"+"─"*win.size[0]+"┤", pos=["m", 6])

            win.add_text(text=toggle[self.autopilot], pos=["nr", 2], format=format["bold"] +
                         format["fore"]["green"] if self.autopilot else format["bold"]+format["fore"]["red"])
            win.add_text(text=toggle[self.show_path], pos=["nr", 3], format=format["bold"] +
                         format["fore"]["green"] if self.show_path else format["bold"]+format["fore"]["red"])
            win.add_text(text=toggle[self.obstacle], pos=["nr", 4], format=format["bold"] +
                         format["fore"]["green"] if self.obstacle else format["bold"]+format["fore"]["red"])
            win.add_text(text=intensity[self.step_time], pos=[
                         "nr", 5], format=format["bold"] + format["fore"]["blue"])

            win.add_text(text="enter", pos=[
                         "r", 7], format=format["underlined"])
            win.add_text(text="n", pos=["r", 8], format=format["underlined"])
            win.add_text(text="backspace", pos=[
                         "r", 9], format=format["underlined"])
            win.add_text(text="esc", pos=["r", 10],
                         format=format["underlined"])
            win.add_text(text="a", pos=["r", 2], format=format["underlined"])
            win.add_text(text="p", pos=["r", 3], format=format["underlined"])
            win.add_text(text="o", pos=["r", 4], format=format["underlined"])
            win.add_text(text="s", pos=["r", 5], format=format["underlined"])

            screen.add_window(win)
            match self.pressed_key:
                case "r":
                    self.pressed_key = None
                    code = 6
                    break
                case "n":
                    self.pressed_key = None
                    code = 2
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
                case "o":
                    self.obstacle = not self.obstacle
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

    def load_data(self):
        with open(self.data_path, "r") as file:
            self.data = load(file)
        return

    def save_data(self):
        with open(self.data_path, "w") as file:
            dump(self.data, file, indent=4)
        return

    def game_over(self):
        self.window.set_border(format=format["fore"]["red"]+format["bold"])
        scr = Screen()
        scr.add_window(self.window)
        scr.add_window(self.stat)
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
        self.pressed_key = None
        self.save_data()
        return

    def leaders(self):
        score_list = [(user, self.data[user][str(self.wall)]["hs"])
                      for user in self.data]
        score_list.sort(key=lambda a: a[1])
        top = score_list[-4:]
        if (self.username, self.data[self.username][str(self.wall)]["hs"]) not in top:
            top[0] = (self.username, self.data[self.username]
                      [str(self.wall)]["hs"])
        return top[::-1]

    def start(self):
        self.score = 0
        self.direction = (0, 1)
        game_size = self.size
        if self.wall:
            game_size += 2
        win = Window((game_size*2, game_size))
        self.window = win
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

        win.apples = []
        self.drop_food()
        self.obstacles = []

        return self.run()

    def shrink(self, times=1):
        for _ in range(times):
            if len(self.snake_body) > 3:
                self.window.board.minus(*self.snake_body)
                self.snake_body.pop(0)
        return

    def make_obstacle(self, head):
        if self.obstacle and choice([0, 0, 0, 1]):
            loc = self.window.board.drop_apple()[0]
            if loc in self.window.board.neighbors(head, distance=-1)+[a[0] for a in self.window.apples]:
                return
            self.window.board.set(loc, value=-1)
            self.obstacles.append(loc)
            if len(self.obstacles) == (self.size**2//20):
                self.window.board.set(self.obstacles.pop(0), value=0)
        return

    def drop_food(self, head=None):
        while len(self.window.apples) < self.foods:
            new_apple = self.window.board.drop_apple()
            if new_apple[0] not in [apple[0] for apple in self.window.apples]+[head] and len(self.window.board.neighbors(new_apple[0])) >= 2:
                self.window.apples.append(new_apple)
        return

    def run(self):
        self.load_data()

        add_hotkey("esc", self.press_key, args=["esc"], suppress=True)
        add_hotkey("a", self.press_key, args=["a"], suppress=True)
        add_hotkey("p", self.press_key, args=["p"], suppress=True)
        add_hotkey("s", self.press_key, args=["s"], suppress=True)
        add_hotkey("o", self.press_key, args=["o"], suppress=True)
        add_hotkey("up", self.set_direction, args=["up"], suppress=True)
        add_hotkey("down", self.set_direction,
                   args=["down"], suppress=True)
        add_hotkey("right", self.set_direction,
                   args=["right"], suppress=True)
        add_hotkey("left", self.set_direction,
                   args=["left"], suppress=True)

        win = self.window
        win.show_path = self.show_path
        statics = Window(size=[20, 17], pos=("m", "m"))
        self.stat = statics
        statics.main = False
        statics.set_header(title="Leaderboard")
        top = self.leaders()

        scr = Screen()
        while True:
            statics.text = []
            statics.set_border()
            statics.set_pos(pos=(win.pos[0]-24, win.pos[1]+self.wall))
            statics.add_text(text="User", pos=["l", 1], format=format["dim"])
            statics.add_text(text="Best", pos=["r", 1], format=format["dim"])
            statics.add_text(text="├"+"─"*statics.size[0]+"┤", pos=["m", 6])
            statics.add_text(text="├"+"─"*statics.size[0]+"┤", pos=["m", 13])
            top.sort(key=lambda a: 1/(a[1]+1))
            rank = 1
            for user, best in top:
                if user == self.username:
                    f = format["bold"]+format["fore"]["yellow"]
                    top[rank-1] = (user, self.data[user][str(self.wall)]["hs"])
                else:
                    f = format["regular"]
                statics.add_text(
                    text=f"{rank}-{user}", pos=["l", 1+rank], format=f)
                statics.add_text(text=str(best), pos=[
                    "r", 1+rank], format=f)
                rank += 1
            statics.add_text(text="prize", pos=[8, 7], format=format["dim"])
            statics.add_text(text="growth", pos=["r", 7], format=format["dim"])
            for i in range(1, 6):
                statics.add_text(
                    text=apple_shapes[apple_prizes[i][2]][2], pos=["l", 7+i], format=apple_colors[i]
                )
                statics.add_text(text=str(apple_prizes[i][0]), pos=[12, 7+i])
                statics.add_text(
                    text=str(1-apple_prizes[i][1]), pos=["r", 7+i])
            statics.add_text(text=toggle[self.autopilot], pos=["nr", 14], format=format["bold"] +
                             format["fore"]["green"] if self.autopilot else format["bold"]+format["fore"]["red"])
            statics.add_text(text=toggle[self.show_path], pos=["nr", 15], format=format["bold"] +
                             format["fore"]["green"] if self.show_path else format["bold"]+format["fore"]["red"])
            statics.add_text(text=toggle[self.obstacle], pos=["nr", 16], format=format["bold"] +
                             format["fore"]["green"] if self.obstacle else format["bold"]+format["fore"]["red"])
            statics.add_text(text=intensity[self.step_time], pos=[
                "nr", 17], format=format["bold"] + format["fore"]["blue"])
            statics.add_text(text="AutoPilot", pos=["l", 14])
            statics.add_text(text="ShowPath", pos=["l", 15])
            statics.add_text(text="Obstacles", pos=["l", 16])
            statics.add_text(text="Speed", pos=["l", 17])
            statics.add_text(
                text="a", pos=["r", 14], format=format["underlined"])
            statics.add_text(
                text="p", pos=["r", 15], format=format["underlined"])
            statics.add_text(
                text="o", pos=["r", 16], format=format["underlined"])
            statics.add_text(
                text="s", pos=["r", 17], format=format["underlined"])

            scr.add_window(statics)
            win.set_header(title=str(self.score))
            win.set_pos(("m", "m"))

            match self.pressed_key:
                case "esc":
                    self.save_data()
                    self.pressed_key = None
                    return 5
                case "a":
                    self.get_direction()
                    self.autopilot = not self.autopilot
                    self.pressed_key = None
                case "p":
                    self.show_path = not self.show_path
                    self.window.show_path = self.show_path
                    self.pressed_key = None
                case "s":
                    self.step_time = self.step_time - 10 if self.step_time != 5 else 25
                    self.pressed_key = None
                case "o":
                    self.obstacle = not self.obstacle
                    self.pressed_key = None

            if self.autopilot:
                sleep(self.step_time/100)
                if not win.paused:
                    steps = win.board.find_path(
                        self.snake_body[-1], [a[0] for a in win.apples])
                    if not steps:
                        self.game_over()
                        break
                    win.path = steps
                    next_step = steps[-1]
                scr.add_window(win)
                scr.show()
            else:
                win.path = win.board.find_path(
                    self.snake_body[-1], [a[0] for a in win.apples])
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
                if next_step in [a[0] for a in win.apples]:
                    i = 0
                    while i < self.foods:
                        if win.apples[i][0] == next_step:
                            break
                        i += 1
                    self.score += apple_prizes[win.apples[i][1]][0]
                    if self.data[self.username][str(self.wall)]["hs"] < self.score:
                        self.data[self.username][str(
                            self.wall)]["hs"] = self.score
                        self.record_broken = True
                    self.shrink(times=apple_prizes[win.apples[i][1]][1])
                    win.apples.pop(i)
                    self.make_obstacle(head=next_step)
                    self.drop_food(head=next_step)
                else:
                    self.shrink()
                self.snake_body.append(next_step)
                win.board.set(next_step, value=len(self.snake_body))

                self.data[self.username][str(self.wall)]["ml"] = max(len(self.snake_body),
                                                                     self.data[self.username][str(self.wall)]["ml"])
            scr.clear()

        return 1
