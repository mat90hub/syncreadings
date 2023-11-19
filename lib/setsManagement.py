#!/usr/bin/env python3

from collections import defaultdict
from collections.abc import Callable
from datetime import datetime, timedelta
from math import lcm, gcd
import pandas as pd
from tabulate import tabulate
import random
import re

from tkinter import messagebox

"""
The default choices for synchronizing the data sets
- start, end: max, min or a date-time as a string ;
- step: min, max, lcm, gcd, or a sting expressing a duration 
  (converted by pandas.Timedelta)

step = min: we use the shortest step
step = max: we use the greatest step

step = lcm: we use the Lower Common Multiplier
step = gcd: we use the Greater Common Divider,
Both lcm or gcd can have an advantage if there is a
common starting point, since they are maximizing the
number of coincidences. lcm > gcd

step = integer: means a time step is imposed disregarding existing
ones. A general interpolation will be done.

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
>> In the first version we choose: 
>>  step=gcd
>>  start=max
>>  end=min
>> which means no need of interpolation and exact values
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
"""

default_choices = {
    'start': 'max',
    'end': 'min',
    'step': 'gcd',
    'datetime_format': '%Y-%m-%d %H:%M:%S'
}
def get_default_choices() -> dict:
    return default_choices


def read_measures(filename: str) -> dict:
    """
    Read a filename containing sets of data one below each other
    and return a list measures.

    The result is structured as following:
    {
        'meas01': [(date, value), (date, value) ...],
        'meas02': [(date, value), (date, value) ...],
        ...
    }
    """
    with open(filename, 'r') as file:
        lines = file.readlines()

        measures = defaultdict(list)
        # see : https://docs.python.org/fr/3/library/collections.html
        # Usually, a Python dictionary throws a KeyError if you try
        # to get an item with a key that is not currently in the
        # dictionary. The defaultdict in contrast will simply create
        # any items that you try to access (provided of course they
        # do not exist yet).

        name = 'xxx'
        date_format_checked = False
        datetime_format = '%Y-%m-%d %H:%M:%S'
        for line in lines:
            if ',' in line:
                date_str, value_str = line.strip().split(',')
                if not date_format_checked:
                    datetime_format = check_datetime_format(date_str)
                    date_format_checked = True
                try:
                    date = datetime.strptime(date_str, datetime_format)
                    value = float(value_str)
                except ValueError as err:
                    messagebox.showerror(
                        title='ValueError with File',
                        message="Script and data file format don't match."
                    )
                measures[name].append((date, value))
            else:
                name = line.strip()
                # if ms for one set, applies for all
                if (datetime_format[-1] != 'f'):
                    date_format_checked = False
        return measures

def check_constant_time_step(data:dict, nb_tests=3) -> bool:
    """
    Check if the time steps between measure is constant.
    The complete check is too long for large sets,
    so we do sampling test instead.
    """
    for k in data.keys():
        _NUMB_MEAS = len(data[k])
        if _NUMB_MEAS <= 1:
            raise NameError(f'List {data[k]} has only 1 or less element!')

        _STEP = data[k][1][0] - data[k][0][0]           # first step

        if (data[k][-1][0] - data[k][-2][0] != _STEP):  # compare with last step
            return False

        for N in range(nb_tests):                       # do random tests
            _NUM = random.randint(1, _NUMB_MEAS-2)
            if (data[k][_NUM+1][0] - data[k][_NUM][0] != _STEP):
                return False
    return True

def check_datetime_format(date_str:str) -> str:
    """
    Analyze the sets of measures and determine the
    exact format of the datetime
        'datetime_format': '%Y-%m-%d %H:%M:%S'    (default)
        'datetime_format': '%Y-%m-%d %H:%M:%S.%f' (with milliseconds)
    """
    pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}'
    if bool(re.search(pattern, date_str)):
        result = '%Y-%m-%d %H:%M:%S.%f'
        default_choices['datetime_format'] = result
        return result

    pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'
    if bool(re.search(pattern, date_str)):
        result = '%Y-%m-%d %H:%M:%S'
        return result

    pattern = r'\d{2}:\d{2}:\d{2}\.\d{3}'
    if bool(re.search(pattern, date_str)):
        result = '%H:%M:%S.%f'
        default_choices['datetime_format'] = result
        return result

    pattern = r'\d{2}:\d{2}:\d{2}'
    if bool(re.search(pattern, date_str)):
        result = '%H:%M:%S'
        return result

