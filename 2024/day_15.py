#!/usr/bin/python3

from utils import read_stream
import re


def transformer(input):
    sections = re.split('\n\n', input.rstrip())
    warehouse = []
    for line in sections[0].split('\n'):
        warehouse.append(list(line))
    return warehouse, ''.join(sections[1].split('\n'))


def show_warehouse(prefix, warehouse):
    for row in range(len(warehouse)):
        print(prefix, ''.join(warehouse[row]))
    print()


def expand_warehouse(warehouse):
    new_warehouse = []
    for x in range(len(warehouse)):
        row = []
        for y in warehouse[x]:
            if y == '#': row += ['#'] + ['#']
            if y == 'O': row += ['['] + [']']
            if y == '@': row += ['@'] + ['.']
            if y == '.': row += ['.'] + ['.']
        new_warehouse.append(row)
    return new_warehouse


def find_robot(warehouse):
    for x in range(len(warehouse)):
        for y in range(len(warehouse[0])):
            if warehouse[x][y] == '@':
                return [x, y]
    return []


def set_location(warehouse, c, x, y):
    warehouse[x] = warehouse[x][:y] + [str(c)] + warehouse[x][y + 1:]


def box_can_move_north(warehouse, x, y):
    if warehouse[x][y] == ']': y -= 1
    if warehouse[x][y] != '[': return False
    x -= 1

    if warehouse[x][y] == '.':
        if warehouse[x][y + 1] == '.':
            return True

    if warehouse[x][y] == '#': return False
    if warehouse[x][y + 1] == '#': return False

    if warehouse[x][y] == '[':
        return box_can_move_north(warehouse, x, y)

    if warehouse[x][y] == ']':
        if warehouse[x][y + 1] == '[':
            return box_can_move_north(warehouse, x, y - 1) and box_can_move_north(warehouse, x, y + 1)
        return box_can_move_north(warehouse, x, y - 1)

    if warehouse[x][y + 1] == '[':
        return box_can_move_north(warehouse, x, y + 1)


def box_can_move_south(warehouse, x, y):
    if warehouse[x][y] == ']': y -= 1
    if warehouse[x][y] != '[': return False
    x += 1

    if warehouse[x][y] == '.':
        if warehouse[x][y + 1] == '.':
            return True

    if warehouse[x][y] == '#': return False
    if warehouse[x][y + 1] == '#': return False

    if warehouse[x][y] == '[':
        return box_can_move_south(warehouse, x, y)

    if warehouse[x][y] == ']':
        if warehouse[x][y + 1] == '[':
            return box_can_move_south(warehouse, x, y - 1) and box_can_move_south(warehouse, x, y + 1)
        return box_can_move_south(warehouse, x, y - 1)

    if warehouse[x][y + 1] == '[':
        return box_can_move_south(warehouse, x, y + 1)


def move_box_north(warehouse, x, y):
    if warehouse[x][y] == ']': y -= 1
    if warehouse[x][y] != '[': return False

    if not box_can_move_north(warehouse, x, y):
        return False

    if warehouse[x - 1][y] == '.':
        if warehouse[x - 1][y + 1] == '.':
            set_location(warehouse, '[', x - 1, y)
            set_location(warehouse, ']', x - 1, y + 1)
            set_location(warehouse, '.', x, y)
            set_location(warehouse, '.', x, y + 1)
            return True

    if warehouse[x - 1][y] == '[':
        move_box_north(warehouse, x - 1, y)
        set_location(warehouse, '[', x - 1, y)
        set_location(warehouse, ']', x - 1, y + 1)
        set_location(warehouse, '.', x, y)
        set_location(warehouse, '.', x, y + 1)
        return True

    if warehouse[x - 1][y] == ']':
        move_box_north(warehouse, x - 1, y - 1)
        if warehouse[x - 1][y + 1] == '[':
            move_box_north(warehouse, x - 1, y + 1)
        set_location(warehouse, '[', x - 1, y)
        set_location(warehouse, ']', x - 1, y + 1)
        set_location(warehouse, '.', x, y)
        set_location(warehouse, '.', x, y + 1)
        return True

    if warehouse[x - 1][y + 1] == '[':
        move_box_north(warehouse, x - 1, y + 1)
        set_location(warehouse, '[', x - 1, y)
        set_location(warehouse, ']', x - 1, y + 1)
        set_location(warehouse, '.', x, y)
        set_location(warehouse, '.', x, y + 1)
        return True

    return False


