from array import array
import numpy as np
import random
import array
import copy
from functools import wraps
from timeit import default_timer as timer
import matplotlib.pyplot as plt

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


def gauss_seidel_numpy(f):
    newf = f.copy()

    for i in range(1,newf.shape[0]-1):
        for j in range(1,newf.shape[1]-1):
            newf[i,j] = 0.25 * (newf[i,j+1] + newf[i,j-1] +
                newf[i+1,j] + newf[i-1,j])
    
    return newf

def gauss_seidel_array(f, N):
    newf = copy.deepcopy(f)

    for i in range(1,N-1):
        for j in range(1,N-1):
            newf[i*N + j] = 0.25 * (newf[i*N + j+1] + newf[i*N + j-1] +
                newf[(i+1)*N+j] + newf[(i-1)*N + j])
    
    return newf


def gauss_seidel_list(f):
    newf = f.copy()
    for i in range(1,len(newf)-1):
        for j in range(1,len(newf[0])-1):
            newf[i][j] = 0.25 * (newf[i][j+1] + newf[i][j-1] +
                newf[i+1][j] + newf[i-1][j])
    
    return newf

@timefn
def runGauss_numpy(f):
    for _ in range(100):    
        f = gauss_seidel_numpy(f)

@timefn
def runGauss_list(f):
    for _ in range(100):    
        f = gauss_seidel_list(f)

@timefn
def runGauss_array(f, N):
    for _ in range(100):    
        f = gauss_seidel_array(f, N)



def main():
    times = [[],[],[]]
    y = [10*i for i in range(10)]
    for N in y:
        pyList = [[random.random()] * N for _ in range(N)]
        pyArray = array.array('d', [random.random()] * N * N)
        numpyArray = np.random.rand(N, N)
        _, listTime = runGauss_list(pyList)
        _, arrayTime = runGauss_array(pyArray, N)
        _, numpyTime = runGauss_numpy(numpyArray)
        times[0].append(listTime)
        times[1].append(arrayTime)
        times[2].append(numpyTime)

    return times, y



if __name__ == "__main__":
    times, y = main()
    plt.plot(y,times[0],label="List")
    plt.plot(y,times[1],label="Array")
    plt.plot(y,times[2],label="Numpy")
    plt.legend()
    plt.show()