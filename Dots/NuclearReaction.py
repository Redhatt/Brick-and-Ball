from  engine_refined import *

gravity_world.g = 0

ve = [[1, 1], [2, 1], [2, 4], [1, 4], [0.5, 2]]
p = polygon(ve, 200, 200)

# impulses
# p.impulse_force(np.array([100, 50], dtype=np.float32))
# p.impulse_torque(10)

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
    p.motion_dynamics(time(), forces_func=[gravity_world], torque_func=[ang_spring])
    text(screen, f"FPS: {1000 // (ff)}, T: {ff} ms", 600, 10)
    pygame.display.flip()
    end = time()
    if (time()%10 == 0): 
        ff = end - start
