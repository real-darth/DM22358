import sys
import os
# set temporary path so we can find modules in parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from line_profiler import LineProfiler
from simulate import simulate_flocking
from benchmark import parse_parameters_arguments

def profile_simulation(func, N, Nt):
    """
    Run the cprofile simulation with the set parameters
    """
    print(f"running line_profiler with {N} birds...")

    # create a line-profiler
    profiler = LineProfiler()
    # add function to be profiled
    profiler.add_function(simulate_flocking)
    # run profiler
    profiler.enable_by_count()
    simulate_flocking(N, Nt)
    profiler.disable_by_count()


    # create a directory for the results if it does not exist
    if not os.path.exists("benchmarks/results_line_profiler"):
        os.makedirs("benchmarks/results_line_profiler")

    # save results to a file in the specified directory
    with open("benchmarks/results_line_profiler/profiler_results.txt", "w") as f:
        # print them but redirect stream to file
        profiler.print_stats(stream=f)

if __name__== "__main__":
    # parse command-line arguments
    args = parse_parameters_arguments()
    # get parameters
    N = args.num_birds
    Nt = args.simulation_length
    # run simulation
    profile_simulation(None, N, Nt)

    print("line_profiler complete! Results output in 'results_line_profiler'.")