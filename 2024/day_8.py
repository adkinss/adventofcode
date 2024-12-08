#!/usr/bin/python3

from utils import read_stream


def transformer(line):
    [input_map, output_map] = [[], []]
    for l in line.split('\n'):
        if l == '': continue
        input_map.append(list(l))
        output_map.append('.' * len(l))
    return input_map, output_map


def print_map(prefix, map):
    for row in range(len(map)):
        input = ''.join(map[row])
        print(prefix, input)


def print_both_maps(prefix, input_map, output_map):
    for row in range(len(input_map)):
        input = ''.join(input_map[row])
        output = ''.join(output_map[row])
        print(prefix, input, '    ', output)


def scan_map(input_map):
    satelite_dishes = {}
    for row in range(len(input_map)):
        for col in range(len(input_map[0])):
            if input_map[row][col] == '.': continue
            if input_map[row][col] not in satelite_dishes:
                satelite_dishes[input_map[row][col]] = []
            satelite_dishes[input_map[row][col]].append([row, col])
    return satelite_dishes


def find_antinodes(satelite_dishes, output_map, updated_model):
    max_len = len(output_map[0])
    for s in satelite_dishes:
        for i in range(len(satelite_dishes[s])):
            for j in range(len(satelite_dishes[s])):
                p1 = satelite_dishes[s][i]
                p2 = satelite_dishes[s][j]
                if i == j:
                    if updated_model:
                        before = output_map[p1[0]][:p1[1]]
                        after = output_map[p1[0]][p1[1] + 1:]
                        output_map[p1[0]] = before + '#' + after
                    continue
                dx = p1[0] + (p1[0] - p2[0])
                dy = p1[1] + (p1[1] - p2[1])
                while dx >= 0 and dx < max_len and dy >= 0 and dy < max_len:
                    before = output_map[dx][:dy]
                    after = output_map[dx][dy + 1:]
                    output_map[dx] = before + '#' + after
                    if not updated_model: break
                    dx = dx + (p1[0] - p2[0])
                    dy = dy + (p1[1] - p2[1])

    total = 0
    for row in range(len(output_map)):
        for col in range(len(output_map[0])):
            if output_map[row][col] == '#':
                total += 1
    return total


[input_map, output_map] = read_stream('8', transformer, example=True)
satelite_dishes = scan_map(input_map)
total = find_antinodes(satelite_dishes, output_map, False)
print(f'Part 1 Example:\t{total}\tIs Correct? {total == 14}')

[input_map, output_map] = read_stream('8', transformer, example=False)
satelite_dishes = scan_map(input_map)
total = find_antinodes(satelite_dishes, output_map, False)
print(f'Part 1 Actual:\t{total}\tIs Correct? {total == 254}')

[input_map, output_map] = read_stream('8', transformer, example=True)
satelite_dishes = scan_map(input_map)
total = find_antinodes(satelite_dishes, output_map, True)
print(f'Part 2 Example:\t{total}\tIs Correct? {total == 34}')

[input_map, output_map] = read_stream('8', transformer, example=False)
satelite_dishes = scan_map(input_map)
total = find_antinodes(satelite_dishes, output_map, True)
print(f'Part 2 Actual:\t{total}\tIs Correct? {total == 951}')
