import numpy as np, pygame, sys

def r2a(r):
    return r * (180 / np.pi)

def a2r(a):
    return a * (np.pi / 180)


def centeriod(vert: list):
    '''
    @param: vertices list of numpy.array type
    return: numpy array -> centeriod of shape
    '''
    x, y = 0, 0
    n = len(vert)
    if n == 0:
        raise "vetix container empty !"
    for i in vert:
        x += i[0]
        y += i[1]
    return np.array([x/n, y/n])

def normalize(a):
	v = np.linalg.norm(a)
	# if v < 1e-10: return np.array([0.0, 0.0])
	a = a / v
	return a

def align(a, b):
    if np.dot(a, b)<0: return -a
    return a

def normal(a, b=None, nrm=False):
    '''
    @param:a-> normal to find against
    @param:b-> nomral direction along
    here p is counter clockwise rotated by default
    '''
    p = np.array([a[1], -a[0]], dtype=np.float32)
    # p = a@np.array([[0, -1], 
    #                 [1,  0]])

    if nrm: 
    	p = normalize(p)

    if b is None: 
        return p

    return align(p, b)


def cross(v1, v2, magnitude=True):
    return v1[0]*v2[1] -v1[1]*v2[0]


# truth value of vec in same direction to d.
def same_dir(vec, d):
    return np.dot(vec, d)>0


def support(a, b, d):
    '''
    @param: a-> shape A 
    @param: b-> shape B
    @param:dir-> direction (numpy.array shape (2, ))
    returns: 2D point with max dot pord
    '''
    return a.find_furthest(d) - b.find_furthest(-d)
