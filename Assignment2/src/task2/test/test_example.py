import pytest

def get_sum_test_data():
        return [(3,5,8), (-2,-2,-4), (-1,5,4), (3,-5,-2), (0,5,5)]@pytest.mark.parametrize('num1, num2, expected',get_sum_test_data())
def test_sum(num1, num2, expected):
        assert sum(num1, num2) == expected