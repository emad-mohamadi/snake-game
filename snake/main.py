import pkg_resources


def path(file_name):
    return pkg_resources.resource_filename(__name__, f'{file_name}')


def main():
    from snake.logic import Game, sleep
    from snake.display import welcome, Screen, format

    with open(path("logo.txt"), "r") as logo:
        print(logo.read())
    sleep(1)
    welcome(name="marboro")

    snake = Game(size=16, wall=True, autopilot=True, show_path=True)
    snake.data_path = path("data.json")

    code = 3
    while code:
        code = snake.switch(code)

    scr = Screen()
    scr.show(end=format["from-beginning"])


if __name__ == "__main__":
    main()
