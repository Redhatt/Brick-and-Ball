# collision
import numpy as np
from engine_refined import *

from time import time as t

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


def GJK(a, b):
	'''
	@param: a-> shape A 
	@param: b-> shape B
	return: truth value of collision btw the shapes
	'''
	unit_x = np.array([1.0, -1.0], dtype=np.float32)
	simplex_points = list()

	sup = support(a, b, unit_x)
	simplex_points.append(sup)
	d = -sup

	while True:
		sup = support(a, b, d)
		if np.dot(d, sup) <= 0:
			return False

		simplex_points.append(sup)

		val, simplex_points, d = next_simplex(simplex_points, d)
		if val: return True

def support(a, b, d):
	'''
	@param: a-> shape A 
	@param: b-> shape B
	@param:dir-> direction (numpy.array shape (2, ))
	returns: 2D point with max dot pord
	'''
	return a.find_furthest(d) - b.find_furthest(-d)

# returns the simplex 
def next_simplex(simplex_points, d):
	if len(simplex_points) == 2: return line(simplex_points, d)
	elif len(simplex_points) == 3: return triangle(simplex_points, d)
	elif len(simplex_points) == 4: return tetrahedron(simplex_points, d) # not needed now, since 2D only.
	return False, None, None

def line(simplex_points, d):
	# print('line')
	a, b = simplex_points
	ab = b - a
	ao = -a

	# comment code also works but good for 3D stuff
	# # ----------------------------------------------
	# if same_dir(ab, ao):

	# 	# setting direction normal to ab in direction of ao
	# 	d = normal(ab, ao)
	# 	return False, simplex_points, d
	
	# simplex_points = [a]
	# d = ao
	# return False, simplex_points, d
	# # ----------------------------------------------

	# optimised code for 2D 
	# # ----------------------------------------------
	d = normal(ab, ao)
	return False, simplex_points, d
	# # ----------------------------------------------


def triangle(simplex_points, d):
	c, b, a = simplex_points

	ab = b - a 
	ac = c - a 
	ao = -a

	# checking if origin is outside ac
	# getting normal of ac in directions -ab
	ac_n = normal(ac, -ab)

	# checking if ao along ac_n, if yes its outside
	if same_dir(ac_n, ao):

		# comment code also works but good for 3D stuff
		# # ----------------------------------------------
		# if same_dir(ac, ao):
		# 	# remove b from simplex
		# 	simplex_points = [a, c]
		# 	d = normal(ac, ao)
		# 	return False, simplex_points, d
		# else:
		# 	return line([a, b], d)
		# # ----------------------------------------------

		# optimised code for 2D 
		# ----------------------------------------------
		simplex_points = [a, c]
		d = ac_n
		return False, simplex_points, d
		# ----------------------------------------------

	# if outside ab
	else:
		ab_n = normal(ab, -ac)

		if same_dir(ab_n, ao):

			# comment code also works but good for 3D stuff
			# # ----------------------------------------------
			# return line([a, b], d)
			# # ----------------------------------------------

			# optimised code for 2D 
			# ----------------------------------------------
			simplex_points = [a, b]
			d = ab_n
			return False, simplex_points, d
			# ----------------------------------------------

		else:
			return True, simplex_points, d


# truth value of vec in same direction to d.
def same_dir(vec, d):
	return np.dot(vec, d)>0



if __name__ == '__main__':
	v1 = [[1, 1], [3,1], [3,3], [1,3], [0.5, 2]]
	p = polygon(v1, 200, 200, color='green')
	r = polygon(v1, 200, 200)
	
	shift = [6/1000, 0/1000]
	turn = 0.1
	
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

		# if SAT(r, p):
		# 	pygame.draw.rect(screen, colors['red'], (0, 0, length, breadth), 10)

		if GJK(r, p):
			pygame.draw.rect(screen, colors['red'], (0, 0, length, breadth), 10)

		text(screen, f"FPS: {1000 // (ff)}, T: {ff} ms", 600, 10)
		pygame.display.flip()
		end = time()
		if (time()%10 == 0): 
			ff = end - start
