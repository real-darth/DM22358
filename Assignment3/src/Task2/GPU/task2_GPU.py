import matplotlib.pyplot as plt
from array import array
import numpy as np
import random
import array
import copy
from functools import wraps
from timeit import default_timer as timer
import matplotlib.pyplot as plt
import test
import torch
"cuda" if torch.cuda.is_available() else "cpu"
import cupy as cp

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


ITERS = 10

def gauss_seidel_torch(f: torch.Tensor):
    """
    Applies the Gauss-Seidel method to solve a system of linear equations represented by the input tensor.

    Parameters:
    f (torch.Tensor): The input tensor representing the system of linear equations.

    Returns:
    torch.Tensor: The updated tensor after applying the Gauss-Seidel method.
    """
    newf = f.clone().detach()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    newf = newf.to(device)
    newf[[-1,0],:] = 0
    newf[:,[-1,0]] = 0


    newf[1:-1, 1:-1] = 0.25 * (
            torch.roll(newf, 1, dims=0)[1:-1, 1:-1]
            + torch.roll(newf, -1, dims=0)[1:-1, 1:-1]
            + torch.roll(newf, 1, dims=1)[1:-1, 1:-1]
            + torch.roll(newf, -1, dims=1)[1:-1, 1:-1]
        )

    return newf


def gauss_seidel_cupy(f: cp.ndarray):
    """
    Applies the Gauss-Seidel method to solve a 2D array using the Cupy library.

    Args:
        f (cp.ndarray): The input 2D array.

    Returns:
        cp.ndarray: The updated 2D array after applying the Gauss-Seidel method.
    """
    newf = cp.array(f)
    newf[[-1,0],:] = 0
    newf[:,[-1,0]] = 0


    newf[1:-1, 1:-1] = 0.25 * (
            cp.roll(newf, 1, axis=0)[1:-1, 1:-1]
            + cp.roll(newf, -1, axis=0)[1:-1, 1:-1]
            + cp.roll(newf, 1, axis=1)[1:-1, 1:-1]
            + cp.roll(newf, -1, axis=1)[1:-1, 1:-1]
        )


    return newf


@timefn
def runGauss_torch(f):
  for i in range(ITERS):
        f = test.gauss_seidel_torch(f)
@timefn
def runGauss_cupy(f):
    for i in range(ITERS):
        f = test.gauss_seidel_cupy(f)

@timefn
def runGauss_torch2(f):
  for i in range(ITERS):
        f = gauss_seidel_torch(f)
@timefn
def runGauss_cupy2(f):
    for i in range(ITERS):
        f = gauss_seidel_cupy(f)



def main():
    times = [[],[],[],[]]
    with open("torch.dat", "w") as file:
      pass
    with open("cupy.dat", "w") as file:
      pass
    y = [10, 50, 100, 500, 1000, 5000]
    for N in y:
        print(N)
        torchTensor = torch.rand(N, N)
        cudaArray =  cp.random.rand(N, N)
        torchTensor2 = torch.rand(N, N)
        cudaArray2 =  cp.random.rand(N, N)
        _, torch_time = runGauss_torch(torchTensor)
        _, cupy_time = runGauss_cupy(cudaArray)
        _, torch_time2 = runGauss_torch2(torchTensor2)
        _, cupy_time2 = runGauss_cupy2(cudaArray2)
        times[0].append(torch_time)
        times[1].append(cupy_time)
        times[2].append(torch_time2)
        times[3].append(cupy_time2)
        with open("torch.dat", "a") as file:
          file.write(f"{N}, {torch_time}\n")
        with open("cupy.dat", "a") as file:
          pass
          file.write(f"{N}, {cupy_time}\n")

    return times, y




times, y = main()
plt.loglog(y,times[0],label="PyTorch")
plt.loglog(y,times[1], label="CuPy")
plt.loglog(y,times[2],label="PyTorch (without cython)")
plt.loglog(y,times[3], label="CuPy (without cython)")
plt.xlabel("Grid Size")
plt.ylabel("Execution Time (s)")
plt.title("Execution Time of Gauss-Seidel Method")
plt.legend()
plt.show()