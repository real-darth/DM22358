import argparse
import subprocess
import sys

# location of all the benchmarking scripts
directory = "benchmarks\\" # use this instead for linux: "benchmarks/"

DEFAULT_N_PARAMETER = 500
DEFAULT_NT_PARAMETER = 200

def set_parameters():
    """Set the simulation parameters by input from user."""
    global param_N, param_Nt
    # set the parameters based on user input or default values
    print("Set simulation parameters. Leave blank if using default values.")
    param_N = input("Enter the simulation parameter for [number of birds] (INTEGER): ")
    if param_N == None or param_N == "":
        param_N = DEFAULT_N_PARAMETER
    else:
        param_N = int(param_N)
    
    param_Nt = input("Enter the simulation parameter for [simulation time] (INTEGER): ")
    if param_Nt == None or param_Nt == "":
        param_Nt = DEFAULT_NT_PARAMETER
    else:
        param_Nt = int(param_Nt)

def set_simulation():
    global simulation_type
    print("\nSelect which simulation to run:")
    print("1. Original")
    print("2. Vectorized")
    print("3. Torch")
    print("4. Cython")
    print("5. Concurrent")
    print("6. CuPy")

    user_input = input("\nEnter your choice: ")

    if user_input == '1' or user_input.lower() == "original":
        simulation_type = 0
    elif user_input == '2' or user_input.lower() == "vectorized":
        simulation_type = 1
    elif user_input == '3' or user_input.lower() == "torch":
        simulation_type = 2
    elif user_input == '4' or user_input.lower() == "cython":
        simulation_type = 3
    elif user_input == '5' or user_input.lower() == "concurrent":
        simulation_type = 4
    elif user_input == '6' or user_input.lower() == "cuPy":
        simulation_type = 5
    else:
        # default to original simulation
        simulation_type = 0

def parse_parameters_arguments():
    parser = argparse.ArgumentParser(description="Simulation script with customizable parameters.")
    parser.add_argument("-N", "--num_birds", type=int, default=None,
                        help="Number of birds for the simulation")
    
    parser.add_argument("-Nt", "--simulation_length", type=int, default=None,
                        help="Simulation length (number of time steps)")
    
    parser.add_argument("-SIM", "--simulation_type", type=int, default=None,
                        help="The type of simulation calculation to use")
    return parser.parse_args()

def run_benchmark():
    print("----------------- BENCHMARK TOOL -----------------")
    # set simulation parameters at the start of the tool
    set_parameters()
    set_simulation()
    print("Simulation Parameters assigned:")
    print(f"N: {param_N}, Nt: {param_Nt}")
    print(f"Simulation set: {simulation_type + 1}")

    while True:
        print("\n" "---------------------------------------------------")
        print("Select a benchmark to run:")
        print("1. cProfile")
        print("2. line_profiler")
        print("3. memory_profiler")
        print("\nor\n")
        print("Type 'sim' to change simulation type.")
        print("Type 'params' to change simulation parameters.")
        print("Type 'exit' to quit.")

        user_input = input("\nEnter your choice: ")

        if user_input == '1' or user_input.lower() == "cprofile":
            subprocess.run([sys.executable, directory + "cprofile.py", "-N", str(param_N), "-Nt", str(param_Nt), "-SIM", str(simulation_type)])
        elif user_input == '2' or user_input.lower() == "line_profiler":
            subprocess.run([sys.executable, directory + "line_profile.py", "-N", str(param_N), "-Nt", str(param_Nt), "-SIM", str(simulation_type)])
        elif user_input == '3' or user_input.lower() == "memory_profiler":
            subprocess.run([sys.executable, directory + "memory_profile.py", "-N", str(param_N), "-Nt", str(param_Nt), "-SIM", str(simulation_type)])
        elif user_input.lower() == "sim":
            set_simulation()
            print(f"Simulation set: {simulation_type + 1}")
        elif user_input.lower() == "param":
            set_parameters()
            print("Simulation Parameters assigned:")
            print(f"N: {param_N}, Nt: {param_Nt}")
        elif user_input.lower() == "exit":
            break
        else:
            print("Invalid input. Please try again.")

if __name__ == "__main__":
    run_benchmark()
