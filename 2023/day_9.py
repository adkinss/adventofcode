#!/usr/bin/python3

from utils import read_input


def transformer(line):
    values = []
    for s in line.split('\n'):
        all_numbers = s.split(' ')
        values = [int(n) for n in all_numbers]
    return values


def create_new_series(series):
    """
    Given a series, create a set of new series that are subsets of the previous
    series which are deltas between consecutive numbers in the previous series.
    When a new series is all zeros, return a list containing the original series
    and all the new series created, including the series of all zeros.
    Example: [0, 3, 6, 9, 12, 15]
    Returns: [[0, 3, 6, 9, 12, 15], [3, 3, 3, 3, 3], [0, 0, 0, 0]]
    """
    all_series = [series]

    this_series = all_series[-1]
    while sum(map(abs, this_series)) > 0:
        new_series = []
        for i in range(len(this_series) - 1):
            new_series.append(this_series[i + 1] - this_series[i])
        if new_series == []:
            new_series = [0]
        all_series.append(new_series)
        this_series = all_series[-1]

    return all_series


def find_next_value(all_series):
    """
    Given the a series and all the subset series created from it, determine the
    next value of the series and return it. The next value is derived from the
    next value of the subset series.
    """
    for i in reversed(range(len(all_series))):
        this_series = all_series[i]
        if sum(map(abs, this_series)) == 0:
            all_series[i].append(0)
            continue

        next_series = all_series[i + 1]
        all_series[i].append(this_series[-1] + next_series[-1])

    return all_series[0][-1]


def find_all_values(all_series):
    """
    For each series, create the subset series in order to find the next value.
    Calculate the next vaue and return a list of all the next values found.
    """
    next_values = []
    for series in all_series:
        new_series = create_new_series(series)
        next_value = find_next_value(new_series)
        next_values.append(next_value)
    return next_values


input = read_input("9a", transformer, example=True)
next_value = sum(find_all_values(input))
print(f'Part 1 Example A: {next_value}\tExpecting: 114')

input = read_input("9b", transformer, example=True)
next_value = sum(find_all_values(input))
print(f'Part 1 Example B: {next_value}\tExpecting: 68')

input = read_input("9a", transformer, example=True)
for i in range(len(input)):
    input[i] = list(reversed(input[i]))
next_value = sum(find_all_values(input))
print(f'Part 2 Example A: {next_value}\tExpecting: 2')

input = read_input("9b", transformer, example=True)
for i in range(len(input)):
    input[i] = list(reversed(input[i]))
next_value = sum(find_all_values(input))
print(f'Part 2 Example A: {next_value}\tExpecting: -4\n')

input = read_input("9", transformer, example=False)
next_value = sum(find_all_values(input))
print(f'Part 1: {next_value}\tExpecting: 2043677056')

input = read_input("9", transformer, example=False)
for i in range(len(input)):
    input[i] = list(reversed(input[i]))
next_value = sum(find_all_values(input))
print(f'Part 2: {next_value}\t\tExpecting: 1062')
