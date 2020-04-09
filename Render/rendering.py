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
	def __init__(self, frame, cam, nodes, edges, spherical=False, node_color=(200, 0, 0), edge_color=(0, 0, 0)):
		self.coordinates = np.array([1,1,1])
		self.frame = frame
		self.center_x, self.center_y = self.frame[0] * 0.5, self.frame[1] * 0.5
		self.cam = cam
		self.projected_coordinates = np.array([1, 1])
		self.spherical = spherical
		self.edges = edges
		self.edge_color = edge_color
		self.nodes = nodes
		self.node_color = node_color

	# shifting coordinate system...
	def translate(self):
		self.coordinates -= np.array(self.cam.pos)

	def rotate_3D(self):
		vec = quaternions.qrot_vec(self.coordinates, self.cam.rot_x, self.cam.azimuthal_vec, self.cam.pos)
		vec = quaternions.qrot_vec(vec, self.cam.rot_y, self.cam.pitch_vec, self.cam.pos)
		self.coordinates = vec

	def project(self):
		self.coordinates = np.array(self.coordinates)
		some_factor = 10000 # pixel to unit ratio inverse.
		planner = np.dot(self.coordinates, self.cam.roll_vec)
		sphere = np.linalg.norm(self.coordinates)
		angle = sphere/planner

		if not self.spherical:
			ratio = self.cam.radius/planner
			projected_vec = ratio*self.coordinates-self.cam.roll_vec*self.cam.radius
			along = np.dot(self.cam.azimuthal_vec, projected_vec)
			prepen = np.dot(self.cam.pitch_vec, projected_vec)
			self.projected_coordinates = [int(prepen*some_factor + self.center_x), int(along*some_factor + self.center_y)]
		else:
			ratio = self.cam.radius/sphere
			projected_vec = ratio*self.coordinates-self.cam.roll_vec*self.cam.radius
			along = np.dot(self.cam.azimuthal_vec, projected_vec)
			prepen = np.dot(self.cam.pitch_vec, projected_vec)
			self.projected_coordinates = [int(prepen*some_factor + self.center_x), int(along*some_factor + self.center_y)]


	def select_transform(self):
		# pretty useless
		# pos = self.cam.pos
		if True:#not self.rot:
			#self.rotate_3D()
			self.translate()
			self.project()
		else:
			self.cam.pos = np.array([0, 0, 0])
			#self.rotate_3D()
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
		if color == None or color == (125, 56, 89):
			color = self.node_color
		for node in nodes:
			self.coordinates = node
			self.select_transform()
			if node == (-1,1,1):
				color = (125, 56, 89)
			pygame.draw.circle(screen, color, self.projected_coordinates, 5, 0)

	def render_axis(self, screen):
		axis_color = ((255, 0, 0), (0, 255, 0), (0, 0, 255), (252, 85, 8))
		axis_letter = ('X', 'Y', 'Z')
		vertices_a = [(0,0,0), (3,0,0), (0,3,0), (0,0,3)]
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
			pygame.draw.circle(screen, axis_color[i], self.projected_coordinates, 5, 0)
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
			dt = clock.tick()/1000.0
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
				self.render_nodes(screen, self.nodes, self.node_color)
			if axis:
				self.render_axis(screen)
			pygame.display.flip()
			key = pygame.key.get_pressed()
			if key[pygame.K_t]:
				if self.spherical:
					time.sleep(0.5)
					self.spherical=False
				else:
					time.sleep(0.5)
					self.spherical=True
			self.cam.update(dt, key)

			t += dt
			if t >5000:
				t = 1


