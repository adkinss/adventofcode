#!/usr/bin/python3

import copy
import sys
from utils import read_input

# Use this flag to display each field as the problem is worked.
DEBUG = False


def transformer(line):
    values = []
    for s in line.split('\n'):
        for c in s:
            values.append(c)
    return values


def display_all_fields(field_list, title_list):
    """
    Display each field as a visual map side by side. All the fields need to be
    the same size. No validation is done to confirm sizing.
    """
    if not DEBUG:
        return

    num_fields = len(field_list)
    num_rows = len(field_list[0])
    num_cols = len(field_list[0][0])

    print()
    for f in range(num_fields):
        title = title_list[f]
        formatted_title = title + " " * (num_cols + 2)
        print(f"{formatted_title[:num_cols+2]}  ", end="")
    print()

    for f in range(num_fields):
        field = field_list[f]
        print("┏" + ("━" * num_cols) + "┓  ", end="")
    print()

    for r in range(num_rows):
        for f in range(num_fields):
            field = field_list[f]
            print("┃", end="")
            for c in range(num_cols):
                row = field[r]
                if row[c] == ".": print(" ", end="")
                else: print(row[c], end="")
            print("┃  ", end="")
        print()

    for f in range(num_fields):
        field = field_list[f]
        print("┗" + ("━" * num_cols) + "┛  ", end="")
    print()
    print()


def display_single_field(field, title):
    """
    Display the field as a visual map.
    """
    if not DEBUG:
        return

    print(title)
    print("┏" + ("━" * len(field[0])) + "┓")
    for row in field:
        print("┃", end="")
        for c in range(len(row)):
            if row[c] == ".": print(" ", end="")
            else: print(row[c], end="")
        print("┃")
    print("┗" + ("━" * len(field[0])) + "┛")


def zoom_in(field):
    """
    Create a new zoomed in field from the one provided. Connect pipes as
    approprate so that there are no gaps after zooming in.
    """
    max_rows = len(field)
    max_cols = len(field[0])

    new_max_rows = 2 * max_rows - 1
    new_max_cols = 2 * max_cols - 1

    # Initialize a bigger field.
    zoom_field = []
    for r in range(new_max_rows):
        zoom_field.append(["."] * (new_max_cols))

    for r in range(max_rows):
        for c in range(max_cols):
            this_pipe = field[r][c]
            zoom_field[2 * r][2 * c] = this_pipe
            if this_pipe == "-":
                if 2 * c - 1 >= 0:
                    zoom_field[2 * r][2 * c - 1] = "-"
                if 2 * c + 1 < new_max_cols:
                    zoom_field[2 * r][2 * c + 1] = "-"
            if this_pipe == "|":
                if 2 * r - 1 >= 0:
                    zoom_field[2 * r - 1][2 * c] = "|"
                if 2 * r + 1 < new_max_rows:
                    zoom_field[2 * r + 1][2 * c] = "|"
            if this_pipe == "F":
                if 2 * c + 1 < new_max_cols:
                    zoom_field[2 * r][2 * c + 1] = "-"
                if 2 * r + 1 < new_max_rows:
                    zoom_field[2 * r + 1][2 * c] = "|"
            if this_pipe == "7":
                if 2 * c - 1 >= 0:
                    zoom_field[2 * r][2 * c - 1] = "-"
                if 2 * r + 1 < new_max_rows:
                    zoom_field[2 * r + 1][2 * c] = "|"
            if this_pipe == "J":
                if 2 * r - 1 >= 0:
                    zoom_field[2 * r - 1][2 * c] = "|"
                if 2 * c - 1 >= 0:
                    zoom_field[2 * r][c * 2 - 1] = "-"
            if this_pipe == "L":
                if 2 * r - 1 >= 0:
                    zoom_field[2 * r - 1][2 * c] = "|"
                if 2 * c + 1 < new_max_cols:
                    zoom_field[2 * r][2 * c + 1] = "-"

    return zoom_field


def find_start(field):
    """
    Return the coordinates of the starting location marked with an "S".
    """
    for row in range(len(field)):
        for col in range(len(field[row])):
            if field[row][col] == "S":
                return row, col
    return -1, -1


