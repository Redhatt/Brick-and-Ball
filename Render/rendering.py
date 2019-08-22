import pygame
import sys, math, time
import quaternions
import numpy as np
'''
def rotate2d(pos, rad):
 	x,y = pos
 	s,c = (math.sin(rad), math.cos(rad))
 	return x*c-y*s, y*c+x*s
'''

class projectOnScreen:
	def __init__(self, frame, cam, nodes, edges, rot=False, node_color=(200, 0, 0), edge_color=(0, 0, 0)):
		self.coordinates = [1,1,1]
		self.frame = frame
		self.center_x, self.center_y = self.frame[0] * 0.5, self.frame[1] * 0.5
		self.cam = cam
		self.projected_coordinates = [1, 1]
		self.rot = rot
		self.edges = edges
		self.edge_color = edge_color
		self.nodes = nodes
		self.node_color = node_color
	#x = coordinates[0]
	#y = coordinates[1]
	#z = coordinates[2]

	#x, z = rotate2d((x, z), cam.rot[0])
	#y, z = rotate2d((y, z), cam.rot[1])

	# shifting coordinate system...
	def translate(self):
		self.coordinates -= np.array(self.cam.pos)
		#x -= cam.pos[0]
		#y -= cam.pos[1]
		#z -= cam.pos[2]

	def rotate_3D(self):
		vec = quaternions.qrot_vec(self.coordinates, self.cam.rot_x, self.cam.axis_y, self.cam.pos)
		vec = quaternions.qrot_vec(vec, self.cam.rot_y, self.cam.axis_x, self.cam.pos)
		self.coordinates = vec
		#x, z = rotate2d((x, z), cam.rot[0])
		#y, z = rotate2d((y, z), cam.rot[1])

	def project(self):
		f = 200 / float(self.coordinates[2])
		self.projected_coordinates = [int(self.coordinates[0]*f + self.center_x), int(self.coordinates[1]*f + self.center_y)]

	def select_transform(self):
		pos = self.cam.pos
		if not self.rot:
			self.rotate_3D()
			self.translate()
			self.project()
		else:
			self.cam.pos = (0, 0, 0)
			self.rotate_3D()
			self.cam.pos = pos
			self.translate()
			self.project()

	def render_edges(self,screen, edges, vertices, color=None):
		if color == None:
			color = self.edge_color
		for edge in edges:
			points = []
			for coordinates in (vertices[edge[0]], vertices[edge[1]]):
				self.coordinates = coordinates
				self.select_transform()
				points += [self.projected_coordinates]
			pygame.draw.line(screen, color, points[0], points[1], 3)

	def render_nodes(self, screen, nodes, color=None):
		if color == None:
			color = self.node_color
		for node in nodes:
			self.coordinates = node
			self.select_transform()
			pygame.draw.circle(screen, color, self.projected_coordinates, 2, 0)

	def render_axis(self, screen):
		axis_color = ((255, 0, 0), (0, 255, 0), (0, 0, 255), (252, 85, 8))
		axis_letter = ('X', 'Y', 'Z')
		vertices_a = [(0,0,0), (7,0,0), (0,7,0), (0,0,7)]
		edges_a = [(0,1), (0,2), (0,3)]
		#self.render_edges(screen, edges_a, vertices_a, (0,0,255))
		#self.render_nodes(screen, vertices_a, (0,255,0))
		for i, edge in enumerate(edges_a):
			points = []
			for coordinates in (vertices_a[edge[0]], vertices_a[edge[1]]):
				self.coordinates = coordinates
				self.select_transform()
				points += [self.projected_coordinates]
			pygame.draw.line(screen, axis_color[i], points[0], points[1], 1)

		font = pygame.font.Font('freesansbold.ttf', 22) 
		for i, node in enumerate(vertices_a[1:]):
			self.coordinates = node
			self.select_transform()
			pygame.draw.circle(screen, axis_color[i], self.projected_coordinates, 2, 0)
			text = font.render(axis_letter[i], True,axis_color[i]) 
			textRect = text.get_rect()  
			textRect.center = (self.projected_coordinates[0], self.projected_coordinates[1]) 
			screen.blit(text, textRect)

		 

	def run(self, edges=True, nodes=True, axis=False):
		pygame.init()
		center_x, center_y = self.frame[0] * 0.5, self.frame[1] * 0.5
		center_x, center_y = int(center_x), int(center_y)
		screen = pygame.display.set_mode(self.frame)
		clock = pygame.time.Clock()
		pygame.event.get()
		pygame.mouse.get_rel()
		pygame.mouse.set_visible(0)
		pygame.event.set_grab(1)

		mouse_mov = [0,0]
		m_pos = [-100,-100]
		t = 0
		error = True
		while True:
			dt = clock.tick()/float(1000)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						pygame.quit()
						sys.exit()

				if error is False:
					posNew = pygame.mouse.get_pos()
					mouse_mov[0] = posNew[0] - m_pos[0]
					mouse_mov[1] = posNew[1] - m_pos[1]
					if (posNew[0] < 2):
						pygame.mouse.set_pos((self.frame[0]-5, posNew[1]))
						m_pos = pygame.mouse.get_pos()
					if (posNew[0] > self.frame[0]-2):
						pygame.mouse.set_pos((5, posNew[1]))
						m_pos = pygame.mouse.get_pos()
					if (posNew[1] < 2):
						pygame.mouse.set_pos((posNew[0], self.frame[1]-5))
						m_pos = pygame.mouse.get_pos()
					if (posNew[1] > self.frame[1]-2):
						pygame.mouse.set_pos(((posNew[0], 5)))
						m_pos = pygame.mouse.get_pos()
					if m_pos != posNew:
						m_pos = posNew
						error = self.cam.mouse_events(mouse_mov, event)
					else:
						error = self.cam.mouse_events((0,0), event)
				else:
					error = self.cam.mouse_events(mouse_mov, event)
				
				posNew = pygame.mouse.get_pos()
				if (posNew[0] < 2):
					pygame.mouse.set_pos((self.frame[0]-5, posNew[1]))
				if (posNew[0] > self.frame[0]-2):
					pygame.mouse.set_pos((5, posNew[1]))
				if (posNew[1] < 2):
					pygame.mouse.set_pos((posNew[0], self.frame[1]-5))
				if (posNew[1] > self.frame[1]-2):
					pygame.mouse.set_pos(((posNew[0], 5)))
				error = self.cam.mouse_events(mouse_mov, event)
			screen.fill((200, 200, 200))
			if edges:
				self.render_edges(screen, self.edges, self.nodes)
			if nodes:
				self.render_nodes(screen, self.nodes)
			if axis:
				self.render_axis(screen)
			pygame.display.flip()
			key = pygame.key.get_pressed()
			if key[pygame.K_t]:
				if self.rot:
					time.sleep(0.5)
					self.rot=False
				else:
					time.sleep(0.5)
					self.rot=True
			self.cam.update(dt, key)

			t += dt
			if t >5000:
				t = 1


