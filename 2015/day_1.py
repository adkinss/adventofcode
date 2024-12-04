#!/usr/bin/python3

from utils import read_input


def transformer(line):
    """
    Keep track of the level we are on and which level was the level
    that we first entered the basement (level -1). For each "(", we go
    up a level, and for each ")", we go down a level.
    """
    values = []
    for s in line.split('\n'):
        level, pos, basement = [0, 0, 0]
        for c in s:
            pos += 1
            if c == "(": level += 1
            if c == ")": level -= 1
            if level == -1 and basement == 0:
                basement = pos
        values = [level, basement]
    return values


input = read_input("1a", transformer, example=True)
expected_answers = [0, 0, 3, 3, 3, -1, -1, -3, -3]
for line in input:
    print(f"Part 1 Example: {line[0]}\tExpecting: {expected_answers.pop(0)}")
print()

input = read_input("1b", transformer, example=True)
expected_answers = [1, 5]
for line in input:
    print(f"Part 2 Example: {line[1]}\tExpecting: {expected_answers.pop(0)}")
print()

input = read_input("1", transformer, example=False)
expected_answers = [74]
for line in input:
    print(f"Part 1: {line[0]}\t\tExpecting: {expected_answers.pop(0)}")

input = read_input("1", transformer, example=False)
expected_answers = [1795]
for line in input:
    print(f"Part 2: {line[1]}\t\tExpecting: {expected_answers.pop(0)}")
