import pygame, numpy as np, sys
from _math_ import *
time = pygame.time.get_ticks
ex = sys.exit

colors = {'red': (200, 0, 0), 'blue': (20, 50, 225), 'yellow': (255, 255, 0), 'white': (200, 200, 200), 
          'green': (10, 200, 50), 'black': (10, 10, 10), 'cyan': (0, 255, 255)}

length, breadth = 1000, 700
dim = np.array([500, 300])
FPS = 60
scale = 100

class Polygon:
    def __init__(self, vert: list, mass: float, mi: float, vel=np.array([0, 0], dtype=np.float32), w=0, e=1, move=True, color='red'):
        '''
        @param:vert-> list a 2d list with each vertix's coordinates
        @param:mass-> mass of the shape
        @param:mi-> moment of inertia of shape
        @param:vel-> initial velocity of the shape
        @param:w-> initial angular velocity of shape
        @param:color (string) color of the shape
        '''
        self.color = colors[color]
        self.type = type(self)
        self.move = move
        # mass inertia postions coff of restitution
        self.mass = mass
        self.mi = mi
        self.vert = [np.array(i, dtype=np.float32) for i in vert]
        self.e = e


        # velocities and angluar velocities
        self.vel = vel
        self.w = w

        # forces and torques
        self.forces = np.array([0.0, 0.0])
        self.torque = 0
        self.momentum = mass * self.vel
        self.ang_mom = mi * w

        # center of mass and orient
        self.cm_pos = centeriod(self.vert)
        self.cm_pos_last = self.cm_pos.copy()
        self.cm_pos_ang = 0
        self.cm_pos_ang_last = 0

    # to shift the shape
    def shift(self, shift):
        shift = np.array(shift)

        self.cm_pos += shift
        self.cm_pos_last += shift

        for i in range(len(self.vert)):
            self.vert[i] += shift

    # to turn the shape
    def turn(self, angle):
        self.cm_pos_ang += angle
        self.cm_pos_ang_last += angle

        rot_mat = np.array([[np.cos(angle), - np.sin(angle)], [np.sin(angle), np.cos(angle)]])
        for i in range(len(self.vert)):
            vert = self.vert[i] - self.cm_pos
            vert = rot_mat@vert
            self.vert[i] = vert + self.cm_pos

    # to place the shape at desired location
    def place(self, pos):
        pos = np.array(pos)
        delta = pos - self.cm_pos
        self.shift(delta)

    # to tune the shape at desired orientation
    def orient(self, angle):
        delta =angle - self.cm_pos_ang
        self.turn(delta)
        
    # draw utility method
    def draw(self, screen, cm=True):
        con = [(int(scale*i[0]), int(scale*i[1])) for i in self.vert]
        cen = (int(scale*self.cm_pos[0]), int(scale*self.cm_pos[1]))
        pygame.draw.polygon(screen, self.color, con)
        if cm:
            pygame.draw.circle(screen, colors['black'], cen, 2)

    # translation method used in motion dynamics
    def translatation(self):
        delta = self.cm_pos - self.cm_pos_last
        for i in range(len(self.vert)):
            self.vert[i] += delta

    # rotation method used in motion dynamics
    def rotation(self):
        angle = self.cm_pos_ang - self.cm_pos_ang_last
        rot_mat = np.array([[np.cos(angle),   np.sin(angle)], 
                            [-np.sin(angle),  np.cos(angle)]])
        for i in range(len(self.vert)):
            vert = self.vert[i] - self.cm_pos
            vert = rot_mat@vert
            self.vert[i] = vert + self.cm_pos

    # to simulate impulse force on the shape
    def impulse_force(self, p):
        '''
        @param: p-> impulse momentum (numpy.array with shape (2, ))
        '''
        self.vel += p/self.mass

    # to simulate impulse turque on the shape
    def impulse_torque(self, t):
        '''
        @param: t-> impulse anglur momentum (float)
        '''
        self.w += t/self.mi

    # utitlity method to calculate the both linear and angular postions and velocities of the shape
    def motion_dynamics(self, t, dt=1, forces_func=None, torque_func=None):
        '''
        @param: t-> time in msec (int)
        @param: dt-> delta time in msec (int)
        TODO: yet to decide
        '''
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

        self.translatation()
        self.rotation()

    # finds furthest point in some direction
    def find_furthest(self, direction=np.array([1.0, 0.0]), dot=False, index=False):
        '''
        @param: direction-> directions in which to find the farthest point
        ereturn: point-> 2D point (numpy.array shape (2, )) 
        '''
        max_d = -float('inf')
        max_point = None
        ind = 0
        for i, vert in enumerate(self.vert):
            val = np.dot(vert, direction)
            if val > max_d:
                max_d = val
                max_point = vert
                ind = i
        if index: return ind
        if dot: return max_d
        return max_point


