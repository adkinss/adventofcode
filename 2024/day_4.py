#!/usr/bin/python3

from utils import read_stream


def transformer(line):
    grid = []
    padding = ''
    for l in line.split('\n'):
        if len(l) > 0:
            if not grid:
                padding = '.' * (len(l) + 2)
                grid.append(padding)
            grid.append('.' + l + '.')
    grid.append(padding)
    return grid


def count_xmas_p1(grid):
    total_found = 0
    for y in range(len(input)):
        for x in range(len(input[y])):
            for d in [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]:
                [dx, dy, found] = [x, y, 1]
                for c in 'XMAS':
                    if input[dy][dx] != c:
                        found = 0
                        break
                    dx += d[0]
                    dy += d[1]
                total_found += found
    return total_found


def count_xmas_p2(grid):
    total_found = 0
    for y in range(len(input)):
        for x in range(len(input[y])):
            if input[y][x] == 'A':
                x = input[y - 1][x - 1] + input[y - 1][x + 1] + input[y + 1][x - 1] + input[y + 1][x + 1]
                if x in ['MSMS', 'MMSS', 'SSMM', 'SMSM']:
                    total_found += 1
    return total_found


input = read_stream('4', transformer, example=True)
total = count_xmas_p1(input)
print(f'Part 1 Example:\t{total}\tIs Correct? {total == 18}')

input = read_stream('4', transformer, example=False)
total = count_xmas_p1(input)
print(f'Part 1 Actual:\t{total}\tIs Correct? {total == 2547}')

input = read_stream('4', transformer, example=True)
total = count_xmas_p2(input)
print(f'Part 2 Example:\t{total}\tIs Correct? {total == 9}')

input = read_stream('4', transformer, example=False)
total = count_xmas_p2(input)
print(f'Part 2 Actual:\t{total}\tIs Correct? {total == 1939}')
