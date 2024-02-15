import copy


#cython: boundscheck=False
def gauss_seidel_numpy(f, N):

    cdef unsigned int len1, len2, i, j
    cdef float val

    newf = f.copy()

    len1 = newf.shape[0]-1
    len2 = newf.shape[1]-1
    i = 1
    j = 1

    for _ in range(1,len1):
        for _ in range(1,len2):
            val = 0.25 * (newf[i,j+1] + newf[i,j-1] +
                newf[i+1,j] + newf[i-1,j])
            newf[i,j] = val
            j += 1
        j = 1
        i += 1
    
    return newf

#cython: boundscheck=False
def gauss_seidel_array(f, N):

    cdef unsigned int len, nn, i ,j
    cdef float val
    nn = N

    newf = copy.deepcopy(f)
    len = nn-1

    i = 1
    j = 1

    for _ in range(1,len):
        for _ in range(1,len):
            val = 0.25 * (newf[i*nn+j+1]+newf[i*nn+j-1]+newf[(i+1)*nn+j]+newf[(i-1)*nn+j])
            newf[i*nn + j] = val
            j += 1
        j = 1
        i += 1
    
    return newf

#cython: boundscheck=False
def gauss_seidel_list(f, N):

    cdef unsigned int len1, len2, i, j
    cdef float val

    newf = f.copy()

    len1 = len(newf)-1
    len2 = len(newf[0])-1
    i = 1
    j = 1

    for _ in range(1,len1):
        for _ in range(1,len2):
            val = 0.25 * (newf[i][j+1] + newf[i][j-1] + newf[i+1][j] + newf[i-1][j])
            newf[i][j] = val
            j += 1
        j = 1
        i += 1
    
    return newf
