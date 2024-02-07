import numpy as np
import random
import time
import array
from functools import wraps
import matplotlib.pyplot as plt
import pandas as pd

N = 1 # default to one 

# comment / uncomment the TEST_SIZES you want to run
# max size of 1000 takes around 2 hours and 30 minutes to run
# max size of 300 takes around 3 minutes and 38 seconds to run

TEST_SIZES = [10, 30, 50, 70, 100, 200, 300, 500, 700, 1000]
#TEST_SIZES = [10, 30, 50, 70, 100, 200, 300]

FUNCTIONS_COUNT = 4 # we have four functions to test

# set seeds for determenistic
np.random.seed(0)
random.seed(0)

# time decorator to measure time
def timefn(fn):
    from timeit import default_timer as timer
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1 = timer()
        result = fn(*args, **kwargs)
        t2 = timer()
        time_delta = t2 - t1
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
        A = np.random.rand(N, N)    # dtype = float64 by default, float64 = double-precision
    if B is None:
        B = np.random.rand(N, N)
    C = np.zeros((N, N), dtype='float64')

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

def caluclate_flops_s(N, time_delta) -> float:
    """
    This function calculates the FLOPS/s
    :param N: The size of the matrices
    :param time_delta: Time it took to complete the DGEMM
    :return: The FLOPS/s for these parameters
    """
    return (2 * pow(N, 3)) / time_delta

def measure_main_functions():
    """
    1. Get all measurements for each of the four functions
    2. Write collected data to files
    3. Plot the results in graph

    Function time varies by how many sizes will be tested and how large the sizes are
    Default max size is set to 1000, can be changed in TEST_SIZES
    """
    # testing with different sizes
    sizes = TEST_SIZES
    # testing four functions, 10 times, for all sizes
    time_measurments = np.zeros((FUNCTIONS_COUNT, len(sizes), 10))
    # calculate the flops at each dimension (N) to get some measurements
    FLOPS_S = np.zeros((FUNCTIONS_COUNT, len(sizes), 10))
    # iterate over increasing sizes to see how performance is affected
    runtime = time.time()
    for size in sizes:
        print('Running for size {} X {}'.format(size, size))
        # repeat all calculations 10 times
        for i in range(0, 10):
            # get the result of the DGEMM and the time it took to complete it
            # numpy
            result, dt = dgemm_numpy_array(N=size)
            time_measurments[0][sizes.index(size)][i] = dt
            FLOPS_S[0][sizes.index(size)][i] = caluclate_flops_s(size, dt)

            # lists
            result, dt = dgemm_python_list(N=size)
            time_measurments[1][sizes.index(size)][i] = dt
            FLOPS_S[1][sizes.index(size)][i] = caluclate_flops_s(size, dt)
            
            # arrays
            result, dt = dgemm_python_array(N=size)
            time_measurments[2][sizes.index(size)][i] = dt
            FLOPS_S[2][sizes.index(size)][i] = caluclate_flops_s(size, dt)

            # BLAS
            result, dt = dgemm_blas(N=size)
            time_measurments[3][sizes.index(size)][i] = dt
            FLOPS_S[3][sizes.index(size)][i] = caluclate_flops_s(size, dt)
    
    print('Measurements took {} seconds'.format(time.time() - runtime))
    print('Calculating Average Times and writing to file...')
    
    # calculate average times
    average_time = np.mean(time_measurments, axis=2)
    average_FLOPS = np.mean(FLOPS_S, axis=2)
    # calculate the std
    std_time = np.std(time_measurments, axis=2)
    std_FLOPS = np.std(FLOPS_S, axis=2)

    # write data to file
    clear_previous_data()

    labels = ['numpy', 'list', 'array', 'BLAS']
    for i in range(FUNCTIONS_COUNT):
        write_data(sizes, average_time[i], std_time[i], labels[i], 'time')
        write_data(sizes, average_FLOPS[i], std_FLOPS[i], labels[i], 'flops')

    # create plots of data
    print('Plotting Time Results')
    plt.figure("Time Results")
    for i in range(FUNCTIONS_COUNT):
        plt.plot(sizes, average_time[i], label=labels[i])  # plot the average time vs size
        plt.xticks(sizes, labels=sizes)
        plt.xlabel('Size of Matrix (N x N)')
        plt.ylabel('Average Time (s)')

    plt.title("Average Time of DGEMM Computation by Matrix Size")
    plt.legend()

    print('Plotting FLOPS Results')
    plt.figure("FLOPSs Results")
    # skip the BLAS function, since it disrupts the FLOP/s graph (for now)
    for i in range(FUNCTIONS_COUNT - 1):
        plt.plot(sizes, average_FLOPS[i], label=labels[i])  # plot the average FLOPS/s vs size
        plt.xticks(sizes, labels=sizes)
        plt.xlabel('Size of Matrix (N x N)')
        plt.ylabel('Average FLOPS/s')
    
    plt.title("FLOPS/s by Matrix Size")
    plt.legend()

    plt.show()

def clear_previous_data():
    """
    Function that removes all previous data to make room for the new data
    Be carefull when using, since it will delete the 'data' folder
    """
    import os
    import shutil

    # delete the 'data' directory if it exists
    if os.path.exists('data'):
        shutil.rmtree('data')

    # create new 'data' directory to put files in
    os.makedirs('data')

def write_data(sizes, averages, std, label, prefix) -> None:
    """
    Function that writes data to a file
    :param sizes: The different sizes of the matrices
    :param averages: Average time to complete the DGEMM computation for each size
    :param std: Standard deviation for each time measurement
    :param label: The function that was tested
    :return: None
    """
    # write measurment-data to file    
    df = pd.DataFrame({
        'Size': sizes,
        'Average': averages,
        'STD Deviation': std
    })
    # add file
    df.to_csv(f'data/{label}_{prefix}.csv', index=False)

def main():
    measure_main_functions()

if __name__ == "__main__":
    main()