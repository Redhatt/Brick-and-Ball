import numpy as np 

def lineSplit(pos1, pos2, lis, factor):
	point1 = np.array(pos1)
	point2 = np.array(pos2)
	distance = np.linalg.norm(point2-point1)

	if distance > 4:
		new_point = (point1+point2)//2
		lineSplit(pos1, new_point, lis, factor)
		lineSplit(new_point, pos2, lis, factor)
	else:
		for i in point1:
			lis.append(i)
		for i in point2:
			lis.append(i)

if __name__ == "__main__":
	lis = []
	lineSplit((0,0), (200, 200), lis, 40)
	print(lis)