def sets_starts_ends_steps(data: dict) -> dict:
    """
    Analyze the characteristics of sets of measures:
    - the min, max starting date-time
    - the min, max ending date-time
    - the time steps with their gcd and lcm
    """
    result = {}
    _starts = [data[k][0][0] for k in data.keys()]
    result['starts'] = _starts
    result['start_earliest'] = min(_starts)
    result['start_latest'] = max(_starts)
    _ends = [data[k][-1][0] for k in data.keys()]
    result['ends'] = _ends
    result['end_earliest'] = min(_ends)
    result['end_latest'] = max(_ends)

    _time_steps = [(data[k][1][0] - data[k][0][0]) for k in data.keys()]
    result['time_step'] = _time_steps
    result['time_step_shortest'] = min(_time_steps)
    result['time_step_longest'] = max(_time_steps)

    if default_choices['datetime_format'][-1] == 'f':
        # datetime used milliseconds, lcm and gcd are calculated with ms
        _time_steps_ms = [int(step.total_seconds()*1000)
                          for step in _time_steps]
        result['time_step_lcm'] = timedelta(milliseconds= lcm(*_time_steps_ms))
        result['time_step_gcd'] = timedelta(milliseconds= gcd(*_time_steps_ms))
    else:
        _time_steps = [int(step.total_seconds()) for step in _time_steps]
        result['time_step_lcm'] = timedelta(seconds=lcm(*_time_steps))
        result['time_step_gcd'] = timedelta(seconds= gcd(*_time_steps))

    return result

def report_on_sets(data: dict) -> str:
    """
    Give chosen characteristics in a string.
    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    In the first version, we just declare choice made.
    There is no possibility given to change it.
    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    """
    _RES = sets_starts_ends_steps(data)

    time_format = default_choices['datetime_format']
    if (time_format[-1] == 'f'):
        with_ms = True
    else:
        with_ms = False

    _LLIST = []
    if with_ms:
        _LLIST.append(['earliest start is',
                       _RES['start_earliest'].strftime(time_format)[0:-3]])
        _LLIST.append(['latest start is',
                       _RES['start_latest'].strftime(time_format)[0:-3]])
        _LLIST.append(['retained start is',
                       _RES['start_latest'].strftime(time_format)[0:-3]])
        _LLIST.append(['',''])

        _LLIST.append(['earliest end is',
                       _RES['end_earliest'].strftime(time_format)[0:-3]])
        _LLIST.append(['latest end is',
                       _RES['end_latest'].strftime(time_format)[0:-3]])
        _LLIST.append(['retained end is',
                       _RES['end_earliest'].strftime(time_format)[0:-3]])
        _LLIST.append(['',''])
    else:
        _LLIST.append(['earliest start is',
                       _RES['start_earliest'].strftime(time_format)])
        _LLIST.append(['latest start is',
                       _RES['start_latest'].strftime(time_format)])
        _LLIST.append(['retained start is',
                       _RES['start_latest'].strftime(time_format)])
        _LLIST.append(['',''])

        _LLIST.append(['earliest end is',
                       _RES['end_earliest'].strftime(time_format)])
        _LLIST.append(['latest end is',
                       _RES['end_latest'].strftime(time_format)])
        _LLIST.append(['retained end is',
                       _RES['end_earliest'].strftime(time_format)])
        _LLIST.append(['',''])

    steps_list = ''
    unit = 's'
    for step in _RES['time_step']:
        steps_list += f'{step.total_seconds()}{unit}, '
    steps_list = steps_list.strip(', ')
    _LLIST.append(['time steps are', steps_list])
    _LLIST.append(['time steps lcm is', f"{_RES['time_step_lcm'].total_seconds()}{unit}"])
    _LLIST.append(['time steps gcd is', f"{_RES['time_step_gcd'].total_seconds()}{unit}"])

    return tabulate(_LLIST)

