import task1
import matplotlib.pyplot as plt
import numpy as np
from old import run_stream_test

size = 1_000_000
plot_old = False

if __name__ == "__main__":
    print("Run started!")
    x = [i * 10_000 + 10_000 for i in range(size) if i * 10_000 + 10_000 <= size]
    # Cython benchmarks
    y1 = [[],[],[],[]]
    y2 = [[],[],[],[]]
    # Old benchmarks
    y3 = [[],[],[],[]]
    y4 = [[],[],[],[]]

    for val in x:
        # call cython function
        data1 = task1.run_stream_test("list", False, val)
        data2 = task1.run_stream_test("array", False, val)
        y1[0].append(data1[0])
        y1[1].append(data1[1])
        y1[2].append(data1[2])
        y1[3].append(data1[3])
        y2[0].append(data2[0])
        y2[1].append(data2[1])
        y2[2].append(data2[2])
        y2[3].append(data2[3])
        # extra: call old functions as well
        data3 = run_stream_test("l", False, val)
        data4 = run_stream_test("array", False, val)
        y3[0].append(data3[0])
        y3[1].append(data3[1])
        y3[2].append(data3[2])
        y3[3].append(data3[3])
        y4[0].append(data4[0])
        y4[1].append(data4[1])
        y4[2].append(data4[2])
        y4[3].append(data4[3])
        print("Task for ", val, " complete...")

    print("Plotting!")
    # Ugly code for adding to plots
    # Please ignore 
    fig, axs = plt.subplots(2, 2)  # a figure with a 2x2 grid of Axes
    fig.suptitle('List & Array comparison (Cython and Python)')
    # Cython
    axs[0, 0].plot(x,y1[0],label="List Cython")
    axs[0, 0].set_title('Copy')
    axs[0, 1].plot(x,y1[1],label="List Cython")
    axs[0, 1].set_title('Add')
    axs[1, 0].plot(x,y1[2],label="List Cython")
    axs[1, 0].set_title('Scale')
    axs[1, 1].plot(x,y1[3],label="List Cython")
    axs[1, 1].set_title('Triad')
    axs[0, 0].plot(x,y2[0],label="Array Cython")
    axs[0, 1].plot(x,y2[1],label="Array Cython")
    axs[1, 0].plot(x,y2[2],label="Array Cython")
    axs[1, 1].plot(x,y2[3],label="Array Cython")
    # Python
    if plot_old:
        axs[0, 0].plot(x,y3[0],label="List Python")
        axs[0, 0].set_title('Copy')
        axs[0, 1].plot(x,y3[1],label="List Python")
        axs[0, 1].set_title('Add')
        axs[1, 0].plot(x,y3[2],label="List Python")
        axs[1, 0].set_title('Scale')
        axs[1, 1].plot(x,y3[3],label="List Python")
        axs[1, 1].set_title('Triad')
        axs[0, 0].plot(x,y4[0],label="Array Python")
        axs[0, 1].plot(x,y4[1],label="Array Python")
        axs[1, 0].plot(x,y4[2],label="Array Python")
        axs[1, 1].plot(x,y4[3],label="Array Python")
    axs[0, 0].legend()
    axs[0, 1].legend()
    axs[1, 0].legend()
    axs[1, 1].legend()

    # Set common labels

    fig.text(0.5, 0.04, 'N', ha='center', va='center')
    fig.text(0.06, 0.5, 'GB/s', ha='center', va='center', rotation='vertical')

    plt.show()

