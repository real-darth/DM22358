from timeit import default_timer as timer
import sys

STREAM_ARRAY_SIZE = 10_000

def run_stream_test():
    a = [1.0]*STREAM_ARRAY_SIZE
    b = [2.0]*STREAM_ARRAY_SIZE
    c = [0.0]*STREAM_ARRAY_SIZE

    scalar = 2.0
    times = [0.0]*4
    #copy
    times[0] = timer()
    for j in range(STREAM_ARRAY_SIZE):
        c[j] = a[j]
    times[0] = timer() - times[0]

    # scale
    times[1] = timer()
    for j in range(STREAM_ARRAY_SIZE):
        b[j] = scalar*c[j]
    times[1] = timer() - times[1]
     
     #sum
    times[2] = timer()
    for j in range(STREAM_ARRAY_SIZE):
        c[j] = a[j]+b[j]
    times[2] = timer() - times[2]

    # triad
    times[3] = timer()
    for j in range(STREAM_ARRAY_SIZE):
        a[j] = b[j]+scalar*c[j]
    times[3] = timer() - times[3]

    copy = 2 * sys.getsizeof(float) * STREAM_ARRAY_SIZE
    add = 2 * sys.getsizeof(float) * STREAM_ARRAY_SIZE
    scale = 3 * sys.getsizeof([]) * STREAM_ARRAY_SIZE
    triad = 3 * sys.getsizeof([]) * STREAM_ARRAY_SIZE
    print("Copy size:", copy)
    print("Add size:",add)
    print("Scale size:",scale)
    print("Triad size:",triad)

    print("Copy size:",copy/times[0])
    print("Copy size:",add/times[1])
    print("Copy size:",scale/times[2])
    print("Copy size:",triad/times[3])

if __name__ == "__main__":
    run_stream_test()