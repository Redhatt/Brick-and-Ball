import pygame
import sys, math, time
import quaternions
import numpy as np
import mapConversion


class projectOnScreen:
	def __init__(self, frame, cam, nodes, edges, faces, spherical=False, node_color=(200, 0, 0), edge_color=(0, 0, 0), face_color=None):
		self.coordinates = np.array([1,1,1])
		self.frame = frame
		self.center_x, self.center_y = self.frame[0] * 0.5, self.frame[1] * 0.5
		self.cam = cam
		self.projected_coordinates = np.array([1, 1, 1])
		self.spherical = spherical
		self.edges = edges
		self.faces = faces
		self.edge_color = edge_color
		self.nodes = nodes
		self.node_color = node_color
		self.face_color = face_color

	# shifting coordinate system...
	def translate(self):
		self.coordinates = np.float64(self.coordinates)
		self.coordinates -= np.array(self.cam.pos)

	def rotate_3D(self):
		vec = quaternions.qrot_vec(self.coordinates, self.cam.rot_x, self.cam.azimuthal_vec, self.cam.pos)
		vec = quaternions.qrot_vec(vec, self.cam.rot_y, self.cam.pitch_vec, self.cam.pos)
		self.coordinates = vec

	def project(self):
		self.coordinates = np.array(self.coordinates)
		planner = np.dot(self.coordinates, self.cam.roll_vec)
		sphere = np.linalg.norm(self.coordinates)
		tt = self.cam.radius/planner
		if 0<tt<0.9:#math.copysign(1,planner) == 1:
			visible = 1
		else:
			visible = 0
		if not self.spherical:
			ratio = self.cam.radius/planner
			projected_vec = ratio*self.coordinates-self.cam.roll_vec*self.cam.radius
			along = np.dot(self.cam.azimuthal_vec, projected_vec)
			perpen = np.dot(self.cam.pitch_vec, projected_vec)
			self.projected_coordinates = [int(perpen*self.cam.scale + self.center_x), int(along*self.cam.scale + self.center_y), visible]
		else:
			ratio = self.cam.radius/sphere
			projected_vec = ratio*self.coordinates-self.cam.roll_vec*self.cam.radius
			along = np.dot(self.cam.azimuthal_vec, projected_vec)
			perpen = np.dot(self.cam.pitch_vec, projected_vec)
			self.projected_coordinates = [int(perpen*self.cam.scale + self.center_x), int(along*self.cam.scale + self.center_y), visible]


	def edgeVisiblePoint(self, visible_points, points):
		point1 = [x for x in points[0]]
		point2 = [x for x in points[1]]
		self.coordinates = np.float64(self.coordinates)
		if point1[2] == 0 and point2[2] == 0:
			return None
		else:
			if point2[2] == 0:
				b = visible_points[1]-visible_points[0]
				# a = visible_points[0]
				# self.coordinates = a+((self.cam.radius-np.dot(a, self.cam.roll_vec))/(np.dot(b,self.cam.roll_vec)))*b
				self.coordinates = visible_points[0]+((self.cam.radius-np.dot(visible_points[0], self.cam.roll_vec))/(np.dot(b,self.cam.roll_vec)))*b
				self.project()
				point2 = self.projected_coordinates
			elif point1[2] == 0:
				b = visible_points[0]-visible_points[1]
				#a = visible_points[1]
				self.coordinates = visible_points[1]+((self.cam.radius-np.dot(visible_points[1], self.cam.roll_vec))/(np.dot(b,self.cam.roll_vec)))*b
				self.project()
				point1 = self.projected_coordinates
			else:
				return points
		return [point1, point2]

	def faceVisiblePoint(self, visible_points, new_face):
		n = len(new_face)
		count = 0
		changed_faces = []
		for i in range(n):
			if new_face[i][2] == 0 and new_face[(i+1)%n][2] == 0:
				count += 1
			elif new_face[i][2] == 1 and new_face[(i+1)%n][2] == 1:
				changed_faces.append(new_face[i])
			else:
				first, second = self.edgeVisiblePoint([visible_points[i], visible_points[(i+1)%n]], [new_face[i], new_face[(i+1)%n]])
				changed_faces.append(first)
				changed_faces.append(second)
		if count == n:
			return None
		else:
			return changed_faces

	def select_transform(self):
		self.translate()
		self.project()

	def render_faces(self, screen, faces, vertices, color=None):
		color = self.face_color
		if color:
			colors = [color]
		else:
			colors = ((200, 100, 50), (10, 200, 90), (50, 40, 200), (100, 200, 80), (158, 197, 145), (159, 40, 200), (110, 110, 110))
		c = len(colors)
		sort_face = []
		for i, face in enumerate(faces):
			mean = np.array([0,0,0], dtype=np.float64)
			new_face = []
			visible_points = []
			for nodes in face:
				self.coordinates = np.array(vertices[nodes])
				self.select_transform()
				visible_points += [self.coordinates]
				mean += np.array(self.coordinates)
				new_face.append(self.projected_coordinates)
			new_face = self.faceVisiblePoint(visible_points, new_face)
			sort_face.append((new_face, np.linalg.norm(mean/4), colors[i%c]))
		sort_face.sort(key=lambda x: x[1], reverse=True)

		for face in sort_face:
			if face[0] is not None:
				points_list = []
				for i in face[0]:
					points_list.append(i[:2])
				pygame.draw.polygon(screen, face[2], points_list)

	def render_edges(self,screen, edges, vertices, color=None):
		if color == None:
			color = self.edge_color
		for edge in edges:
			points = []
			visible_points = []
			for coordinates in (vertices[edge[0]], vertices[edge[1]]):
				self.coordinates = coordinates
				self.select_transform()
				visible_points += [self.coordinates]
				points += [self.projected_coordinates]
			points = self.edgeVisiblePoint(visible_points, points)
			if points is not None:
				pygame.draw.line(screen, color, points[0][:2], points[1][:2], 1)

	def render_nodes(self, screen, nodes, color=None):
		if color == None:
			color = self.node_color
		temp = []
		for i, node in enumerate(nodes):
			self.coordinates = node
			self.select_transform()
			temp.append((i, self.projected_coordinates))
			if self.projected_coordinates[2] == 1:
				pygame.draw.circle(screen, color, self.projected_coordinates[:2], 1, 0)
				# font = pygame.font.Font('freesansbold.ttf', 18)
				# text = font.render(f"{i}", True,(0,0,0))
				# textRect = text.get_rect()
				# textRect.center = (self.projected_coordinates[:2])
				# screen.blit(text, textRect)

	def render_axis(self, screen):
		axis_color = ((255, 0, 0), (0, 255, 0), (0, 0, 255), (252, 85, 8))
		axis_letter = ('X', 'Y', 'Z')
		vertices_a = [(0,0,0), (3,0,0), (0,3,0), (0,0,3)]
		edges_a = [(0,1), (0,2), (0,3)]
		for i, edge in enumerate(edges_a):
			points = []
			visible_points = []
			for coordinates in (vertices_a[edge[0]], vertices_a[edge[1]]):
				self.coordinates = coordinates
				self.select_transform()
				visible_points += [self.coordinates]
				points += [self.projected_coordinates]
			points = self.edgeVisiblePoint(visible_points, points)
			if points is not None:
				pygame.draw.line(screen, axis_color[i], points[0][:2], points[1][:2], 1)

		font = pygame.font.Font('freesansbold.ttf', 22)
		for i, node in enumerate(vertices_a[1:]):
			self.coordinates = node
			self.select_transform()
			if self.projected_coordinates[2] == 1:
				pygame.draw.circle(screen, axis_color[i], self.projected_coordinates[:2], 5, 0)
				text = font.render(axis_letter[i], True,axis_color[i])
				textRect = text.get_rect()	
				textRect.center = (self.projected_coordinates[0], self.projected_coordinates[1])
				screen.blit(text, textRect)
			# font = pygame.font.Font('freesansbold.ttf', 12)
			# text = font.render(f"{math.degrees(math.acos(self.cam.azimuthal_vec[2]))}", True,(0,0,0))
			# textRect = text.get_rect()
			# textRect.center = (500,10)
			# screen.blit(text, textRect)


	def run(self, faces=False, edges=True, nodes=True, axis=False, FPS=30):
		pygame.init()
		center_x, center_y = self.frame[0] * 0.5, self.frame[1] * 0.5
		center_x, center_y = int(center_x), int(center_y)
		screen = pygame.display.set_mode(self.frame)
		clock = pygame.time.Clock()
		pygame.event.get()
		pygame.mouse.get_rel()
		pygame.mouse.set_visible(0)
		pygame.event.set_grab(1)

		while True:
			dt = clock.tick(FPS)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						pygame.quit()
						sys.exit()
				self.cam.mouse_events(event)

			screen.fill((200, 200, 200))
			if faces:
				self.render_faces(screen, self.faces, self.nodes)
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
			self.cam.update(key)

