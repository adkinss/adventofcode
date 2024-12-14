#!/usr/bin/python3

from utils import read_stream


def transformer(input):
    garden = []
    padding = ""
    for line in input.split("\n"):
        if len(line) > 0:
            if not garden:
                padding = "." * (len(line) + 2)
                garden.append(padding)
            garden.append("." + line + ".")
    garden.append(padding)
    return garden


def print_garden(prefix, garden):
    for row in garden:
        print(prefix, "".join(row))
    if prefix != "": print()


def region_size(garden, region):
    [min_x, max_x, min_y, max_y] = [len(garden), 0, len(garden[0]), 0]
    for x, y in region:
        if x < min_x: min_x = x
        if x > max_x: max_x = x
        if y < min_y: min_y = y
        if y > max_y: max_y = y

    # build a newer, smaller garden with just the region
    new_garden = []
    new_garden.append("." * ((max_y - min_y + 1) * 2 + 3))
    for x in range((max_x - min_x + 1) * 2 + 1):
        new_garden.append("." * ((max_y - min_y + 1) * 2 + 3))
    new_garden.append("." * ((max_y - min_y + 1) * 2 + 3))

    # zoom in on the region
    for x, y in region:
        new_x = 2 * (x - min_x) + 2
        new_y = 2 * (y - min_y) + 2
        new_garden[new_x] = new_garden[new_x][:new_y] + "X" + new_garden[new_x][new_y + 1:]

    # fill in the gaps between all the plants
    for x in range(2, len(new_garden), 2):
        for y in range(2, len(new_garden[0]), 2):
            if new_garden[x][y] != "X": continue
            if x - 2 >= 0:
                if new_garden[x - 2][y] == "X":
                    new_garden[x - 1] = new_garden[x - 1][:y] + " " + new_garden[x - 1][y + 1:]
            if y - 2 >= 0:
                if new_garden[x][y - 2] == "X":
                    new_garden[x] = new_garden[x][:y - 1] + " " + new_garden[x][y:]

    # put in the side fencing
    for x in range(len(new_garden)):
        for y in range(len(new_garden[0]) - 1):
            if new_garden[x][y + 1] != ".":
                c = "+" if x % 2 else "|"
                new_garden[x] = new_garden[x][:y] + c + new_garden[x][y + 1:]
                break
        for y in range(len(new_garden[0]) - 1, 0, -1):
            if new_garden[x][y - 1] != ".":
                c = "+" if x % 2 else "|"
                new_garden[x] = new_garden[x][:y] + c + new_garden[x][y + 1:]
                break

    # put in the top and bottom fencing
    for y in range(len(new_garden[0])):
        for x in range(len(new_garden) - 1):
            if new_garden[x + 1][y] != ".":
                c = "+" if y % 2 else "-"
                new_garden[x] = new_garden[x][:y] + c + new_garden[x][y + 1:]
                break
        for x in range(len(new_garden) - 1, 0, -1):
            if new_garden[x - 1][y] != ".":
                c = "+" if y % 2 else "-"
                new_garden[x] = new_garden[x][:y] + c + new_garden[x][y + 1:]
                break

    # put in the fencing inside gaps within the plants
    for x in range(len(new_garden)):
        for y in range(len(new_garden[0])):
            if new_garden[x][y] != "X": continue
            if new_garden[x - 1][y] == ".":
                new_garden[x - 1] = new_garden[x - 1][:y - 1] + "+-+" + new_garden[x - 1][y + 2:]
            if new_garden[x + 1][y] == ".":
                new_garden[x + 1] = new_garden[x + 1][:y - 1] + "+-+" + new_garden[x + 1][y + 2:]
            if new_garden[x][y - 1] == ".":
                new_garden[x - 1] = new_garden[x - 1][:y - 1] + "+" + new_garden[x - 1][y:]
                new_garden[x] = new_garden[x][:y - 1] + "|" + new_garden[x][y:]
                new_garden[x + 1] = new_garden[x + 1][:y - 1] + "+" + new_garden[x + 1][y:]
            if new_garden[x][y + 1] == ".":
                new_garden[x - 1] = new_garden[x - 1][:y + 1] + "+" + new_garden[x - 1][y + 2:]
                new_garden[x] = new_garden[x][:y + 1] + "|" + new_garden[x][y + 2:]
                new_garden[x + 1] = new_garden[x + 1][:y + 1] + "+" + new_garden[x + 1][y + 2:]

    # count the fences to get the perimeter
    perimeter = 0
    for x in range(len(new_garden)):
        for y in range(len(new_garden[0])):
            if new_garden[x][y] in ["-", "|"]:
                perimeter += 1

    # walk the fence line to count the horizontal sides
    # take the fencing down while we are counting
    sides = 0
    for x in range(1, len(new_garden) - 1):
        for y in range(1, len(new_garden[0]) - 1):
            if new_garden[x][y] == '-':
                sides += 1
                is_below = True if new_garden[x + 1][y] == 'X' else False
                new_garden[x] = new_garden[x][:y - 1] + '..' + new_garden[x][y + 1:]
                for new_y in range(y + 1, len(new_garden[0]) - 1):
                    if new_garden[x][new_y] not in ['+', '-']: break
                    if is_below:
                        if new_garden[x - 1][new_y] == 'X':
                            is_below = False
                            sides += 1
                    else:
                        if new_garden[x + 1][new_y] == 'X':
                            is_below = True
                            sides += 1
                    new_garden[x] = new_garden[x][:new_y] + '.' + new_garden[x][new_y + 1:]

    # walk the fence line to count the vertical sides
    # take the fencing down while we are counting
    for x in range(2, len(new_garden)):
        for y in range(1, len(new_garden[0])):
            if new_garden[x][y] == '|':
                sides += 1
                new_garden[x - 1] = new_garden[x - 1][:y] + '.' + new_garden[x - 1][y + 1:]
                new_garden[x] = new_garden[x][:y] + '.' + new_garden[x][y + 1:]
                for new_x in range(x + 1, len(new_garden) - 1):
                    if new_garden[new_x][y] not in ['+', '|']: break
                    new_garden[new_x] = new_garden[new_x][:y] + '.' + new_garden[new_x][y + 1:]

    return [len(region), perimeter, sides]


