import re

def dataFunction(file='mapFile.txt', factor=100, plane1=True, plane2=False):
	vertices = []
	edges = []
	faces = []
	height1 = 0
	height2 = 1

	with open(file, 'r')as fp:
		data = fp.read()
		info = re.findall(r'\-?\+?\d+', data)
		lines = []
		line = []
		for i, j in enumerate(info):
			lines.append(int(j)//factor)
		count = 0
		for i in range(0, len((lines))-3, 4):
			vertix1 = [lines[i], lines[i+1]]
			vertix2 = [lines[i+2], lines[i+3]]
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

			edges.append([count, count+1])
			edges.append([count+1, count+2])
			edges.append([count+2, count+3])
			edges.append([count+3, count])

			faces.append([count, count+1, count+2, count+3])
			count += 4
	if plane1:
		maxx, minn = max(lines), min(lines)
		total = maxx-minn
		vertices.append((total, total, height1))
		vertices.append((-total, total, height1))
		vertices.append((-total, -total, height1))
		vertices.append((total, -total, height1))
		edges.append([count, count+1])
		edges.append([count+1, count+2])
		edges.append([count+2, count+3])
		edges.append([count+3, count])
		faces.append([count, count+1, count+2, count+3])
		count+=4
	if plane2:
		vertices.append((total, total, height2))
		vertices.append((-total, total, height2))
		vertices.append((-total, -total, height2))
		vertices.append((total, -total, height2))
		edges.append([count, count+1])
		edges.append([count+1, count+2])
		edges.append([count+2, count+3])
		edges.append([count+3, count])
		faces.append([count, count+1, count+2, count+3])
	return vertices, edges, faces

if __name__ == "__main__":
	v,e,f = dataFunction()
	print(v)

