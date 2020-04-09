import quaternions as Q
import numpy as np
import math
pi = 3.14159

axis1 = [0,0,1]
# axis2 = np.array([0,1,0])
# axis2 = np.random.random((1,3)).reshape(3,)
# axis3 = np.array([0,0,1])
direction = [1,0,0]
orientation = [ 0.99178131, -0.12794466,  0]
pitch = [0,1,0]
# al = [direction, orientation, pitch]
# q = ['i', 'k', 'j']
point = np.array([0,0,0])
angle = -1.2425
v1 = Q.qrot_vec(orientation, angle, axis1, point=point)
print(v1)
# print(math.degrees(math.acos(np.dot(orientation, v1))))
# print(math.degrees(angle))
# v2 = Q.qrot_vec(orientation, pi/3, axis1, point=point)
# pitch = np.cross(v2,v1)
# ans1 = Q.qrot_vec(v1, pi/3, pitch, point=point)
# ans2 = Q.qrot_vec(v2, pi/3, pitch, point=point)
# v1 = Q.qrot_vec(pitch, pi/3, axis1, point=point)
# v1 = Q.qrot_vec(orientation, pi/3, axis1, point=point)
# direction = np.cross(pitch, orientation)

# print(ans1, np.linalg.norm(ans1))
# print(ans2, np.linalg.norm(ans2))


# v1 = Q.qrot_vec(direction, pi/3, axis1, point=point)
# v2 = Q.qrot_vec(orientation, pi/3, axis1, point=point)
# pitch = np.cross(v2,v1)
# ans1 = Q.qrot_vec(v1, pi/3, pitch, point=point)
# print(ans1, ans2)

a = -1.24
x = np.array([0.99178131, -0.12794466]).reshape(2,1)

R = np.array([[np.cos(a), -np.sin(a)],
               [np.sin(a),  np.cos(a)]])
y = R@x
print(y)
#print(R.shape, x.shape)

    # 0 -1 1 = 0  
    # 1  0 0   1

    # c -s
    # s  c