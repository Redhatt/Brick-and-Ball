import numpy as np
from _math_ import *
from colors import *
import pygame

class Spring:
    def __init__(self, k=1, beta=0.1, length=1, color=None):
        self.k = k
        self.beta = beta 
        self.length = length
        self.a = self.b = None
        self.force = 0.0
        self.stretch = 0.0
        self.v_ab = 0
        self.color = clr(color)
    
    def update(self):
        self.left = self.a.cm_pos
        self.right = self.b.cm_pos
        d, mag = unit(self.left - self.right, mag=True)
        self.stretch = mag - self.length
        self.v_ab = abs(vdot(d, self.a.vel - self.b.vel))
    

    def attach_to_shape(self, shape, end):
        if end == 'Left':
            self.a = shape
        elif end == 'Right':
            self.b = shape

    def adjust(self):
        self.length = norm(self.a.cm_pos - self.b.cm_pos)

    def attach(self, a, b, adjust=False):
        self.attach_to_shape(a, 'Left')
        self.attach_to_shape(b, 'Right')
        if adjust: self.adjust()
        self.update()

    def apply(self, t, dt):
        self.update()
        self.force = -self.stretch * self.k
        if self.force > 0:
            self.force -= self.beta * self.v_ab
        else:
            self.force += self.beta * self.v_ab
        
    def get(self, shape):
        return self.force * unit(shape.cm_pos - (self.left + self.right)/2)
    
    def draw(self, screen, scale, width=2):
        pygame.draw.line(screen, self.color, scale * self.left, scale * self.right, width)
    
class GravityWorld:
    def __init__(self, g=0.981, direction=np.array([0.0, 1.0])):
        self.g = g
        self.direction = direction
        self.apl = 0
    
    def apply(self, t, dt):
        self.apl = 1
    
    def get(self, shape):
        return (self.apl * self.g * shape.mass * self.direction)
    
    def draw(self, screen, scale):
        pass

class Drag:
    def __init__(self, k=0.55):
        self.k = k
        self.apl = 0
    
    def apply(self, t, dt):
        self.apl = 1
    
    def get(self, shape):
        return -shape.vel * self.k *self.apl
    
    def draw(self, screen, scale):
        pass

class DragAng(Drag):
    def __init__(self, k=0.11):
        Drag.__init__(self, k=k)
    
    def get(self, shape):
        return -shape.w * self.k * self.apl
    
    def draw(self, screen, scale):
        pass