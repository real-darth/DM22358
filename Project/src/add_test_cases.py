from json import JSONEncoder
import json
import numpy as np
from simulate import simulate_flocking, calc_loop_value, calculate_mean_theta

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


def remove_test(test_name)  -> None:
    '''
    Function that removes a given test case from the test_data.json file

    Args:
        test_name (String): Name of the test to be removed
    '''

    # Load existing test case
    with open("test_suite/test_data.json", "r") as read_file:
        test_data = json.load(read_file)

    # Remove the test case
    try:
        del test_data[test_name]
    except IndexError:
        print("No test with that name could be found")

    # Write updated test data to the JSON file
    with open("test_suite/test_data.json", "w") as write_file:
        json.dump(test_data, write_file, indent=4)

def add_test(test_name, N=500, nt=200, seed=17, params={}) -> None:
    '''
    Function that adds a test case to the test_data.json file

    Args:
        test_name (String): Name of the new test
        N (int): Number of birds simulated
        Nt (int): Simulation length, number of time steps
        Seed(int): Seed for the randomness in the simulation
        Params (dict): Optional dictionary containing specifications of parameters, like starting velocity, fluctuation etc
    '''

    # Check if there already exists data
    try:
        with open("test_suite/test_data.json", "r") as read_file:
            tests = json.load(read_file)
    except FileNotFoundError:
        tests = {}

    if test_name in tests:
        return

    # Fetch the simulated data results
    change_factor = np.random.rand(N,1)
    x, y,start_x,start_y,startTheta = simulate_flocking(N,nt,seed,params,change_factor=change_factor)

    # Append inputs and outputs to the test
    test_data = {"N":N,"nt":nt, "seed":seed, "params":params,"start_x":start_x,"start_y":start_y,
                 "start_theta":startTheta,"change_factor":change_factor,"x": x, "y": y}

    tests[test_name] = test_data
    # Write test data to the JSON file
    with open("test_suite/test_data.json", "w") as write_file:
        json.dump(tests, write_file, cls=NumpyArrayEncoder, indent=4)

def add_test_loop_singular(test_name,N=500,L=10,R=1) -> None:
    '''
    Function that adds a test case to the test_data.json file

    Args:
        test_name (String): Name of the new test
        N (int): Number of birds simulated
        Nt (int): Simulation length, number of time steps
        Seed(int): Seed for the randomness in the simulation
        Params (dict): Optional dictionary containing specifications of parameters, like starting velocity, fluctuation etc
    '''

    # Check if there already exists data
    try:
        with open("test_suite/test_data_loop.json", "r") as read_file:
            tests = json.load(read_file)
    except FileNotFoundError:
        tests = {}

    if test_name in tests:
        return

    # Fetch the simulated data results
    x = np.random.rand(N,1)*L
    y = np.random.rand(N,1)*L
    b = np.random.randint(0, N)
    theta = 2 * np.pi * np.random.rand(N,1)
    testVal = calc_loop_value(x,y,b,R,theta)

    test_data = {"x":x,"y":y,
                 "theta":theta,"b":b,"R": R, "res": testVal}

    tests[test_name] = test_data
    # Write test data to the JSON file
    with open("test_suite/test_data_loop.json", "w") as write_file:
        json.dump(tests, write_file, cls=NumpyArrayEncoder, indent=4)


def add_test_loop(test_name,N=500,L=10,R=1) -> None:
    '''
    Function that adds a test case to the test_data.json file

    Args:
        test_name (String): Name of the new test
        N (int): Number of birds simulated
    '''

    # Check if there already exists data
    try:
        with open("test_suite/test_data_whole_loop.json", "r") as read_file:
            tests = json.load(read_file)
    except FileNotFoundError:
        tests = {}

    if test_name in tests:
        return

    # Fetch the simulated data results
    x = np.random.rand(N,1)*L
    y = np.random.rand(N,1)*L
    theta = 2 * np.pi * np.random.rand(N,1)
    mean_theta,_,_ = calculate_mean_theta(x,y,theta,R)

    test_data = {"x":x,"y":y,
                 "theta":theta,"R": R, "result": mean_theta}

    tests[test_name] = test_data
    # Write test data to the JSON file
    with open("test_suite/test_data_whole_loop.json", "w") as write_file:
        json.dump(tests, write_file, cls=NumpyArrayEncoder, indent=4)

if __name__== "__main__":
    for i in range(40,60,8):
        name = "simple_test" + str(i*10)
        add_test(name,i*10)
        for j in range(1,2):
            name = "v0=" + str(j) + "_test"
            add_test(name,i*10,params={'v0':j})
        name = "single_loop_test" + str(i*10)
        add_test_loop_singular(name,i*10)
        name = "whole_loop_test" + str(i*10)
        add_test_loop(name,i*10)
        
    print("All tests added.")