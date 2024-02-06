import pandas as pd
import matplotlib.pyplot as plt

# Define the labels
labels = ['numpy', 'list', 'array']
path = '1000' # CHANGE THIS in order to view the other data paths

# Initialize an empty list to store average times
average_time = []

# Loop over the labels to read the data from the corresponding CSV files
for label in labels:
    # Read the data from the CSV file
    data = pd.read_csv(f'data_n{path}/{label}_time.csv')
    
    # Append the 'Average' column to the average_time list
    average_time.append(data['Average'])

# Get the sizes from the first file (assuming all files have the same sizes)
sizes = data['Size']

# Create plots of data
print('Plotting Time Results')
plt.figure("Time Results")
for i in range(len(labels)):
    plt.plot(sizes, average_time[i], label=labels[i])  # plot the average time vs size
    plt.xticks(sizes, labels=sizes)
    plt.xlabel('Size of Matrix (N x N)')
    plt.ylabel('Average Time (s)')

plt.title("Average Time of DGEMM Computation by Matrix Size")
plt.legend()
plt.show()
