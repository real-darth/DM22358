import pytest
import array
import numpy as np
import DGEMM

def test_dgemm_numpy_array():
    size = 3
    A = np.array([[1,2,3], [3,2,1], [1,2,3]])
    B = np.array([[4,5,6], [6,5,4], [4,6,5]])

    C_expected = np.array([[28,33,29], [28,31,31], [28,33,29]])
    C_result, time = DGEMM.dgemm_numpy_array(A, B, size)

    assert len(C_expected) == len(C_result)
    assert np.all(C_result == C_expected)



def test_dgemm_python_list():
    size = 4
    A = [[1] * 4, [2] * 4, [3] * 4, [4] * 4]
    B = [[1,2,3,4] for _ in range(4)]

    C_expected = [[4,8,12,16], [8,16,24,32], [12,24,36,48], [16,32,48,64]]
    C_result, time = DGEMM.dgemm_python_list(A, B, size)

    assert len(C_expected) == len(C_result)
    assert np.all(C_result == C_expected)



def test_dgemm_python_array():
    size = 2
    A = array.array('d', [1, -1, 2, 2])
    B = array.array('d', [-2, 0, 0.5, -2])

    C_expected = array.array('d', [-2.5, 2, -3, -4])
    C_result, time = DGEMM.dgemm_python_array(A, B, size)

    assert len(C_expected) == len(C_result)
    assert np.all(C_result == C_expected)



def test_dgemm_blas():
    size = 6
    A = np.array([[7,2,7,6,7,6], 
                  [0,2,5,8,0,7], 
                  [0,0,4,3,4,0], 
                  [0,0,0,8,5,8], 
                  [0,0,0,0,5,0], 
                  [0,0,0,0,0,1]])

    B = np.array([[2,3,2,3,0,3], 
                  [3,3,0,0,3,0], 
                  [2,0,0,0,3,3], 
                  [3,0,0,1,0,2], 
                  [0,3,3,0,1,2], 
                  [3,0,3,2,2,0]])

    C_expected = np.array([[70,48,53,39,46,68], 
                           [61,6,21,22,35,31], 
                           [17,12,12,3,16,26], 
                           [48,15,39,24,21,26], 
                           [0,15,15,0,5,10], 
                           [3,0,3,2,2,0]])
    C_result, time = DGEMM.dgemm_blas(A, B, size)

    assert len(C_expected) == len(C_result)
    assert np.all(C_result == C_expected)