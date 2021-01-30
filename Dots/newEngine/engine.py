import pygame, numpy as np, sys
from _math_ import *
from colors import *
time = pygame.time.get_ticks
ex = sys.exit

length, breadth = 1000, 700
FPS = 60
scale = 20

class Polygon:
    def __init__(self, vert: list, mass: float, mi: float, points=[], cm_pos=None, vel=np.array([0, 0], dtype=np.float64), w=0, e=1, move=True, color=None, type='Polygon', mu=0.1):
        '''
        @param:vert-> list a 2d list with each vertix's coordinates
        @param:mass-> mass of the shape
        @param:mi-> moment of inertia of shape
        @param:vel-> initial velocity of the shape
        @param:w-> initial angular velocity of shape
        @param:color (string) color of the shape
        '''
        self.color = clr(color)
        self.type = type
        self.move = move
        self.tol_v = 0.005
        self.tol_w = 0.005


        # mass inertia postions coff of restitution
        self.mass = mass
        self.mi = mi
        self.vert = [np.array(i, dtype=np.float64) for i in vert]
        self.points = [np.array(i, dtype=np.float64) for i in points]
        self.e = e
        self.mu = mu

        # velocities and angluar velocities
        self.vel = vel
        self.w = w
        self.acc = np.array([0.0, 0.0])
        self.acc_ang = 0

        # forces and torques
        self.force_func = set()
        self.torque_func = set()

        # center of mass and orient
        self.cm_pos = centroid(self.vert) if cm_pos is None else np.array(cm_pos, dtype=np.float64)
        self.cm_pos_last = self.cm_pos.copy()
        self.cm_ang = 0
        self.cm_ang_last = 0
    
    def scale(self, s, cent=None):
        cent = centroid(self.vert) if cent is None else cent
        for i in range(len(self.vert)):
            self.vert[i] = s*(self.vert[i] - cent) + cent
        
        for i in range(len(self.points)):
            self.points[i] = s*(self.points[i] - cent) + cent
            

    # to shift the shape
    def shift(self, shift):
        shift = np.array(shift)

        self.cm_pos += shift
        self.cm_pos_last += shift

        for i in range(len(self.vert)):
            self.vert[i] += shift
        
        for i in range(len(self.points)):
            self.points[i] += shift

    # to turn the shape
    def turn(self, angle):
        self.cm_ang += angle
        self.cm_ang_last += angle

        rot_mat = np.array([[np.cos(angle), - np.sin(angle)], [np.sin(angle), np.cos(angle)]])
        for i in range(len(self.vert)):
            vert = self.vert[i] - self.cm_pos
            vert = vrot(rot_mat, vert)
            # vert = rot_mat@vert
            self.vert[i] = vert + self.cm_pos
        
        for i in range(len(self.points)):
            vert = self.points[i] - self.cm_pos
            vert = vrot(rot_mat, vert)
            # vert = rot_mat@vert
            self.points[i] = vert + self.cm_pos


    # to place the shape at desired location
    def place(self, pos):
        pos = np.array(pos)
        delta = pos - self.cm_pos
        self.shift(delta)

    # to tune the shape at desired orientation
    def orient(self, angle):
        delta =angle - self.cm_ang
        self.turn(delta)
        
    # draw utility method
    def draw(self, screen, cm=True, dot_color='black'):
        con = [(int(scale*i[0]), int(scale*i[1])) for i in self.vert]
        cen = (int(scale*self.cm_pos[0]), int(scale*self.cm_pos[1]))
        pygame.draw.polygon(screen, self.color, con)
        points = [(int(scale*i[0]), int(scale*i[1])) for i in self.points]
        for i in points:
            pygame.draw.circle(screen, clr(dot_color), i, 2)
        if cm:
            pygame.draw.circle(screen, clr(dot_color), cen, 2)

    # translation method used in motion dynamics
    def translatation(self):
        delta = self.cm_pos - self.cm_pos_last
        for i in range(len(self.vert)):
            self.vert[i] += delta
        
        for i in range(len(self.points)):
            self.points[i] += delta

    # rotation method used in motion dynamics
    def rotation(self):
        angle = self.cm_ang - self.cm_ang_last
        rot_mat = np.array([[np.cos(angle),   np.sin(angle)], 
                            [-np.sin(angle),  np.cos(angle)]])
        for i in range(len(self.vert)):
            vert = self.vert[i] - self.cm_pos
            vert = vrot(rot_mat, vert)
            # vert = rot_mat@vert
            self.vert[i] = vert + self.cm_pos
        
        for i in range(len(self.points)):
            vert = self.points[i] - self.cm_pos
            vert = vrot(rot_mat, vert)
            # vert = rot_mat@vert
            self.points[i] = vert + self.cm_pos

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

    def attach_force(self, func):
        self.force_func.add(func.get)

    def attach_torque(self, func):
        self.torque_func.add(func.get)

    # utitlity method to calculate the both linear and angular postions and velocities of the shape
    def motion_dynamics(self, t, dt=1):
        '''
        @param: t-> time in msec (int)
        @param: dt-> delta time in msec (int)
        TODO: yet to decide
        '''
        # storing last postions 
        self.cm_pos_last = self.cm_pos.copy()
        self.cm_ang_last = self.cm_ang

        # getting acc from superpostions of applied forces and torques
        for force in self.force_func:
            self.acc += force(self) / self.mass
        
        for torque in self.torque_func:
            self.acc_ang += torque(self) / self.mi

        # linear and angular integration
        Linear_integrator(self, dt)
        angular_integrator(self, dt)

        self.acc = np.array([0.0, 0.0])
        self.acc_ang = 0.0
        if norm(self.vel) < self.tol_v:
            self.vel = np.array([0.0, 0.0])
        
        if abs(self.w) < self.tol_w:
            self.w = 0.0

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
            val = vdot(vert, direction)
            if val > max_d:
                max_d = val
                max_point = vert
                ind = i
        if index: return ind
        if dot: return max_d
        return max_point