def find_pipe_entries(field, row, col):
    """
    Return a list containing the coordinates of the two entrances for the
    given pipe. Valid pipes include the following: S, -, |, F, 7, J, L
    """
    # Figure out what pipe we are in
    this_pipe = field[row][col]
    if this_pipe == "-": return [row, col - 1], [row, col + 1]
    if this_pipe == "|": return [row - 1, col], [row + 1, col]
    if this_pipe == "F": return [row, col + 1], [row + 1, col]
    if this_pipe == "7": return [row, col - 1], [row + 1, col]
    if this_pipe == "J": return [row - 1, col], [row, col - 1]
    if this_pipe == "L": return [row - 1, col], [row, col + 1]

    # We aren't in a pipe. This is bad, mmm'kay?
    if this_pipe != "S":
        return []

    # We are on the starting pipe, so we don't know the real pipe we are in.
    # Probe around us for valid pipes that could come into this one.
    coords = []
    if row > 0 and field[row - 1][col] in "F|7":
        coords.append([row - 1, col])
    if col < len(field[row]) - 1 and field[row][col + 1] in "7-J":
        coords.append([row, col + 1])
    if row < len(field) - 1 and field[row + 1][col] in "L|J":
        coords.append([row + 1, col])
    if col > 0 and field[row][col - 1] in "L-F":
        coords.append([row, col - 1])
    return coords[0], coords[1]


def travel_pipes(field):
    """
    Find the starting pipe where we begin travel. Find the entry points for it and
    move in one of those directions. From the new pipe, find its entry points and
    move in a direction that we weren't just at. Continue doing this until we get
    back to the starting pipe and return the number of pipes seen while traveling.
    """
    # Look for the pipe we will start from and then entries to that pipe.
    row, col = find_start(field)
    coords = find_pipe_entries(field, row, col)

    # Start with the next pipe and travel until we get back to the starting
    # pipe. Keep track of where we have been so we don't go backwards.
    prev_row, prev_col = row, col
    row, col = coords[0]
    total_pipes = 1
    while field[row][col] != "S":
        coords = find_pipe_entries(field, row, col)
        next_row, next_col = coords[0]
        if next_row == prev_row and next_col == prev_col:
            next_row, next_col = coords[1]
        prev_row, prev_col = row, col
        row, col = next_row, next_col
        total_pipes += 1

    return total_pipes


def remove_junk(field):
    """
    Assuming the pipe loop on the field was converted to some other character,
    such as an "X", any other pipes in the field must be junk. Find all the
    junk pipes and convert them to an empty location.
    """
    new_field = copy.deepcopy(field)
    for r in range(len(field)):
        for c in range(len(field[0])):
            if new_field[r][c] != "x":
                new_field[r][c] = "."
    return new_field


def mark_pipe_loop(field):
    """
    With the given field, return a new field where all the locations of the loop
    are marked with an "x" and all the locations that are obviously outside the
    loop are marked with an "O".
    """
    new_field = copy.deepcopy(field)

    # Look for the pipe we will start from and then entries to that pipe.
    starting_row, starting_col = find_start(field)
    coords = find_pipe_entries(new_field, starting_row, starting_col)
    new_field[starting_row][starting_col] = "x"

    # Start with the next pipe and travel until we get back to the starting
    # pipe. Keep track of where we have been so we don't go backwards.
    prev_row, prev_col = starting_row, starting_col
    row, col = coords[0]
    while field[row][col] != "S":
        new_field[row][col] = "x"
        coords = find_pipe_entries(field, row, col)
        next_row, next_col = coords[0]
        if next_row == prev_row and next_col == prev_col:
            next_row, next_col = coords[1]
        prev_row, prev_col = row, col
        row, col = next_row, next_col

    return new_field


def mark_outside(field, r, c):
    """
    Given a row and column in a field, recursively look around the current
    location and mark it as an outside location if it is an empty space.
    """
    # We landed on a filled space. We are done.
    if field[r][c] != ".":
        return

    # Mark the current location as an outside location.
    field[r][c] = "O"

    # Look around the current location for an empty space and go check it.
    if c > 0 and field[r][c - 1] == ".":
        mark_outside(field, r, c - 1)
    if c < len(field[0]) - 1 and field[r][c + 1] == ".":
        mark_outside(field, r, c + 1)
    if r > 0 and field[r - 1][c] == ".":
        mark_outside(field, r - 1, c)
    if r < len(field) - 1 and field[r + 1][c] == ".":
        mark_outside(field, r + 1, c)

    # Look diagonally too.
    if c > 0 and r > 0 and field[r - 1][c - 1] == ".":
        mark_outside(field, r - 1, c - 1)
    if c > 0 and r < len(field) - 1 and field[r + 1][c - 1] == ".":
        mark_outside(field, r + 1, c - 1)
    if c < len(field[0]) - 1 and r > 0 and field[r - 1][c + 1] == ".":
        mark_outside(field, r - 1, c + 1)
    if c < len(field[0]) - 1 and r < len(field) - 1 and field[r + 1][c + 1] == ".":
        mark_outside(field, r + 1, c + 1)

    # There's nothing empty around this location. We are done.
    return