class Cam:
	def __init__(self, pos=(1,1,1)):
			self.axis_x=np.array([1,0,0])
			self.axis_y=np.array([0,1,0])
			self.pos = list(pos)
			self.rot_x = 0
			self.rot_y = 0
			#self.direction = ()
	def mouse_events(self, m_pos, event):
		try:
			x, y = event.rel
			error = True
		except Exception as e:
			error = True
			x, y = m_pos
		else:
			pass
		finally:
			pass
		x = x/float(800)
		y = y/float(800)
		self.rot_x += x
		self.rot_y -= y

		return error

	def update(self, dt, key):
		s = dt*10
		if key[pygame.K_a]: self.pos[0] -= s
		if key[pygame.K_s]: self.pos[1] += s
		if key[pygame.K_w]: self.pos[1] -= s
		if key[pygame.K_d]: self.pos[0] += s
		if key[pygame.K_q]: self.pos[2] += s
		if key[pygame.K_e]: self.pos[2] -= s

		#x,y = s*math.sin(self.rot[0]), s*math.cos(self.rot[1])
		#if key[pygame.K_UP]: self.pos[0] += x; self.pos[2] += y
		#if key[pygame.K_DOWN]: self.pos[0] -= x; self.pos[2] -= y
		#if key[pygame.K_RIGHT]: self.pos[0] += y; self.pos[2] += x
		#if key[pygame.K_LEFT]: self.pos[0] -= y; self.pos[2] -= x

