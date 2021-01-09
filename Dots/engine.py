import pygame, numpy as np

# WORK FLOW: 
#   Classes: (Ball, Polygon, Rectangle, Line)
#   Methods: insertions_sort, text, update_collision, collision_detection, isCollision

colors = {'red': (139, 0, 0), 'blue': (70, 20, 225), 'yellow': (120, 120, 0), 'white': (200, 200, 200),
           'black': (10, 10, 10)}

length, breadth = 700, 500
dim = np.array([500, 300])
factor = np.sqrt(0.5)
limit = 10
g = 0.0


class Ball:
    radius = 20
    mass = 100
    color = colors['white']
    def __init__(self, pos, velocity):
        self.pos = pos
        self.velocity = np.array(velocity)

    def motion(self):

        # gravity 
        self.velocity[1] += g

        # boundary constraints 
        if 10 + self.radius > self.pos[0]:
            self.velocity[0] = -self.velocity[0]
            self.pos[0] = 10 + self.radius

        elif length - 10 - self.radius < self.pos[0]:
            self.velocity[0] = -self.velocity[0]
            self.pos[0] = length - 10 - self.radius

        if 10 + self.radius > self.pos[1]:
            self.velocity[1] = -self.velocity[1]
            self.pos[1] = 10 + self.radius

        elif breadth - 10 - self.radius < self.pos[1]:
            self.velocity[1] = -self.velocity[1]
            self.pos[1] = breadth - 10 - self.radius

        # updating 
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, tuple(map(int, self.pos)), self.radius)


class Polygon:
    def __init__(self, vertices=[]):
        self.vertices = vertices
        self.make_polygon()

    def motion(self):
        # gravity 
        self.velocity[1] += g

        # updating
        for i in range(len(self.vertices)):
            self.vertices[i][0] += self.velocity[0]
            self.vertices[i][1] += self.velocity[1]

        # boundary constraints
        

    def make_polygon(self):
        # getting left most point
        left = min(self.vertices, key=lambda x: x[0])
        # sorting counter-clock wise
        self.vertices.sort(key=lambda x: (x[1] - left[1])/(x[0] - left[0]) if x != left else -1e10)

    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.vertices)


class Rectangle:
    color = colors['black']
    e_ = 1
    def __init__(self, rect=None):
        if rect is None:
            self.rect = pygame.Rect(100, 100, 100, 100)
        else: 
            self.rect = rect



# only takes O(n) approx, when elements are almost sorted
def insertion_sort(lis, atr):
    for i in range(len(lis)):
        key = lis[i]
        j = i-1
        while j>=0 and getattr(lis[j+1], atr)>getattr(key, atr):
            lis[j+1] = lis[j]
            j-=1
        lis[j+1] = key


def text(screen, text, x, y, size=10, font_type='freesansbold.ttf', color=colors['black']):
    text = str(text)
    font = pygame.font.Font(font_type, size)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))

def update_collision(a, b):
    # if a.mass > b.mass: a, b = b, a
    velocity1, velocity2, pos1, pos2, radius1, radius2, mass1, mass2 = a.velocity, b.velocity, \
            a.pos, b.pos, a.radius, b.radius, a.mass, b.mass

    ratio = mass2 / mass1

    lineOfImpact = np.array([pos2[0] - pos1[0], pos2[1] - pos1[1]])
    norm = np.linalg.norm(lineOfImpact)
    lineOfImpact = lineOfImpact / norm
    PlineOfImpact = np.array([pos2[1] - pos1[1], -(pos2[0] - pos1[0])]) / norm

    alongImpactvelocity1 = np.dot(velocity1, lineOfImpact)
    alongImpactvelocity2 = np.dot(velocity2, lineOfImpact)

    pImapactvelocity1 = np.dot(velocity1, PlineOfImpact)
    pImapactvelocity2 = np.dot(velocity2, PlineOfImpact)

    velocity2 = (2 * alongImpactvelocity1 + (ratio - 1) * alongImpactvelocity2) / (ratio + 1)
    velocity1 = (2 * ratio * alongImpactvelocity2 + (1 - ratio) * alongImpactvelocity1) / (ratio + 1)

    a.velocity = velocity1 * lineOfImpact + pImapactvelocity1 * PlineOfImpact
    b.velocity = velocity2 * lineOfImpact + pImapactvelocity2 * PlineOfImpact

    center = np.array(pos1)*0.5 + np.array(pos2)*0.5
    a.pos = list(center - radius2*lineOfImpact)
    b.pos = list(center + radius1*lineOfImpact)


def isCollision(a, b):
    if a and b: return (a.pos[0] - b.pos[0])**2 + (a.pos[1] - b.pos[1])**2 <= (a.radius + b.radius)**2
    return False


def collision_detections(ball_set):
    # sorting ball_set
    # insertion_sort(ball_set, 'pos')
    ball_set.sort(key=lambda x: x.pos)
    # sweepline to detect collision
    last = None
    for cur in ball_set:
        if isCollision(last, cur):
            update_collision(last, cur)
        cur.motion()
        if last: last.motion()
        last = cur



p = Polygon(vertices=[[0, 5], [3, -1], [2, -2], [5, -10]])
print(p.vertices)