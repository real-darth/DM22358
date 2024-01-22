import numpy as np



def checktick(time_func):
   M = 200
   timesfound = np.empty((M,))
   for i in range(M):
      t1 = time_func # get timestamp from timer
      t2 = time_func # get timestamp from timer
      while (t2 - t1) < 1e-16: # if zero then we are below clock granularity, retake timing
          t2 = time_func # get timestamp from timer
      t1 = t2 # this is outside the loop
      timesfound[i] = t1 # record the time stamp
   minDelta = 1000000
   Delta = np.diff(timesfound) # it should be cast to int only when needed
   minDelta = Delta.min()

   return minDelta