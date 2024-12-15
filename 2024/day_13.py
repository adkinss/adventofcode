#!/usr/bin/python3

from utils import read_stream
import re


def transformer(input):
    machines = []
    for machine in re.split('\n\n', input.rstrip()):
        lines = machine.split('\n')
        button_a = [int(i) for i in re.findall('\\d+', lines[0])]
        button_b = [int(i) for i in re.findall('\\d+', lines[1])]
        prize = [int(i) for i in re.findall('\\d+', lines[2])]
        machines.append([button_a, button_b, prize])
    return machines


def by_brute_force(machine, error_correction):
    [button_a, button_b, prize] = machine
    if error_correction:
        prize[0] += 10000000000000
        prize[1] += 10000000000000

    found_x = []
    for a in range(int(prize[0] / button_a[0]) + 1):
        for b in range(int(prize[0] / button_b[0]) + 1):
            x = button_a[0] * a + button_b[0] * b
            if x > prize[0]: break
            if x == prize[0]:
                found_x.append([a, b])
                break

    found_y = []
    for a in range(int(prize[1] / button_a[1]) + 1):
        for b in range(int(prize[1] / button_b[1]) + 1):
            y = button_a[1] * a + button_b[1] * b
            if y > prize[1]: break
            if y == prize[1]:
                found_y.append([a, b])
                break

    if len(found_x) and len(found_y):
        intersection = list(filter(lambda p: p in found_x, found_y))
        if len(intersection):
            cost = []
            for i in intersection:
                tokens = i[0] * 3 + i[1]
                cost.append(tokens)
            return min(cost)

    return 0


def by_calculation(machine, error_correction):
    [a, b, p] = machine
    if error_correction:
        p[0] += 10000000000000
        p[1] += 10000000000000

    x = (p[0] * b[1] - p[1] * b[0]) / (a[0] * b[1] - a[1] * b[0])
    y = (p[0] * a[1] - p[1] * a[0]) / (b[0] * a[1] - a[0] * b[1])
    if x == int(x) and y == int(y):
        return int(x * 3 + y)

    return 0


def main():
    print('By brute force:')

    machines = read_stream('13', transformer, example=True)
    total = 0
    for machine in machines:
        total += by_brute_force(machine, False)
    print(f'Part 1 Example: {total}\t\tIs Correct? {total == 480}')

    machines = read_stream('13', transformer, example=False)
    total = 0
    for machine in machines:
        total += by_calculation(machine, False)
    print(f'Part 1 Actual:  {total}\t\tIs Correct? {total == 28138}')

    print('\nBy calculation:')

    machines = read_stream('13', transformer, example=True)
    total = 0
    for machine in machines:
        total += by_calculation(machine, False)
    print(f'Part 1 Example: {total}\t\tIs Correct? {total == 480}')

    machines = read_stream('13', transformer, example=False)
    total = 0
    for machine in machines:
        total += by_calculation(machine, False)
    print(f'Part 1 Actual:  {total}\t\tIs Correct? {total == 28138}')

    machines = read_stream('13', transformer, example=True)
    total = 0
    for machine in machines:
        total += by_calculation(machine, True)
    print(f'Part 2 Example: {total}\tIs Correct? {total == 875318608908}')

    machines = read_stream('13', transformer, example=False)
    total = 0
    for machine in machines:
        total += by_calculation(machine, True)
    print(f'Part 2 Actual:  {total}\tIs Correct? {total == 108394825772874}')


main()
