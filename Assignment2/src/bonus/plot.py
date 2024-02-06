import matplotlib.pyplot as plt

# Data provided in the output
sizes = []
times = []
with open("data/times.dat", "r") as f:
    for line in f:
        sizes.append(int(line.split(",")[0]))
        times.append(float(line.split(",")[1]))

times_opt = []
with open("data/times_opt.dat", "r") as f:
    for line in f:
        times_opt.append(float(line.split(",")[1]))

# Plot the data
print(sizes)
print(times)
print(times_opt)
plt.plot(sizes, times)
plt.plot(sizes, times_opt)
plt.legend(["Unoptimized", "Optimized"])
plt.title("Time vs Grid Size")
plt.xlabel("Grid Size")
plt.ylabel("Time (seconds)")
plt.grid(True)
plt.show()
# save the plot
plt.savefig("data/plot.png")
