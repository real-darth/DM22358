import numpy as np
import random
import array

N = 5 # temporary value
# double-precision floating-point number
dt = np.dtype('d')

# set seeds for determenistic
np.random.seed(0)
random.seed(0)

def dgemm_blas(A=None, B=None, N=N) -> np.ndarray:
    """
    This function performs DGEMM using np.matmul for BLAS
    :param name: The name of the person to greet
    :return: C matrix
    """

    if A is None:
        A = np.random.rand(N, N)
    if B is None:
        B = np.random.rand(N, N)
    # matmul is better for matrix multiplication
    # dot is better for vectors (and has high speed)
    C = np.matmul(A, B)
    return C 

# DGEMM (Double Precision General Matrix Multiplication)
def dgemm_numpy_array(A=None, B=None, N=N) -> np.ndarray:
    """
    This function performs DGEMM, implemented with numpy arrays
    :param A: First input matrix, if None, run random values
    :param B: Second input matrix, if None, run random values
    :param N: The size of the matrices
    :return: C matrix
    """

    if A is None:
        A = np.random.rand(N, N)  
    if B is None:
        B = np.random.rand(N, N)
    C = np.zeros((N, N)) #, dtype=double)

    # dot product of A x B
    for i in range(N):
        for j in range(N):
            for k in range(N):
                C[i][j] += A[i][k] * B[k][j]

    return C 

def dgemm_python_list(A=None, B=None, N=N) -> list:
    """
    This function performs DGEMM, implemented with python lists
    :param A: First input matrix, if None, run random values
    :param B: Second input matrix, if None, run random values
    :param N: The size of the matrices
    :return: C matrix
    """
    if A is None:
        A = [[random.random()] * N for _ in range(N)]
    if B is None:
        B = [[random.random()] * N for _ in range(N)]
    C = [[0.0] * N for _ in range(N)]

    # dot product of A x B
    for i in range(N):
        for j in range(N):
            for k in range(N):
                C[i][j] += A[i][k] * B[k][j]
    
    return C

def dgemm_python_array(A=None, B=None, N=N) -> array:
    """
    This function performs DGEMM, implemented with python arrays
    :param A: First input array, if None, run random values
    :param B: Second input array, if None, run random values
    :param N: The size of the matrices
    :return: C matrix
    """

    # python arrays only support one dimension
    # thus we have to adjust how we initialize and calculate the multiplication
    # array type 'd' = double-precision floating-point number
    if A is None:
        A = array.array('d', [random.random()] * N * N)
    if B is None:
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