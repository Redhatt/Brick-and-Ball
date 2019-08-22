from wireFrame import *
from rendering import *
from quaternions import *



#cube = Wireframe()
node_list = [(-1,-1,-1), (1,-1,-1), (1,1,-1), (-1,1,-1),
			(-1,-1,1), (1,-1,1), (1,1,1), (-1,1,1)]

edge_list = [(0,1),(1,2), (2,3), (3,0),
			 (0,4),(1,5), (2,6), (3,7),
			 (4,5),(5,6), (6,7), (7,4)]

#cube.addNodes(node_list)
#cube.addEdges(edge_list)
myscreen = projectOnScreen((1000, 600),Cam(pos=(0,0,5)), node_list, edge_list, rot=False)
myscreen.run(edges=True, nodes=True, axis=True)