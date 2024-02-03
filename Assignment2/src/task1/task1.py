from timeit import default_timer as timer
import sys
from array import array
import matplotlib.pyplot as plt

STREAM_ARRAY_SIZE = 10_000

scalar = 2.0

def get_copy_size(size):
    return 2 * sys.getsizeof(float) * size
def get_add_size(size):
    return 2 * sys.getsizeof(float) * size
def get_scale_size(size):
    return 3 * sys.getsizeof(float) * size
def get_triad_size(size):
    return 3 * sys.getsizeof(float) * size

def time_copy(a, c, size):
    time = timer()
    for j in range(size):
        c[j] = a[j]
    return timer() - time

def time_scale(b, c, size):
    time = timer()
    for j in range(size):
        b[j] = scalar*c[j]
    return timer() - time

def time_sum(a, b, c, size):
    time = timer()
    for j in range(size):
        c[j] = a[j]+b[j]
    return timer() - time

def time_triad(a, b, c, size):
    time = timer()
    for j in range(size):
        a[j] = b[j]+scalar*c[j]
    return timer() - time


def run_stream_test(type, size,debug):
    if type=="l":
        a = [1.0]*size
        b = [2.0]*size
        c = [0.0]*size
    else:
        a = array('f', [1.0] * size)
        b = array('f', [2.0] * size)
        c = array('f', [0.0] * size)

    times = [0.0]*4

    #copy
    times[0] = time_copy(a, c, size)

    # scale
    times[1] = time_scale(b, c, size)
     
     #sum
    times[2] = time_sum(a, b, c, size)

    # triad
    times[3] = time_triad(a, b, c, size)

    #print("Copy size:", copy)
    #print("Add size:",add)
    #print("Scale size:",scale)
    #print("Triad size:",triad)

    copyStream = (get_copy_size(size)/times[0])/1e9
    addStream = (get_add_size(size)/times[1])/1e9
    scaleStream = (get_scale_size(size)/times[2])/1e9
    triadStream = (get_triad_size(size)/times[3])/1e9

    total = copyStream + addStream + scaleStream + triadStream
    if debug:
        print("Copy GB/s:",copyStream)
        print("Add GB/s:",addStream)
        print("Scale GB/s:",scaleStream)
        print("Triad GB/s:",triadStream)

    return total


if __name__ == "__main__":
    x = [i * 10 + 100 for i in range(100000) if i * 10 + 100 <= 100_000]
    y1 = []
    y2 = []
    for val in x:
        y1.append(run_stream_test("l",val, False))
        y2.append(run_stream_test("array",val, False))
    plt.plot(x,y1)
    plt.plot(x,y2)
    plt.show()