class Line(Polygon):

    def normal(self):
        return normal(self.vert[1] - self.vert[0], normalize=True)

    def draw(self, screen, cm=True, width=5):
        start_pos, end_pos = [(int(scale*i[0]), int(scale*i[1])) for i in self.vert]
        cen = (int(scale*self.cm_pos[0]), int(scale*self.cm_pos[1]))
        pygame.draw.line(screen, self.color, start_pos, end_pos, width)
        if cm:
            pygame.draw.circle(screen, colors['black'], cen, width//2)


def solver(a, b, n, dis, contact):
    # reltive positions from com of shapes to contact
    r_ap = contact - a.cm_pos
    r_bp = contact - b.cm_pos

    # v_ap = v_acom + w_a * r_ap  and v_bp = v_bcom + w_b * r_bp
    v_ap = a.vel + a.w * normal(r_ap)
    v_bp = b.vel + b.w * normal(r_bp)

    # v_ab = v_ap - v_bp
    v_ab = v_ap - v_bp

    e = (a.e * b.e)/2
    numerator = -(1 + e)*np.dot(v_ab, n)

    if (not a.move) and b.move:
        denominator = (1/b.mass) + (np.dot(normal(r_bp), n)**2) / b.mi
        J =  (numerator / denominator)*n
        T_b = cross(J, r_bp)
        b.impulse_force(-J)
        b.impulse_torque(-T_b)
        k = 1

    elif a.move and (not b.move):
        denominator = (1/a.mass) + (np.dot(normal(r_ap), n)**2) / a.mi
        J =  (numerator / denominator)*n
        T_a = cross(J, r_ap)
        a.impulse_force(J)
        a.impulse_torque(T_a)
        k = 0
        
    else:
        denominator = (1/a.mass + 1/b.mass) + (np.dot(normal(r_ap), n)**2) / a.mi + (np.dot(normal(r_bp), n)**2) / b.mi
        J =  (numerator / denominator)*n
        T_a = cross(J, r_ap)
        T_b = cross(J, r_bp)
        a.impulse_force(J)
        b.impulse_force(-J)
        a.impulse_torque(T_a)
        b.impulse_torque(-T_b)
        k = a.mass / (a.mass + b.mass)

    a.shift(-dis*(1-k)*n)
    b.shift((dis*k*n))


# utility functions to stick text on screen
def text(screen, text, x, y, size=10, font_type='freesansbold.ttf', color=colors['black']):
    '''
    @param:screen object 
    @param:text to stick 
    @param:x rect position
    @param:y rect position
    @param:size size of the text
    @param:font_type
    @param:color
    '''
    text = str(text)
    font = pygame.font.Font(font_type, size)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))

 
 # TODO: froces yet to decide 
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

def draw_points(screen, points, size=5):
    for i in points:
        pygame.draw.circle(screen, colors['black'], i*scale, size)

if __name__ == '__main__':
    # ve = [[1, 1], [2, 1], [2, 4], [1, 4], [0.5, 2]]
    # p = Polygon(ve, 200, 200)

    ve = [[1,1], [2, 2]]
    p = Line(ve, 200, 200)

    # impulses
    # p.impulse_force(np.array([100, 50], dtype=np.float32))
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