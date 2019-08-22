# ================================================  Ball Jump is READY !!!! =======================================================
# =================================
# =================================
# =================================
# =================================
# =================================
# =================================


import pygame
from random import randint
from time import sleep
import os

numSize = 2
length, breadth = 900, 900
x1 = length - numSize * 7 - 5
x2 = x1 - numSize * 7 - 2
x3 = x2 - numSize * 7 - 2
x4 = x3 - numSize * 7 - 2
y1 = 10
plength, pwidth = 150, 30
px, py = randint(2, length - plength - 5), 850
ballWidth = 20
side = 10
radius = int(ballWidth / 2)
bx, by = int(px + plength / 2), int(py - ballWidth - 2)
wallSize = 30
FPS = 60

Brick = (0, 84, 84)
Grey = (128, 128, 128)
Black = (0, 0, 0)
Red = (139, 0, 0)
Blue = (103, 225, 225)
Green = (0, 240, 120)
Cyn = (0, 220, 220)
Magenta = (137, 0, 40)


class Ball:
    def __init__(self):

        self.rect = pygame.Rect(bx, by, ballWidth, ballWidth)

    xx = 0
    yy = 0
    half = int(ballWidth / 2)
    speed = 5

    def turn(self):

        if plank.rect.colliderect(self.rect):
            self.yy += 1

        for wall in walls:
            if wall.rect.collidepoint(self.rect[0] + self.half, self.rect[1]) or wall.rect.collidepoint(self.rect[0] +
                                                                                                        self.half,
                                                                                                        self.rect[
                                                                                                            1] + ballWidth):
                self.yy += 1

            if wall.rect.collidepoint(self.rect[0], self.rect[1] + self.half) or wall.rect.collidepoint(self.rect[0] +
                                                                                                        ballWidth,
                                                                                                        self.rect[
                                                                                                            1] + self.half):
                self.xx += 1

        for brick in fixWall:
            if brick.rect.collidepoint(self.rect[0] + self.half, self.rect[1]) or brick.rect.collidepoint(self.rect[0] +
                                                                                                          self.half,
                                                                                                          self.rect[
                                                                                                              1] + ballWidth):
                self.yy += 1

            if brick.rect.collidepoint(self.rect[0], self.rect[1] + self.half) or brick.rect.collidepoint(self.rect[0] +
                                                                                                          ballWidth,
                                                                                                          self.rect[
                                                                                                              1] + self.half):
                self.xx += 1

        return self.xx, self.yy

    def motion(self, pause):

        self.xx, self.yy = self.turn()
        if pause is False:
            if self.xx % 2 == 0:
                self.rect.x -= self.speed
            else:
                self.rect.x += self.speed

            if self.yy % 2 == 0:
                self.rect.y -= self.speed
            else:
                self.rect.y += self.speed


class Wall:
    def __init__(self, pos):
        self.pos = pos
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], wallSize, wallSize)

    def nothing(self):
        pass


class Danger:
    def __init__(self, pos):
        self.pos = pos
        dangers.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], wallSize, wallSize)


class fix:
    def __init__(self, pos):
        self.pos = pos
        fixWall.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], wallSize, wallSize)


class Plank:
    def __init__(self):
        self.rect = pygame.Rect(px, py, plength, pwidth)

    def move(self, dx):
        if dx != 0:
            self.axis(dx)

    def axis(self, dx):
        self.rect.x += dx

        for wall in walls:
            if wall.rect.colliderect(self.rect):
                if dx > 0:
                    self.rect.right = wall.rect.left
                elif dx < 0:
                    self.rect.left = wall.rect.right


class Numb:
    def __init__(self, pos):
        self.pos = pos
        numb.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], numSize, numSize)


pygame.init()
pygame.font.init()
pygame.display.set_caption("Ball Jump !!")
screen = pygame.display.set_mode((length, breadth))
clock = pygame.time.Clock()
walls = []
dangers = []
fixWall = []
player = Ball()
plank = Plank()

numbers = [["ooooooo",
            "o     o",
            "o     o",
            "o     o",
            "o     o",
            "o     o",
            "ooooooo", ],
           ["    o  ",
            "  ooo  ",
            "    o  ",
            "    o  ",
            "    o  ",
            "    o  ",
            " oooooo", ],
           [" oooo  ",
            "o    o ",
            "    o  ",
            "   o   ",
            "  o    ",
            " o     ",
            " oooooo", ],
           ["ooooooo",
            "     o ",
            "    o  ",
            "     o ",
            "      o",
            "      o",
            "oooooo ", ],
           ["  o   o",
            " o    o",
            "o     o",
            "ooooooo",
            "      o",
            "      o",
            "      o", ],
           ["ooooooo",
            "o      ",
            "oooooo ",
            "     o ",
            "     o ",
            "     o ",
            "oooooo ", ],
           ["ooooooo",
            "o      ",
            "o      ",
            "ooooooo",
            "o     o",
            "o     o",
            "ooooooo", ],
           ["ooooooo",
            "      o",
            "     o ",
            "    o  ",
            "   o   ",
            "   o   ",
            "   o   ", ],
           ["ooooooo",
            "o     o",
            "o     o",
            "ooooooo",
            "o     o",
            "o     o",
            "ooooooo", ],
           ["ooooooo",
            "o     o",
            "o     o",
            "ooooooo",
            "      o",
            "      o",
            "      o", ],
           ]


