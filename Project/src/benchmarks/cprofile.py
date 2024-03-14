##
# @file
# File containing code for running the c profilier
#
import sys
import os
# set temporary path so we can find modules in parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import cProfile
from simulate import simulate_flocking
from benchmark import parse_parameters_arguments

def profile_simulation(simulation, N, Nt):
    """
    Run the cprofile simulation with the set parameters
    """
    print(f"running cProfile with {N} birds, simulation {simulation}...")

    # run cProfiler on simulation
    profiler = cProfile.Profile()
    profiler.enable()
    simulate_flocking(N, Nt, simulation=simulation)
    profiler.disable()

    # create a directory for the results if it does not exist
    if not os.path.exists("benchmarks/results_cProfile"):
        os.makedirs("benchmarks/results_cProfile")

    # save results to a file
    profiler.dump_stats(f"benchmarks/results_cProfile/cout_{simulation}_n_{N}.profile")

if __name__== "__main__":
    # parse command-line arguments
    args = parse_parameters_arguments()
    # get parameters
    N = args.num_birds
    Nt = args.simulation_length
    sim = args.simulation_type
    # run simulation
    profile_simulation(sim, N, Nt)

    print("cProfile complete! Results output in 'results_cProfile'.")
