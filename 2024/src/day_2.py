#!/usr/bin/python3

from utils import read_input


def transformer(line):
    string_list = line.split()
    return [int(s) for s in string_list]


def is_safe(levels):
    [up, down] = [0, 0]
    for idx, i in enumerate(levels):
        if idx == 0:
            continue
        if levels[idx] - levels[idx - 1] > 0:
            up += 1
        if levels[idx] - levels[idx - 1] < 0:
            down += 1

    if up > 0 and down > 0:
        return False

    for idx, i in enumerate(levels):
        if idx == 0:
            continue
        d = abs(levels[idx] - levels[idx - 1])
        if d < 1 or d > 3:
            return False

    return True


input = read_input('2', transformer, example=True)
total_safe = 0
for l in input:
    if is_safe(l):
        total_safe += 1
print(f'Part 1 Example:\t{total_safe}\tIs Correct? {total_safe == 2}')

input = read_input('2', transformer, example=False)
total_safe = 0
for l in input:
    if is_safe(l):
        total_safe += 1
print(f'Part 1 Actual:\t{total_safe}\tIs Correct? {total_safe == 299}')

input = read_input('2', transformer, example=True)
total_safe = 0
for l in input:
    if is_safe(l):
        total_safe += 1
        continue
    for idx, i in enumerate(l):
        smaller = l.copy()
        del smaller[idx]
        if is_safe(smaller):
            total_safe += 1
            break
print(f'Part 2 Example:\t{total_safe}\tIs Correct? {total_safe == 4}')

input = read_input('2', transformer, example=False)
total_safe = 0
for l in input:
    if is_safe(l):
        total_safe += 1
        continue
    for idx, i in enumerate(l):
        smaller = l.copy()
        del smaller[idx]
        if is_safe(smaller):
            total_safe += 1
            break
print(f'Part 2 Actual:\t{total_safe}\tIs Correct? {total_safe == 364}')
