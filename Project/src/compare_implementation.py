import sys
import matplotlib.pyplot as plt
import numpy as np
from functools import wraps
import torch
from simulate import calculate_mean_theta, calculate_mean_theta_vect, calculate_mean_theta_torch, calcualte_mean_theta_cython, calculate_mean_theta_conc, calculate_mean_theta_cupy

##main

R = 1
# do a performance comparison

print("Running comparision, this might take a while...")

sizes = range(2_000, 15_000, 1000) #[500, 1000, 2000, 5000, 10_000, 12_000, 15_000, 17_000]
Nt = 500
avgs = [[], [],[], [], [], []]
stds = [[], [],[], [], [], []]
for N in sizes:  # [500, 1000, 1500, 2000]:
    #if N % 10_000 == 0:
    # print(f"Reached N = {N}")
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
    _, avg, std = calcualte_mean_theta_cython(x, y, theta, R)
    avgs[3].append(avg)
    stds[3].append(std)
    _, avg, std = calculate_mean_theta_conc(x, y, theta, R)
    avgs[4].append(avg)
    stds[4].append(std)
    _, avg, std = calculate_mean_theta_cupy(x, y, theta, R)
    avgs[5].append(avg)
    stds[5].append(std)

# plot
plt.errorbar(sizes, avgs[0], yerr=stds[0], label="standard")
plt.errorbar(sizes, avgs[1], yerr=stds[1], label="vectorized")
plt.errorbar(sizes, avgs[2], yerr=stds[2], label="torch")
plt.errorbar(sizes, avgs[3], yerr=stds[3], label="cython")
plt.errorbar(sizes, avgs[4], yerr=stds[4], label="concurrent")
plt.errorbar(sizes, avgs[5], yerr=stds[5], label="cupy")
plt.xlabel("Number of birds")
plt.legend()
plt.ylabel("Average time to simulate (s)")
plt.show()