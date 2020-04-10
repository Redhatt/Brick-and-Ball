import pygame
import numpy as np
import time

factor = np.sqrt(0.5)
length, breadth = 1500, 800
FPS = 60

Red = (139, 0, 0)
Blue = (70, 20, 225)
Yellow = (120, 120, 0)
origin = (0, 0, 0)
xAxis = (1,0,0)
yAxis = (0,1,0)

pygame.init()
pygame.font.init()
pygame.display.set_caption("Maps!")
screen = pygame.display.set_mode((length, breadth))
clock = pygame.time.Clock()
# pygame.event.get()
# pygame.mouse.get_rel()
# pygame.mouse.set_visible(1)
# pygame.event.set_grab(1)
run = True
lines = []
black = (110,110,110)
count = 0
center = (length//2, breadth//2)
while run:
    clock.tick(FPS)
    screen.fill((200, 200, 200))
    pygame.draw.circle(screen, black, center, 3)
    x, y = pygame.mouse.get_pos()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            run = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_s:
            with open("mapFile.txt", 'w') as file:
                if len(lines)>=2:
                    for i in range(0, len(lines), 2):
                        value1, value2 = lines[i], lines[i+1]
                        file.write(str((-value1[0]+center[0], value1[1]-center[1]))+ " "+str((value2[0]-center[0], value2[1]-center[1])))
                        #file.write("@")


    click = pygame.mouse.get_pressed()

    if click == (1,0,0):
        time.sleep(0.3)
        #x, y = pygame.mouse.get_pos()
        count+=1
        lines.append((x,y))


    elif click == (0,0,1):
        time.sleep(0.3)
        for i in range(2):
            if len(lines):
                lines.pop()
        x0, y0 = x, y
        count -= 1

    if count%2 == 1:
        #print("hello")
        if lines:
            pygame.draw.line(screen, black, lines[-1], (x,y), 5)

            font = pygame.font.Font('freesansbold.ttf', 12)
            text = font.render(f"{x, y}", True,(100,20,20))
            textRect = text.get_rect()
            textRect.center = (x,y)
            screen.blit(text, textRect)


    if len(lines)>=2:
        for i in range(0, len(lines)-1, 2):
            pygame.draw.line(screen, black, lines[i], lines[i+1], 5)

            font = pygame.font.Font('freesansbold.ttf', 12)
            text = font.render(f"{lines[i]}", True,(220,0,0))
            textRect = text.get_rect()
            textRect.center = lines[i]
            screen.blit(text, textRect)

            font = pygame.font.Font('freesansbold.ttf', 12)
            text = font.render(f"{lines[i+1]}", True,(220,0,0))
            textRect = text.get_rect()
            textRect.center = lines[i+1]
            screen.blit(text, textRect)

    pygame.display.flip()
