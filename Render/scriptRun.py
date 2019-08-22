from wireFrame import *
from rendering import *
from quaternions import *



#cube = Wireframe()
node_list = [(0,0,0), (0,2,0), (0,1,1), 
			 (1,1,0), (-1,3,0), (0,2,1)]

edge_list = [(0,1),(1,2), (2,0), (3,4),
			 (4,5),(3,5)]

#face_list = [(), ()]

#cube.addNodes(node_list)
#cube.addEdges(edge_list)
myscreen = projectOnScreen((1000, 600),Cam(pos=(5,5,5)), node_list, edge_list, rot=False)
myscreen.run(edges=True, nodes=True, axis=True)


