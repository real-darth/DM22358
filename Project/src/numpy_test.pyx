import numpy as np
cimport cython

cpdef np.ndarray[np.int_t, ndim=1] calculate_neighbors(np.ndarray[np.float64_t, ndim=1] x, np.ndarray[np.float64_t, ndim=1] y, int b, double R_squared):
    return (x[b] - x)**2 + (y[b] - y)**2 < R_squared