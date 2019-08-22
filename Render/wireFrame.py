from rendering import *


# to trace Coordinate of nodes...
class Node:
	def __init__(self, coordinates):
		self.coordinates = coordinates
		self.x = coordinates[0]
		self.y = coordinates[1]
		self.z = coordinates[2]


# to trace Edge...
class Edge:
	# start and stop are integers defining virtual(non existing field) index of Nodes...
	def __init__(self, start, stop):
		self.start = start
		self.stop = stop


# to trace Wireframe from edge and nodes...
class Wireframe:
	# defining node list and edge list...
	def __init__(self):
		self.nodes = []
		self.edges = []

	# adds node object in self.nodes...
	def addNodes(self, nodeList):
		for node in nodeList:
			self.nodes.append(Node(node))

	# adds Edges in order corresponding to edgeList...
	def addEdges(self, edgeList):
		for (start, stop) in edgeList:
			self.edges.append(Edge(self.nodes[start], self.nodes[stop]))


if __name__ == "__main__":
	node_list = [(-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
				 (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)]
	edge_list = [(0, 1), (1, 2), (2, 3), (3, 0),
				 (0, 4), (1, 5), (2, 6), (3, 7),
				 (4, 5), (5, 6), (6, 7), (7, 4)]

	wire_frame = Wireframe()
	wire_frame.addNodes(node_list)
	wire_frame.addEdges(edge_list)
	# _________________________________________________________________________
	pygame.init()
	frame = (1000, 600)
	center_x, center_y = frame[0]*0.5, frame[1]*0.5
	center_coordinates = int(center_x), int(center_y)
	screen = pygame.display.set_mode(frame)
	clock = pygame.time.Clock()
	# _________________________________________________________________________
	
	while True:
		dt = clock.tick()/float(1000)
		screen.fill((200, 200, 200))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()

		for i in wire_frame.edges:		
			pygame.draw.line(screen, (0,0,0),  (projectOnScreen(i.start.coordinates, center_coordinates)), 
										(projectOnScreen(i.stop.coordinates, center_coordinates)), 1)
		for i in wire_frame.nodes:
			pygame.draw.circle(screen, (0,0,0), (projectOnScreen(i.coordinates, center_coordinates)), 2, 0)
		pygame.display.flip()
