from JuliaSet import calc_pure_python
import pytest
import json
import os
 
def get_test_data():
        testList = []
        
        # Get the path to test data
        current_dir = os.path.dirname(__file__)
        json_file_path = os.path.join(current_dir,  'testData.json')
        
        f = open(json_file_path)
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