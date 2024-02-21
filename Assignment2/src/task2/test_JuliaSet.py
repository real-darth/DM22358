from JuliaSet import calc_pure_python
import pytest
import json
 
def get_test_data():
        testList = []
        try:
            f = open('testData.json')
        except FileNotFoundError:
            f = open('tests/testData.json')
        jsonDict = json.load(f)
        for i in jsonDict['tests']:
            testList.append((i['width'], i['iterations'], i['expected']))
        f.close()
        return testList

@pytest.mark.parametrize('width, iterations, expected', get_test_data())
def test_calc_pure_python(width, iterations, expected):
    lst = calc_pure_python(desired_width=width, max_iterations=iterations)
    assert sum(lst) == expected
    assert type(lst) is list