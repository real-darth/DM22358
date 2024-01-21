import JuliaSet  # noqa: F401


# Task 1.1 Calculate the Clock Granularity of different Python Timers (on your system).

# Task 1.2 Timing the Julia set code functions

# Task 1.3 T Profile the Julia set code with cProfile and line_profiler the computation

# For the task 1.3.1 I used the cProfile package

# python -m cProfile -o calc_pure_python.stat JuliaSet.py
# python -m snakeviz calc_pure_python.stat --server

# For the task 1.3.2 I used the line_profiler package

# add the @profile decorator to the function you want to profile
# time python -m kernprof -l JuliaSet.py
# python -m line_profiler -l JuliaSet.py.lprof


# Task 1.4 Memory-profile the Juliaset code. Use the memory_profiler and mprof
# to profile the computation in JuliaSet code.

# add the @profile decorator to the function you want to profile
# importing it as `from memory_profiler import profile`


# 1.4.1
# time python -m memory_profiler JuliaSet.py

# 1.4.2
# time python -m mprof run JuliaSet.py
# python -m mprof plot <file>.dat


# main
if __name__ == "__main__":
    pass