if __name__ == "__main__":
	vertices = ((-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
					(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1))

	edges = ((0, 1), (1, 2), (2, 3), (3, 0),
			 (0, 4), (1, 5), (2, 6), (3, 7),
			 (4, 5), (5, 6), (6, 7), (7, 4))

	myscreen = projectOnScreen((1000, 600),Cam(pos=(0,0,5)), vertices, edges, rot=True)
	myscreen.run(edges=True, nodes=True, axis=True)

#	pygame.init()
#	frame = (1000, 600)
#	center_x, center_y = frame[0] * 0.5, frame[1] * 0.5
#	center_x, center_y = int(center_x), int(center_y)
#	screen = pygame.display.set_mode(frame)
#	clock = pygame.time.Clock()
#
#	vertices = ((-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
#				(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1),
#				(0,0,0), (10,0,0), (0,10,0), (0,0,10))
#
#	edges = ((0, 1), (1, 2), (2, 3), (3, 0),
#			 (0, 4), (1, 5), (2, 6), (3, 7),
#			 (4, 5), (5, 6), (6, 7), (7, 4),
#			 (8,9), (8,10), (8,11))
#
#	cam = Cam(pos=(0,0,5))
#	pygame.event.get()
#	pygame.mouse.get_rel()
#	pygame.mouse.set_visible(1)
#	pygame.event.set_grab(1)
#
#	mouse_mov = [0,0]
#	m_pos = [-100,-100]
#	t = 0
#	error = True
#
#	while True:
#		dt = clock.tick()/float(1000)
#		for event in pygame.event.get():
#			if event.type == pygame.QUIT:
#				pygame.quit()
#				sys.exit()
#			if event.type == pygame.KEYDOWN:
#				if event.key == pygame.K_ESCAPE:
#					pygame.quit()
#					sys.exit()
#			
#			
#			if error is False:
#				posNew = pygame.mouse.get_pos()
#				mouse_mov[0] = posNew[0] - m_pos[0]
#				mouse_mov[1] = posNew[1] - m_pos[1]
#				if (posNew[0] < 2):
#					pygame.mouse.set_pos((frame[0]-5, posNew[1]))
#					m_pos = pygame.mouse.get_pos()
#				if (posNew[0] > frame[0]-2):
#					pygame.mouse.set_pos((5, posNew[1]))
#					m_pos = pygame.mouse.get_pos()
#				if (posNew[1] < 2):
#					pygame.mouse.set_pos((posNew[0], frame[1]-5))
#					m_pos = pygame.mouse.get_pos()
#				if (posNew[1] > frame[1]-2):
#					pygame.mouse.set_pos(((posNew[0], 5)))
#					m_pos = pygame.mouse.get_pos()
#				if m_pos != posNew:
#					m_pos = posNew
#					error = cam.mouse_events(mouse_mov, event)
#				else:
#					error = cam.mouse_events((0,0), event)
#			else:
#				error = cam.mouse_events(mouse_mov, event)
#			
#			posNew = pygame.mouse.get_pos()
#			if (posNew[0] < 2):
#				pygame.mouse.set_pos((frame[0]-5, posNew[1]))
#			if (posNew[0] > frame[0]-2):
#				pygame.mouse.set_pos((5, posNew[1]))
#			if (posNew[1] < 2):
#				pygame.mouse.set_pos((posNew[0], frame[1]-5))
#			if (posNew[1] > frame[1]-2):
#				pygame.mouse.set_pos(((posNew[0], 5)))
#			error = cam.mouse_events(mouse_mov, event)
#		screen.fill((200, 200, 200))
#
#		for i, edge in enumerate(edges):
#			points = []
#			for tt in (vertices[edge[0]], vertices[edge[1]]):
#				#print(tt)
#				x, y, z = tt
#				x -= cam.pos[0]
#				y -= cam.pos[1]
#				z -= cam.pos[2]
#
#				#x,z = rotate2d((x,z), cam.rot[0])
#				#y,z = rotate2d((y,z), cam.rot[1])
#				vec = quaternions.qrot_vec([x, y, z], cam.rot_x, cam.axis_y, cam.pos)
#				vec = quaternions.qrot_vec(vec, cam.rot_y, cam.axis_x, cam.pos)
#				x, y, z = vec
#				f = 200/float(z)
#				x, y = x*f, y*f
#				points += [(center_x+int(x), center_y+int(y))]
#			if i == 12:
#				pygame.draw.line(screen, (200,0,0), points[0], points[1], 1)
#			elif i == 13:
#				pygame.draw.line(screen, (0,200,0), points[0], points[1], 1)
#			elif i == 14:
#				pygame.draw.line(screen, (0,0,200), points[0], points[1], 1)
#			else:
#				pygame.draw.line(screen, (0,0,0), points[0], points[1], 1)
#
#		#vert_list = []
#		#screen_coords = []
#		#for x, y, z in vertices:
#		#	x -= cam.pos[0]
#		#	y -= cam.pos[1]
#		#	z -= cam.pos[2]
#		#	x,z = rotate2d((x,z), cam.rot[0])
#		#	y,z = rotate2d((y,z), cam.rot[1]
#		#	f = 200/float(z)
#		#	x, y = x*f, y*f
#		#	points += [(center_x+int(x), center_y+int(y))]
#		pygame.display.flip()
#		key = pygame.key.get_pressed()
#		cam.update(dt, key)
#
#		t += dt
#		if t >5000:
#			t = 1

# frame, cam, nodes, edges
