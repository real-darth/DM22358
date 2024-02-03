from JuliaSet import calc_pure_python
import pytest
import json
 
def get_test_data():
        testList = []
        f = open('testData.json')
        jsonDict = json.load(f)
        for i in jsonDict['tests']:
            testList.append((i['width'], i['iterations'], i['expected']))
        f.close()
        return testList

@pytest.mark.parametrize('width, iterations, expected', get_test_data())
def test_calc_pure_python(width, iterations, expected):
    print(width)
    print(iterations)
    assert sum(calc_pure_python(desired_width=width, max_iterations=iterations)) == expected

@pytest.mark.parametrize('width, iterations, expected', get_test_data())
def test_calc_pure_python_type(width, iterations, expected):
    assert type(calc_pure_python(desired_width=width, max_iterations=iterations)) is list