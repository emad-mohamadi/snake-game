from keyboard import add_hotkey
from display import Screen, Window, welcome, sleep, borders


class Game:
    def __init__(self, size=16, wall=False, step_time=0.05):
        self.size = size
        self.wall = wall
        self.step_time = step_time
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

    def run(self, autopilot=False, show_path=False):
        self.direction = (0, 1)
        if not autopilot:
            add_hotkey("up", self.set_direction, args=["up"], suppress=True)
            add_hotkey("down", self.set_direction, args=["down"], suppress=True)
            add_hotkey("right", self.set_direction, args=["right"], suppress=True)
            add_hotkey("left", self.set_direction, args=["left"], suppress=True)
        if self.wall:
            self.size += 2
        win = Window((self.size*2, self.size))
        self.window = win
        win.show_path = show_path
        win.set_board(self.size)
        if self.wall:
            win.board.set(*[(0, i) for i in range(self.size)])
            win.board.set(*[(i, 0) for i in range(self.size)])
            win.board.set(*[(self.size-1, i) for i in range(self.size)])
            win.board.set(*[(i, self.size-1) for i in range(self.size)])
            win.set_border(*borders["no-border"])
        else:
            win.set_border(*borders["rounded"])

        # test
        # win.board.set(*[(i, self.size-3) for i in range(2)])

        # snake_body = [win.board.drop_apple()]
        # test
        snake_body = [(1, self.size//2-1), (1, self.size//2),
                      (1, self.size//2+1)]
        win.board.set(snake_body[0], value=1)
        win.board.set(snake_body[1], value=2)
        win.board.set(snake_body[2], value=3)

        # test
        # win.apple = (1, self.size-2)
        win.apple = win.board.drop_apple()
        scr = Screen()
        # print(win.board)
        while True:
            win.set_header(title=str(len(snake_body)-3))
            win.set_pos(("m", "m"))
            sleep(self.step_time)

            steps = win.board.find_path(snake_body[-1], win.apple)
            if not steps:
                self.game_over()
                break
            win.path = steps
            if not autopilot:
                next_step = (win.board.fix(
                    snake_body[-1][0]+self.direction[0]), win.board.fix(snake_body[-1][1]+self.direction[1]))
                if win.board.is_blocked(next_step, distance=1):
                    self.game_over()
                    break
            else:
                next_step = steps.pop()

            scr.add_window(win)
            scr.show()
            # print(self.direction)
            scr.clear()

            if next_step == win.apple:
                win.apple = win.board.drop_apple()
            else:
                # win.board.set(snake_body.pop(0), value=0)
                win.board.minus(*snake_body)
                snake_body.pop(0)
            snake_body.append(next_step)
            win.board.set(next_step, value=len(snake_body))


snake = Game(step_time=0.1)
snake.run(autopilot=False, show_path=True)
