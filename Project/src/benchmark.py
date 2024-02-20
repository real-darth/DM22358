import subprocess
import sys


# location of all the benchmarking scripts
directory = "benchmarks\\"

DEFAULT_N_PARAMETER = 500
DEFAULT_NT_PARAMETER = 200

# global variables for simulation parameters
param_N = DEFAULT_N_PARAMETER       # number of birds
param_Nt = DEFAULT_NT_PARAMETER     # number of time steps

def set_parameters():
    """Set the simulation parameters by input from user."""
    # set the parameters based on user input or default values
    print("Set simulation parameters. Leave blank if using default values.")
    param_N = input("Enter the simulation parameter for [number of birds] [INTEGER]: ")
    if param_N == None or param_N == "":
        param_N = DEFAULT_N_PARAMETER
    
    param_Nt = input("Enter the simulation parameter for [simulation time] [INTEGER]: ")
    if param_Nt == None or param_Nt == "":
        param_Nt = DEFAULT_NT_PARAMETER

def get_parameters() -> tuple:
    """Function to get the simulation parameters specified by the user.

    Returns:
        (tuple) Returns the parameters used by the simulation in this order:
            1. Number of birds
            2. Simulation length
    """
    # return the parameters
    return (param_N, param_Nt)

def run_benchmark():
    print("----------------- BENCHMARK TOOL -----------------")
    # set simulation parameters at the start of the tool
    set_parameters()
    print("Simulation Parameters assigned")

    while True:
        print("\n" "---------------------------------------------------")
        print("Select a benchmark to run:")
        print("1. cProfile")
        print("2. line_profiler")
        print("3. memory_profiler")
        print("Type 'exit' to quit.")

        user_input = input("\nEnter your choice: ")

        if user_input == '1' or user_input.lower() == "cprofile":
            subprocess.run([sys.executable, directory + "cprofile.py"])
        elif user_input == '2' or user_input.lower() == "line_profiler":
            subprocess.run([sys.executable, directory + "line_profile.py"])
        elif user_input == '3' or user_input.lower() == "memory_profiler":
            subprocess.run([sys.executable, directory + "memory_profile.py"])
        elif user_input.lower() == "exit":
            break
        else:
            print("Invalid input. Please try again.")

if __name__ == "__main__":
    run_benchmark()
