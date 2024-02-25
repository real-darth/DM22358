import numpy as np
cimport numpy as cnp
from libc.math cimport cos, sin, atan2
from cython.parallel import prange
cimport cython

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing.
cpdef void calculate_mean_theta(double[::1] x, double[::1] y, double[::1] theta, int N, double R, double[::1] mean_theta):
    cdef int b, i
    cdef double R_squared = R**2
    cdef double sx, sy, dist_squared
    
    for b in prange(N, nogil=True):
        sx = 0
        sy = 0
        for i in prange(b+1, N, nogil=False):
            dist_squared = (x[i] - x[b]) ** 2 + (y[i] - y[b]) ** 2
            if dist_squared < R_squared:
                sx += cos(theta[i])
                sy += sin(theta[i])
        mean_theta[b] = atan2(sy, sx)
