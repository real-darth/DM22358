import pytest
import json
import numpy as np
import os
from simulate import simulate_flocking, calc_loop_value, calculate_mean_theta, calculate_mean_theta_vect, calculate_mean_theta_torch, calcualte_mean_theta_cython, calculate_mean_theta_cupy, calculate_mean_theta_conc

def get_test_data(name):
    # Get the path to the test data
    current_dir = os.path.dirname(__file__)
    json_file_path = os.path.join(current_dir, 'test_suite', name)

    f = open(json_file_path)
    testList = {}
    jsonDict = json.load(f)
    for test in jsonDict:
        testTuple = ()
        for val in jsonDict.get(test):
            testTuple = testTuple + (jsonDict.get(test).get(val),)
        testList.update({test: testTuple})
    f.close()
    return testList


# Could make improvement to not call get_test_data() twice
'''
@pytest.mark.parametrize('N, nt, seed, params, start_x,start_y,start_theta,change_factor, x, y', get_test_data().values(), ids=get_test_data().keys())
def test_simulate(N, nt, seed, params,start_x,start_y,start_theta,change_factor, x, y):
    res_x, res_y,_,_,_ = simulate_flocking(N, nt, seed,params,np.array(start_x),
                                     np.array(start_y),np.array(start_theta),np.array(change_factor))
    print(res_x[0])
    print(x[0])
    print(res_y[0])
    print(y[0])
    assert np.array_equal(np.around(res_x,5),np.around(x,5))
    assert np.array_equal(np.around(res_y,5),np.around(y,5))
'''

# Could make improvement to not call get_test_data() twice
@pytest.mark.parametrize('x, y,theta,b, R, res', get_test_data("test_data_loop.json").values(), ids=get_test_data("test_data_loop.json").keys())
def test_calculate_mean_singular(x, y,theta, b, R, res):
    result = calc_loop_value(np.array(x),np.array(y),b,R,np.array(theta))
    print("Result was: ", result)
    print("It should be: ", res)
    assert result == res

@pytest.mark.parametrize('x, y,theta, R, res', get_test_data("test_data_whole_loop.json").values(), ids=get_test_data("test_data_whole_loop.json").keys())
def test_calculate_mean(x, y, theta, R, res):
    result_norm,_,_ = calculate_mean_theta(np.array(x),np.array(y),np.array(theta),R)
    result_vect,_,_ = calculate_mean_theta_vect(np.array(x),np.array(y),np.array(theta),R)
    result_conc,_,_ = calculate_mean_theta_conc(np.array(x),np.array(y),np.array(theta),R)
    result_torch,_,_ = calculate_mean_theta_torch(np.array(x),np.array(y),np.array(theta),R)
    result_cupy,_,_ = calculate_mean_theta_cupy(np.array(x),np.array(y),np.array(theta),R)
    result_cython,_,_ = calcualte_mean_theta_cython(np.array(x),np.array(y),np.array(theta),R)
    
    print("Result was (for normal): ", result_norm[0])
    print("Result was (for cython): ", result_cython[0])
    print("Result was (for cupy):: ", result_cupy[0])
    print("Result was (for torch):: ", result_torch[0])
    print("Result was (for concurrent):: ", result_conc[0])
    
    assert np.array_equal(np.around(np.array(res)),np.around(result_norm))
    assert np.array_equal(np.around(result_vect),np.around(result_norm))
    assert np.array_equal(np.around(result_torch),np.around(result_norm))
    assert np.array_equal(np.around(result_cupy),np.around(result_norm))
    assert np.array_equal(np.around(result_conc),np.around(result_norm))

    assert np.array_equal(np.around(result_cython),np.around(result_norm))