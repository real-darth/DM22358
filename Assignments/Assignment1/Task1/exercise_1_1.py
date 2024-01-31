#import JuliaSet  # noqa: F401
import numpy as np
import time
from timeit import default_timer as timer
from functools import wraps

# Task 1.1 Calculate the Clock Granularity of different Python Timers (on your system).
# code for calculating the 'clock granularity', source from Canvas
def checktick(time_func):
   M = 200
   timesfound = np.empty((M,))
   for i in range(M):
      t1 = time_func() # get timestamp from timer
      t2 = time_func() # get timestamp from timer
      while (t2 - t1) < 1e-16: # if zero then we are below clock granularity, retake timing
          t2 = time_func() # get timestamp from timer
      t1 = t2 # this is outside the loop
      timesfound[i] = t1 # record the time stamp
   minDelta = 1000000
   Delta = np.diff(timesfound) # it should be cast to int only when needed
   minDelta = Delta.min()

   return minDelta

# run the different time modules multiple times
def run_clock_granularity_benchmark():
   case_1_arr = []
   case_2_arr = []
   case_3_arr = []
   for _ in range (100):
      case_1 = checktick(time.time)
      case_2 = checktick(timer)
      case_3 = checktick(time.time_ns)

      case_1_arr.append(case_1)
      case_2_arr.append(case_2)
      case_3_arr.append(case_3)

   # print the results of the different timers
   print("1 - average time.time(): {} (s), STD: {}".format(np.average(case_1_arr), np.std(case_1_arr)))
   print("2 - average timeit: {} (s), STD: {}".format(np.average(case_2_arr), np.std(case_2_arr)))
   print("3 - average time.time_ns(): {} (ns), STD: {}".format(np.average(case_3_arr), np.std(case_3_arr)))

# Task 1.2 Timing the Julia set code functions
def decorator_func(fn):
   from timeit import default_timer as ittimer
   @wraps(fn)
   def measure_time(*args, **kwargs):
      resultArray = np.array([])
      for _ in range(5):
         t1 = ittimer()
         result = fn(*args, **kwargs)
         t2 = ittimer()
         resultArray = np.append(resultArray,[t2-t1])
         print(f"@timefn: {fn.__name__} took {t2 - t1} seconds")
      print(f"Average: {np.average(resultArray)}")
      print(f"Standard deviation: {np.std(resultArray)}")
      return result
   return measure_time


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

# 1.4.1
# time python -m memory_profiler JuliaSet.py

# 1.4.2
# time python -m mprof run JuliaSet.py
# python -m mprof plot <file>.dat


# main
if __name__ == "__main__":
    pass