def move_box_south(warehouse, x, y):
    if warehouse[x][y] == ']': y -= 1
    if warehouse[x][y] != '[': return False

    if not box_can_move_south(warehouse, x, y):
        return False

    if warehouse[x + 1][y] == '.':
        if warehouse[x + 1][y + 1] == '.':
            set_location(warehouse, '[', x + 1, y)
            set_location(warehouse, ']', x + 1, y + 1)
            set_location(warehouse, '.', x, y)
            set_location(warehouse, '.', x, y + 1)
            return True

    if warehouse[x + 1][y] == '[':
        move_box_south(warehouse, x + 1, y)
        set_location(warehouse, '[', x + 1, y)
        set_location(warehouse, ']', x + 1, y + 1)
        set_location(warehouse, '.', x, y)
        set_location(warehouse, '.', x, y + 1)
        return True

    if warehouse[x + 1][y] == ']':
        move_box_south(warehouse, x + 1, y - 1)
        if warehouse[x + 1][y + 1] == '[':
            move_box_south(warehouse, x + 1, y + 1)
        set_location(warehouse, '[', x + 1, y)
        set_location(warehouse, ']', x + 1, y + 1)
        set_location(warehouse, '.', x, y)
        set_location(warehouse, '.', x, y + 1)
        return True

    if warehouse[x + 1][y + 1] == '[':
        move_box_south(warehouse, x + 1, y + 1)
        set_location(warehouse, '[', x + 1, y)
        set_location(warehouse, ']', x + 1, y + 1)
        set_location(warehouse, '.', x, y)
        set_location(warehouse, '.', x, y + 1)
        return True

    return False


def move_north(warehouse):
    [x, y] = find_robot(warehouse)

    if warehouse[x - 1][y] == '.':
        set_location(warehouse, '@', x - 1, y)
        set_location(warehouse, '.', x, y)
        return True

    if warehouse[x - 1][y] == 'O':
        for new_x in range(x - 2, 0, -1):
            if warehouse[new_x][y] == '#': break
            if warehouse[new_x][y] == '.':
                set_location(warehouse, 'O', new_x, y)
                set_location(warehouse, '@', x - 1, y)
                set_location(warehouse, '.', x, y)
                return True

    if warehouse[x - 1][y] == '[':
        if box_can_move_north(warehouse, x - 1, y):
            move_box_north(warehouse, x - 1, y)
            set_location(warehouse, '@', x - 1, y)
            set_location(warehouse, '.', x - 1, y + 1)
            set_location(warehouse, '.', x, y)
            return True
        return False

    if warehouse[x - 1][y] == ']':
        if box_can_move_north(warehouse, x - 1, y - 1):
            move_box_north(warehouse, x - 1, y - 1)
            set_location(warehouse, '@', x - 1, y)
            set_location(warehouse, '.', x - 1, y - 1)
            set_location(warehouse, '.', x, y)
            return True
        return False

    return False


def move_south(warehouse):
    [x, y] = find_robot(warehouse)

    if warehouse[x + 1][y] == '.':
        set_location(warehouse, '@', x + 1, y)
        set_location(warehouse, '.', x, y)
        return True

    if warehouse[x + 1][y] == 'O':
        for new_x in range(x + 2, len(warehouse) - 1):
            if warehouse[new_x][y] == '#': break
            if warehouse[new_x][y] == '.':
                set_location(warehouse, 'O', new_x, y)
                set_location(warehouse, '@', x + 1, y)
                set_location(warehouse, '.', x, y)
                return True

    if warehouse[x + 1][y] == '[':
        if box_can_move_south(warehouse, x + 1, y):
            move_box_south(warehouse, x + 1, y)
            set_location(warehouse, '@', x + 1, y)
            set_location(warehouse, '.', x + 1, y + 1)
            set_location(warehouse, '.', x, y)
            return True
        return False

    if warehouse[x + 1][y] == ']':
        if box_can_move_south(warehouse, x + 1, y - 1):
            move_box_south(warehouse, x + 1, y - 1)
            set_location(warehouse, '@', x + 1, y)
            set_location(warehouse, '.', x + 1, y - 1)
            set_location(warehouse, '.', x, y)
            return True
        return False

    return False


