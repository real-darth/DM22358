from timeit import default_timer as timer
import sys
from array import array
import matplotlib.pyplot as plt
import numpy as np

STREAM_ARRAY_SIZE = 10_000_000

scalar = 2.0

def get_copy_size():
    return (2 * np.nbytes[float] * STREAM_ARRAY_SIZE)

def get_add_size():
    return (2 * np.nbytes[float] * STREAM_ARRAY_SIZE)

def get_scale_size():
    return (3 * np.nbytes[float] * STREAM_ARRAY_SIZE)

def get_triad_size():
    return (3 * np.nbytes[float] * STREAM_ARRAY_SIZE)



def run_stream_test(type,debug):

    # List 
    if type=="l":
        a = [1.0]*STREAM_ARRAY_SIZE
        b = [2.0]*STREAM_ARRAY_SIZE
        c = [0.0]*STREAM_ARRAY_SIZE
    # Array
    else:
        a = array('f', [1.0] * STREAM_ARRAY_SIZE)
        b = array('f', [2.0] * STREAM_ARRAY_SIZE)
        c = array('f', [0.0] * STREAM_ARRAY_SIZE)

    # This should not actually do anything
    for j in range(STREAM_ARRAY_SIZE):
        a[j] = 1.0
        b[j] = 2.0
        c[j] = 0.0

    times = [0.0]*4

    ## Calculate time to do operations:

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

    # Get the amount of data moved
    copy = get_copy_size()
    add = get_add_size()
    scale = get_scale_size()
    triad = get_triad_size()


    # Calculate bandwidth
    copyStream = 1.0e-09 * (copy/times[0])
    addStream = 1.0e-09 * (add/times[1])
    scaleStream = 1.0e-09 * (scale/times[2])
    triadStream = 1.0e-09 * (triad/times[3])

    total = copyStream + addStream + scaleStream + triadStream

    if debug:
        print("Copy GB/s:",copyStream)
        print("Add GB/s:",addStream)
        print("Scale GB/s:",scaleStream)
        print("Triad GB/s:",triadStream)
        
    # Return
    return [copyStream,addStream,scaleStream,triadStream]


if __name__ == "__main__":

    x = [i * 10_000 + 10_000 for i in range(10_000) if i * 10_000 + 10_000 <= 10_000_000]
    y1 = [[],[],[],[]]
    y2 = [[],[],[],[]]


    for val in x:
        STREAM_ARRAY_SIZE = val
        data1 = run_stream_test("l", False)
        data2 = run_stream_test("array", False)
        y1[0].append(data1[0])
        y1[1].append(data1[1])
        y1[2].append(data1[2])
        y1[3].append(data1[3])
        y2[0].append(data2[0])
        y2[1].append(data2[1])
        y2[2].append(data2[2])
        y2[3].append(data2[3])

    # Ugly code for adding to plots
    # Please ignore 


    fig, axs = plt.subplots(2, 2)  # a figure with a 2x2 grid of Axes
    fig.suptitle('List & Array comparison')
    axs[0, 0].plot(x,y1[0],label="List")
    axs[0, 0].set_title('Copy')
    axs[0, 1].plot(x,y1[1],label="List")
    axs[0, 1].set_title('Add')
    axs[1, 0].plot(x,y1[2],label="List")
    axs[1, 0].set_title('Scale')
    axs[1, 1].plot(x,y1[3],label="List")
    axs[1, 1].set_title('Triad')
    axs[0, 0].plot(x,y2[0],label="Array")
    axs[0, 1].plot(x,y2[1],label="Array")
    axs[1, 0].plot(x,y2[2],label="Array")
    axs[1, 1].plot(x,y2[3],label="Array")
    axs[0, 0].legend()
    axs[0, 1].legend()
    axs[1, 0].legend()
    axs[1, 1].legend()

    # Set common labels

    fig.text(0.5, 0.04, 'N', ha='center', va='center')
    fig.text(0.06, 0.5, 'GB/s', ha='center', va='center', rotation='vertical')

    plt.show()