class Cam:
	def __init__(self, pos=(1,1,1), FPS=30):
		self.FPS = FPS
		self.scale = 10000
		self.sensitivity = 0.5
		self.factorForRotation = 500*self.sensitivity/(self.FPS*self.scale)
		self.factorForTranslation = 2000/(self.FPS*self.scale)
		self.z_axis = np.array([0,0,1])
		self.radius = 0.02956
		self.pos = np.array(pos)
		self.rot_x = 0
		self.rot_y = 0
		self.roll_vec = np.array((0,0,-1))
		self.azimuthal_vec = -np.array((1,0,0)) # azimuthal negetive because in pygames pixel coords for y axis is negetive
												# and z projects to y_pixel
		self.pitch_vec = np.cross(self.azimuthal_vec, self.roll_vec)
		
	def mouse_events(self, event):
		try:
			x, y = event.rel
			error = True
		except Exception as e:
			error = True
			x, y = 0,0
		else:
			pass
		finally:
			pass
		self.rot_x = -x*self.factorForRotation
		self.rot_y = -y*self.factorForRotation
		if abs(self.rot_x)>(self.FPS*0.6125):
			self.rot_x = 0
		if abs(self.rot_y)>(self.FPS*0.6125):
			self.rot_y = 0
		self.roll_vec = quaternions.qrot_vec(self.roll_vec, self.rot_x, self.z_axis) # rotating about z-axis
		self.azimuthal_vec = quaternions.qrot_vec(self.azimuthal_vec, self.rot_x, self.z_axis)# rotating about z-axiz
		self.pitch_vec = quaternions.qrot_vec(self.pitch_vec, self.rot_x, self.z_axis)# rotating about z-axiz
		self.roll_vec = quaternions.qrot_vec(self.roll_vec, self.rot_y, self.pitch_vec) # rotating about z-axis
		self.azimuthal_vec = quaternions.qrot_vec(self.azimuthal_vec, self.rot_y, self.pitch_vec) # rotating about z-axis

	def update(self, key):
		self.pos = np.array(self.pos, dtype=np.float64)
		if key[pygame.K_LSHIFT]:
			s = 4*self.factorForTranslation
			if key[pygame.K_a]: self.pos -= self.pitch_vec*s
			if key[pygame.K_s]: self.pos -= self.roll_vec*s
			if key[pygame.K_w]: self.pos += self.roll_vec*s
			if key[pygame.K_d]: self.pos += self.pitch_vec*s
			if key[pygame.K_q]: self.pos += self.azimuthal_vec*s
			if key[pygame.K_e]: self.pos -= self.azimuthal_vec*s
		else:
			s = 10*self.factorForTranslation
			if key[pygame.K_a]: self.pos -= self.pitch_vec*s
			if key[pygame.K_s]: self.pos -= self.roll_vec*s
			if key[pygame.K_w]: self.pos += self.roll_vec*s
			if key[pygame.K_d]: self.pos += self.pitch_vec*s
			if key[pygame.K_q]: self.pos += self.azimuthal_vec*s
			if key[pygame.K_e]: self.pos -= self.azimuthal_vec*s

		if key[pygame.K_r]:
			self.pos = np.array([0,0,5])
			self.roll_vec -= np.array([0,0,-1])
			self.azimuthal_vec -= np.array([1,0,0])

