import sys
import os
# set temporary path so we can find modules in parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import fileinput
from benchmark import parse_parameters_arguments

# very hacky solution
def uncomment_profile_decorator(filepath):
    with fileinput.FileInput(filepath, inplace=True) as file:
        for line in file:
            # change the line in the code to enable memory profiler
            print(line.replace("#@profile", "@profile"), end='')

def comment_profile_decorator(filepath):
    with fileinput.FileInput(filepath, inplace=True) as file:
        for line in file:
            # remove profile from source
            print(line.replace("@profile", "#@profile"), end='')

def profile_simulation(simulation, N, Nt):

    print(f"running memory_profiler with {N} birds...")

    # path to the simulate.py module
    filepath = "simulate.py"

    # uncomment the @profile decorator
    uncomment_profile_decorator(filepath)

    # create a directory for the results if it does not exist
    if not os.path.exists("benchmarks/results_memory_profiler"):
        os.makedirs("benchmarks/results_memory_profiler")

    # set output path
    output_path = f"benchmarks/results_memory_profiler/mpout_{simulation}_n_{N}.txt"

    # run the memory profiler and save the output to a file
    os.system(sys.executable + " -m memory_profiler simulate.py " + str(N) + " " + str(Nt) + str(simulation) + " > " + output_path)

    # comment the @profile decorator
    comment_profile_decorator(filepath)

    print("memory_profiler complete! Results output in 'results_memory_profiler'.")

if __name__== "__main__":
    # parse command-line arguments
    args = parse_parameters_arguments()
    # get parameters
    N = args.num_birds
    Nt = args.simulation_length
    sim = args.simulation_type
    # run simulation
    profile_simulation(sim, N, Nt)
