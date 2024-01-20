import JuliaSet  # noqa: F401
import cProfile
import snakeviz

# Task 1.1 Calculate the Clock Granularity of different Python Timers (on your system).

# Task 1.2 Timing the Julia set code functions

# Task 1.3 T Profile the Julia set code with cProfile and line_profiler the computation


def task_1_3():
    cProfile.run("JuliaSet.calc_pure_python(10000, 300)", "calc_pure_python.stat")
    # for mor info see: https://jiffyclub.github.io/snakeviz/
    snakeviz.view("calc_pure_python.stat")


# Task 1.4 Memory-profile the Juliaset code. Use the memory_profiler and mprof
# to profile the computation in JuliaSet code.


# main
if __name__ == "__main__":
    task_1_3()
