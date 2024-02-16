# TO BUILD run: python setup.py build_ext --inplace

from timeit import default_timer as timer
from array import array
import numpy as np
cimport numpy as np

cdef int STREAM_ARRAY_SIZE = 1_000_000

cdef float scalar = 2.0

cdef int get_copy_size():
    return (2 * np.nbytes[np.float64] * STREAM_ARRAY_SIZE)

cdef int get_add_size():
    return (2 * np.nbytes[np.float64] * STREAM_ARRAY_SIZE)

cdef int get_scale_size():
    return (3 * np.nbytes[np.float64] * STREAM_ARRAY_SIZE)

cdef int get_triad_size():
    return (3 * np.nbytes[np.float64] * STREAM_ARRAY_SIZE)

def run_stream_test(type, debug):
    cdef list times = [0.0] * 4
    cdef int copy, add, scale, triad
    cdef float copyStream, addStream, scaleStream, triadStream
    # cdef list a_list, b_list, c_list

    # List
    if type == "list":
        a_list = [1.0] * STREAM_ARRAY_SIZE
        b_list = [2.0] * STREAM_ARRAY_SIZE
        c_list = [0.0] * STREAM_ARRAY_SIZE

        times[0] = timer()
        c_list[:] = a_list[:]
        times[0] = timer() - times[0]

        times[1] = timer()
        b_list = [scalar * x for x in c_list]
        times[1] = timer() - times[1]
        
        times[2] = timer()
        c_list = [x + y for x, y in zip(a_list, b_list)]
        times[2] = timer() - times[2]

        times[3] = timer()
        a_list = [x + scalar * y for x, y in zip(b_list, c_list)]
        times[3] = timer() - times[3]
    # Array
    else:
        # cannot define python arrays as cdef varaibles
        a_array = array('f', [1.0] * STREAM_ARRAY_SIZE)
        b_array = array('f', [2.0] * STREAM_ARRAY_SIZE)
        c_array = array('f', [0.0] * STREAM_ARRAY_SIZE)

        times[0] = timer()
        c_array[:] = a_array[:]
        times[0] = timer() - times[0]

        times[1] = timer()
        b_array = array('d', [scalar * x for x in c_array])
        times[1] = timer() - times[1]
        
        times[2] = timer()
        c_array = array('d', [x + y for x, y in zip(a_array, b_array)])
        times[2] = timer() - times[2]

        times[3] = timer()
        a_array = array('d', [x + scalar * y for x, y in zip(b_array, c_array)])
        times[3] = timer() - times[3]

    copy = get_copy_size()
    add = get_add_size()
    scale = get_scale_size()
    triad = get_triad_size()

    copyStream = 1.0e-09 * (copy/times[0])
    addStream = 1.0e-09 * (add/times[1])
    scaleStream = 1.0e-09 * (scale/times[2])
    triadStream = 1.0e-09 * (triad/times[3])

    if debug:
        print("Copy GB/s:", copyStream)
        print("Add GB/s:", addStream)
        print("Scale GB/s:", scaleStream)
        print("Triad GB/s:", triadStream)
        
    return [copyStream, addStream, scaleStream, triadStream]
