import threading
import time
import matplotlib.pyplot as plt
import os
import numpy as np
from conway import OFF, ON


def init_grd(N):
    sequence = [0, 0, 1] * (N // 3) + [0, 0, 1][: N % 3]
    # create matrix of size N*N with the sequence
    grid = np.array([sequence] * N)
    # convert

    return grid


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
    grid[:] = newGrid[:]


def update_opt(grid, N):
    # Counting the number of neighbours.
    neighbourCount = np.zeros(grid.shape)
    neighbourCount[1:-1, 1:-1] += (
        grid[:-2, :-2]
        + grid[:-2, 1:-1]
        + grid[:-2, 2:]
        + grid[1:-1, :-2]
        + grid[1:-1, 2:]
        + grid[2:, :-2]
        + grid[2:, 1:-1]
        + grid[2:, 2:]
    ) / 255  # Dividing by 255 to get the number of neighbours, because ON = 255 and OFF = 0.

    # Apply rules.
    birth = (neighbourCount == 3)[1:-1, 1:-1] & (grid[1:-1, 1:-1] == OFF)
    survive = ((neighbourCount == 2) | (neighbourCount == 3))[1:-1, 1:-1] & (grid[1:-1, 1:-1] == ON)

    grid[...] = OFF
    grid[1:-1, 1:-1][birth | survive] = ON


def experiment(N, update_funct):
    grid = np.array([])
    grid = init_grd(N)

    # iter until convergence, if it does not converge check the last 10 grids
    while True:
        last_grid = grid.copy()
        update_funct(grid, N)
        if np.array_equal(grid, last_grid):
            break


def main():
    times = []
    times_opt = []
    print("Running the experiment...")
    sizes = range(100, 1001, 100)
    for upd_func in [update, update_opt]:
        print("Running experiment for ", upd_func.__name__)
        for i in sizes:
            # execute the conway.py  with flag --grid-size i
            for j in range(5):
                print("Running experiment ", j, " for grid size ", i)
                values = []
                thread = threading.Thread(target=experiment, args=(i, upd_func))
                start = time.time()
                experiment(i, upd_func)
                end = time.time()
                time_taken = end - start
                values.append(time_taken)
            if upd_func == update:
                times.append(np.mean(values))
            else:
                times_opt.append(np.mean(values))
            print("Time taken: ", time_taken)

    print("Plotting the results...")

    plt.plot(list(sizes), times)
    plt.plot(list(sizes), times_opt)
    plt.xlabel("Grid Size")
    plt.ylabel("Time")
    plt.title("Time vs Grid Size")
    plt.legend(["Unoptimized", "Optimized"])
    # save data to file from times and times_opt
    if not os.path.exists("data"):
        os.makedirs("data")
    # save the grid size and its time, with formta grid_size, time
    with open("data/times.dat", "w") as f:
        for i in range(len(sizes)):
            f.write(str(sizes[i]) + "," + str(times[i]) + "\n")
    with open("data/times_opt.dat", "w") as f:
        for i in range(len(sizes)):
            f.write(str(sizes[i]) + "," + str(times_opt[i]) + "\n")

    plt.show()


# call main
if __name__ == "__main__":
    main()
