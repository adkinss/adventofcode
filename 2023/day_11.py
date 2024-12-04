#!/usr/bin/python3

import copy
from utils import read_input

# Use this flag to display each field as the problem is worked.
DEBUG = False


def transformer(line):
    values = []
    for s in line.split('\n'):
        for c in s:
            values.append(c)
    return values


def display_data(data, title):
    """
    Display the data as a visual grid.
    """
    if not DEBUG:
        return

    print(title)
    print("┏" + ("━" * len(data[0])) + "┓")
    for row in data:
        print("┃", end="")
        for c in range(len(row)):
            if row[c] == ".": print(".", end="")
            else: print(row[c], end="")
        print("┃")
    print("┗" + ("━" * len(data[0])) + "┛")


def expand_data(original_data):
    """
    For every row or column of all dots, insert a duplicate of that row or
    column immediately following the row or column of all dots.  Return the
    new data with the expanded rows and columns.
    """
    # Copy the data first and return the copy.
    data = copy.deepcopy(original_data)

    # First, scan the columns. Go backwards, as that allows us to add new
    # columns on the fly without confusing the loop because of added data.
    max_rows, max_cols = [len(data), len(data[0])]
    for c in range(max_cols - 1, -1, -1):
        all_dots = True
        for r in range(max_rows):
            if data[r][c] != ".":
                all_dots = False
        if all_dots:
            for r in range(max_rows):
                data[r].insert(c + 1, ",")

    # Now, do the rows in a similar manner as the columns. If we added any
    # columns from above, the max_cols will need to be updated.
    max_cols = len(data[0])
    for r in range(max_rows - 1, -1, -1):
        all_dots = True
        for c in range(max_cols):
            if data[r][c] != "." and data[r][c] != ",":
                all_dots = False
        if all_dots:
            data.insert(r + 1, [","] * max_cols)

    return data


def mark_empty_rows_and_columns(original_data):
    """
    For every row or column of all dots, convert the row or column to all commas
    instead. This will make it easier to identify empty rows and columns in the
    future without scanning the entire row or column.  Return the new data with
    the marked empty rows and columns.
    """
    # Copy the data first and return the copy.
    data = copy.deepcopy(original_data)

    # First, scan the columns. Go backwards, as that allows us to add new
    # columns on the fly without confusing the loop because of added data.
    max_rows, max_cols = [len(data), len(data[0])]
    for c in range(max_cols - 1, -1, -1):
        all_dots = True
        for r in range(max_rows):
            if data[r][c] != ".":
                all_dots = False
        if all_dots:
            for r in range(max_rows):
                data[r][c] = ","

    # Now, do the rows in a similar manner as the columns. If we added any
    # columns from above, the max_cols will need to be updated.
    max_cols = len(data[0])
    for r in range(max_rows - 1, -1, -1):
        all_dots = True
        for c in range(max_cols):
            if data[r][c] != "." and data[r][c] != ",":
                all_dots = False
        if all_dots:
            for c in range(max_cols):
                data[r][c] = ","

    return data


def find_all_galaxies(data):
    """
    Find the locations of all the galaxies and return a list of coordinates
    for each galaxy.
    """
    galaxies = []
    max_rows, max_cols = [len(data), len(data[0])]
    for r in range(max_rows):
        for c in range(max_cols):
            if data[r][c] == "#":
                galaxies.append([r, c])
    return galaxies


def find_shortest_distances(original_data):
    """
    Find the locations of all the galaxies in the data and calculate the
    shortest distance between each galaxy. Return the sum of all the shortest
    distances for all the pairs of galaxies.
    """
    # Expand the data by adding new rows and columns after empty ones.
    display_data(original_data, "Original")
    data = expand_data(original_data)
    display_data(data, "Expanded")

    # First, find all the galaxies
    galaxies = find_all_galaxies(data)

    # Pair up the galaxies and find the shortest distance between them.
    shortest_distances = 0
    for g1 in range(len(galaxies)):
        for g2 in range(g1 + 1, len(galaxies)):
            p = [galaxies[g1][0], galaxies[g1][1]]
            q = [galaxies[g2][0], galaxies[g2][1]]

            # Calculate the Manhatton Distance between two points
            d = abs(p[0] - q[0]) + abs(p[1] - q[1])
            shortest_distances += d

    return shortest_distances


def find_shortest_distances_with_expansion(original_data, expansion):
    """
    Find the locations of all the galaxies in the data and calculate the
    shortest distance between each galaxy. If the path crosses an expanded
    row or column, add 1 millin to the coordinate.  Return the sum of all
    the shortest distances for all the pairs of galaxies.
    """
    # Mark the data by replacing empty rows and columns with commas.
    display_data(original_data, "Original")
    data = mark_empty_rows_and_columns(original_data)
    display_data(data, "Marked")

    # First, find all the galaxies
    galaxies = find_all_galaxies(data)

    # Now, look at each galaxy and adjust it for any expansions
    expanded_galaxies = []
    for coord in galaxies:
        [empty_rows, empty_cols] = [0, 0]
        for r in range(coord[0]):
            if data[r][coord[1]] == ",":
                empty_rows += 1
        for c in range(coord[1]):
            if data[coord[0]][c] == ",":
                empty_cols += 1
        new_row = coord[0] + empty_rows * (expansion - 1)
        new_col = coord[1] + empty_cols * (expansion - 1)
        expanded_galaxies.append([new_row, new_col])

    # Pair up the galaxies and find the shortest distance between them.
    shortest_distances = 0
    for g1 in range(len(expanded_galaxies)):
        for g2 in range(g1 + 1, len(expanded_galaxies)):
            p = [expanded_galaxies[g1][0], expanded_galaxies[g1][1]]
            q = [expanded_galaxies[g2][0], expanded_galaxies[g2][1]]

            # Calculate the Manhatton Distance between two points
            d = abs(p[0] - q[0]) + abs(p[1] - q[1])
            shortest_distances += d

    return shortest_distances


data = read_input("11", transformer, example=True)
shortest_distances = find_shortest_distances(data)
print(f"Part 1 Example: {shortest_distances}\tExpecting: 374")

shortest_distances = find_shortest_distances_with_expansion(data, 10)
print(f"Part 2 Example A: {shortest_distances}\tExpecting: 1030")

shortest_distances = find_shortest_distances_with_expansion(data, 100)
print(f"Part 2 Example B: {shortest_distances}\tExpecting: 8410")
print()

data = read_input("11", transformer, example=False)
shortest_distances = find_shortest_distances(data)
print(f"Part 1: {shortest_distances}\t\tExpecting: 9329143")

shortest_distances = find_shortest_distances_with_expansion(data, 1000000)
print(f"Part 2: {shortest_distances}\tExpecting: 710674907809")
