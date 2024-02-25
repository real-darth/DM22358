import sys
import matplotlib.pyplot as plt
import numpy as np
import torch

'''
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
'''

"""
Simulate Viscek model for flocking birds.

Script based on code made originaly by 
Philip Mocz (2021) Princeton Univeristy, @PMocz
"""

#@profile
def simulate_flocking(N, Nt, seed=17, params = {}, start_x = [], start_y = [], start_theta = [], change_factor = []):
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
    plotRealTime = params.get('plotRealTime', False) # Flag for updating the graph in real-time
    
    # Initialize
    torch.manual_seed(seed)   # set the random number generator seed
    # bird positions
    if len(start_x) == 0:
        start_x = torch.rand(N,1)*L
        start_y = torch.rand(N,1)*L
    else:
        start_x = torch.from_numpy(start_x)
        start_y = torch.from_numpy(start_y)

    x = start_x.detach().clone()
    y = start_y.detach().clone()
    
    # bird velocities
    if len(start_theta) == 0:
        start_theta = 2 * torch.pi * torch.rand(N,1)
    else:
        start_theta = torch.from_numpy(start_theta)

    theta = start_theta.detach().clone()
    vx = v0 * torch.cos(theta)
    vy = v0 * torch.sin(theta)
    
    use_rand_change = False
    if len(change_factor) == 0:
        use_rand_change = True
    else:
        change_factor = torch.from_numpy(change_factor)

    # Prep figure
    if plotRealTime:
        fig = plt.figure(figsize=(4,4), dpi=80)
        ax = plt.gca()
    
    # Simulation Main Loop
    #neighbors = np.ones(np.shape(x), dtype=bool)
    for i in range(Nt):

        # move
        x += vx*dt
        y += vy*dt
        
        # apply periodic BCs
        x = x % L
        y = y % L
        
        # find mean angle of neighbors within R
        mean_theta = theta
        # Calculate squared distances in one go
        distances = (x.unsqueeze(1) - x) ** 2 + (y.unsqueeze(1) - y) ** 2
        # Mask out non-neighbors using broadcasting
        neighbors = distances < R**2
        # Vectorized sum of cosine and sine using masked reduction
        sx = torch.sum(torch.cos(theta) * neighbors, dim=1)
        sy = torch.sum(torch.sin(theta) * neighbors, dim=1)
        # Calculate mean theta using safe division (avoiding potential divide by zero)
        mean_theta = torch.atan2(sy, sx + 1e-8)  # Add small epsilon for safety
            
        # add random perturbations
        if use_rand_change:
            theta = mean_theta + eta*(torch.rand(N,1)-0.5)
        else: 
            theta = mean_theta + eta*(change_factor-0.5)

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
    return x, y, start_x, start_y, start_theta

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
