import pygame
import numpy as np

factor = np.sqrt(0.5)
f_length, f_breadth = (500, 400)
FPS = 60
limit_1 = 10
limit_2 = 10

Red = (139, 0, 0)


class dot():
	width 5
	radius = int(factor*width)
	intensity = 100

	def __init__(self, x = None, y=None):
		if x is None:
            self.x = np.random.randint(width, f_length - width)
            self.y = np.random.randint(width, f_breadth - width)
        else:
            self.x = x
            self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.width)
        self.velocity = np.array([np.random.randint(-limit1, limit1), np.random.randint(-limit1, limit1)])

    def motion(self):
    	self.velocity = self.updateVelocity():
    	self.rect.x += int(self.velocity[0])
        self.rect.y += int(self.velocity[1])