def counter(val, a, b):
    x = a
    y = b
    for rows in numbers[val]:
        for cols in rows:
            if cols == "o":
                Numb((x, y))
            x += numSize
        y += numSize
        x = a


def convert(no):
    count = str(no)

    if len(count) == 1:
        q2 = '0'
        q1 = '0'
        r = count[0]
    elif len(count) == 2:
        q2 = '0'
        q1 = count[0]
        r = count[1]

    elif len(count) == 3:
        q2 = count[0]
        q1 = count[1]
        r = count[2]

    return q2, q1, r


level = ["  **************************  ",  # 1
         "**#        ##      #########**",  # 2
         "*#  ##                      #*",  # 3
         "*#  ##  #####  #####    #   #*",  # 4
         "*#  ##         #####   ###   *",  # 5
         "*#  ##  #  ##  ####    ###   *",  # 6
         "*#  ##  # ###  ###     ######*",  # 7
         "*#  ##         ####   #      *",  # 8
         "*##     #####  ###   #    #  *",  # 9
         "*#      ####       ##    #   *",  # 10
         "*#      #############    #  #*",  # 11
         "*                            *",  # 12
         "*                            *",  # 13
         "*                            *",  # 14
         "*                            *",  # 15
         "*##  #   ####### # #####     *",  # 16
         "*##      ######    #####     *",  # 17
         "*####       ###       ##     *",  # 18
         "*######   # ########  ##     *",  # 19
         "*######     #######   ##     *",  # 20
         "*######     ######    ##     *",  # 21
         "*#####  #   ####      ##     *",  # 22
         "*                            *",  # 23
         "*                            *",  # 24
         "*                            *",  # 25
         "*                            *",  # 26
         "*                            *",  # 27
         "*                            *",  # 28
         "*                            *",  # 29
         "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  # 30
         ]

xx = 0
yy = 0
for row in level:
    for col in row:
        if col == "#":
            Wall((xx, yy))
        elif col == "*":
            fix((xx, yy))
        elif col == "x":
            Danger((xx, yy))
        xx += wallSize
    yy += wallSize
    xx = 0

folder = os.getcwd()
f = open(folder+'\\BallJump.txt', 'w+')
f.write('1')
f.close()
fr = open(folder+'\\BallJump.txt', 'r')
value = int(fr.read())
fr.close()


run = True
pause = True
q = 0
ii = 0

while run is True:

    clock.tick(FPS)

    numb = []

    q2, q1, r = convert(ii)
    counter(int(q2), x3, y1)
    counter(int(q1), x2, y1)
    counter(int(r), x1, y1)

    if ii < value:
        a2, a1, b = convert(value)
    else:
        a2, a1, b = convert(ii)
    counter(int(a2), x3 - 845, y1)
    counter(int(a1), x2 - 845, y1)
    counter(int(b), x1 - 845, y1)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            run = False

    player.motion(pause)
    key = pygame.key.get_pressed()
    if key[pygame.K_SPACE]:
        sleep(0.01)
        q += 1
        if q % 2 == 0:
            pause = False
        else:
            pause = True

    if key[pygame.K_LEFT]:
        plank.move(-side)

    if key[pygame.K_RIGHT]:
        plank.move(side)

    screen.fill(Black)
    for i, wall in enumerate(walls):
        pygame.draw.rect(screen, Brick, wall.rect)
        if wall.rect.colliderect(player.rect):
            player.motion(pause)
            del walls[i]
            ii += 1

    for numbs in numb:
        pygame.draw.rect(screen, Cyn, numbs.rect)

    for brick in fixWall:
        pygame.draw.rect(screen, Magenta, brick.rect)
        pass

    for danger in dangers:
        pygame.draw.rect(screen, Red, danger.rect)
        if danger.rect.colliderect(player.rect):
            sleep(1)
            run = False

    pygame.draw.rect(screen, Blue, plank.rect)
    pygame.draw.circle(screen, Green, (player.rect[0] + radius, player.rect[1] + radius), radius)
    pygame.display.flip()

    if run is False:
        f = open(folder+'\\BallJump.txt', 'r')
        if int(f.read()) < ii:
            f.close()
            fp = open(folder+'\\BallJump.txt', 'w')
            train = str(ii)
            fp.write(train)
            fp.close()

