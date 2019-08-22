import pygame
import random
import numpy as np
import time 

run = True
speed_limit = 50
spawn = 100
length , breadth = 1400, 1000
FPS = 60
dot_width = 30
dot_x, dot_y = random.randint(0, 900), random.randint(0, 700)
RED = (200, 40, 40)
WHITE = (180, 180, 180)
YELLOW = (200, 200, 10)
sleep_time = 0.5
main_dot = (500, 300)
W2 = 2

class Dot:
	def __init__(self):
		self.rect = pygame.Rect(dot_x, dot_y, dot_width, dot_width)
		self.velocity = np.zeros((1, 2))
		self.dead = False
		self.dist = None

#-----------------------------------------------------------------------------
# to control motion.........
	def motion(self):
		if np.linalg.norm(self.velocity) < speed_limit:
			self.rect.x += int(self.velocity[0, 0])
			self.rect.y += int(self.velocity[0, 1])
		else:
			self.velocity * (speed_limit / np.linalg.norm(self.velocity))

		if (self.rect.x < 0) or (self.rect.x > length - dot_width):
			self.dead = True

		if (self.rect.y) < 0 or (self.rect.y > breadth - dot_width):
			self.dead = True

#-----------------------------------------------------------------------------
# to control random postion and velocity.....
	def randomize(self):
		self.velocity = np.array([[np.random.randint(-speed_limit, speed_limit),np.random.randint(-speed_limit, speed_limit)]])
		self.rect.x, self.rect.y = random.randint(0, length - spawn), random.randint(0, spawn)
		
#-----------------------------------------------------------------------------
# to return distances such as distance from main dot and walls, to AI......
	def distance(self):
		self.dist = np.linalg.norm(np.array([[self.rect.x, self.rect.y]]) - np.array([[main_dot[0], main_dot[1]]]))
		self.vwLeft = self.rect.x
		self.vwRight = length - self.rect.x 
		self.hwBottom = breadth - self.rect.y
		self.hwTop = self.rect.y
		return self.dist
#-----------------------------------------------------------------------------
	def velocities(self):
		self.velocity -= 0 * np.array([[self.rect.x, self.rect.y]]) - np.array([[main_dot[0], main_dot[1]]])
# 
pygame.init()
pygame.display.set_caption("DOT !")
screen = pygame.display.set_mode((length, breadth))
clock = pygame.time.Clock()

dots = []
for i in range(10):
	dots.append(Dot())
	dots[i].randomize()

while run:
	clock.tick(FPS)
	screen.fill(WHITE)
	for dot in dots:
		dot.motion()
		dot.velocities()
		pygame.draw.circle(screen, (RED), (int(dot.rect.x + dot_width /2), int(dot.rect.y + dot_width / 2)), int(dot_width / 2))
		if dot.dead is True:
			del dot

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.KEYDOWN and event.type == pygame.K_ESCAPE:
			run = False
		
	pygame.draw.circle(screen, (YELLOW), main_dot, 50)
	pygame.display.flip()
	



