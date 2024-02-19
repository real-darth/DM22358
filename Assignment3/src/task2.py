from array import array
import numpy as np
import random
import array
import copy
from functools import wraps
from timeit import default_timer as timer
import matplotlib.pyplot as plt
import task2C
#import task2CFew
import task2Mid


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


@profile
def gauss_seidel_numpy(f, N):
    newf = f.copy()

    for i in range(1,newf.shape[0]-1):
        for j in range(1,newf.shape[1]-1):
            newf[i,j] = 0.25 * (newf[i,j+1] + newf[i,j-1] +
                newf[i+1,j] + newf[i-1,j])
    
    return newf

@profile
def gauss_seidel_array(f, N):
    newf = copy.deepcopy(f)

    for i in range(1,N-1):
        for j in range(1,N-1):
            newf[i*N + j] = 0.25 * (newf[i*N + j+1] + newf[i*N + j-1] +
                newf[(i+1)*N+j] + newf[(i-1)*N + j])
    
    return newf

@profile
def gauss_seidel_list(f, N):
    newf = f.copy()
    for i in range(1,len(newf)-1):
        for j in range(1,len(newf[0])-1):
            newf[i][j] = 0.25 * (newf[i][j+1] + newf[i][j-1] +
                newf[i+1][j] + newf[i-1][j])
    
    return newf



@timefn
def runGauss(f, fn, N):
    for _ in range(1000):    
        f = fn(f, N)
    return f



def main():
    times = [[],[],[],[],[],[],[]]
    y = [10,50,100,500, 1000, 5000, 10_000]
    for N in y:
        print(N)
        pyList = [[random.random()] * N for _ in range(N)]
        pyList2 = pyList.copy()
        pyArray = array.array('f', [random.random()] * N * N)
        pyArray2 = copy.deepcopy(pyArray)
        numpyArray = np.random.rand(N,N)
        numpyArray2 = numpyArray.copy()
        _, listTime = runGauss(pyList, gauss_seidel_list, N)
        _, arrayTime = runGauss(pyArray, gauss_seidel_array,N)
        _, numpyTime = runGauss(numpyArray, gauss_seidel_numpy, N)
        _, listTime2 = runGauss(pyList2, task2Mid.gauss_seidel_list, N)
        _, arrayTime2 = runGauss(pyArray2, task2Mid.gauss_seidel_array,N)
        _, numpyTime2 = runGauss(numpyArray2, task2Mid.gauss_seidel_numpy, N)
        times[0].append(listTime)
        times[1].append(arrayTime)
        times[2].append(numpyTime)
        times[3].append(listTime2)
        times[4].append(arrayTime2)
        times[5].append(numpyTime2)
    return times, y



if __name__ == "__main__":
    times, y = main()
    plt.loglog(y,times[0],label="List (various)")
    plt.loglog(y,times[3],label="List (using cdef)")
    plt.loglog(y,times[1],label="Array (various)")
    plt.loglog(y,times[4],label="Array (using cdef)")
    plt.loglog(y,times[2],label="Numpy (various)")
    plt.loglog(y,times[5],label="Numpy (using cdef)")
    plt.legend()
    plt.show()