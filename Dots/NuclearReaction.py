from  engine_refined import *
from collision import *

length, breadth = 1300, 800

diff = 0.25
OX, OY, X, Y = diff, diff, length / scale -diff, breadth / scale - diff

vep = [[1, 1], [2, 1], [3, 2.5], [2, 4], [0.5, 2]]
ver = [[1, 1], [2, 1], [2, 4], [1, 5], [0.5, 2]]

top = [[OX, OY], [X, OY]]
lef = [[OX, OY], [OX, Y]]

p = Polygon(vep, 200, 200, color='blue', e=1)
r = Polygon(ver, 200, 200, color='green', e=1)
r.shift([3, 1])

wall_top = Line(top, 1e9, 1e9, color='cyan', e=1, move=False)
wall_down = Line(top, 1e9, 1e9, color='cyan', e=1, move=False)
wall_left = Line(lef, 1e9, 1e9, color='cyan', e=1, move=False)
wall_right = Line(lef, 1e9, 1e9, color='cyan', e=1, move=False)

wall_down.shift([0, Y-OY])
wall_right.shift([X-OX, 0])


contianer = [r, p, wall_left, wall_right, wall_top, wall_down]
# contianer = [r, wall_top]
pygame.init()
pygame.font.init()
pygame.display.set_caption("Nuclear Reaction !")
screen = pygame.display.set_mode((length, breadth))
clock = pygame.time.Clock()
run = True
start, end = 0, 0
ff = 1 # frame frame

turn = 0.1
while run:
    start = time()
    # clock.tick(FPS)

    key = pygame.key.get_pressed()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            run = False

        if e.type == pygame.MOUSEMOTION:
                x, y = e.pos
                # p.place([x / scale, y/scale])
                # p.impulse_force(0.1*(np.array([x / scale, y/scale]) - p.cm_pos))
                # r.impulse_force(0.1*(np.array([x / scale, y/scale]) - r.cm_pos))


    if key[pygame.K_LEFT]:
        r.impulse_torque(0.1)
        # r.turn(-turn)
        
    if key[pygame.K_RIGHT]:
        r.impulse_torque(-0.1)
        # r.turn(turn)

    if key[pygame.K_a]:
        r.impulse_force(np.array([-0.1, 0]))
        # r.shift(np.array([-0.1, 0]))

    if key[pygame.K_d]:
        r.impulse_force(np.array([0.1, 0]))
        # r.shift(np.array([0.1, 0]))

    if key[pygame.K_w]:
        r.impulse_force(np.array([0, -0.1]))
        # r.shift(np.array([0, -0.1]))

    if key[pygame.K_s]:
        r.impulse_force(np.array([0, 0.1]))
        # r.shift(np.array([0, 0.1]))

    screen.fill(colors['white'])

    for shape in contianer:
        shape.motion_dynamics(time())
        shape.draw(screen)

    points = collision_handler(contianer)
    draw_points(screen, points)

    text(screen, f"FPS: {1000 // (ff)}, T: {ff} ms", 600, 10, color=colors['yellow'])
    pygame.display.flip()
    end = time()
    if (time()%10 == 0): 
        ff = end - start
