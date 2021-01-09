from engine import *

FPS = 60
length, breadth = 700, 500

class Uranium(Ball):
    color = colors['red']
    radius = 20
    mass = 235

class Neutron(Ball):
    color = colors['blue']
    radius = 5
    mass = 1


if __name__ == "__main__":
    count_uranium = 5
    count_neutron = 0

    R_pos = lambda : list(np.multiply(dim, np.random.rand(2)))
    R_vel = lambda : np.random.randint(-limit, limit) * np.random.rand(2)
    
    uranium = [Uranium(R_pos(), R_vel()) for i in range(count_uranium)]
    neutron = [Neutron(R_pos(), R_vel()) for i in range(count_neutron)]
    balls = uranium + neutron

    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Nuclear Reaction !")
    screen = pygame.display.set_mode((length, breadth))
    clock = pygame.time.Clock()
    run = True
    start, end = 0, 0
    while run:
        clock.tick(FPS)

        start = pygame.time.get_ticks()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                run = False

        screen.fill(colors['white'])

        collision_detections(balls)

        for ball in balls:
            pygame.draw.circle(screen, ball.color, tuple(map(int, ball.pos)), ball.radius)
        end = pygame.time.get_ticks()
        text(screen, f"FPS: {1 / (end - start + 1e-6)}", 600, 10)
        pygame.display.flip()
