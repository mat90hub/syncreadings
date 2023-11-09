import pytest

'''
This script is rapid checks that can be launched with the
command `pytest`
'''


import os
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
LIB_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '../../lib'))
DAT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '../../dat'))

import sys
sys.path.append(LIB_DIR)


from lib.setsManagement import read_measures, check_constant_time_step
from lib.setsManagement import check_datetime_format, sets_starts_ends_steps
from lib.setsManagement import sets_starts_ends_steps, report_on_sets

# we read files to be tested and converts to sets dictionaries
@pytest.fixture
def SETS():
    _result = []
    for name in ["data.csv", "data_ms.csv"]:
        _filename = os.path.abspath(os.path.join(DAT_DIR, name))
        _result.append(read_measures(_filename))
    return _result


def test_read_names(SETS) -> None:
    '''
    Test we are recovering the correct measure names
    '''
    _result= True
    for _sets in SETS:        
        for _key in _sets.keys():
            if _key not in ["LBA10CT001", "LBA10CP001", "LBA10CF001"]:
                _result = False
    assert _result == True


def test_check_constant_time_step(SETS) -> None:
    '''Test the time step is constant in the sets'''
    for _sets in SETS:
        assert check_constant_time_step(_sets)


# different time formats to be recognized
@pytest.mark.parametrize("DATE, FORMAT", [
    ("2023-10-22 08:10:30","%Y-%m-%d %H:%M:%S"),
    ("2023-10-22 08:10:30.432","%Y-%m-%d %H:%M:%S.%f"),
])
def test_check_datetime_format(DATE, FORMAT):
    assert check_datetime_format(DATE) == FORMAT


'''
>> add some test for
sets_starts_ends_steps
report_on_sets
chose_start_end_steps
'''


# for debugging the test file!
if __name__ == "__main__":

    test_read_measures()

    test_check_constant_time_step()