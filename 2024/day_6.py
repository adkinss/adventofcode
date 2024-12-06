#!/usr/bin/python3

from utils import read_stream
from copy import deepcopy


def transformer(line):
    map = []
    padding = ''
    for l in line.split('\n'):
        if len(l) > 0:
            if not map:
                padding = ' ' * (len(l) + 2)
                map.append(list(padding))
            map.append(list(' ' + l + ' '))
    map.append(list(padding))
    return map


def print_map(prefix, map):
    for row in map:
        print(prefix, ''.join(row))


def walk_the_map(map):
    found = False
    for row in range(len(map)):
        for col in range(len(map[row])):
            if map[row][col] == '^':
                found = True
                break
        if found:
            break

    # give_up = len(map) * len(map[0])
    give_up = 10000
    while give_up > 0:
        give_up -= 1
        if map[row][col] == '^':
            if map[row - 1][col] == '^':
                return -1
            if map[row - 1][col] not in ['#', 'O', ' ']:
                row -= 1
                map[row][col] = '^'
                continue
            if map[row - 1][col] in ['#', 'O']:
                map[row][col] = '>'
                continue
            break
        if map[row][col] == '>':
            if map[row][col + 1] == '>':
                return -1
            if map[row][col + 1] not in ['#', 'O', ' ']:
                col += 1
                map[row][col] = '>'
                continue
            if map[row][col + 1] in ['#', 'O']:
                map[row][col] = 'v'
                continue
            break
        if map[row][col] == 'v':
            if map[row + 1][col] == 'v':
                return -1
            if map[row + 1][col] not in ['#', 'O', ' ']:
                row += 1
                map[row][col] = 'v'
                continue
            if map[row + 1][col] in ['#', 'O']:
                map[row][col] = '<'
                continue
            break
        if map[row][col] == '<':
            if map[row][col - 1] == '<':
                return -1
            if map[row][col - 1] not in ['#', 'O', ' ']:
                col -= 1
                map[row][col] = '<'
                continue
            if map[row][col - 1] in ['#', 'O']:
                map[row][col] = '^'
                continue
            break

    if give_up < 1:
        return -1

    count = 0
    for row in range(len(map)):
        for col in range(len(map[row])):
            if map[row][col] in ['^', '>', 'v', '<']:
                count += 1
    return count


map = read_stream('6', transformer, example=True)
total = walk_the_map(map)
print(f'Part 1 Example:\t{total}\tIs Correct? {total == 41}')

map = read_stream('6', transformer, example=False)
total = walk_the_map(map)
print(f'Part 1 Actual:\t{total}\tIs Correct? {total == 4778}')

map = read_stream('6', transformer, example=True)
total = 0
for row in range(1, len(map) - 1):
    for col in range(1, len(map[row]) - 1):
        if map[row][col] == '.':
            map_copy = deepcopy(map)
            map_copy[row][col] = 'O'
            if walk_the_map(map_copy) < 0:
                total += 1
print(f'Part 2 Example:\t{total}\tIs Correct? {total == 6}')

map = read_stream('6', transformer, example=False)
total = 0
for row in range(1, len(map) - 1):
    for col in range(1, len(map[row]) - 1):
        if map[row][col] == '.':
            map_copy = deepcopy(map)
            map_copy[row][col] = 'O'
            if walk_the_map(map_copy) < 0:
                total += 1
print(f'Part 2 Actual:\t{total}\tIs Correct? {total == 1618}')
