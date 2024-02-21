import pytest
import json
import numpy as np
from simulate import simulate_flocking



def get_test_data():
    try:
        f = open('test_suite/test_data.json')
    except FileNotFoundError:
        f = open('tests/test_data.json')
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
    res_x, res_y = simulate_flocking(N, nt,seed,params)
    assert np.array_equal(res_x,x)
    assert np.array_equal(res_y,y)
