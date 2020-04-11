import numpy as np 

def lineSplit(pos1, pos2, lis, factor):
	point1 = np.array(pos1)
	point2 = np.array(pos2)
	distance = np.linalg.norm(point2-point1)

	if distance > 10:
		new_point = (point1+point2)/2
		lineSplit(pos1, new_point, lis, factor)
		lineSplit(new_point, pos2, lis, factor)
	else:
		for i in point1:
			lis.append(i)
		for i in point2:
			lis.append(i)

def Solver(line1, line2):
	"""
	line1 = [[1,2,3], [1,2,3]]
	line2 = [[1,2,3], [1,2,3]]
	a = line1[0]
	b = line1[1]
	"""
	a = np.array(line1[0])
	b = np.array(line1[1])
	u = np.array(line2[0])
	v = np.array(line2[1])
	#print(a,b,u,v)
	c = u[:2]-a[:2]
	A = np.vstack((b[:2],-v[:2])).T
	#print(A)
	x = np.linalg.solve(A,c)
	#print(x)
	p = a+x[0]*b
	#print(p)
	return p

def planCreator(pos1, pos2, pos3, pos4, allPoints):
	lis12 = []
	lis41 = []

	dir1 = np.array(pos2)- np.array(pos1)
	dir2 = np.array(pos4)- np.array(pos1)

	lineSplit(pos1, pos2, lis12, 0)
	lineSplit(pos1, pos4, lis41, 0)

	for i in range(0,len(lis12)-5, 3):
		for j in range(0,len(lis41)-5, 3):
			a = np.array((lis12[i], lis12[i+1], lis12[i+2]))
			u = np.array((lis41[j], lis41[j+1], lis41[j+2]))
			# print(a,u,dir1, dir2)
			p = Solver([a, dir2], [u, dir1])
			# print(p)
			allPoints.append(list(p))

			a = np.array((lis12[i+3], lis12[i+4], lis12[i+5]))
			u = np.array((lis41[j], lis41[j+1], lis41[j+2]))
			# print(a,u,dir2,dir2)
			p = Solver([a, dir2], [u, dir1])
			# print(p)
			allPoints.append(list(p))

			a = np.array((lis12[i+3], lis12[i+4], lis12[i+5]))
			u = np.array((lis41[j+3], lis41[j+4], lis41[j+4]))
			# print(a,u,dir2, dir2)
			p = Solver([a, dir2], [u, dir1])
			# print(p)
			allPoints.append(list(p))

			a = np.array((lis12[i], lis12[i+1], lis12[i+2]))
			u = np.array((lis41[j+3], lis41[j+4], lis41[j+5]))
			# print(a,u,dir2, dir2)
			p = Solver([a, dir2], [u, dir1])
			# print(p)
			allPoints.append(list(p))
	# print(allPoints)
	return allPoints




if __name__ == "__main__":
	lis = []
	a = [5,2,-1]
	b = [1,-2,-3]

	u = [2,0,4]
	v = [1,2,-1]
	l1 = [a, [6,0,-4]]
	l2 = [a, [3,2,3]]
	#lineSplit((0,0), (200, 200), lis, 40)
	#print(Solver(l1, l2))
	planCreator((0,0,0), (5,0,0), (5,5,0), (0,5,0))
