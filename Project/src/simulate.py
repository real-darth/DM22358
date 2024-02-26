import sys
import matplotlib.pyplot as plt
import numpy as np
from functools import wraps
import torch
import tester

"""
Simulate Viscek model for flocking birds.

Script based on code made originaly by 
Philip Mocz (2021) Princeton Univeristy, @PMocz
"""

def timem(fn):
    from timeit import default_timer as ittimer

    @wraps(fn)
    def measure_time(*args, **kwargs):
        resultArray = np.array([])
        for _ in range(5):
            t1 = ittimer()
            result = fn(*args, **kwargs)
            t2 = ittimer()
            resultArray = np.append(resultArray, [t2 - t1])
            #print(f"@timefn: {fn.__name__} took {t2 - t1} seconds")
        avg = np.average(resultArray)
        #print(f"Average: {avg}")
        std = np.std(resultArray)
        #print(f"Standard deviation: {std}")
        return  result,avg, std

    return measure_time


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
        # IF WE HAVE TIME WRAPPER, WE NEED TO REMOVE THE TIMES AS WELL
        #mean_theta, _, _ = calculate_mean_theta(x,y,theta,R)
        mean_theta, _, _ = calcualte_mean_theta_cython(x,y,theta,R)

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

@timem
def calculate_mean_theta(x, y, theta, R):
    N = len(x)
    mean_theta = np.zeros((N, 1))
    for b in range(N):
        # When making changes in this loop, please also change calc_loop_value if possible
        mean_theta[b] = calc_loop_value(x,y,b,R,theta)

    return mean_theta

@timem
def calculate_mean_theta_vect(x, y, theta, R):
    N = len(x)
    mean_theta = np.zeros((N, 1))

    diff_squared = (x[:, np.newaxis] - x) ** 2 + (y[:, np.newaxis] - y) ** 2

    neighbors = diff_squared < R**2

    # Compute summed cosine and sine values using advanced indexing
    sx = np.sum(np.cos(theta) * neighbors, axis=1)
    sy = np.sum(np.sin(theta) * neighbors, axis=1)

    # Compute mean_theta using arctan2
    mean_theta = np.arctan2(sy, sx)

    return mean_theta

@timem
def calculate_mean_theta_torch(x, y, theta, R):
    x = torch.from_numpy(x)
    y = torch.from_numpy(y)
    theta = torch.from_numpy(theta)
    N = len(x)
    mean_theta = torch.zeros((N, 1))
    diff_squared = (x.unsqueeze(1) - x) ** 2 + (y.unsqueeze(1) - y) ** 2
    neighbors = diff_squared < R**2
    # Compute summed cosine and sine values using advanced indexing
    sx = torch.sum(torch.cos(theta) * neighbors, dim=1)
    sy = torch.sum(torch.sin(theta) * neighbors, dim=1)
    # Compute mean_theta using arctan2
    mean_theta = torch.atan2(sy, sx)

    return mean_theta

@timem
def calculate_mean_theta_conc(
    x: np.ndarray, y: np.ndarray, theta: np.ndarray, R: float
) -> np.ndarray:
    N = len(x)
    mean_theta = np.zeros((N, 1))

    def process_data(b):
        neighbors = (x - x[b]) ** 2 + (y - y[b]) ** 2 < R**2
        sx = np.sum(np.cos(theta[neighbors]))
        sy = np.sum(np.sin(theta[neighbors]))
        return np.arctan2(sy, sx)

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(process_data, b) for b in range(N)]
        for b, future in enumerate(futures):
            mean_theta[b] = future.result()

    return mean_theta


@timem
def calcualte_mean_theta_cython(x, y, theta, R):
    N = len(x)
    mean_theta = np.zeros((N, 1))
    #print("before", mean_theta)
    flatten = mean_theta.flatten()
    tester.calculate_mean_theta(x.flatten(), y.flatten(), theta.flatten(), N, R, flatten)
    # print("after", flatten)
    return flatten.reshape(x.shape)

## Is right now the original code...
def calc_loop_value(x,y,b,R,theta):
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
        '''cN = TYPE_INT(N)
        cb = TYPE_INT(b)
        cR = TYPE_INT(R)
        pointerX = x.ctypes.data_as(TYPE_DOUBLE_LIST)
        pointerY = y.ctypes.data_as(TYPE_DOUBLE_LIST)
        pointerRes = neighbors.ctypes.data_as(TYPE_BOOL_LIST)

        _getNeighbors.neighbors(pointerX,pointerY,cN,cb,cR,pointerRes)'''
        
        neighbors = (x-x[b])**2+(y-y[b])**2 < R**2
        sx = np.sum(np.cos(theta[neighbors]))
        sy = np.sum(np.sin(theta[neighbors]))

        # optimization 3?:
        val = np.arctan2(sy, sx)

        return val

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
    '''
    test = "cuda" if torch.cuda.is_available() else "cpu"
    if test == "cpu":
        print("ABORT, CPU WAS SELECTED")
    else:
        main()
        print("Simulation Executed.")
    '''

    main()
    print("Simulation Executed.")
