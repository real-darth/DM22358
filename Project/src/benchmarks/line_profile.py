##
# @file
# File containing code for running the line profilier
#

import sys
import os
# set temporary path so we can find modules in parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from line_profiler import LineProfiler
from simulate import simulate_flocking
from simulate import calculate_mean_theta, calculate_mean_theta_vect, calculate_mean_theta_torch, calcualte_mean_theta_cython, calculate_mean_theta_conc, calculate_mean_theta_cupy
from benchmark import parse_parameters_arguments

def profile_simulation(simulation, N, Nt):
    """
    Run the cprofile simulation with the set parameters
    """
    print(f"running line_profiler with {N} birds, simulation {simulation}...")

    # create a line-profiler
    profiler = LineProfiler()

    # add the main function to the profiling kit
    profiler.add_function(simulate_flocking)
    # add the simulation function that is selected
    if (simulation == 0):
        profiler.add_function(calculate_mean_theta.__wrapped__)
    elif (simulation == 1):
        profiler.add_function(calculate_mean_theta_vect.__wrapped__)
    elif (simulation == 2):
        profiler.add_function(calculate_mean_theta_torch.__wrapped__)
    elif (simulation == 3):
        profiler.add_function(calcualte_mean_theta_cython.__wrapped__)
    elif (simulation == 4):
        profiler.add_function(calculate_mean_theta_conc.__wrapped__)
    elif (simulation == 5):
        profiler.add_function(calculate_mean_theta_cupy.__wrapped__)

    # add the correct function to track as well
    # run profiler
    profiler.enable_by_count()
    simulate_flocking(N, Nt, simulation=simulation)
    profiler.disable_by_count()

    # create a directory for the results if it does not exist
    if not os.path.exists("benchmarks/results_line_profiler"):
        os.makedirs("benchmarks/results_line_profiler")

    # save results to a file in the specified directory
    with open(f"benchmarks/results_line_profiler/out_{simulation}_n_{N}.txt", "w") as f:
        # print them but redirect stream to file
        profiler.print_stats(stream=f)

if __name__== "__main__":
    # parse command-line arguments
    args = parse_parameters_arguments()
    # get parameters
    N = args.num_birds
    Nt = args.simulation_length
    sim = args.simulation_type

    # run simulation
    profile_simulation(sim, N, Nt)

    print("line_profiler complete! Results output in 'results_line_profiler'.")