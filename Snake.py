import os
import sys
import time

from enum   import Enum, auto
from random import randint

from importlib.util import find_spec
if not find_spec("pynput"): os.system("pip install pynput")
from pynput.keyboard import Listener, Key


class Dir(Enum):
    Up    = auto()
    Left  = auto()
    Down  = auto()
    Right = auto()


class Snake:
    def __init__(self, W, H, T):
        if not (3 <= W <= 30) or not (3 <= H <= 30):
            print("Width and Height should be in range of (3, 30)")
            return

        self.W = W
        self.H = H

        self.over = False

        self.grid = [[(0, 0) for i in range(W)] for i in range(H)]

        self.now = Dir.Up
        self.nxt = Dir.Up

        self.size = 1
        self.head = (H//2, W//2)
        self.food = (-1, -1)

        self.grid[self.head[0]][self.head[1]] = (1, 1)

        Listener(on_press=self.on_press).start()
        while True:
            self.update()
            self.render()
            time.sleep(T/1000)

    def render(self):
        grid = "╔" + "═"*self.W + "╗\n"

        for y in self.grid:
            tmp = "║"

            for x in y:
                match x:
                    case ( 0,  0): tmp += " "
                    case (-1, -1): tmp += "@"

                    case (): tmp += "O"

                    case (1, 2) | (2, 1): tmp += "┛"
                    case (1, 3) | (3, 1): tmp += "┃"
                    case (1, 4) | (4, 1): tmp += "┗"
                    case (2, 3) | (3, 2): tmp += "┓"
                    case (2, 4) | (4, 2): tmp += "━"
                    case (3, 4) | (4, 3): tmp += "┏"

                    case (1, 1): tmp += "╹"
                    case (2, 2): tmp += "╸"
                    case (3, 3): tmp += "╻"
                    case (4, 4): tmp += "╺"

            grid += tmp + "║\n"
        grid += "╚" + "═"*self.W + "╝"

        sys.stdout.write("\n"*10 + grid)

    def update(self):
        if self.over: exit()
        y, x = self.head

        if self.grid[y][x] != (0, 0) and self.grid[y][x] != (-1, -1):
            self.over = True
            return

        self.place_food()
        pass

    def place_food(self):
        if self.food != (-1, -1): return

        while True:
            y = randint(0, self.H-1)
            x = randint(0, self.W-1)

            if self.grid[y][x] == (0, 0):
                self.grid[y][x] = (-1, -1)
                self.food = (y, x)
                return

    def on_press(self, key):
        match key:
            case Key.up:
                if self.now != Dir.Down:
                    self.nxt = Dir.Up

            case Key.left:
                if self.now != Dir.Right:
                    self.nxt = Dir.Left

            case Key.down:
                if self.now != Dir.Up:
                    self.nxt = Dir.Down

            case Key.right:
                if self.now != Dir.Left:
                    self.nxt = Dir.Right

            case Key.esc:
                self.over = True


def Input(msg="", default=None):
    while True:
        try: return int(input(msg))

        except KeyboardInterrupt: exit()
        except:
            if default: return default

            print("Wrong input, please type in integer!")


while True:
    Snake(
        Input("Width: "),
        Input("Height: "),
        Input("Interval(ms): ")
    )



