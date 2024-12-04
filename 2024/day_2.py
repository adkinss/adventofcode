#!/usr/bin/python3

from utils import read_input


def transformer(line):
    string_list = line.split()
    return [int(s) for s in string_list]


def is_safe(levels):
    if levels in [sorted(levels), sorted(levels, reverse=True)]:
        deltas = list(map(lambda x, y: abs(y - x), levels[:-1], levels[1:]))
        return all(d in [1, 2, 3] for d in deltas)
    return False


def is_mostly_safe(levels):
    if is_safe(levels):
        return True

    for idx in range(len(levels)):
        if is_safe(levels[:idx] + levels[idx + 1:]):
            return True
    return False


input = read_input('2', transformer, example=True)
total_safe = sum(list(map(is_safe, input)))
print(f'Part 1 Example:\t{total_safe}\tIs Correct? {total_safe == 2}')

input = read_input('2', transformer, example=False)
total_safe = sum(list(map(is_safe, input)))
print(f'Part 1 Actual:\t{total_safe}\tIs Correct? {total_safe == 299}')

input = read_input('2', transformer, example=True)
total_safe = sum(list(map(is_mostly_safe, input)))
print(f'Part 2 Example:\t{total_safe}\tIs Correct? {total_safe == 4}')

input = read_input('2', transformer, example=False)
total_safe = sum(list(map(is_mostly_safe, input)))
print(f'Part 2 Actual:\t{total_safe}\tIs Correct? {total_safe == 364}')
