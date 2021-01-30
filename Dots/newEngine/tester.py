from engine import *
from collision import *
from force import *

length, breadth = 1300, 700
unit_len = 0.15
OX, OY, X, Y = unit_len, unit_len, length / scale -unit_len, breadth / scale - unit_len

square = [[0, 0], [unit_len, 0], [unit_len, unit_len], [0, unit_len]]
hexa = [[0, 0], [unit_len/2, -unit_len/2], [unit_len, 0], [unit_len, unit_len], [unit_len/2, 3*unit_len/2], [0, unit_len]]

top = [[OX, OY], [X, OY]]
lef = [[OX, OY], [OX, Y]]

# p = Polygon(hexa, 200, 200, color='blue', e=1)
r = Polygon(vert=square, mass=200000, mi=200000, color='green', e=1)
p = Polygon(vert=square, mass=20, mi=20, color='green', e=1)
c = Cirlce([2.0, 2], unit_len, 20, 2, color='red', e=1, mu=0.8)
c.place([X/2, Y/2])
r.place([2, 3])
p.place([6, 3])
p.scale(3)
r.scale(8)
c.scale(3)
boxes = [c, r, p]


wall_top = Line(top, 1e9, 1e9, color='cyan', e=0.5, move=False)
wall_down = Line(top, 1e9, 1e9, color='cyan', e=0.5, move=False)
wall_left = Line(lef, 1e9, 1e9, color='cyan', e=0.5, move=False)
wall_right = Line(lef, 1e9, 1e9, color='cyan', e=0.5, move=False)
wall_down.shift([0, Y-OY - unit_len])
wall_right.shift([X-OX-unit_len, 0])

gravity = GravityWorld()
drag = Drag()
drag_ang = DragAng()
contianer = []
forces = []
walls = [wall_left, wall_right, wall_top, wall_down]
boxes = []
nt = 8
for i in range(nt):
    v = Polygon(vert=square, mass=20, mi=2, e=0.5)
    # v = Cirlce(center=[0, 0], radius=unit_len, mass=20, mi=2, e=0.5, mu=0.9)
    # pos = [((OX+2*unit_len)*(nt-i) + (OX + nt*unit_len + 2)*(i))/nt, Y-3*unit_len]
    pos = [X/2, ((OY+1*unit_len)*(nt-i) + (OY + nt*unit_len + 2)*(i))/nt]
    v.place(pos)
    v.scale(2)
    v.attach_force(gravity)
    v.attach_force(drag)
    v.attach_torque(drag_ang)
    boxes.append(v)
    control = v 

control = boxes[-1]
for i in boxes:
    contianer.append(i)


spring = Spring(k=10, beta=1)
spring.attach(r, p, adjust=1)
r.attach_force(spring)
p.attach_force(spring)
r.attach_force(gravity)
p.attach_force(gravity)
c.attach_force(gravity)
forces.append(spring)
forces.append(gravity)
forces.append(drag)
forces.append(drag_ang)

FPS = 1000
pygame.init()
pygame.font.init()
pygame.display.set_caption("Nuclear Reaction !")
screen = pygame.display.set_mode((length, breadth))
clock = pygame.time.Clock()
run = True
start, end = 0, 0
ff = 1 # frame frame
dt = 0.01

while run:
    start = time()
    clock.tick(FPS)

    key = pygame.key.get_pressed()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            run = False

        if e.type == pygame.MOUSEMOTION:
                x, y = e.pos
                # control.place([x / scale, y/scale])
                # p.impulse_force(0.1*(np.array([x / scale, y/scale]) - p.cm_pos))
                # r.impulse_force(0.1*(np.array([x / scale, y/scale]) - r.cm_pos))


    if key[pygame.K_LEFT]:
        control.impulse_torque(0.5)
        
    if key[pygame.K_RIGHT]:
        control.impulse_torque(-0.5)

    if key[pygame.K_a]:
        control.impulse_force(np.array([-0.5, 0]))

    if key[pygame.K_d]:
        control.impulse_force(np.array([0.5, 0]))

    if key[pygame.K_w]:
        control.impulse_force(np.array([0, -0.5]))

    if key[pygame.K_s]:
        control.impulse_force(np.array([0, 0.5]))

    screen.fill('grey')

    for shape in boxes:
        shape.motion_dynamics(time(), dt=dt)

    for shape in walls:
        shape.draw(screen)

    for shape in contianer:
        shape.draw(screen)

    for force in forces:
        force.apply(time(), dt=dt)
        force.draw(screen, scale)

    points = collision_handler(contianer, walls)
    # draw_points(screen, points)

    text(screen, f"FPS: {1000 // (ff)}, T: {ff} ms", length-150, 10, color=clr('black'))
    pygame.display.flip()
    end = time()
    if (time()%10 == 0): 
        ff = end - start
