from display import Screen, Window, welcome, sleep, borders


class Game:
    def __init__(self, size=16, wall=False, step_time=0.05):
        self.size = size
        self.wall = wall
        self.step_time = step_time
        return

    def run(self, autopilot=True):
        if self.wall:
            self.size += 2
        win = Window((self.size*2, self.size))
        self.window = win
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
        snake_body = [(1, self.size//2), (1, self.size//2+1),
                      (1, self.size//2+2)]
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
                scr.add_window(win)
                scr.show()
                scr.clear()
                print("GAME-OVER")
                break
            next_step = steps[-1] if autopilot else None
            win.path = steps
            scr.add_window(win)
            scr.show()
            scr.clear()

            if next_step == win.apple:
                win.apple = win.board.drop_apple()
            else:
                win.board.set(snake_body.pop(0), value=0)
                win.board.minus(*snake_body)
            snake_body.append(next_step)
            win.board.set(next_step, value=len(snake_body))


snake = Game(step_time=0.08)
snake.run()
