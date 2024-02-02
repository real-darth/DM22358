import numpy as np
import random
import array
from functools import wraps
from timeit import default_timer as timer
import matplotlib.pyplot as plt

N = 5 # temporary value

# set seeds for determenistic
np.random.seed(0)
random.seed(0)

# time decorator to measure time
def timefn(fn):
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1 = timer()
        result = fn(*args, **kwargs)
        t2 = timer()
        time_delta = t2 - t1
        # print(f"@timefn: {fn.__name__} took {time_delta} seconds")
        return result, time_delta  # return result and time delta
    return measure_time

@timefn
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
@timefn
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

@timefn
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

@timefn
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

def caluclate_flops(N, time_delta):
    """
    This function calculates the FLOPS/s
    :param N: The size of the matrices
    :param time_delta: Time it took to complete the DGEMM
    :return: The FLOPS/s for these parameters
    """
    return (2 * pow(N, 3)) / time_delta

def measure_main_functions():
    # testing with different sizes
    sizes = [5, 10, 20, 30, 40, 50, 60, 70]#, 100]#, 200, 300, 500]
    # testing three functions, 10 times, for all sizes
    time_measurments = np.zeros((3, len(sizes), 10))
    # calculate the flops at each dimension to get some measurements
    #FLOPS = np.zeros((3, len(sizes), 10))  
    # iterate over increasing sizes to see how performance is affected
    for size in sizes:
        print('Running for size {} X {}'.format(size, size))
        # repeat all calculations 10 times
        for i in range(0, 10):
            # get the result of the DGEMM and the time it took to complete it
            # numpy
            result, dt = dgemm_numpy_array(N=size)
            time_measurments[0][sizes.index(size)][i] = dt
            #FLOPS[0][sizes.index(size)][i] = caluclate_flops(size, dt)

            # lists
            result, dt = dgemm_python_list(N=size)
            time_measurments[1][sizes.index(size)][i] = dt
            
            # arrays
            result, dt = dgemm_python_array(N=size)
            time_measurments[2][sizes.index(size)][i] = dt
    
    print('Calculating Average Times')
    # calculate average times
    averages = np.mean(time_measurments, axis=2)
    
    # create the plots
    print('Plotting Results')
    lables = ['numpy', 'list', 'array']
    for i in range(3):
        plt.plot(sizes, averages[i], label=lables[i])  # plot the average time vs size
        plt.xticks(sizes, labels=sizes)
        plt.xlabel('Size of Matrix (N x N)')
        plt.ylabel('Average Time')
    
    plt.legend()
    plt.show()

def measure_blas_function():
    return 0

def main():
    measure_main_functions()

if __name__ == "__main__":
    main()