# collision
import numpy as np
from engine import *

# Polygon collision detections-----------------------------------

def broad_collision_check(a, b, x=np.array([1.0, 0.0]), y=np.array([0.0, 1.0])):
	al, ar = -a.find_furthest(-x, dot=True), a.find_furthest(x, dot=True)
	bl, br = -b.find_furthest(-x, dot=True), b.find_furthest(x, dot=True)
	if min(ar, br) <= max(al, bl):
		return False
	al, ar = -a.find_furthest(-y, dot=True), a.find_furthest(y, dot=True)
	bl, br = -b.find_furthest(-y, dot=True), b.find_furthest(y, dot=True)
	print(al, ar, bl, br)
	if min(ar, br) <= max(al, bl):
		return False

	return True


# SAT algorithm--------------------------------------------------
def SAT(a, b):
	'''
	@param: a-> shape A 
	@param: b-> shape B
	return: truth value of collision btw the shapes
	'''
	# iterating over the shapes
	for shape in (a, b):
		k = len(shape.vert)
		for i in range(k):
			vert1, vert2 = shape.vert[i], shape.vert[(i+1)%k]

			# getting normal axis
			axis = normal(vert2 - vert1)

			# getting min max for shape A
			min_A, max_A = np.float('inf'), -np.float('inf')
			min_B, max_B = np.float('inf'), -np.float('inf')
			ma, mb, Ma, Mb = np.array([0, 0]), np.array([0, 0]), np.array([0, 0]), np.array([0, 0])
			for vert in a.vert:
				min_A, max_A = min(min_A, vdot(vert, axis)), max(max_A, vdot(vert, axis))

			for vert in b.vert:
				min_B, max_B = min(min_B, vdot(vert, axis)), max(max_B, vdot(vert, axis))
			
			# condition to check overlapping
			if min_A<=min_B<=max_A or min_A<=max_B<=max_A or \
				(min_A<=min_B and max_A>=max_B) or (min_B<=min_A and max_B>=max_A):
				continue
			else:
				return False
	return True
# ---------------------------------------------------------------


# GJK and EPA ---------------------------------------------------
# utility function for GJK 
def next_simplex(simplex, d):
	'''
	@param:simplex->list of 2D numpy array shape (2, )
	@param: directions numpy array shape (2, )
	'''
	# switch case for 2, 3, 4 size of simplex
	if len(simplex) == 2: return line(simplex, d)
	elif len(simplex) == 3: return triangle(simplex, d)
	#elif len(simplex) == 4: return tetrahedron(simplex, d) # not needed now, since 2D only.
	return False, None, None


# utility function for GJK-next_simplex
def line(simplex, d):
	'''
	@param:simplex->list of 2D numpy array shape (2, )
	@param: directions numpy array shape (2, )
	'''
	a, b = simplex
	ab = b - a
	ao = -a

	# comment code also works but good for 3D stuff
	# # ----------------------------------------------
	# if same_dir(ab, ao):

	# 	# setting direction normal to ab in direction of ao
	# 	d = normal(ab, ao)
	# 	return False, simplex, d
	
	# simplex = [a]
	# d = ao
	# return False, simplex, d
	# # ----------------------------------------------

	# optimised code for 2D 
	# # ----------------------------------------------
	d = normal(ab, ao)
	return False, simplex, d
	# # ----------------------------------------------


# utility function for GJK-next_simplex
def triangle(simplex, d):
	'''
	@param:simplex->list of 2D numpy array shape (2, )
	@param: directions numpy array shape (2, )
	'''
	c, b, a = simplex

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
		# 	simplex = [a, c]
		# 	d = normal(ac, ao)
		# 	return False, simplex, d
		# else:
		# 	return line([a, b], d)
		# # ----------------------------------------------

		# optimised code for 2D 
		# ----------------------------------------------
		simplex = [a, c]
		d = ac_n
		return False, simplex, d
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
			simplex = [a, b]
			d = ab_n
			return False, simplex, d
			# ----------------------------------------------
		# it is inside
		else:
			return True, simplex, d


