import sys
import os
# set temporary path so we can find modules in parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import fileinput
from benchmark import get_parameters

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

def profile_simulation():

    print("running memory_profiler...")

    # path to the simulate.py module
    filepath = "simulate.py"

    # uncomment the @profile decorator
    uncomment_profile_decorator(filepath)

    # create a directory for the results if it does not exist
    if not os.path.exists("benchmarks/results_memory_profiler"):
        os.makedirs("benchmarks/results_memory_profiler")

    # get parameters
    N, Nt = get_parameters()
    # set output path
    output_path = "benchmarks/results_memory_profiler/profiler_results.txt"

    # run the memory profiler and save the output to a file
    os.system(sys.executable + " -m memory_profiler simulate.py " + str(N) + " " + str(Nt) + " > " + output_path)

    # comment the @profile decorator
    comment_profile_decorator(filepath)

    print("memory_profiler complete! Results output in 'results_memory_profiler'.")

if __name__== "__main__":
    profile_simulation()
