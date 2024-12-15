#!/usr/bin/python3

from utils import read_input
from re import findall
from functools import reduce
from operator import mul


def transformer(line):
    robots = []
    for robot in line.split('\n'):
        [x, y, dx, dy] = findall('-?\\d+', robot)
        robots += (int(x), int(y)), (int(dx), int(dy))
    return robots


def create_lobby(cols, rows):
    lobby = []
    tiles = '.' * cols
    for row in range(rows):
        lobby.append(tiles)
    return lobby


def show_lobby(prefix, lobby):
    for row in range(len(lobby)):
        print(prefix, ''.join(lobby[row]))
    print('')


def add_robot(lobby, p):
    """
    Add a robot to tile 'p' by replacing the tile with the total number of
    robots occupying the tile after placement. An empty tile becomes '1'.
    A tile that had 1 robot on it becomes '2'.
    """
    [x, y] = p
    tile = '1'
    if lobby[y][x] != '.':
        tile = str(int(lobby[y][x]) + 1)
    lobby[y] = lobby[y][:x] + tile + lobby[y][x + 1:]


def remove_robot(lobby, p):
    """
    Remove  a robot from tile 'p' by replacing the tile with the total number
    of robots occupying the tile after removal. A tile that had 2 robots on it
    becomes '1'. A tile that had 1 robot on it becomes '.'.
    """
    [x, y] = p
    tile = '.'
    if lobby[y][x] != '.':
        tile = str(int(lobby[y][x]) - 1)
        if tile == '0': tile = '.'
    lobby[y] = lobby[y][:x] + tile + lobby[y][x + 1:]


def move_robot(lobby, robot):
    """
    Move robot from tile 'p' by a distance of 'v'. If the robot reaches the
    edge of the lobby, it wraps around to the other side of the lobby and
    continues on its path. Return the new robot as a new [p, v] location.
    """
    [max_rows, max_cols] = [len(lobby), len(lobby[0])]
    [x, y] = robot[0]
    [dx, dy] = robot[1]
    new_p = ((x + dx) % max_cols, (y + dy) % max_rows)
    remove_robot(lobby, robot[0])
    add_robot(lobby, new_p)
    return [new_p, robot[1]]


def move_robots(lobby, robots):
    """
    Given a list of robots, move each robot from their current tile to a new
    location based on that robot's velocity.  Return an update list of robots
    with their new positions.
    """
    new_robots = []
    for robot in robots:
        new_robots.append(move_robot(lobby, robot))
    return new_robots


def place_robots(lobby, robots):
    """
    Given a list of robots, place each robot onto a tile in the lobby. Each
    robot is represented by a point and a vector. Only the points are needed
    to place the robots in the lobby.
    """
    for robot in robots:
        p = (int(robot[0][0]), int(robot[0][1]))
        add_robot(lobby, p)


def safety_factor(lobby):
    """
    Divide the lobby into quadrants while ignoring the middle row and column.
    Total up the number of robots found in each quadrant and then multiply each
    quadrants' totals to determine the safety factor of the lobby.
    """
    [max_rows, max_cols] = [len(lobby), len(lobby[0])]
    [quad_rows, quad_cols] = [int(max_rows / 2), int(max_cols / 2)]
    quadrants = []
    for qx, qy in [(0, 0), (1, 0), (0, 1), (1, 1)]:
        quadrant = 0
        for row in range(qy * (1 + quad_rows), qy * (1 + quad_rows) + quad_rows):
            for col in range(qx * (1 + quad_cols), qx * (1 + quad_cols) + quad_cols):
                if lobby[row][col] == '.': continue
                quadrant += int(lobby[row][col])
        quadrants.append(quadrant)
    return(reduce(mul, quadrants))


def is_xmas_tree(lobby, robots):
    """
    Look at the lobby and return True or False if it is believed the robots are
    arranged in a way to form a Christmas Tree. The assumption being made here is
    the tip of the tree forms the center of the tree and each row below expands
    outwards by 1, filled in, forming a triangle.  It should be sufficient to
    only check the top few rows of the tree and have confidence that a tree has
    been found.
    """
    [max_rows, max_cols] = [len(lobby), len(lobby[0])]
    for row in range(max_rows):
        for col in range(max_cols):
            if lobby[row][col] != '.':
                count = 1
                for y in range(row + 1, max_rows):
                    if y > row + 4: break
                    for x in range(col + (row - y), col - (row - y)):
                        if x < 0 or x >= max_cols: break
                        if lobby[y][x] == '.': break
                        count += 1
                if count > 20: return True

    return False


def main():
    robots = read_input('14', transformer, example=True)
    lobby = create_lobby(11, 7)
    place_robots(lobby, robots)
    for seconds in range(100):
        robots = move_robots(lobby, robots)
    total = safety_factor(lobby)
    print(f'Part 1 Example: {total}\t\tIs Correct? {total == 12}')

    robots = read_input('14', transformer, example=False)
    lobby = create_lobby(101, 103)
    place_robots(lobby, robots)
    for seconds in range(100):
        robots = move_robots(lobby, robots)
    total = safety_factor(lobby)
    print(f'Part 1 Actual:  {total}\tIs Correct? {total == 215987200}')

    robots = read_input('14', transformer, example=False)
    lobby = create_lobby(101, 103)
    place_robots(lobby, robots)
    for seconds in range(10000):
        robots = move_robots(lobby, robots)
        if is_xmas_tree(lobby, robots):
            show_lobby('', lobby)
            break
    print(f'Part 2 Actual:  {seconds + 1} seconds\tIs Correct? {seconds + 1 == 8050}')


main()
