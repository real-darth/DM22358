from array import array
import numpy as np
import random
import array
import copy
from functools import wraps
from timeit import default_timer as timer
import matplotlib.pyplot as plt
import task2C
import torch


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


def gauss_seidel_numpy(f, N):
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

def gauss_seidel_list(f, N):
    newf = f.copy()
    for i in range(1,len(newf)-1):
        for j in range(1,len(newf[0])-1):
            newf[i][j] = 0.25 * (newf[i][j+1] + newf[i][j-1] +
                newf[i+1][j] + newf[i-1][j])
    
    return newf

def gauss_seidel_torch(f: torch.Tensor):
    """
    Applies the Gauss-Seidel method to solve a system of linear equations represented by the input tensor.

    Parameters:
    f (torch.Tensor): The input tensor representing the system of linear equations.

    Returns:
    torch.Tensor: The updated tensor after applying the Gauss-Seidel method.
    """
    newf = f.clone()

    for _ in range(1, newf.shape[0] - 1):
        newf[1:-1, 1:-1] = 0.25 * (
            torch.roll(newf, 1, dims=0)[1:-1, 1:-1]
            + torch.roll(newf, -1, dims=0)[1:-1, 1:-1]
            + torch.roll(newf, 1, dims=1)[1:-1, 1:-1]
            + torch.roll(newf, -1, dims=1)[1:-1, 1:-1]
        )

    return newf

@timefn
def runGauss(f, fn, N):
    for _ in range(10):    
        f = fn(f, N)
    return f



def main():
    times = [[],[],[],[],[],[],[]]
    y = [10,50,100,200,300, 500]
    for N in y:
        print(N)
        pyList = [[random.random()] * N for _ in range(N)]
        pyList2 = pyList.copy()
        pyArray = array.array('f', [random.random()] * N * N)
        pyArray2 = copy.deepcopy(pyArray)
        numpyArray = np.random.rand(N,N)
        numpyArray2 = numpyArray.copy()
        f1, listTime = runGauss(pyList, task2C.gauss_seidel_list, N)
        f2, arrayTime = runGauss(pyArray, task2C.gauss_seidel_array,N)
        f3, numpyTime = runGauss(numpyArray, task2C.gauss_seidel_numpy, N)
        f1, listTime2 = runGauss(pyList2, gauss_seidel_list, N)
        f2, arrayTime2 = runGauss(pyArray2, gauss_seidel_array,N)
        f3, numpyTime2 = runGauss(numpyArray2, gauss_seidel_numpy, N)
        times[0].append(listTime)
        times[1].append(arrayTime)
        times[2].append(numpyTime)
        times[3].append(listTime2)
        times[4].append(arrayTime2)
        times[5].append(numpyTime2)
    return times, y



if __name__ == "__main__":
    times, y = main()
    plt.plot(y,times[0],label="List C")
    plt.plot(y,times[1],label="Array C")
    plt.plot(y,times[2],label="Numpy C")
    plt.plot(y,times[3],label="List")
    plt.plot(y,times[4],label="Array")
    plt.plot(y,times[5],label="Numpy")
    plt.legend()
    plt.show()