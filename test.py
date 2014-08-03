import curses
import time

class Drawable(object):
    to_draw = []

    def __init__(self, x, y, x_size, y_size):
        self.x = x
        self.y = y
        self.x_size = x_size
        self.y_size = y_size

        self.to_draw.append(self)

    def erase(self):
        self.draw(" ")

    def draw(self, _chr="#"):
        for i in xrange(self.y_size):
            for j in xrange(self.x_size):
                win.addch(self.y + i, self.x + j, _chr)

    @classmethod
    def draw_all(cls):
        for d in cls.to_draw:
            d.draw()


class Player(Drawable):
    UP = 0
    DOWN = 1

    def __init__(self, x, y):
        super(Player, self).__init__(x, y, 1, 4)

    def move(self, direction):
        self.erase()
        if direction == self.UP:
            if self.y > 0:
                self.y -= 1
        elif direction == self.DOWN:
            if self.y + self.y_size < height:
                self.y += 1
        self.draw()

class Ball(Drawable):
    def __init__(self, x, y):
        self.direction = [-1, 1]
        super(Ball, self).__init__(x, y, 1, 1)

    def move(self):
        self.erase()
        self.x, self.y = [sum(i) for i in zip([self.x, self.y], self.direction)]

        if self.y >= height-self.y_size or self.y <= 0:
            self.direction[1] *= -1

        if self.x >= width-self.x_size or self.x <= 0:
            self.direction[0] *= -1

        self.draw()

import pingo

ard = pingo.arduino.get_arduino()
pin = ard.pins['A0']

try:
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()

    height, rwidth = stdscr.getmaxyx()
    width = rwidth # int(rwidth/1.5) # include a margin (to put name/score)?

    win = curses.newwin(height, width, 0, (rwidth-width)/2)
    # win = curses.newwin(height, width, begin_y, begin_x)

    #  These loops fill the pad with letters; this is
    # explained in the next section
    for y in range(0, height-1):
        for x in range(0, width-1):
            win.addch(y,x, " ")

    # the "ball"
    b = Ball(width/2, height/2)

    p1 = Player(0, 0)
    # p2 = Player(width-1, 0)

    # Draw everything
    win.refresh()

    time.sleep(1);

    while True:
        p1.erase()
        p1.y = int(round(pin.ratio() * (height-p1.y_size), 0))
        p1.draw()

        b.move()

        win.refresh()

        if b.x == 1 and b.direction[0] == -1:
            if b.y > p1.y and b.y < p1.y + p1.y_size:
                b.direction[0] = 1

        if b.x == 0: # or b.x == width-1:
            assert False, "game over!"

        if b.direction[0] == 1:
            time.sleep(.05)
        else:
            time.sleep(.10)

finally:
    # back to shell mode
    curses.reset_shell_mode()
    print
