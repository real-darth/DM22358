import sys
import matplotlib.pyplot as plt
import numpy as np
import neighbors

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
    np.random.seed(seed)      # set the random number generator seed
    # bird positions
    if len(start_x) == 0:
        start_x = np.random.rand(N,1)*L
        start_y = np.random.rand(N,1)*L

    x = np.copy(start_x)
    y = np.copy(start_y)
    
    # bird velocities
    if len(start_theta) == 0:
        start_theta = 2 * np.pi * np.random.rand(N,1)

    theta = np.copy(start_theta)
    vx = v0 * np.cos(theta)
    vy = v0 * np.sin(theta)
    
    use_rand_change = False
    if len(change_factor) == 0:
        use_rand_change = True

    # Prep figure
    if plotRealTime:
        fig = plt.figure(figsize=(4,4), dpi=80)
        ax = plt.gca()
    
    # calcualte R_squared once
    R_squared = R * R

    #neighbors_org = np.ones(np.shape(x), dtype=bool)
    #neighbors_array = np.ones(x.shape[0], dtype=np.intc)
    neighbors_array = np.ones(np.shape(x), dtype=np.intc)
    neighbors_flattened = neighbors_array.flatten()

    #print(np.shape(neighbors_flattened))
    #print(np.shape(x))
    #print(np.shape(y))

    # Simulation Main Loop
    for i in range(Nt):

        # move
        x += vx*dt
        y += vy*dt
        
        # apply periodic BCs
        x = x % L
        y = y % L
        
        # find mean angle of neighbors within R
        mean_theta = theta
        # flatten neighbors array before passing it to the Cython function
        neighbors.calculate_neighbors(x.flatten(), y.flatten(), N, R_squared, neighbors_flattened)

        # reshape neighbors back to its original shape
        neighbors_array = neighbors_flattened.reshape(neighbors_array.shape)

        for b in range(N):
            # Original code for neighbors
            '''
            neighbors = (x - x[b])**2 + (y - y[b])**2 < R**2
            '''

            ## Optimization 1, improvement 1 (numpy vectorization)
            # Reduces performance slightly 
            '''x_a = (np.square(np.subtract(x,x[b])))
            y_a = (np.square(np.subtract(y,y[b])))
            neighbors = x_a + y_a < R**2'''

            sx = np.sum(np.cos(theta[neighbors_array]))
            sy = np.sum(np.sin(theta[neighbors_array]))

            # optimization 3?:
            mean_theta[b] = np.arctan2(sy, sx)
            
        # add random perturbations
        if use_rand_change:
            theta = mean_theta + eta*(np.random.rand(N,1)-0.5)
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
