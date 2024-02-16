import task1
import matplotlib.pyplot as plt

if __name__ == "__main__":
    x = [i * 10_000 + 10_000 for i in range(100_000) if i * 10_000 + 10_000 <= 100_000]
    y1 = [[],[],[],[]]
    y2 = [[],[],[],[]]

    for val in x:
        STREAM_ARRAY_SIZE = val
        # call cython function
        data1 = task1.run_stream_test("list", False)
        data2 = task1.run_stream_test("array", False)
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

