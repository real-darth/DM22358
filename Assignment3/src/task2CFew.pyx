import numpy as np
import array
import copy

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