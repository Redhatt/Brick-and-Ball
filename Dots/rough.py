import numpy as np 
from time import time

r = 10
t = int(1e5)
avg = 0
a = np.array([1.1, 2.2])
b = np.array([1.1, 2.2])

for i in range(r):
    s = time()
    for i in range(t):
        # v = np.dot(a, b)
        v = a[0]*b[0] + a[1]*b[1]
    e = time()
    print(e - s)
    avg += (e-s)
print('final', avg/r)

# np norm -> 0.11472735404968262
# no np   -> 0.09704227447509765