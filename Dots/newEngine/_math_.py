import numpy as np, pygame, sys

def r2a(r):
    return r * (180 / np.pi)

def a2r(a):
    return a * (np.pi / 180)


def centroid(vert: list):
    '''
    @param: vertices list of numpy.array type
    return: numpy array -> centroid of shape
    '''
    x, y = 0, 0
    n = len(vert)
    if n == 0:
        raise "vetix container empty !"
    for i in vert:
        x += i[0]
        y += i[1]
    return np.array([x/n, y/n])

def norm(a):
    return (a[0]**2 + a[1]**2)**0.5

def vdot(a, b):
    return a[0]*b[0] + a[1]*b[1]

def vrot(mat, a):
    return np.array([mat[0][0]*a[0] + mat[0][1]*a[1], mat[1][0]*a[0] + mat[1][1]*a[1]])

def unit(a, mag=False):
    v = norm(a)
    a = a / v
    if mag:
        return a, v
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
    p = np.array([a[1], -a[0]], dtype=np.float64)
    # p = a@np.array([[0, -1], 
    #                 [1,  0]])

    if nrm: 
    	p = unit(p)

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

def constraint_solver(amass, bmass, ami, bmi, av, bv):
    pass