def walk_garden(garden, c, x, y):
    if garden[x][y] == c:
        garden[x] = garden[x][:y] + "." + garden[x][y + 1:]
        n = walk_garden(garden, c, x - 1, y)
        e = walk_garden(garden, c, x, y + 1)
        s = walk_garden(garden, c, x + 1, y)
        w = walk_garden(garden, c, x, y - 1)
        return sorted([(x, y)] + n + e + s + w)
    return []


def calculate_using_perimeter(garden):
    regions = []
    for x in range(len(garden)):
        for y in range(len(garden[0])):
            if garden[x][y] != ".":
                regions.append(walk_garden(garden, garden[x][y], x, y))

    total_price = 0
    for region in regions:
        (area, perimeter, sides) = region_size(garden, region)
        price = area * perimeter
        total_price += price

    return total_price


def calculate_using_number_of_sides(garden):
    regions = []
    for x in range(len(garden)):
        for y in range(len(garden[0])):
            if garden[x][y] != ".":
                regions.append(walk_garden(garden, garden[x][y], x, y))

    total_price = 0
    for region in regions:
        (area, perimeter, sides) = region_size(garden, region)
        price = area * sides
        total_price += price

    return total_price


garden = read_stream("12a", transformer, example=True)
total = calculate_using_perimeter(garden)
print(f"Part 1a Example: {total}\t\tIs Correct? {total == 140}")

garden = read_stream("12b", transformer, example=True)
total = calculate_using_perimeter(garden)
print(f"Part 1b Example: {total}\t\tIs Correct? {total == 772}")

garden = read_stream("12c", transformer, example=True)
total = calculate_using_perimeter(garden)
print(f"Part 1c Example: {total}\t\tIs Correct? {total == 1930}")

garden = read_stream("12", transformer, example=False)
total = calculate_using_perimeter(garden)
print(f"Part 1 Actual:   {total}\tIs Correct? {total == 1359028}")

garden = read_stream("12a", transformer, example=True)
total = calculate_using_number_of_sides(garden)
print(f"Part 2a Example: {total}\t\tIs Correct? {total == 80}")

garden = read_stream("12b", transformer, example=True)
total = calculate_using_number_of_sides(garden)
print(f"Part 2b Example: {total}\t\tIs Correct? {total == 436}")

garden = read_stream("12d", transformer, example=True)
total = calculate_using_number_of_sides(garden)
print(f"Part 2c Example: {total}\t\tIs Correct? {total == 236}")

garden = read_stream("12e", transformer, example=True)
total = calculate_using_number_of_sides(garden)
print(f"Part 2d Example: {total}\t\tIs Correct? {total == 368}")

garden = read_stream("12", transformer, example=False)
total = calculate_using_number_of_sides(garden)
print(f"Part 2 Actual:   {total}\t\tIs Correct? {total == 839780}")
