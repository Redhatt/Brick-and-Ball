import pygame, numpy as np, sys
from pygame import *
time = pygame.time.get_ticks
ex = sys.exit

# WORK FLOW: 
#   Classes: (Ball, Polygon, Rectangle, Line)
#   Methods: insertions_sort, text, update_collision, collision_detection, isCollision

colors = {'red': (139, 0, 0), 'blue': (70, 20, 225), 'yellow': (120, 120, 0), 'white': (200, 200, 200),
           'black': (10, 10, 10)}

length, breadth = 1000, 700
dim = np.array([500, 300])
FPS = 60
scale = 100

def cm_cal(vert: list):
    x, y = 0, 0
    n = len(vert)
    if n == 0:
        raise "vetix container empty !"
    for i in vert:
        x += i[0]
        y += i[1]
    return np.array([x/n, y/n])


class polygon:
    def __init__(self, vert: list, mass: float, mi: float, vel=np.array([0, 0], dtype=np.float32), w=0, color='red'):
        self.color = colors[color]

        # mass inertia postions
        self.mass = mass
        self.mi = mi
        self.vert = [np.array(i, dtype=np.float32) for i in vert]


        # velocities and angluar velocities
        self.vel = vel
        self.w = w

        # forces and torques
        self.forces = np.array([0.0, 0.0])
        self.torque = 0
        self.momentum = mass * self.vel
        self.ang_mom = mi * w

        # center of mass
        self.cm_pos = cm_cal(self.vert)
        self.cm_pos_last = self.cm_pos
        self.cm_pos_ang = 0
        self.cm_pos_ang_last = 0


    def draw(self, screen, cm=True):
        con = [(int(scale*i[0]), int(scale*i[1])) for i in self.vert]
        cen = (int(scale*self.cm_pos[0]), int(scale*self.cm_pos[1]))
        pygame.draw.polygon(screen, self.color, con)
        if cm:
            pygame.draw.circle(screen, colors['black'], cen, 2)

    def translate(self):
        delta = self.cm_pos - self.cm_pos_last
        for i in range(len(self.vert)):
            self.vert[i] += delta

    def rotate(self):
        angle = self.cm_pos_ang - self.cm_pos_ang_last
        rot_mat = np.array([[np.cos(angle), - np.sin(angle)], [np.sin(angle), np.cos(angle)]])
        for i in range(len(self.vert)):
            vert = self.vert[i] - self.cm_pos
            vert = rot_mat@vert
            self.vert[i] = vert + self.cm_pos

    def impulse_force(self, p):
        self.vel += p/self.mass

    def impulse_torque(self, t):
        self.w += t/self.mi

    def motion_dynamics(self, t, dt=1, forces_func=None, torque_func=None):

        # storing last postions 
        e = self.cm_pos
        a = self.cm_pos_ang

        # linear
        acc = self.forces / self.mass
        vel_half = self.vel + 0.5 * acc * dt

        self.cm_pos = self.cm_pos + (vel_half) * dt

        # linear motion dependent forces calcuations 
        acc_= np.array([0, 0], dtype=np.float32)
        if forces_func is None:
            acc_ = acc
        else:
            for fun in forces_func:
                acc_ += fun(t, self.cm_pos, self.vel, self.mass) / self.mass
        self.vel = vel_half + (0.5 * acc_ * dt)

        # angular
        acc_ang = self.torque / self.mi
        w_half = self.w + 0.5 * acc_ang * dt

        self.cm_pos_ang = self.cm_pos_ang + (w_half) * dt

        # angular motion dependent torque calcuations 
        acc_ang_ = 0
        if torque_func is None:
            acc_ang_ = acc_ang
        else:
            for fun in torque_func:
                acc_ang_ += fun(t, self.cm_pos_ang, self.w, self.mi) / self.mi
        self.w = w_half + (0.5 * acc_ang_ * dt)

        # updating last positions
        self.cm_pos_last = e
        self.cm_pos_ang_last = a

        self.translate()
        self.rotate()

def Collide(a, b):
    pass

def collision_detection(collection):
    pass



def text(screen, text, x, y, size=10, font_type='freesansbold.ttf', color=colors['black']):
    text = str(text)
    font = pygame.font.Font(font_type, size)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))

 
def spring(t, pos, vel, mass):
    # origin
    org = np.array([2, 2], dtype=np.float32)
    # spring cosntants
    k = np.array([5, 4])
    # betas
    beta = np.array([1, 2], dtype=np.float32)

    # equations
    d = pos - org
    force = np.multiply(-d, k) + np.multiply(-vel, beta)
    return force

def ang_spring(t, theta, w, mi):
    # origin
    org = 1.0
    # spring cosntants
    k = 2
    # betas
    beta = 1

    # equations
    d = theta - org
    torque = (-k * theta) + (-w * beta)
    return torque

def gravity_world(t, pos, vel, mass):
    g = 0.001
    return np.array([0, g*mass], dtype=np.float32)


if __name__ == '__main__':
    ve = [[1, 1], [2, 1], [2, 4], [1, 4], [0.5, 2]]
    p = polygon(ve, 200, 200)

    # impulses
    p.impulse_force(np.array([100, 50], dtype=np.float32))
    p.impulse_torque(10)

    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Nuclear Reaction !")
    screen = pygame.display.set_mode((length, breadth))
    clock = pygame.time.Clock()
    run = True
    start, end = 0, 0
    ff = 1 # frame frame
    while run:
        start = time()
        clock.tick(FPS)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                run = False

        screen.fill(colors['white'])

        p.draw(screen)    
        p.motion_dynamics(time(), forces_func=[spring], torque_func=[ang_spring])
        text(screen, f"FPS: {1000 // (ff)}, T: {ff} ms", 600, 10)
        pygame.display.flip()
        end = time()
        if (time()%10 == 0): 
            ff = end - start
            