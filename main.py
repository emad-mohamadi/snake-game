from logic import Game, sleep
from display import welcome, Screen, format

with open("logo.txt", "r") as logo:
    print(logo.read())
sleep(1)
welcome(name="marboro")

snake = Game(size=16, wall=True, autopilot=True, show_path=True)

code = 3
while code:
    code = snake.switch(code)

scr = Screen()
scr.show(end=format["from-beginning"])