def choose_start_end_step(data: dict, synchro_choice=default_choices) -> list:
    """
    From sets of data and settings determine start, end and step.
    """
    # determine start / end / step according to settings
    char = sets_starts_ends_steps(data)
    start_with_empties = False
    end_with_empties = False

    match synchro_choice['start']:
        case 'min':
            _start = char['time_step']
            start_with_empties = True
        case 'max':
            _start = char['start_latest']
        case _:
            try:
                _start = datetime.strptime(char['start'], 
                                           synchro_choice['datetime_format'])
                if (_start < char['start_latest']):
                    start_with_empties = True
            except ValueError:
                messagebox.showerror(
                        title='Date format error',
                        message=f'Start date {_start} not matching chosen format settings.')

    match synchro_choice['end']:
        case 'min':
            _end = char['end_earliest']
        case 'max':
            _end = char['end_latest']
            end_with_empties = True
        case _:
            try:
                _end = datetime.strptime(char['date'], 
                                         synchro_choice['datetime_format'])
                if (_end > char['end_soonest']):
                    end_with_empties = False
            except ValueError:
                messagebox.showerror(
                        title='Date format error', 
                        message=f'End date {_end} not matching chosen format settings.')
    
    match synchro_choice['step']:
        case 'lcm':
            _step = char['time_step_lcm']
        case 'gcd':
            _step = char['time_step_gcd']            
        case 'max':
            _step = char['time_step_longest']
        case 'min':
            _step = char['time_step_shortest']
        case _:
            # the synchro_choice['step'] should give the exact chosen step
            _step = pd.Timedelta(synchro_choice['step'])
            
    # stopping for not developed options
    if (start_with_empties):
        messagebox.showinfo('Development pending', 'For this version, all sets shall have beginning values.')
        return {}
    if (end_with_empties):
        messagebox.showinfo('Development pending', 'For this version, all sets shall have ending values.')
        return {}

    return (_start,  _end, _step)


def synchronized_sets(data: dict, 
                      synchro_choice=default_choices, 
                      choose_value=lambda x: round(sum(x)/len(x),4),
                      interpol=lambda t,t1,t2,v1,v2: round(v1 + (t-t1)*(v2-v1)/(t2-t1),4)) -> pd.DataFrame:
    '''
    From a dict containing all measures, propose the common time frame
    and re-arrange measure into a table, which is a list of list.
    The internal list is composed of a date-time followed by each values,
    the external list loops over time.
    '''

    # get the start, end and step from data and settings
    _start, _end, _step = choose_start_end_step(data, synchro_choice)

    # Create a table of synchronized time ticks
    dataSync = {}
    numb_posSync = int((_end - _start).total_seconds() // _step.total_seconds())
    dataSync['time'] = [_start + i*_step for i in range(numb_posSync)]
    lastPosSync = numb_posSync - 1

    # generate list of synchronized values
    for name in data.keys():
        
        pos = 0       # position in the source list
        lastPos = len(data[name]) - 1

        dataSync[name] = [None] * numb_posSync
        posSync = 0   # number of ticks in source
        
        while pos < lastPos:
            time, value = data[name][pos]
            if time < _start:
                pos += 1
                continue
            elif time > _end:
                break
            else:# if interval was overpassed, one step before
                timeSync = dataSync['time'][posSync]
                timeSup = timeSync + _step  # the limit sup of the interval
                intVal = []                 # the values taken in the interval
                lenInt = 0                  # number of value in an interval
                while time < timeSup:       # retrieve all values of the interval
                    intVal.append(value)
                    lenInt += 1
                    pos += 1                 # prepare for next?
                    time, value = data[name][pos]
                    if pos >= lastPos:
                        break                    
                if lenInt > 0:               # at least one value in the interval                    
                    dataSync[name][posSync] = choose_value(intVal)                    
                else:
                    # recover the first preceding value (already stored)
                    if time == _start:
                        _tim1 = data[name][0][0]
                        _val1# if interval was overpassed, one step before = data[name][0][1]
                    else:
                        _tim1 = data[name][pos-1][0]
                        _val1 = data[name][pos-1][1]                        
                    # recover the first next value
                    _tim2 = data[name][pos+1][0]
                    _val2 = data[name][pos+1][1]                    
                    dataSync[name][posSync] = interpol(timeSync, _tim1, _tim2, _val1, _val2)
                # if interval was overpassed, one step before
                if time >= timeSup:      
                    pos -= 1
            # update positions
            pos += 1
            posSync += 1
            if posSync > lastPosSync:
                break

    # transfer into a pandas DateFrame
    df = pd.DataFrame({'datetime':pd.to_datetime(dataSync['time'])})
    for name in data.keys():
        df[name] = dataSync[name]
    df.set_index('datetime', inplace=True)

    return df


if __name__ == '__main__':

    filename = './dat/data.csv'
    data_set = read_measures(filename)

    # Recover characteristics of the sets
    char = sets_starts_ends_steps(data_set)
    result = ''
    for k in char.keys():
        result += f'{k}: {char[k]}\n'
    print(f'\n{result}\n')

    df = synchronized_sets(data_set)

    print(df.head(5))