if __name__ == "__main__":
	# cube = ((-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
	# 				(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1))

	# cube_edges = ((0, 1), (1, 2), (2, 3), (3, 0),
	# 		 (0, 4), (1, 5), (2, 6), (3, 7),
	# 		 (4, 5), (5, 6), (6, 7), (7, 4))

	# #                  -z            z              -x           x             -y            y
	# cube_faces = ((0, 1, 2, 3), (4, 5, 6, 7), (0, 4, 7, 3), (1, 5, 6, 2), (0, 1, 5, 4), (3, 2, 6, 7))
	# cube_faces_X = ((0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (3, 2, 6, 7))
	# cube_faces_Y = ((0, 1, 2, 3), (4, 5, 6, 7), (0, 4, 7, 3), (1, 5, 6, 2))

	# vertices = []
	# edges = []
	# faces = []

	# for c_nodes in cube:
	# 	value = list(c_nodes[:])
	# 	vertices.append(value)

	# for i in range(1,4):
	# 	for c_nodes in cube:
	# 		value = list(c_nodes[:])
	# 		value[0] += i*2
	# 		vertices.append(value)

	# for i in range(1,4):
	# 	for c_nodes in cube:
	# 		value = list(c_nodes[:])
	# 		value[1] += i*2
	# 		vertices.append(value)

	# for i, face in enumerate(cube_faces):
	# 	if i == 3 or i == 5:
	# 		continue
	# 	else:
	# 		faces.append(face)

	# for i in range(1,4):
	# 	for c_faces in cube_faces_X:
	# 		value3 = list(c_faces[:])
	# 		for k in range(len(value3)):
	# 			value3[k] += i*8
	# 		faces.append(value3)

	# for i in range(4,7):
	# 	for c_faces in cube_faces_Y:
	# 		value3 = list(c_faces[:])
	# 		for k in range(len(value3)):
	# 			value3[k] += i*8
	# 		faces.append(value3)

	# for i in range(7):
	# 	for c_edge in cube_edges:
	# 		value2 = list(c_edge[:])
	# 		for j in range(len(value2)):
	# 			value2[j] += i*8
	# 		edges.append(value2)


	vertices, edges, faces = mapConversion.dataFunction(file="Maze.txt", factor=80, plane1=False, plane2=False)	
	# vertices, edges, faces = mapConversion.dataFunction(factor=100, plane1=False, plane2=False)	

	# myscreen = projectOnScreen((1000, 600),Cam(pos=(0,0,5)), cube, cube_edges, cube_faces, spherical=False, node_color=(200, 0, 0))
	# myscreen.run(faces=True, edges=True, nodes=True, axis=True, FPS=30)

	myscreen = projectOnScreen((1500, 600),Cam(pos=(0,0,0.5)), vertices, edges, faces, spherical=False,)# node_color=(200, 0, 0), face_color=(150, 150, 100))
	myscreen.run(faces=True, edges=False, nodes=False, axis=False, FPS=60)

	# planep = ((0,0,0), (50,0,0), (50,50,0), (0,50,0))
	# edgep = ((0,1), (1,2), (2,3), (3,0))
	# facep = [(0,1,2,3)]
	# myscreen = projectOnScreen((1000, 600),Cam(pos=(0,0,5)), planep, edgep, facep, spherical=False, node_color=(200, 0, 0))
	# myscreen.run(faces=True, edges=True, nodes=True, axis=True, FPS=60)