def move_west(warehouse):
    [x, y] = find_robot(warehouse)

    if warehouse[x][y - 1] == '.':
        set_location(warehouse, '@', x, y - 1)
        set_location(warehouse, '.', x, y)
        return True

    if warehouse[x][y - 1] == 'O':
        for new_y in range(y - 2, 0, -1):
            if warehouse[x][new_y] == '#': break
            if warehouse[x][new_y] == '.':
                set_location(warehouse, 'O', x, new_y)
                set_location(warehouse, '@', x, y - 1)
                set_location(warehouse, '.', x, y)
                return True

    if warehouse[x][y - 1] == ']':
        for new_y in range(y - 3, 0, -1):
            if warehouse[x][new_y] == '#': break
            if warehouse[x][new_y] == '.':
                for i in range(new_y, y):
                    set_location(warehouse, warehouse[x][i + 1], x, i)
                set_location(warehouse, '@', x, y - 1)
                set_location(warehouse, '.', x, y)
                return True

    return False


def move_east(warehouse):
    [x, y] = find_robot(warehouse)

    if warehouse[x][y + 1] == '.':
        set_location(warehouse, '@', x, y + 1)
        set_location(warehouse, '.', x, y)
        return True

    if warehouse[x][y + 1] == 'O':
        for new_y in range(y + 2, len(warehouse[0]) - 1):
            if warehouse[x][new_y] == '#': break
            if warehouse[x][new_y] == '.':
                set_location(warehouse, 'O', x, new_y)
                set_location(warehouse, '@', x, y + 1)
                set_location(warehouse, '.', x, y)
                return True

    if warehouse[x][y + 1] == '[':
        for new_y in range(y + 3, len(warehouse[0]) - 1):
            if warehouse[x][new_y] == '#': break
            if warehouse[x][new_y] == '.':
                for i in range(new_y, y, -1):
                    set_location(warehouse, warehouse[x][i - 1], x, i)
                set_location(warehouse, '@', x, y + 1)
                set_location(warehouse, '.', x, y)
                return True

    return False


def move_robot(warehouse, move):
    if move == '^': move_north(warehouse)
    if move == '>': move_east(warehouse)
    if move == 'v': move_south(warehouse)
    if move == '<': move_west(warehouse)


def sum_gps_coords(warehouse):
    total = 0
    for x in range(len(warehouse)):
        for y in range(len(warehouse[0])):
            if warehouse[x][y] in ['O', '[']:
                total += x * 100 + y
    return total


def main():
    [warehouse, moves] = read_stream('15a', transformer, example=True)
    for move in list(moves):
        move_robot(warehouse, move)
    total = sum_gps_coords(warehouse)
    print(f'Part 1a Example: {total}\t\tIs Correct? {total == 2028}')

    [warehouse, moves] = read_stream('15b', transformer, example=True)
    for move in list(moves):
        move_robot(warehouse, move)
    total = sum_gps_coords(warehouse)
    print(f'Part 1b Example: {total}\t\tIs Correct? {total == 10092}')

    [warehouse, moves] = read_stream('15', transformer, example=False)
    for move in list(moves):
        move_robot(warehouse, move)
    total = sum_gps_coords(warehouse)
    print(f'Part 1 Actual:   {total}\tIs Correct? {total == 1552879}')

    [warehouse, moves] = read_stream('15c', transformer, example=True)
    warehouse = expand_warehouse(warehouse)
    for move in list(moves):
        move_robot(warehouse, move)
    total = sum_gps_coords(warehouse)
    print(f'Part 2a Example: {total}\t\tIs Correct? {total == 618}')

    [warehouse, moves] = read_stream('15b', transformer, example=True)
    warehouse = expand_warehouse(warehouse)
    for move in list(moves):
        move_robot(warehouse, move)
    total = sum_gps_coords(warehouse)
    print(f'Part 2b Example: {total}\t\tIs Correct? {total == 9021}')

    [warehouse, moves] = read_stream('15', transformer, example=False)
    warehouse = expand_warehouse(warehouse)
    for move in list(moves):
        move_robot(warehouse, move)
    total = sum_gps_coords(warehouse)
    print(f'Part 2 Actual:   {total}\tIs Correct? {total == 1561175}')


main()
