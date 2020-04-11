import re
from tools import lineSplit, planCreator

def edgesCounter(edges, vertices):
	n=4
	for i in range(0, len(vertices)-3, 4):
		for j in range(n):
			edges.append([i+j, i+(j+1)%n])

def facesCounter(faces, vertices):
	for i in range(0, len(vertices)-3, 4):
		faces.append([i, i+1, i+2, i+3])

def dataFunction(file='mapFile.txt', factor=40, plane1=False, plane2=False):
	vertices = []
	edges = []
	faces = []
	height1 = 2
	height2 = 0
	aa = 1
	with open(file, 'r')as fp:
		data = fp.read()
		info = re.findall(r'\-?\+?\d+', data)
		old_lines = []
		line = []
		for i, j in enumerate(info):
			old_lines.append(int(j)/factor)
		count = 0

		lines = []
		for i in range(0, len(old_lines)-3, 4):
			lineSplit([old_lines[i], old_lines[i+1]], [old_lines[i+2], old_lines[i+3]], lines, factor)
		# print(old_lines)
		# print(lines)
		for i in range(0, len((lines))-3, 4):
			vertix1 = [int(lines[i]), int(lines[i+1])]
			vertix2 = [int(lines[i+2]), int(lines[i+3])]
			vertix3 = [x for x in vertix2[:]]
			vertix4 = [x for x in vertix1[:]]
			vertix1.append(height1)
			vertix2.append(height1)
			vertix3.append(height2)
			vertix4.append(height2)

			vertices.append(vertix1)
			vertices.append(vertix2)
			vertices.append(vertix3)
			vertices.append(vertix4)

	maxx, minn = max(lines), min(lines)
	total = max(int(maxx-minn)//2, 10)
	if plane1:
		planCreator((total,total,height1), (-total,total,height1), (-total,-total,height1), (total,-total,height1), vertices)
	if plane2:
		planCreator((total,total,height2), (-total,total,height2), (-total,-total,height2), (total,-total,height2), vertices)
	edgesCounter(edges, vertices)
	facesCounter(faces, vertices)

	return vertices, edges, faces

if __name__ == "__main__":
	v,e,f = dataFunction()
	#print(len(v)-4)
	print(v)

