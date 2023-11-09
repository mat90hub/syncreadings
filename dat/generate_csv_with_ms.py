
# -------------------------------------
# Generate a file with milliseconds.
# -------------------------------------

import csv
import random
from datetime import datetime, timedelta

def random_float(start, end):
    '''Generate a random float between a specified range'''
    return round(random.uniform(start, end), 2)

def generate_datetimes_with_ms(start, end, step):
    '''Generate a datetime list with steps including milliseconds'''
    current_time = start
    while current_time <= end:
        yield current_time.strftime('%Y-%m-%d %H:%M:%S.%f')[0:-3]
        current_time += step
    return current_time

# Define the file name and data parameters
file_name = 'dat/data_ms.csv'
titles = ['LBA10CT001', 'LBA10CP001', 'LBA10CF001']
line_counts = [200, 200, 250]
datetime_starts = [datetime(2023, 10, 7, 8, 0, 0, 0), datetime(2023, 10, 7, 7, 45, 0, 0), datetime(2023, 10, 7, 7, 50, 0, 0)]
datetime_ends = [datetime(2023, 10, 7, 10, 0, 0, 0), datetime(2023, 10, 7, 10, 15, 0, 0), datetime(2023, 10, 7, 10, 10, 0, 0)]
datetime_steps = [timedelta(seconds=4.5), timedelta(seconds=2.25), timedelta(seconds=2.25)]
value_ranges = [(89.8, 150.56), (8.45, 14.56), (40.5, 78.5)]

# Generate and write the CSV file
with open(file_name, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    for i in range(3):
        title = titles[i]
        line_count = line_counts[i]
        datetime_start = datetime_starts[i]
        datetime_end = datetime_ends[i]
        datetime_step = datetime_steps[i]
        value_range = value_ranges[i]

        csv_writer.writerow([title])

        for datetime_str in generate_datetimes_with_ms(datetime_start, datetime_end, datetime_step):
            value = random_float(*value_range)
            csv_writer.writerow([datetime_str, value])
