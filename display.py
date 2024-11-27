from navigate import Board
from time import sleep
from random import choice, randint
from math import ceil
from os import get_terminal_size as console_size
from keyboard import add_hotkey, remove_all_hotkeys

toggle = ["☐", "☑"]


apple_prizes = {
    1: (1, 0, 1),
    2: (2, 0, 1),
    3: (3, 0, 1),
    4: (1, 2, 2),
    5: (2, 2, 2)
}

apple_shapes = {
    1: ["▗", "▖", "▗▖"],
    2: ["◀", "▶", "◀▶"]
}

intensity = {
    16: "+",
    24: "++",
    32: "+++",
    5: "+++",
    15: "++",
    25: "+"
}

borders = {
    "no-border": [" ", " ", (" ", " ", " ", " ")],
    "blocks": ["█", "█", ("█", "█", "█", "█")],
    "double-line": ["║", "═", ("╔", "╗", "╚", "╝")],
    "rounded": ["│", "─", ("╭", "╮", "╰", "╯")],
    "dotted": ["╎", "╴", ("╭", "╮", "╰", "╯")]
}

palette = ("red", "green", "yellow", "blue", "purple")

format = {
    "regular": "\033[0m",
    "bold": "\033[1m",
    "dim": "\033[2m",
    "italic": "\033[3m",
    "underlined": "\033[4m",
    "fore": {"black": "\033[30m",
             "red": "\033[31m",
             "green": "\033[32m",
             "yellow": "\033[33m",
             "blue": "\033[34m",
             "purple": "\033[35m",
             "teal": "\033[36m",
             "gray": "\033[37m"},
    "back": {"black": "\033[40m",
             "red": "\033[41m",
             "green": "\033[42m",
             "yellow": "\033[43m",
             "blue": "\033[44m",
             "purple": "\033[45m",
             "teal": "\033[46m",
             "gray": "\033[47m"},
    "from-beginning": "\033[1;1H"
}

apple_colors = {
    1: format["fore"]["yellow"]+format["bold"],
    2: format["fore"]["red"]+format["bold"],
    3: format["fore"]["purple"]+format["bold"],
    4: format["fore"]["green"]+format["bold"],
    5: format["fore"]["teal"]+format["bold"],
}

theme = {
    "classic": format["regular"],
    "beta": format["fore"]["blue"]
}


class Screen:
    def __init__(self, format=format["regular"]):
        self.default = format
        self.clear()
        return

    def clear(self, fill=" "):
        self.matrix = [[fill]*console_size()[0]
                       for i in range(console_size()[1])]
        return

    def __repr__(self):
        stdout = format["from-beginning"] + self.default
        stdout += "\n".join(["".join(row) for row in self.matrix])
        return stdout

    def show(self, end=""):
        print(self, end=end)
        return

    def add_window(self, window):
        window.paused = False
        x_begin = window.pos[0]
        y_begin = window.pos[1]
        x_end = window.pos[0] + window.size[0] + 1
        y_end = window.pos[1] + window.size[1] + 1
        # Borders & Fill
        try:
            char_size = len(window.fill)
            for i in range(x_begin, x_end+1):
                if i < 1:
                    raise IndexError
                for j in range(y_begin, y_end+1):
                    if j < 1:
                        raise IndexError
                    if (x_begin < i < x_end) and (y_begin < j < y_end):
                        self.matrix[j-1][i-1] = window.fill_format + \
                            window.fill[i % char_size] + self.default
                    elif x_begin < i < x_end:
                        self.matrix[j-1][i-1] = window.border_format + \
                            window.horizontal + self.default
                    elif y_begin < j < y_end:
                        self.matrix[j-1][i-1] = window.border_format + \
                            window.vertical + self.default
                    elif i == x_begin and j == y_begin:
                        self.matrix[j-1][i-1] = window.border_format + \
                            window.corners[0] + self.default
                    elif i == x_end and j == y_begin:
                        self.matrix[j-1][i-1] = window.border_format + \
                            window.corners[1] + self.default
                    elif i == x_begin and j == y_end:
                        self.matrix[j-1][i-1] = window.border_format + \
                            window.corners[2] + self.default
                    elif i == x_end and j == y_end:
                        self.matrix[j-1][i-1] = window.border_format + \
                            window.corners[3] + self.default
            # Header
            pos = window.pos[0] + (window.size[0] - len(window.header)) // 2
            for char in window.header:
                self.matrix[y_begin-1][pos] = window.header_format + \
                    char + self.default
                pos += 1
            # Text
            for text, pos, size, format in window.text:
                for i in range(size):
                    self.matrix[y_begin+pos[1]-1][x_begin+pos[0] +
                                                  i-1] = format + text[i] + self.default

            # Snake
            if window.board:
                for i in range(window.board.size):
                    for j in range(window.board.size):
                        if window.board.mat[i][j]:
                            self.matrix[window.pos[1]+i][window.pos[0] +
                                                         j*2] = window.show_board(window.board.mat[i][j]) + self.default
                            self.matrix[window.pos[1]+i][window.pos[0] +
                                                         j*2+1] = window.show_board(window.board.mat[i][j]) + self.default
                        elif window.show_path and (i, j) in window.path:
                            self.matrix[window.pos[1]+i][window.pos[0] +
                                                         j*2] = window.show_board(0) + self.default
                            self.matrix[window.pos[1]+i][window.pos[0] +
                                                         j*2+1] = window.show_board(0) + self.default

            # Apples
            if window.apples:
                for apple, apple_code in window.apples:
                    self.matrix[window.pos[1]+apple[0]][window.pos[0] +
                                                        apple[1]*2] = window.show_board(-2, apple_code, i=0) + self.default
                    self.matrix[window.pos[1]+apple[0]][window.pos[0] +
                                                        apple[1]*2+1] = window.show_board(-2, apple_code, i=1) + self.default
        except IndexError:
            if window.main:
                window.paused = True
                pause = Window(size=(console_size()[0]-2, console_size()[1]-2))
                pause.text = []
                pause.add_text(text="PAUSED", pos=[
                               "m", ceil(console_size()[1]/2)-1])
                self.clear()
                self.add_window(pause)
            else:
                self.clear()
        return


