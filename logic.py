from keyboard import add_hotkey, remove_all_hotkeys
from display import Screen, Window, welcome, sleep, borders, message, format, toggle, intensity


class Game:
    pressed_key = None

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
                return self.menu()
            case 2:
                return self.run()
        return 0

    def menu(self):
        screen = Screen()
        win = Window(size=[25, 8])
        win.set_header(title="Menu")
        win.set_border(*borders["rounded"])

        # file = open(self.data_path, "r")
        # data = json.loads(file.read())
        # file.close()
        # saved = not not data[self.username][self.mode]["saved"]
        # del data

        # if saved:
        #     add_hotkey("shift+l", self.press_key, args=["l"])
        #     f1 = format["fore"]["yellow"]
        #     f2 = format["underlined"]
        # else:
        #     f1 = format["dim"]
        # #     f2 = format["dim"]
        add_hotkey("w", self.press_key, args=["w"], suppress=True)
        add_hotkey("l", self.press_key, args=["l"], suppress=True)
        add_hotkey("s", self.press_key, args=["s"], suppress=True)
        add_hotkey("a", self.press_key, args=["a"], suppress=True)
        add_hotkey("p", self.press_key, args=["p"], suppress=True)
        add_hotkey("enter", self.press_key, args=["enter"], suppress=True)
        add_hotkey("esc", self.press_key, args=["esc"], suppress=True)
        while True:
            win.text = []
            # if saved:
            win.add_text(text="(w) Wall", pos=["l", 2])
            win.add_text(text="(l) Size", pos=["l", 3])
            win.add_text(text="(s) Speed", pos=["l", 4])
            win.add_text(text="(a) AutoPilot", pos=["l", 5])
            win.add_text(text="(p) ShowPath", pos=["l", 6])
            win.add_text(text="├"+"─"*win.size[0]+"┤", pos=["m", 7])
            win.add_text(text="Press enter to start.", pos=["l", 8])

            win.add_text(text=toggle[self.wall], pos=["r", 2])
            win.add_text(text=intensity[self.size], pos=["r", 3])
            win.add_text(text=intensity[self.step_time], pos=["r", 4])
            win.add_text(text=toggle[self.autopilot], pos=["r", 5])
            win.add_text(text=toggle[self.show_path], pos=["r", 6])

            screen.add_window(win)
            screen.show()
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
                case "esc":
                    self.pressed_key = None
                    code = 0
                    break
            sleep(self.step_time/100)
            screen.clear()
            win.set_pos(("m", "m"))
            win.set_header(title="Menu")
        remove_all_hotkeys()
        return code

    # def menu(self):
    #     screen = Screen()
    #     win = Window(size=[18, 7])
    #     win.set_header(title="Menu")
    #     win.set_border(*borders["rounded"])

    #     # file = open(self.data_path, "r")
    #     # data = json.loads(file.read())
    #     # file.close()
    #     # saved = not not data[self.username][self.mode]["saved"]
    #     # del data

    #     # if saved:
    #     #     add_hotkey("shift+l", self.press_key, args=["l"])
    #     #     f1 = format["fore"]["yellow"]
    #     #     f2 = format["underlined"]
    #     # else:
    #     #     f1 = format["dim"]
    #     #     f2 = format["dim"]
    #     add_hotkey("shift+n", self.press_key, args=["n"], suppress=True)
    #     # add_hotkey("shift+c", self.press_key, args=["c"], suppress=True)
    #     add_hotkey("shift+o", self.press_key, args=["o"], suppress=True)
    #     add_hotkey("shift+q", self.press_key, args=["q"], suppress=True)
    #     while True:
    #         win.text = []
    #         # if saved:
    #         win.add_text(text="Load Game", pos=["l", 3])
    #         win.add_text(text="L", pos=["r", 3])
    #         win.add_text(text="New Game", pos=["l", 2])
    #         # win.add_text(text="Change Mode", pos=["l", 5])
    #         # win.add_text(text=f"({self.mode})", pos=["m", 6])
    #         win.add_text(text="Logout", pos=["l", 6])
    #         win.add_text(text="Quit", pos=["l", 7])
    #         win.add_text(text="N", pos=["r", 2], format=format["underlined"])
    #         # win.add_text(text="C", pos=["r", 5], format=format["underlined"])
    #         win.add_text(text="O", pos=["r", 6], format=format["underlined"])
    #         win.add_text(text="Q", pos=["r", 7], format=format["underlined"])
    #         screen.add_window(win)
    #         screen.show()
    #         match self.pressed_key:
    #             case "l":
    #                 self.pressed_key = None
    #                 code = 0
    #                 break
    #             case "n":
    #                 self.pressed_key = None
    #                 code = 2
    #                 break
    #             # case "c":
    #             #     self.pressed_key = None
    #             #     self.mode = "beta" if self.mode == "classic" else "classic"
    #             #     file = open(self.data_path, "r")
    #             #     data = json.loads(file.read())
    #             #     self.high_score = data[self.username][self.mode]["high-score"]
    #             #     self.max_lines = data[self.username][self.mode]["max-lines"]
    #             #     self.best_level = data[self.username][self.mode]["best-level"]
    #             #     code = 1
    #             #     break
    #             case "o":
    #                 self.pressed_key = None
    #                 code = 5
    #                 self.username = None
    #                 break
    #             case "q":
    #                 self.pressed_key = None
    #                 code = 0
    #                 break
    #         sleep(self.step_time)
    #         screen.clear()
    #         win.set_pos(("m", "m"))
    #         win.set_header(title="Menu")
    #     remove_all_hotkeys()
    #     return code

    def press_key(self, key):
        self.pressed_key = key
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

    def game_over(self):
        scr = Screen()
        scr.add_window(self.window)
        scr.show()
        scr.clear()
        print("GAME-OVER")
        return

    def run(self):

        if not self.autopilot:
            add_hotkey("up", self.set_direction, args=["up"], suppress=True)
            add_hotkey("down", self.set_direction,
                       args=["down"], suppress=True)
            add_hotkey("right", self.set_direction,
                       args=["right"], suppress=True)
            add_hotkey("left", self.set_direction,
                       args=["left"], suppress=True)
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
            win.set_border(*borders["rounded"])

        # test
        # win.board.set(*[(i, game_size-3) for i in range(2)])

        # snake_body = [win.board.drop_apple()]
        # test
        snake_body = [(1, game_size//2-1), (1, game_size//2),
                      (1, game_size//2+1)]
        win.board.set(snake_body[0], value=1)
        win.board.set(snake_body[1], value=2)
        win.board.set(snake_body[2], value=3)

        # test
        # win.apple = (1, game_size-2)
        win.apple = win.board.drop_apple()
        scr = Screen()
        # print(win.board)
        self.direction = (0, 1)

        while True:

            scr.clear()
            win.set_header(title=str(len(snake_body)-3))
            win.set_pos(("m", "m"))

            if self.autopilot:
                sleep(self.step_time/100)
                steps = win.board.find_path(snake_body[-1], win.apple)
                if not steps:
                    self.game_over()
                    break
                win.path = steps
                next_step = steps[-1]
                scr.add_window(win)
                scr.show()
            else:
                win.path = win.board.find_path(snake_body[-1], win.apple)
                scr.add_window(win)
                scr.show()
                sleep(self.step_time/100)
                next_step = (win.board.fix(
                    snake_body[-1][0]+self.direction[0]), win.board.fix(snake_body[-1][1]+self.direction[1]))
                if win.board.is_blocked(next_step, distance=1):
                    self.game_over()
                    break

            if next_step == win.apple:
                win.apple = win.board.drop_apple()
            else:
                # win.board.set(snake_body.pop(0), value=0)
                win.board.minus(*snake_body)
                snake_body.pop(0)
            snake_body.append(next_step)
            win.board.set(next_step, value=len(snake_body))

            # if not steps:
            #     self.game_over()
            #     break
            # win.path = steps
            # if not self.autopilot:
            #     next_step = (win.board.fix(
            #         snake_body[-1][0]+self.direction[0]), win.board.fix(snake_body[-1][1]+self.direction[1]))
            #     if win.board.is_blocked(next_step, distance=1):
            #         self.game_over()
            #         break
            # else:
            #     next_step = steps.pop()

            # scr.add_window(win)
            # print(self.direction)

        return 1


# snake = Game(step_time=0.1)
# # snake.run()
# snake.menu()
