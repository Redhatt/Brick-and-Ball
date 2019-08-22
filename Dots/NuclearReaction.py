import pygame
import numpy as np

factor = np.sqrt(0.5)
length, breadth = 500, 300
FPS = 60
limit1 = 10
limit2 = 10

Red = (139, 0, 0)
Blue = (70, 20, 225)
Yellow = (120, 120, 0)


def direction(velocity1, velocity2, rect1, rect2, width1, width2, mass1, mass2):

    ratio = mass2 / mass1

    lineOfImpact = np.array([rect2[0] - rect1[0] + (width1 - width2) / 2, rect2[1] - rect1[1]
                                                                    + (width1 - width2) / 2])
    norm = np.linalg.norm(lineOfImpact)
    lineOfImpact = lineOfImpact / norm
    PlineOfImpact = np.array([rect2[1] - rect1[1], -(rect2[0] - rect1[0])]) / norm

    alongImpactvelocity1 = np.dot(velocity1, lineOfImpact)
    alongImpactvelocity2 = np.dot(velocity2, lineOfImpact)

    pImapactvelocity1 = np.dot(velocity1, PlineOfImpact)
    pImapactvelocity2 = np.dot(velocity2, PlineOfImpact)

    velocity2 = (2 * alongImpactvelocity1 + (ratio - 1) * alongImpactvelocity2) / (ratio + 1)
    velocity1 = (2 * ratio * alongImpactvelocity2 + (1 - ratio) * alongImpactvelocity1) / (ratio + 1)

    new_velocity1 = velocity1 * lineOfImpact + pImapactvelocity1 * PlineOfImpact
    new_velocity2 = velocity2 * lineOfImpact + pImapactvelocity2 * PlineOfImpact

    new_velocity1 = new_velocity1.astype(int)
    new_velocity2 = new_velocity2.astype(int)

    return new_velocity1, new_velocity2

class Uranium(object):
    width = 20
    radius = int(factor * width)
    mass = 100

    def __init__(self, x=None, y=None):
        if x is None:
            self.x = np.random.randint(20, length - 20)
            self.y = np.random.randint(20, breadth - 20)
        else:
            self.x = x
            self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.width)
        self.velocity = np.array([np.random.randint(-limit1, limit1), np.random.randint(-limit1, limit1)])

    def motion(self):

        if (self.rect[0] < 10) or (self.rect[0] + self.width > length - 10):
            self.rect.x -= self.velocity[0]
            self.velocity[0] = -self.velocity[0]

        if (self.rect[1] < 10) or (self.rect[1] + self.width > breadth - 10):
            self.rect.y -= self.velocity[1]
            self.velocity[1] = -self.velocity[1]

        self.rect.x += int(self.velocity[0])
        self.rect.y += int(self.velocity[1])


class Neutron(Uranium):
    mass = 10
    width = 7
    radius = int(factor * width)
    velocity = np.array([np.random.randint(-limit2, limit2), np.random.randint(-limit2, limit2)])
    pass


pygame.init()
pygame.font.init()
pygame.display.set_caption("Nuclear Reaction !")
screen = pygame.display.set_mode((length, breadth))
clock = pygame.time.Clock()
uranium = []
neutrons = []

for i in range(2):
    uranium.append(Uranium())

for j in range(2):
    neutrons.append(Neutron())

run = True
while run:

    clock.tick(FPS)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            run = False

    screen.fill((200, 200, 200))

    for u in uranium:
        u.motion()
        pygame.draw.circle(screen, Blue, (u.rect[0] + u.radius, u.rect[1] + u.radius), u.radius)
        pygame.display.flip()

    for n in neutrons:
        n.motion()
        pygame.draw.circle(screen, Red, (n.rect[0] + n.radius, n.rect[1] + n.radius), n.radius)
        pygame.display.flip()

    for i, u in enumerate(uranium):
        for n in neutrons:
            if (np.linalg.norm(np.array(n.rect.center) - np.array(u.rect.center))<n.radius+u.radius):
                    n.rect.center -= n.velocity
                    u.rect.center -= u.velocity
                    n.velocity, u.velocity = direction(n.velocity, u.velocity, n.rect, u.rect, n.width, u.width, n.mass, u.mass)
               #  neutrons.append(Neutron())
               #  neutrons.append(Neutron())  uncoment these lines for nuclear reaction
               #  neutrons.append(Neutron())
               #  del uranium[i]

    for x in uranium:
        for y in uranium:
            if x == y:
                continue
            else:
                if (np.linalg.norm(np.array(x.rect.center) - np.array(y.rect.center))<x.radius+y.radius):
                    x.rect.center -= x.velocity
                    y.rect.center -= y.velocity
                    x.velocity, y.velocity = direction(x.velocity, y.velocity, x.rect, y.rect, x.width, y.width, x.mass, y.mass)

                    if x.velocity.all() == np.array([0, 0]).all() and y.velocity.all() == np.array([0, 0]).all():
                        x.velocity = np.array([np.random.randint(-limit1, limit1), np.random.randint(-limit1, limit1)])
                        y.velocity = -x.velocity
                        print(2)

    for x in neutrons:
        for y in neutrons:
            if x == y:
                continue
            else:
                if (np.linalg.norm(np.array(x.rect.center) - np.array(y.rect.center))<x.radius+y.radius):
                    x.rect.center -= x.velocity
                    y.rect.center -= y.velocity
                    x.velocity, y.velocity = direction(x.velocity, y.velocity, x.rect, y.rect, x.width, y.width, x.mass, y.mass)
