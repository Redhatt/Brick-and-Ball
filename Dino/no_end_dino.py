import pygame
import random
import time
import os

folder = os.getcwd()
os.environ['SDL_VIDEO_WINDOW_POS'] = str('0' + "," + '10')

game = True
length = 900
breadth = 700
a = 1
b = 0

d_height = 100
d_width = 90
dx = 100
dy = breadth - d_height

cx, cy = 56, 115
bx, by = 90, 75
cxp = 100

b_height1 = 180
b_height2 = 135

compress = 45

UP = "up"
DOWN = "down"

bag1 = (pygame.Rect(length, breadth - cy, cx, cy), pygame.Rect(length, breadth - cy, cx + cxp, cy))
bag2 = (pygame.Rect(length, breadth - b_height1, bx, by), pygame.Rect(length, breadth - b_height2, bx, by))
box = []
container = []


class Dinosaur:
    def __init__(self):
        self.rect = pygame.Rect(dx, dy, d_width, d_height)
    load = 0
    speed = 0

    def gravity(self):
        g = 3
        self.speed -= g

    def jump(self, action):
        if action == UP and self.rect.y == breadth - d_height:
            self.speed = 35

    def motion(self):
        self.gravity()
        self.rect.y -= self.speed

        if self.rect.y > breadth - d_height:
            self.rect.y = breadth - d_height + self.load

    def duck(self, value=None):
        if value == DOWN:
            self.load = compress
            self.rect = pygame.Rect(dx, dy+self.load, 125, 55)
        elif value == "released":
            self.rect = pygame.Rect(dx, dy, d_width, d_height)
            self.load = 0


class Cactus:
    def __init__(self):
        self.rect = pygame.Rect(random.choice(bag1))

    speed = 17

    def motion(self):
        self.rect.x -= self.speed

    @classmethod
    def sped(cls, val):
        cls.speed += val

class Bird:
    def __init__(self):
        self.rect = pygame.Rect(random.choice(bag2))

    speed = 25

    def motion(self):
        self.rect.x -= self.speed

    @classmethod
    def sped(cls, val):
        cls.speed += val


def text_objects(text, font):
    textSurface = font.render(text, True, (125, 125, 125))
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',50)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((9*length/10),(1*breadth/10))
    screen.blit(TextSurf, TextRect)

    pygame.display.update()


def game_loop():
    global screen, FPS, run, length, breadth, a, b, d_height, d_width, dx, dy, cx, cy, bx, by, cxp, b_height1, b_height2, compress
    
    FPS = 40
    run = True
    UP = "up"
    DOWN = "down"

    bag1 = (pygame.Rect(length, breadth - cy, cx, cy), pygame.Rect(length, breadth - cy, cx + cxp, cy))
    bag2 = (pygame.Rect(length, breadth - b_height1, bx, by), pygame.Rect(length, breadth - b_height2, bx, by))
    box = []
    container = []
    pygame.init()
    pygame.display.set_caption("Dinosaur")
    screen = pygame.display.set_mode((length, breadth))
    clock = pygame.time.Clock()
    dino_image = pygame.image.load(folder+"\\dino_real.jpg").convert()
    dino_run = pygame.image.load(folder+"\\dino_run.jpg").convert()
    duck_run = pygame.image.load(folder+"\\duck.jpg").convert()
    cactus_image = pygame.image.load(folder+"\\cactus_real.jpg").convert()
    bunch_image = pygame.image.load(folder+"\\bunch_real.jpg").convert()
    bird_image = pygame.image.load(folder+"\\fly.jpg").convert()
    dino_image = pygame.transform.scale(dino_image, (90, d_height))
    bunch_image = pygame.transform.scale(bunch_image, (cx + cxp, cy))
    dino_run = pygame.transform.scale(dino_run, (90, d_height))
    dinosaur = Dinosaur()
    elapse = 0

    while run:
        global game
        clock.tick(FPS)
        screen.fill((245, 245, 245))
        dinosaur.motion()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                game = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False
                game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    dinosaur.jump('up')
                elif event.key == pygame.K_DOWN:
                    dinosaur.duck("down")
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    dinosaur.duck("released")
        if elapse%50 == 0 and random.randint(0, a) != 0:
            box.append(Cactus())

        if elapse%200 == 0 and random.randint(0, b) != 0:
            container.append(Bird())

        for i, j in enumerate(box):
            if dinosaur.rect.colliderect(j.rect):
                run = False
            if box[i].rect.x < 0:
                box.pop(i)
                del j
            else:
                j.motion()
                if j.rect[2] == cx + cxp:
                    screen.blit(bunch_image, (j.rect[0], j.rect[1]))
                else:
                    screen.blit(cactus_image, (j.rect[0], j.rect[1]))
                #pygame.draw.rect(screen, (200, 0, 0), j.rect, 1)

        for i, j in enumerate(container):
            if dinosaur.rect.colliderect(j.rect):
                run = False
            if container[i].rect.x < 0:
                container.pop(i)
                del j
            else:
                j.motion()
                screen.blit(bird_image, (j.rect[0], j.rect[1]))
                #pygame.draw.rect(screen, (200, 0, 0), j.rect, 1)

        if elapse % 6 > 3:
            screen.blit(dino_image, (dinosaur.rect[0], dinosaur.rect[1]))
        else:
            screen.blit(dino_run, (dinosaur.rect[0], dinosaur.rect[1]))

        if dinosaur.load == compress:
            screen.blit(duck_run, (dinosaur.rect[0], dinosaur.rect[1]))

        #pygame.draw.rect(screen, (200, 0, 0), dinosaur.rect, 1)
        if elapse % 600 == 0:
            Cactus.sped(5)
            Bird.sped(5)
            a += 1
            b += 1
            pygame.draw.rect(screen, (200, 0, 0), (0, 0, length, breadth), 30)
            pygame.display.flip()
            time.sleep(0.01)

        message_display(str(elapse))
        pygame.display.flip()
        elapse += 1
        

while game:
    game_loop()



