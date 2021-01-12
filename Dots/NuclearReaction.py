from  engine_refined import *
from collision import SAT

vep = [[1, 1], [2, 1], [3, 2.5], [2, 4], [0.5, 2]]
ver = [[1, 1], [2, 1], [2, 4], [1, 5], [0.5, 2]]

p = polygon(vep, 200, 200, color='blue')
r = polygon(ver, 200, 200, color='green')

# impulses
# p.impulse_force(np.array([100, 50], dtype=np.float32))
# p.impulse_torque(10)

r.shift(shift=np.array([2, 2]))
r.impulse_force(np.array([1, 1], dtype=np.float32))

length, breadth = 1000, 700
contianer = [p, r]
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

    for shape in contianer:
        shape.draw(screen)
        shape.motion_dynamics(time(), forces_func=[spring], torque_func=[ang_spring])
        # shape.motion_dynamics(time(), torque_func=[ang_spring])

    if len(contianer)>1:
        for i in range(len(contianer)-1):
            if SAT(contianer[i], contianer[i+1]):
                pygame.draw.rect(screen, colors['red'], (0, 0, length, breadth), 2)

    text(screen, f"FPS: {1000 // (ff)}, T: {ff} ms", 600, 10)
    pygame.display.flip()
    end = time()
    if (time()%10 == 0): 
        ff = end - start