def count_inner_tiles(field):
    """
    Determine the number of inner tiles that exist inside the pipe loop. This
    requires a few iterations to make it work. First, the field needs to be
    zoomed in so that it is easier to see what is inside the loop vs outside
    the loop. Then the pipe loop needs to be converted to all X's so all the
    junk pipes can be removed. Once the junk is removed, convert the X's back
    to the original pipe characters, though this isn't necessary. Then scan
    all locations and mark the outside locations with O's. Finally, mark the
    inside locations with I's and return how many were found.
    """
    # Zoom in on the field so it is easier to see what's inside vs outside.
    zoomed_in_field = zoom_in(field)
    max_rows = len(zoomed_in_field)
    max_cols = len(zoomed_in_field[0])

    # Convert the pipes to X's to make it easier to find the junk.
    x_field = mark_pipe_loop(zoomed_in_field)

    # Remove the junk pipes laying around the field.
    junk_free_field = remove_junk(x_field)

    # Now convert the "X's back into the original pipe.
    for r in range(max_rows):
        for c in range(max_cols):
            if junk_free_field[r][c] == "x":
                junk_free_field[r][c] = zoomed_in_field[r][c]

    # Make a copy of the junk-free field to do the rest of the work on.
    outside_field = copy.deepcopy(junk_free_field)

    # Scan the outside border for any empty fields and use that to scan for
    # all neighboring locations, marking all locations as outside locations
    # where appropriate.
    for c in range(max_cols):
        if outside_field[0][c] == ".":
            mark_outside(outside_field, 0, c)
        last_row = max_rows - 1
        if outside_field[last_row][c] == ".":
            mark_outside(outside_field, last_row, c)
    for r in range(1, max_rows - 1):
        if outside_field[r][0] == ".":
            mark_outside(outside_field, r, 0)
        last_col = max_cols - 1
        if outside_field[r][last_col] == ".":
            mark_outside(outside_field, r, last_col)

    # Count the number of inner tiles. Keep in mind we are zoomed in, so
    # we only want to count the tiles on even locations.
    inner_tiles = 0
    for r in range(max_rows):
        for c in range(max_cols):
            if r % 2 == 0 and c % 2 == 0:
                if outside_field[r][c] == ".":
                    outside_field[r][c] = "I"
                    inner_tiles += 1

    if max_rows <= 20:
        display_single_field(field, "Input")
        display_all_fields([zoomed_in_field, x_field, junk_free_field, outside_field], ["Zoomed", "Masked", "Decluttered", "Output"])
    else:
        display_single_field(field, "Input")
        display_single_field(zoomed_in_field, "Zoomed")
        display_single_field(outside_field, "Final")

    return inner_tiles


# The field size is big enough that we hit the recursion limit for Python,
# which defaults to 1000. Based on the input file provided, 20k seems to be
# big enough to handle our needs.
sys.setrecursionlimit(20000)

field = read_input("10a", transformer, example=True)
farthest_pipe = int(travel_pipes(field) / 2)
print(f"Part 1 Example A: {farthest_pipe}\tExpecting: 4")

field = read_input("10b", transformer, example=True)
farthest_pipe = int(travel_pipes(field) / 2)
print(f"Part 1 Example B: {farthest_pipe}\tExpecting: 8")
print()

field = read_input("10c", transformer, example=True)
inner_tiles = count_inner_tiles(field)
print(f"Part 2 Example C: {inner_tiles}\tExpecting: 4")

field = read_input("10d", transformer, example=True)
inner_tiles = count_inner_tiles(field)
print(f"Part 2 Example D: {inner_tiles}\tExpecting: 4")

field = read_input("10e", transformer, example=True)
inner_tiles = count_inner_tiles(field)
print(f"Part 2 Example E: {inner_tiles}\tExpecting: 8")

field = read_input("10f", transformer, example=True)
inner_tiles = count_inner_tiles(field)
print(f"Part 2 Example F: {inner_tiles}\tExpecting: 10")
print()

field = read_input("10", transformer, example=False)
farthest_pipe = int(travel_pipes(field) / 2)
print(f"Part 1: {farthest_pipe}\t\tExpecting: 6856")

field = read_input("10", transformer, example=False)
inner_tiles = count_inner_tiles(field)
print(f"Part 2: {inner_tiles}\t\tExpecting: 501")