# GJK algorithm
def GJK(a, b):
	'''
	@param: a-> shape A 
	@param: b-> shape B
	return: truth value of collision btw the shapes
	'''
	unit_x = np.array([1.0, -1.0], dtype=np.float32)
	simplex = list()

	sup = support(a, b, unit_x)
	simplex.append(sup)
	d = -sup

	while True:
		sup = support(a, b, d)
		if vdot(d, sup) <= 0:
			return False , None

		simplex.append(sup)

		val, simplex, d = next_simplex(simplex, d)
		if val: return True , simplex


# findnig contact points
def find_contact(a, b, n, tol=0.02):
	if a.type == 'Polygon' and b.type == 'Polygon':
		index1 = a.find_furthest(n, index=True)
		s1 = len(a.vert)
		v1, v2, v3 = a.vert[(index1 - 1)%s1], a.vert[index1], a.vert[(index1 + 1)%s1]

		index2 = b.find_furthest(-n, index=True)
		s2 = len(b.vert)
		w1, w2, w3 = b.vert[(index2 - 1)%s2], b.vert[index2], b.vert[(index2 + 1)%s2]

		nn = normal(n)
		if abs(vdot(v1-v2, n)) < tol:
			if abs(vdot(w1-w2, n)) < tol:
				ans = sorted((v1, v2, w1, w2), key=lambda x:vdot(x, nn))
				return (ans[1] + ans[2])/2
			elif abs(vdot(w3-w2, n)) < tol:
				ans = sorted((v1, v2, w3, w2), key=lambda x:vdot(x, nn))
				return (ans[1] + ans[2])/2
			else:
				return w2

		elif abs(vdot(v3-v2, n)) < tol:
			if abs(vdot(w1-w2, n)) < tol:
				ans = sorted((v3, v2, w1, w2), key=lambda x:vdot(x, nn))
				return (ans[1] + ans[2])/2
			elif abs(vdot(w3-w2, n)) < tol:
				ans = sorted((v3, v2, w3, w2), key=lambda x:vdot(x, nn))
				return (ans[1] + ans[2])/2
			else:
				return w2
		else:
			return v2


		if (abs(vdot(v1-v2, n)) < tol or abs(vdot(v3-v2, n)) < tol):
			return b.find_furthest(-n)
		return v2

	elif a.type == 'Circle':
		return a.find_furthest(align(n, b.cm_pos - a.cm_pos))
	
	elif b.type == 'Circle':
		return b.find_furthest(align(n, a.cm_pos - b.cm_pos))

	elif (a.type == 'Line' and b.type == 'Polygon') or \
		(a.type == 'Polygon' and b.type == 'Line'):
		a, b = (a, b) if a.type == 'Polygon' else (b, a)

		index1 = a.find_furthest(align(n, b.cm_pos - a.cm_pos), index=True)
		s1 = len(a.vert)
		v1, v2, v3 = a.vert[(index1 - 1)%s1], a.vert[index1], a.vert[(index1 + 1)%s1]

		if abs(vdot(v1-v2, n)) < tol:
			return (v1 + v2)/2
		elif abs(vdot(v3-v2, n)) < tol:
			return (v2 + v3)/2
		elif abs(vdot(b.along(), n))<tol:
			return v2
		else:
			return a.find_furthest(align(n, a.cm_pos - b.cm_pos))
	return None
			

# utility function for EPA
def closest_edge(simplex):
	'''
	@param:simplex->list of 2D numpy array shape (2, )
	'''
	min_dis = float('inf')
	min_index = 0
	min_n = np.array([0, 0])
	size = len(simplex)
	for i in range(size):
		v1, v2 = simplex[i], simplex[(i+1)%size]
		n = normal(v2 - v1, v1, nrm=True)
		d = vdot(n, v1)
		if d < min_dis:
			min_dis = d
			min_index = (i+1)%size
			min_n = n
	return min_n, min_dis, min_index


# EPA algorithm
def EPA(simplex, a, b, tol=0.0001):
	'''
	@param: simplex-> list of 2D numpy array shape (2, ), list of size atleast 3
	@param: a-> shape A 
	@param: b-> shape B
	'''
	# max_size = len(a.vert) * len(b.vert)
	max_size = 10
	while True:
		# get edge_normal closest to origin and its distance
		n, dis, index = closest_edge(simplex)
		p = support(a, b, n)
		d = vdot(p, n)
		if abs(d - dis) < tol or len(simplex)>max_size:
			return n, dis + tol, find_contact(a, b, n)
		else:
			simplex.insert(index, p)
