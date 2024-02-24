# neighbors.pyx
import numpy as np

cimport cython
from libc.math cimport pow

#@cython.boundscheck(False)  # Deactivate bounds checking
#@cython.wraparound(False)   # Deactivate negative indexing.

'''
cpdef int[:] calculate_neighbors(double[:] x, double[:] y, int b, double R_squared, int[:] neighbors):
    cdef int i
    cdef int n = x.shape[0]
    for i in range(n):
        neighbors[i] = (x[b] - x[i]) * (x[b] - x[i]) + (y[b] - y[i]) * (y[b] - y[i]) < R_squared

    return neighbors

'''

cpdef void calculate_neighbors(double[:] x, double[:] y, int N, double R_squared, int[:] neighbors):
    cdef int i, b
    for b in range(N):
        for i in range(N):
            neighbors[i] = (x[b] - x[i]) * (x[b] - x[i]) + (y[b] - y[i]) * (y[b] - y[i]) < R_squared