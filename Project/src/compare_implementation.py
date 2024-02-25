import sys
import matplotlib.pyplot as plt
import numpy as np
from functools import wraps
import torch
from simulate import calculate_mean_theta, calculate_mean_theta_vect, calculate_mean_theta_torch


##main


R = 1
# do a performance comparison


sizes = range(500, 8000, 500)
Nt = 200
avgs = [[], [],[]]
stds = [[], [],[]]
for N in sizes:  # [500, 1000, 1500, 2000]:
    theta = np.random.rand(N)
    x = np.random.rand(N)
    y = np.random.rand(N)
    _, avg, std = calculate_mean_theta(x, y, theta, R)
    avgs[0].append(avg)
    stds[0].append(std)
    _, avg, std = calculate_mean_theta_vect(x, y, theta, R)
    avgs[1].append(avg)
    stds[1].append(std)
    _, avg, std = calculate_mean_theta_torch(x, y, theta, R)
    avgs[2].append(avg)
    stds[2].append(std)
# plot
plt.errorbar(sizes, avgs[0], yerr=stds[0], label="standard")
plt.errorbar(sizes, avgs[1], yerr=stds[1], label="vectorized")
plt.errorbar(sizes, avgs[2], yerr=stds[2], label="torch")
plt.xlabel("Number of birds")
plt.legend()
plt.ylabel("Average time to simulate (s)")
plt.show()