class Line(Polygon):
    def __init__(self, vert: list, mass: float, mi: float, vel=np.array([0, 0], dtype=np.float64), w=0, e=1, move=True, color=None, type='Line', mu=0.1):
        Polygon.__init__(self, vert=vert, mass=mass, mi=mi, vel=vel, w=w, e=e, move=move, color=color, type=type, mu=mu)

    def normal(self):
        return normal(self.vert[1] - self.vert[0], nrm=True)

    def along(self):
        return unit(self.vert[1] - self.vert[0])

    def draw(self, screen, cm=True, width=5, dot_color='black'):
        start_pos, end_pos = [(int(scale*i[0]), int(scale*i[1])) for i in self.vert]
        cen = (int(scale*self.cm_pos[0]), int(scale*self.cm_pos[1]))
        pygame.draw.line(screen, self.color, start_pos, end_pos, width)
        if cm:
            pygame.draw.circle(screen, clr(dot_color), cen, width//2)

class Cirlce(Polygon):
    def __init__(self, center, radius, mass, mi, points=[], vel=np.array([0, 0], dtype=np.float64), w=0, e=1, move=True, color=None, type='Circle', mu=0.1):
        self.radius = radius
        Polygon.__init__(self, vert=[], mass=mass, mi=mi, cm_pos=center, vel=vel, w=w, e=e, move=move, color=color, type=type, mu=mu)
        self.points = points + [self.find_furthest()]

    def scale(self, s):
        Polygon.scale(self, s, cent=self.cm_pos)
        self.radius = s * self.radius

    # to draw
    def draw(self, screen, cm=True, dot_color='black'):
        cen = (int(scale*self.cm_pos[0]), int(scale*self.cm_pos[1]))
        pygame.draw.circle(screen, self.color, cen, scale*self.radius)
        points = [(int(scale*i[0]), int(scale*i[1])) for i in self.points]
        for i in points:
            pygame.draw.circle(screen, clr(dot_color), i, 2)

    # finds furthest point in some direction
    def find_furthest(self, direction=np.array([1.0, 0.0]), dot=False, index=False):
        '''
        @param: direction-> directions in which to find the farthest point
        ereturn: point-> 2D point (numpy.array shape (2, )) 
        '''
        max_d = self.radius * norm(direction)
        max_point = self.radius * unit(direction) + self.cm_pos

        if dot: return max_d
        return max_point[:]

def Linear_integrator(shape, dt=0.1):
    # semi-implicit eularian
    shape.vel += shape.acc * dt
    shape.cm_pos += shape.vel * dt

def angular_integrator(shape, dt=0.1):
    # semi-implicit eularian
    shape.w += shape.acc_ang * dt 
    shape.cm_ang += shape.w * dt

def solver(a, b, n, dis, contact, tol=0.01):
    # reltive positions from com of shapes to contact
    r_ap = contact - a.cm_pos
    r_bp = contact - b.cm_pos

    # v_ap = v_acom + w_a * r_ap  and v_bp = v_bcom + w_b * r_bp
    v_ap = a.vel + a.w * normal(r_ap)
    v_bp = b.vel + b.w * normal(r_bp)

    # v_ab = v_ap - v_bp
    v_ab = v_ap - v_bp

    e = (a.e * b.e)/2
    mu = (a.mu + b.mu)/2
    along = normal(n, v_ab)
    v_al = vdot(v_ab, along)
    if v_al < tol: v_al = 0.0
    else: v_al = 1.0
    numerator = -(1 + e)*vdot(v_ab, n)

    if (not a.move) and b.move:
        denominator = (1/b.mass) + (vdot(normal(r_bp), n)**2) / b.mi
        J = (numerator / denominator)*(n + along*mu*v_al)
        T_b = cross(J, r_bp)
        b.impulse_force(-J)
        b.impulse_torque(-T_b)
        k = 1

    elif a.move and (not b.move):
        denominator = (1/a.mass) + (vdot(normal(r_ap), n)**2) / a.mi
        J =  (numerator / denominator)*(n + along*mu*v_al)
        T_a = cross(J, r_ap)
        a.impulse_force(J)
        a.impulse_torque(T_a)
        k = 0
        
    else:
        denominator = (1/a.mass + 1/b.mass) + (vdot(normal(r_ap), n)**2) / a.mi + (vdot(normal(r_bp), n)**2) / b.mi
        J =  (numerator / denominator)*(n + along*mu*v_al)
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
def text(screen, text, x, y, size=10, font_type='freesansbold.ttf', color='black'):
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
    text = font.render(text, True, clr(color))
    screen.blit(text, (x, y))

 
def draw_points(screen, points, size=5, color='black'):
    for i in points:
        pygame.draw.circle(screen, clr(color), i*scale, size)

if __name__ == '__main__':
    # ve = [[1, 1], [2, 1], [2, 4], [1, 4], [0.5, 2]]
    # p = Polygon(ve, 200, 200)

    ve = [[1,1], [2, 2]]
    p = Line(ve, 200, 200)

    # impulses
    # p.impulse_force(np.array([100, 50], dtype=np.float64))
    p.impulse_torque(10)

    p.attach_force(spring)
    p.attach_force(gravity_world)
    p.attach_torque(ang_spring)
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

        screen.fill(clr('white'))

        p.draw(screen)    
        p.motion_dynamics(time())
        text(screen, f"FPS: {1000 // (ff)}, T: {ff} ms", 600, 10)
        pygame.display.flip()
        end = time()
        if (time()%10 == 0): 
            ff = end - start