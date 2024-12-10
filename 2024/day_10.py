#!/usr/bin/python3

from utils import read_stream


def transformer(line):
    map = []
    padding = ''
    for l in line.split('\n'):
        if len(l) > 0:
            if not map:
                padding = '.' * (len(l) + 2)
                map.append(padding)
            map.append('.' + l + '.')
    map.append(padding)
    return map


def print_map(map):
    for l in map:
        print(''.join(l))


def walk_trail(map, x, y, height):
    if map[x][y] == '9':
        return [(x, y)]

    result = []
    if map[x - 1][y] == str(height + 1):
        result += walk_trail(map, x - 1, y, height + 1)
    if map[x + 1][y] == str(height + 1):
        result += walk_trail(map, x + 1, y, height + 1)
    if map[x][y - 1] == str(height + 1):
        result += walk_trail(map, x, y - 1, height + 1)
    if map[x][y + 1] == str(height + 1):
        result += walk_trail(map, x, y + 1, height + 1)
    return list(set(result))


def walk_distinct_trail(map, x, y, height):
    if map[x][y] == '9':
        return 1

    result = 0
    if map[x - 1][y] == str(height + 1):
        result += walk_distinct_trail(map, x - 1, y, height + 1)
    if map[x + 1][y] == str(height + 1):
        result += walk_distinct_trail(map, x + 1, y, height + 1)
    if map[x][y - 1] == str(height + 1):
        result += walk_distinct_trail(map, x, y - 1, height + 1)
    if map[x][y + 1] == str(height + 1):
        result += walk_distinct_trail(map, x, y + 1, height + 1)
    return result


map = read_stream('10', transformer, example=True)
total = 0
for i in range(len(map)):
    for j in range(len(map[0])):
        if map[i][j] == '0':
            total += len(walk_trail(map, i, j, 0))
print(f'Part 1 Example:\t{total}\tIs Correct? {total == 36}')

map = read_stream('10', transformer, example=False)
total = 0
for i in range(len(map)):
    for j in range(len(map[0])):
        if map[i][j] == '0':
            total += len(walk_trail(map, i, j, 0))
print(f'Part 1 Actual:\t{total}\tIs Correct? {total == 461}')

map = read_stream('10', transformer, example=True)
total = 0
for i in range(len(map)):
    for j in range(len(map[0])):
        if map[i][j] == '0':
            total += walk_distinct_trail(map, i, j, 0)
print(f'Part 2 Example:\t{total}\tIs Correct? {total == 81}')

map = read_stream('10', transformer, example=False)
total = 0
for i in range(len(map)):
    for j in range(len(map[0])):
        if map[i][j] == '0':
            total += walk_distinct_trail(map, i, j, 0)
print(f'Part 2 Actual:\t{total}\tIs Correct? {total == 875}')
