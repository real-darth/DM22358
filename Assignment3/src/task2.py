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
    for _ in range(100):    
        f = fn(f, N)
    return f



def main():
    times = [[],[],[]]
    y = [1000*i for i in range(1,2)]
    for N in y:
        num = random.random()
        pyList = [[num] * N for _ in range(N)]
        pyArray = array.array('f', [num] * N * N)
        numpyArray = num * np.ones((N, N))
        f1, listTime = runGauss(pyList, gauss_seidel_list, N)
        f2, arrayTime = runGauss(pyArray, gauss_seidel_array,N)
        f3, numpyTime = runGauss(numpyArray, gauss_seidel_numpy, N)
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