import sys
import matplotlib.pyplot as plt
import numpy as np
import ctypes
import os

_getNeighbors = ctypes.CDLL(os.path.join(os.path.dirname(__file__),"getNeighbors.so"))

TYPE_BOOL = ctypes.c_bool
TYPE_INT = ctypes.c_int
TYPE_DOUBLE = ctypes.c_double
TYPE_DOUBLE_LIST = ctypes.POINTER(ctypes.c_double)
TYPE_BOOL_LIST = ctypes.POINTER(ctypes.c_bool)

_getNeighbors.neighbors.argtypes = [TYPE_DOUBLE_LIST, TYPE_DOUBLE_LIST, TYPE_INT,TYPE_INT, TYPE_INT, TYPE_BOOL_LIST]
_getNeighbors.neighbors.restype = None


"""
Simulate Viscek model for flocking birds.

Script based on code made originaly by 
Philip Mocz (2021) Princeton Univeristy, @PMocz
"""

#@profile
def simulate_flocking(N, Nt, seed=17, params = {}):
    """Finite Volume simulation.
    
    Args:
        N (int): Number of birds simulated
        Nt (int): Simulation length, number of time steps
        Seed (int): Seed for the random numbers
        Params (dict): Optional dictionary containing specifications of parameters, like starting velocity, fluctuation etc
    """
    
    # Simulation parameters
    v0           = params.get('v0', 1.0)     # velocity
    eta          = params.get('eta', 0.5)    # random fluctuation in angle (in radians)
    L            = params.get('L', 10)       # size of box
    R            = params.get('R', 1)        # interaction radius
    dt           = params.get('dt', 0.2)     # time step
    plotRealTime = params.get('plotRealTime', False)     # Flag for updating the graph in real-time
    
    # Initialize
    np.random.seed(seed)      # set the random number generator seed

    # bird positions
    x = np.random.rand(N,1)*L
    y = np.random.rand(N,1)*L
    
    # bird velocities
    theta = 2 * np.pi * np.random.rand(N,1)
    vx = v0 * np.cos(theta)
    vy = v0 * np.sin(theta)
    
    # Prep figure
    if plotRealTime:
        fig = plt.figure(figsize=(4,4), dpi=80)
        ax = plt.gca()
    
    # Simulation Main Loop
    neighbors = np.ones(np.shape(x), dtype=bool)
    for i in range(Nt):

        # move
        x += vx*dt
        y += vy*dt
        
        # apply periodic BCs
        x = x % L
        y = y % L
        
        # find mean angle of neighbors within R
        mean_theta = theta
        for b in range(N):

            ## Optimization 1, improvement 1 (numpy vectorization)
            # Reduces performance slightly 
            '''x_a = (np.square(np.subtract(x,x[b])))
            y_a = (np.square(np.subtract(y,y[b])))
            neighbors = x_a + y_a < R**2'''

            ## Optimization 1, improvement 2 (Run in C++)
            # Significantly reduces performance
            # Probably because no vectorization/parallelization is used
            # It also stops passing the majority the unit tests, which also probably means I did the code wrong...
            # Is almost 5 times slower
            cN = TYPE_INT(N)
            cb = TYPE_INT(b)
            cR = TYPE_INT(R)
            pointerX = x.ctypes.data_as(TYPE_DOUBLE_LIST)
            pointerY = y.ctypes.data_as(TYPE_DOUBLE_LIST)
            pointerRes = neighbors.ctypes.data_as(TYPE_BOOL_LIST)

            _getNeighbors.neighbors(pointerX,pointerY,cN,cb,cR,pointerRes)
            #neighbors = (x-x[b])**2+(y-y[b])**2 < R**2
            sx = np.sum(np.cos(theta[neighbors]))
            sy = np.sum(np.sin(theta[neighbors]))
            mean_theta[b] = np.arctan2(sy, sx)
            
        # add random perturbations
        theta = mean_theta + eta*(np.random.rand(N,1)-0.5)
        
        # update velocities
        vx = v0 * np.cos(theta)
        vy = v0 * np.sin(theta)
        # plot in real time
        if plotRealTime: # or (i == Nt-1):
            plt.cla()
            plt.quiver(x,y,vx,vy)
            ax.set(xlim=(0, L), ylim=(0, L))
            ax.set_aspect('equal')    
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)
            plt.pause(0.001)
                
    # Save figure
    if plotRealTime:
        plt.savefig('simulation_plots/activematter.png',dpi=240)
        plt.show()
    return x, y

def main():
    N = 500
    Nt = 200

    # check if the necessary parameters are present
    if len(sys.argv) > 2:
        N = int(sys.argv[1])
        Nt = int(sys.argv[2])
    #else:
    #    print("No parameters provided.")

    simulate_flocking(N, Nt)

# if this file is run by itself, run a basic simulation
if __name__== "__main__":
    main()
    print("Simulation Executed.")
