import sys
import os
# set temporary path so we can find modules in parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import cProfile
from simulate import simulate_flocking
from benchmark import get_parameters

def profile_simulation(func, N, Nt):
    """
    Run the cprofile simulation with the set parameters
    """
    print("running cProfile...")

    # run cProfiler on simulation
    profiler = cProfile.Profile()
    profiler.enable()
    simulate_flocking(N, Nt)
    profiler.disable()

    # create a directory for the results if it does not exist
    if not os.path.exists("benchmarks/results_cProfile"):
        os.makedirs("benchmarks/results_cProfile")

    # save results to a file
    profiler.dump_stats("benchmarks/results_cProfile/profiler_results.txt")

if __name__== "__main__":
    # get parameters
    N, Nt = get_parameters() 
    # run simulation
    profile_simulation(None, N, Nt)

    print("cProfile complete! Results output in 'results_cProfile'.")