class Cam:
	def __init__(self, pos=(1,1,1)):
		self.z_axis = np.array([0,0,1])
		self.radius = 0.02
		self.pos = np.array(pos)
		self.rot_x = 0
		self.rot_y = 0
		self.roll_vec = np.array((0,0,-1))
		self.azimuthal_vec = -np.array((1,0,0)) # azimuthal negetive because in pygames pixel coords for y axis is negetive
												# and z projects to y_pixel
		self.pitch_vec = np.cross(self.azimuthal_vec, self.roll_vec)
		self.sensitivity = 800.0
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
		self.rot_x = -x/self.sensitivity
		self.rot_y = y/self.sensitivity
		if abs(self.rot_x)>0.6125:
			self.rot_x = 0
		if abs(self.rot_y)>0.6125:
			self.rot_y = 0
		# try:
		# 	prevR = math.degrees(math.acos(self.roll_vec[0]))
		# 	prevZ = math.degrees(math.acos(self.azimuthal_vec[1]))
		# 	prevP = math.degrees(math.acos(self.pitch_vec[1]))
		# 	prevZ_vec = self.azimuthal_vec
		# 	prevP_vec = self.pitch_vec
		# except:
		# 	pass
		self.roll_vec = quaternions.qrot_vec(self.roll_vec, self.rot_x, self.z_axis) # rotating about z-axis
		self.azimuthal_vec = quaternions.qrot_vec(self.azimuthal_vec, self.rot_x, self.z_axis)# rotating about z-axiz
		self.pitch_vec = quaternions.qrot_vec(self.pitch_vec, self.rot_x, self.z_axis)# rotating about z-axiz
		self.roll_vec = quaternions.qrot_vec(self.roll_vec, self.rot_y, self.pitch_vec) # rotating about z-axis
		self.azimuthal_vec = quaternions.qrot_vec(self.azimuthal_vec, self.rot_y, self.pitch_vec) # rotating about z-axis
		# print(111, self.rot_x)
		# try:
		# 	if abs(prevZ-math.degrees(math.acos(self.azimuthal_vec[1])))>5:
		# 		print("Z")
		# 		print(self.rot_x)
		# 		print(self.rot_y)
		# 		print(prevZ_vec)
		# 		print(prevP_vec)
		# 		print(self.azimuthal_vec)
		# 		print(self.pitch_vec)
		# 		print(prevZ, math.degrees(math.acos(self.azimuthal_vec[1])), prevZ-math.degrees(math.acos(self.azimuthal_vec[1])))
		# 		print(prevP, math.degrees(math.acos(self.pitch_vec[1])), prevP-math.degrees(math.acos(self.pitch_vec[1])))
		# 		print()
		# 	if abs(prevP-math.degrees(math.acos(self.pitch_vec[1])))>5:
		# 		print("P")
		# 		print(self.rot_x)
		# 		print(self.rot_y)
		# 		print(self.azimuthal_vec)
		# 		print(self.pitch_vec)
		# 		print(prevZ_vec)
		# 		print(prevP_vec)
		# 		print(prevZ, math.degrees(math.acos(self.azimuthal_vec[1])), prevZ-math.degrees(math.acos(self.azimuthal_vec[1])))
		# 		print(prevP, math.degrees(math.acos(self.pitch_vec[1])), prevP-math.degrees(math.acos(self.pitch_vec[1])))
		# 		print()
		# except:
		# 	print(self.pitch_vec[1])
		# 	print(self.azimuthal_vec[1])

		# print(f"i {prevR} {math.degrees(math.acos(self.roll_vec[0]))}")
		# print(f"k {prevZ} {math.degrees(math.acos(self.azimuthal_vec[1]))}")
		# print(f"j {prevP} {math.degrees(math.acos(self.pitch_vec[1]))}")
		# print()
		return error

	def update(self, dt, key):
		s = dt*5
		self.pos = np.array(self.pos, dtype=np.float64)
		if key[pygame.K_a]: self.pos -= self.pitch_vec*s
		if key[pygame.K_s]: self.pos -= self.roll_vec*s
		if key[pygame.K_w]: self.pos += self.roll_vec*s
		if key[pygame.K_d]: self.pos += self.pitch_vec*s
		if key[pygame.K_q]: self.pos += self.azimuthal_vec*s
		if key[pygame.K_e]: self.pos -= self.azimuthal_vec*s
		if key[pygame.K_r]:
			# print("HERE!")
			# print(self.azimuthal_vec)
			# print(self.pitch_vec)
			self.pos = np.array([0,0,5])
			self.roll_vec -= np.array([0,0,-1])
			self.azimuthal_vec -= np.array([1,0,0])

if __name__ == "__main__":
	vertices = ((-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
					(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1))

	edges = ((0, 1), (1, 2), (2, 3), (3, 0),
			 (0, 4), (1, 5), (2, 6), (3, 7),
			 (4, 5), (5, 6), (6, 7), (7, 4))

	myscreen = projectOnScreen((1000, 600),Cam(pos=(0,0,5)), vertices, edges, spherical=False, node_color=(200, 0, 0))
	myscreen.run(edges=True, nodes=True, axis=True)

