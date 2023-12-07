#!/usr/bin/python3

from utils import read_multisection_input


def transformer(line):
    values = []
    for value in line.split('\n'):
        if value.isnumeric():
            values.append(int(value))
    return values


input = read_multisection_input("1", transformer, example=True)
largest = max(sum(callories) for callories in input)
largest3 = sum(sorted((sum(calories) for calories in input), reverse=True)[:3])
print(f'Part 1 Example: {largest}\tExpecting: 24000')
print(f'Part 2 Example: {largest3}\tExpecting: 45000\n')

input = read_multisection_input("1", transformer, example=False)
largest = max(sum(calories) for calories in input)
largest3 = sum(sorted((sum(calories) for calories in input), reverse=True)[:3])
print(f'Part 1: {largest}\t\tExpecting: 68802')
print(f'Part 2: {largest3}\t\tExpecting: 205370')
