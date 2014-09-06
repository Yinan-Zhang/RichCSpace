import numpy as np
import math
from scipy import linalg
from hyper_geometry import vec, hyper_sphere

def radical_center(spheres):
    n = len(spheres)
    if n != 4:
        print "Error: number of spheres is not 3"
        return
    M = []
    for i in range(len(spheres)):
        center = spheres[i].center
        radius = spheres[i].radius
        M.append(constraint(center, radius))
    d = len(spheres[0].center)
    b = []
    A = []
    for i in range(len(spheres)-1):
        b.append(M[i][d] - M[i+1][d])
        c = []
        for j in range(d):
            c.append(M[i][j] - M[i+1][j])
        A.append(c)
    print A, b
    x = np.linalg.solve(A,b)
    print x
    p = x.tolist()
    dist = (vec(p) - spheres[0].center).r()
    return dist

def constraint(center, radius):
    A = []
    summation = 0.0
    for i in range(len(center)):
        A.append(-2 * center[i])
        summation += center[i] * center[i]
    A.append(radius * radius - summation)
    return A

def main():
   spheres = []
   spheres.append(sphere([0, 0, 0], 1))
   spheres.append(sphere([0.6, 0.5, 0.6], 1))
   spheres.append(sphere([0.5, 0.5, 0.4], 1))
   spheres.append(sphere([0.3, 0.3, 0.2], 1))
   print radical_center(spheres)

if __name__ == "__main__":
    main()
