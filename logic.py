
from display import Screen, Window, welcome, sleep, randint, borders, format

game_size = 15
bounded = False
break_time = 0.05

if bounded:
    game_size += 2
new_win = Window((game_size*2, game_size))
new_win.set_board(game_size)
if bounded:
    new_win.board.set(*[(0, i) for i in range(game_size)])
    new_win.board.set(*[(i, 0) for i in range(game_size)])
    new_win.board.set(*[(game_size-1, i) for i in range(game_size)])
    new_win.board.set(*[(i, game_size-1) for i in range(game_size)])
    new_win.set_border(*borders["no-border"])
else:
    new_win.set_border(*borders["rounded"])

snake_body = [new_win.board.drop_apple()]
new_win.board.set(*snake_body, value=1)
new_win.apple = new_win.board.drop_apple()
scr = Screen()

while True:
    new_win.set_pos(("m", "m"))
    new_win.set_header(title=str(len(snake_body)))
    scr.add_window(new_win)
    scr.show()
    scr.clear()
    sleep(break_time)
    steps = new_win.board.find_path(snake_body[-1], new_win.apple)
    if not steps:
        print("GAME-OVER")
        break
    next_step = steps.pop()
    new_win.path = steps
    if next_step == new_win.apple:
        new_win.apple = new_win.board.drop_apple()
    else:
        new_win.board.set(snake_body.pop(0), value=0)
        new_win.board.minus(*snake_body)
    snake_body.append(next_step)
    new_win.board.set(next_step, value=len(snake_body))
