import threading
import time
import matplotlib.pyplot as plt
import os
import numpy as np
from conway import randomGrid, OFF, ON


def update(grid, N):
    # copy grid since we require 8 neighbors for calculation
    # and we go line by line
    newGrid = grid.copy()
    for i in range(N):
        for j in range(N):
            # compute 8-neghbor sum
            # using toroidal boundary conditions - x and y wrap around
            # so that the simulaton takes place on a toroidal surface.
            total = int(
                (
                    grid[i, (j - 1) % N]
                    + grid[i, (j + 1) % N]
                    + grid[(i - 1) % N, j]
                    + grid[(i + 1) % N, j]
                    + grid[(i - 1) % N, (j - 1) % N]
                    + grid[(i - 1) % N, (j + 1) % N]
                    + grid[(i + 1) % N, (j - 1) % N]
                    + grid[(i + 1) % N, (j + 1) % N]
                )
                / 255
            )
            # apply Conway's rules
            if grid[i, j] == ON:
                if (total < 2) or (total > 3):
                    newGrid[i, j] = OFF
            else:
                if total == 3:
                    newGrid[i, j] = ON
    # update data

    return newGrid


def experiment(N):
    grid = np.array([])
    grid = randomGrid(N)

    # iter until convergence, if it does not converge check the last 10 grids
    while True:
        newGrid = update(grid, N)
        if np.array_equal(grid, newGrid):
            break
        grid = newGrid


def main():
    times = []
    print("Running the experiment...")
    sizes = range(10, 101, 10)
    for i in sizes:
        # execute the conway.py  with flag --grid-size i
        for j in range(5):
            print("Running experiment ", j, " for grid size ", i)
            values = []
            time_taken = float("inf")
            while not time_taken < 15:
                print("Grid size: ", i)
                thread = threading.Thread(target=experiment, args=(i,))
                start = time.time()
                thread.start()
                thread.join(15)
                end = time.time()
                time_taken = end - start
            values.append(time_taken)
        times.append(np.mean(values))
        print("Time taken: ", time_taken)

    plt.plot(list(sizes), times)

    plt.xlabel("Grid Size")
    plt.ylabel("Time")
    plt.title("Time vs Grid Size")
    plt.show()


# call main
if __name__ == "__main__":
    main()
