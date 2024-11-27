def main():
    from logic import Game, sleep
    from display import welcome, Screen, format
    from os import path

    directory = path.dirname(path.abspath(__file__))

    with open(fr"{directory}\logo.txt", "r") as logo:
        print(logo.read())
    sleep(1)
    welcome(name="marboro")

    snake = Game(size=16, wall=True, autopilot=True, show_path=True)
    snake.data_path = fr"{directory}\data.json"

    code = 3
    while code:
        code = snake.switch(code)

    scr = Screen()
    scr.show(end=format["from-beginning"])


if __name__ == "__main__":
    main()
