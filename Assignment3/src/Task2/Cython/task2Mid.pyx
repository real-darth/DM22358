import numpy as np
import array
import copy

def gauss_seidel_numpy(f, N):
    newf = f.copy()

    cdef unsigned int len1, len2
    cdef float val

    len1 = newf.shape[0]-1
    len2 = newf.shape[1]-1

    for i in range(1,len1):
        for j in range(1,len2):
            val = 0.25 * (newf[i,j+1] + newf[i,j-1] +
                newf[i+1,j] + newf[i-1,j])
            newf[i,j] = val
    
    return newf

def gauss_seidel_array(f, N):

    cdef unsigned int len, nn
    cdef float val
    nn = N

    newf = copy.deepcopy(f)
    len = nn-1

    for i in range(1,len):
        for j in range(1,len):
            val = 0.25 * (newf[i*nn+j+1]+newf[i*nn+j-1]+newf[(i+1)*nn+j]+newf[(i-1)*nn+j])
            newf[i*nn + j] = val
    
    return newf

def gauss_seidel_list(f, N):
    cdef unsigned int len1, len2
    cdef float val, temp

    newf = f.copy()

    len1 = len(newf)-1
    len2 = len(newf[0])-1

    for i in range(1,len1):
        for j in range(1,len2):
            temp = (newf[i][j+1] + newf[i][j-1] + newf[i+1][j] + newf[i-1][j])
            val = 0.25*temp
            newf[i][j] = val

    return newf