# ---------------------------------------------------------------


def collision_handler(container, big=None):
	contacts = []
	size = len(container)
	container.sort(key=lambda x: (x.cm_pos[0]))
	if size>1:
		for b in big:
			for a in container:
				# determine type of collision
				if a.move or b.move:
					collide, simplex = GJK(a, b)
					if collide:
						nor, dis, p = EPA(simplex, a, b)
						if p is None: continue
						solver(a, b, nor, dis, p)
						contacts.append(p)

		for i in range(size):
			a, b = container[i], container[(i+1)%size]
			# determine type of collision
			if a.move or b.move:
				collide, simplex = GJK(a, b)
				if collide:
					nor, dis, p = EPA(simplex, a, b)
					if p is None: continue
					solver(a, b, nor, dis, p)
					contacts.append(p)

		container.sort(key=lambda x: (x.cm_pos[1]))
		for i in range(size):
			a, b = container[i], container[(i+1)%size]
			if a.move or b.move:
				collide, simplex = GJK(a, b)
				if collide:
					nor, dis, p = EPA(simplex, a, b)
					if p is None: continue
					solver(a, b, nor, dis, p)
					contacts.append(p)

	return contacts




if __name__ == '__main__':
	# v1 = [[1, 1], [3,1], [3,3], [1,3], [0.5, 2]]
	v1 = [[1, 1], [3,0.5], [3.2,3], [1.3,2.56], [0.5, 2]]
	# v1 = [[1, 1], [3,1], [3,3], [1,3], [0.5, 2]]
	p = Polygon(v1, 200, 200, color='green')
	r = Polygon(v1, 200, 200)
	

	# p.impulse_force(np.array([100, 50], dtype=np.float32))
	p.impulse_torque(0.1)


	container = [p, r]

	shift = [6/1000, 0/1000]
	turn = 0.01
	
	p.shift([2, 2])
	length, breadth = 1280, 800
	pygame.init()
	pygame.font.init()
	pygame.display.set_caption("Nuclear Reaction !")
	screen = pygame.display.set_mode((length, breadth))
	clock = pygame.time.Clock()
	run = True
	start, end = 0, 0
	ff = 1 # frame frame

	cc = colors['white']
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
				# r.place([x / scale, y/scale])
				# r.impulse_force(0.01*(np.array([x / scale, y/scale]) - r.cm_pos))

		if key[pygame.K_LEFT]:
			# r.turn(-turn)
			r.impulse_force(np.array([-0.1, 0]))

		if key[pygame.K_RIGHT]:
			# r.turn(turn)
			r.impulse_force(np.array([0.1, 0]))
			

		screen.fill(cc)

		for i in container:
			i.motion_dynamics(time())
			i.draw(screen)



		# if broad_collision_check(r, p):
		# 	pygame.draw.rect(screen, colors['red'], (0, 0, length, breadth), 10)

		# if SAT(r, p):
		# 	pygame.draw.rect(screen, colors['red'], (0, 0, length, breadth), 10)

		collision_handler(container)
		
		# collide, simplex = GJK(r, p)
		# if collide:
		# 	nor, dis, pp = EPA(simplex, r, p)

		# 	cc = colors['white']
		# 	center = np.array([length//2, breadth//2])
		# 	last = center + scale*nor

		# 	pygame.draw.line(screen, colors['black'], center, last, 2)
		# 	pygame.draw.circle(screen, colors['cyan'], pp*scale, 5)
		# 	pygame.draw.circle(screen, colors['black'], center, 5)
		# 	text(screen, f"{nor}, {dis}", 600, 20)
		# else:
		# 	cc = colors['white']


		text(screen, f"FPS: {1000 // (ff)}, T: {ff} ms", 600, 10)
		pygame.display.flip()
		end = time()
		if (time()%10 == 0): 
			ff = end - start
