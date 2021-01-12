# collision
import numpy as np
from engine_refined import *

# only for polygon detection.
def SAT(a, b):

	# getting axis to get normals
	for shape in (a, b):
		for i in range(len(shape.vert)-1):
			vert1, vert2 = shape.vert[i], shape.vert[i+1]

			# getting axis
			axis = vert2 - vert1

			# getting min max for shape A
			min_A, max_A = np.float('inf'), -np.float('inf')
			min_B, max_B = np.float('inf'), -np.float('inf')
			ma, mb, Ma, Mb = np.array([0, 0]), np.array([0, 0]), np.array([0, 0]), np.array([0, 0])
			for vert in a.vert:
				min_A, max_A = min(min_A, np.dot(vert, axis)), max(max_A, np.dot(vert, axis))
				
				# if min_A>np.dot(vert, axis):
				# 	min_A = np.dot(vert, axis)
				# 	ma = vert

				# if max_A<np.dot(vert, axis):
				# 	max_A = np.dot(vert, axis)
				# 	Ma = vert

			for vert in b.vert:
				min_B, max_B = min(min_B, np.dot(vert, axis)), max(max_B, np.dot(vert, axis))
				
				# if min_B>np.dot(vert, axis):
				# 	min_B = np.dot(vert, axis)
				# 	mb = vert

				# if max_B<np.dot(vert, axis):
				# 	max_B = np.dot(vert, axis)
				# 	Mb = vert

			# condition to check overlapping

			if min_A<=min_B<=max_A or min_A<=max_B<=max_A or \
				(min_A<=min_B and max_A>=max_B) or (min_B<=min_A and max_B>=max_A):
				continue
			else:
				return False
	return True



if __name__ == '__main__':
	v1 = [[1, 1], [3,1], [3,3], [1,3]] 
	p = polygon(v1, 200, 200, color='green')
	r = polygon(v1, 200, 200)
	
	shift = [2/1000, 1/1000]
	turn = 0.01
	
	length, breadth = 1000, 700
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


		r.turn(turn)
		r.shift(shift)

		p.draw(screen)
		r.draw(screen)
		p.motion_dynamics(time())
		r.motion_dynamics(time())

		if SAT(r, p):
			pygame.draw.rect(screen, colors['red'], (0, 0, length, breadth), 10)

		text(screen, f"FPS: {1000 // (ff)}, T: {ff} ms", 600, 10)
		pygame.display.flip()
		end = time()
		if (time()%10 == 0): 
			ff = end - start
