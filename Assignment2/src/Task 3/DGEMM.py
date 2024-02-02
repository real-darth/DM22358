import numpy as np
import random
import array

N = 5 # temporary value
# double-precision floating-point number
dt = np.dtype('d')

# set seeds for determenistic
np.random.seed(0)
random.seed(0)

def dgemm_blas() -> np.ndarray:
    """
    This function performs DGEMM using np.matmul for BLAS
    :param name: The name of the person to greet
    :return: C matrix
    """

    A = np.random.rand(N, N)  
    B = np.random.rand(N, N)
    # matmul is better for matrix multiplication
    # dot is better for vectors (and has high speed)
    C = np.matmul(A, B)
    return C 

# DGEMM (Double Precision General Matrix Multiplication)
def dgemm_numpy_array() -> np.ndarray:
    """
    This function performs DGEMM, implemented with numpy arrays
    :param name: The name of the person to greet
    :return: C matrix
    """

    A = np.random.rand(N, N)  
    B = np.random.rand(N, N)
    C = np.zeros((N, N)) #, dtype=double)

    # dot product of A x B
    for i in range(N):
        for j in range(N):
            for k in range(N):
                C[i][j] += A[i][k] * B[k][j]

    return C 

def dgemm_python_list() -> list:
    """
    This function performs DGEMM, implemented with python lists
    :param name: The name of the person to greet
    :return: C matrix
    """

    A = [[random.random()] * N for _ in range(N)]
    B = [[random.random()] * N for _ in range(N)]
    C = [[0.0] * N for _ in range(N)]

    # dot product of A x B
    for i in range(N):
        for j in range(N):
            for k in range(N):
                C[i][j] += A[i][k] * B[k][j]
    
    return C

def dgemm_python_array() -> array:
    """
    This function performs DGEMM, implemented with python arrays
    :param name: The name of the person to greet
    :return: C matrix
    """

    # python arrays only support one dimension
    # thus we have to adjust how we initialize and calculate the multiplication
    # array type 'd' = double-precision floating-point number
    A = array.array('d', [random.random()] * N * N)
    B = array.array('d', [random.random()] * N * N)
    C = array.array('d', [0] * N * N)

    # dot product of A x B
    for i in range(N):
        for j in range(N):
            for k in range(N):
                C[(i * N) + j] += A[i * N + k] * B[k * N + j]

    return C


def main():
    return 0

if __name__ == "__main__":
    main()