class Window:
    paused = False
    show_path = False
    main = True
    board = None
    apples = []
    path = None
    text = []

    def __init__(self,  size, pos=("m", "m")):
        self.size = size
        self.set_pos(pos)
        self.set_border()
        self.set_fill()
        self.set_header(title="")
        self.shape = None
        return

    def set_board(self, size):
        self.board = Board(size)
        return

    def show_board(self, code, apple_code=None, i=None):
        if code >= 1:
            # return f"\033[38;5;{232+code//3}m█"
            return format["fore"]["blue"] + "█"
        elif code == 0:
            return format["dim"] + "░"
        elif code == -1:
            return format["regular"] + "█"
        elif code == -2:
            return apple_colors[apple_code] + apple_shapes[apple_prizes[apple_code][2]][i]
            # return format["fore"][choice(colors["apple"])] + "█"

    def set_pos(self, pos):
        pair = list(pos)
        if pair[0] == "m":
            pair[0] = (console_size()[0] - self.size[0]) // 2
        if pair[1] == "m":
            pair[1] = (console_size()[1] - self.size[1]) // 2
        self.pos = tuple(pair)
        return

    def add_text(self, text, pos, format=format["regular"]):
        if pos[0] == "l":
            pos[0] = 2
        elif pos[0] == "r":
            pos[0] = self.size[0] - len(text)
        elif pos[0] == "nr":
            pos[0] = self.size[0] - len(text) - 3
        elif pos[0] == "m":
            pos[0] = (self.size[0] - len(text)) // 2 + 1
        self.text.append((text, pos, len(text), format))
        return

    def set_border(self, vertical="│", horizontal="─", corners=("╭", "╮", "╰", "╯"), format=format["regular"]):
        self.vertical = vertical
        self.horizontal = horizontal
        self.corners = corners
        self.border_format = format
        return

    def set_header(self, title, format=format["regular"]):
        self.header = title
        self.header_format = format
        return

    def set_fill(self, fill=" ", format=format["regular"]):
        self.fill = fill
        self.fill_format = format
        return


def welcome(name="snake"):
    l = len(name)
    scr = Screen()
    welcome = Window(size=(10+l, 2), pos=("m", "m"))
    welcome.set_border(*borders["no-border"])
    new = [""] * l
    remaining = l
    progress = 0.0
    while progress < 12 or remaining > 0:
        if remaining > 0:
            remaining = 0
            for i in range(l):
                if new[i] != name[i]:
                    remaining += 1
                    new[i] = chr(randint(97, 122))
        if progress < 12:
            progress += 0.2
        welcome.text = []
        welcome.add_text(text="  ".join(new), pos=["m", 1],
                         format=format["fore"]["blue"])
        welcome.add_text(text="━"*(12+l), pos=[0, 2])
        welcome.add_text(text="━"*(l-remaining+int(progress)),
                         pos=[0, 2], format=format["fore"]["red"])
        welcome.set_pos(pos=("m", "m"))
        scr.clear()
        scr.add_window(welcome)
        scr.show()
        sleep(0.05)
    sleep(0.5)


def message(message, time, header=None, form=format["regular"], border=borders["no-border"]):
    scr = Screen()
    popup = Window(size=[25, 5])
    if header:
        popup.set_header(title=header, format=form)
    popup.set_border(*border)

    def key_press():
        popup.paused = True
        return
    add_hotkey("enter", key_press)

    while time > 0:
        if popup.paused:
            remove_all_hotkeys()
            return
        popup.text = []
        for t in range(len(message)):
            popup.add_text(text=message[t], pos=["m", t+2],
                           format=form)
        popup.set_pos(pos=("m", "m"))
        scr.clear()
        scr.add_window(popup)
        scr.show()
        sleep(0.05)
        time -= 0.05
    remove_all_hotkeys()
    return
