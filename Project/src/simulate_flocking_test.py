import pytest
import json
import numpy as np
import os
from simulate import simulate_flocking



def get_test_data():

    # Get the path to the test data
    current_dir = os.path.dirname(__file__)
    json_file_path = os.path.join(current_dir, 'test_suite', 'test_data.json')

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
@pytest.mark.parametrize('N, nt, seed, params, x, y', get_test_data().values(), ids=get_test_data().keys())
def test_simulate(N, nt, seed, params, x, y):
    res_x, res_y = simulate_flocking(N, nt, seed,params)
    print(res_x[0])
    print(x[0])
    print(res_y[0])
    print(y[0])
    assert np.array_equal(np.around(res_x,5),np.around(x,5))
    assert np.array_equal(np.around(res_y,5),np.around(y,5))
