from logic import Game

snake = Game(size=16, wall=True, autopilot=True, show_path=True)

code = 1
while code:
    code = snake.switch(code)