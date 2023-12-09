#!/usr/bin/python3

import math
from utils import read_multisection_input


def transformer(line):
    """
    Return the first multiline section as a string that represents the
    instructions to be followed when stepping through the network.  Return
    the second multiline section as a dictionary representing the network
    of nodes and the steps to be taken if going left or right.
    """
    network = {}
    for s in line.split('\n'):
        if s == "": continue
        if s[4:5] != "=": return s

        if s[4:5] == "=":
            node, left, right = s[0:3], s[7:10], s[12:15]
            network[node] = [left, right]

    return network


def walk_map_for_people(map):
    """
    Using starting location "AAA", walk the map by taking steps based on the
    instructions provided. Instructions are a combination of L & R representing
    the left or right values of each location. When the instructions run out,
    repeat the instructions until an ending location has been found. When the
    location is "ZZZ", return the number of steps it took to get there.
    """
    instructions = map[0]
    network = map[1]

    step_count = 0
    location = "AAA"
    while location != "ZZZ":
        for step in instructions:
            if step == "L": location = network[location][0]
            if step == "R": location = network[location][1]
            step_count += 1
            if location == "ZZZ": break

    return step_count


def walk_map_for_ghosts(map):
    """
    Compile a list of locations that end in "A" and use those as starting
    locations, then walk the map by taking steps on all locations at the same
    time based on the instructions provided. Instructions are a combination
    of L & R representing the left or right values of each location. When the
    instructions run out, repeat the instructions until an ending location
    has been found. When the location is "ZZZ", return the number of steps it
    took to get there.
    """
    instructions = map[0]
    network = map[1]

    # Compile a list of all locations that end in "A".
    locations = []
    for key in network:
        if key[2:3] == "A":
            locations.append(key)

    # It would take too long to walk all the locations at the same time until
    # all of them ended at the same time. Instead, determine the step count for
    # each of the starting locations and then take the least common multiple
    # of all the step counts to determine the final step count.
    step_counts = []
    for starting_location in locations:
        step_count = 0
        location = starting_location
        while location[2:3] != "Z":
            for step in instructions:
                if step == "L": location = network[location][0]
                if step == "R": location = network[location][1]
                step_count += 1
                if location[2:3] == "Z":
                    step_counts.append(step_count)
                    break

    # Calculate the least common multiple of the step counts.
    return math.lcm(*step_counts)


map = read_multisection_input("8a", transformer, example=True)
steps = walk_map_for_people(map)
print(f"Part 1 Example A: {steps}\tExpecting: 2")

map = read_multisection_input("8b", transformer, example=True)
steps = walk_map_for_people(map)
print(f"Part 1 Example B: {steps}\tExpecting: 6")

map = read_multisection_input("8c", transformer, example=True)
steps = walk_map_for_ghosts(map)
print(f"Part 2 Example C: {steps}\tExpecting: 6")
print()

map = read_multisection_input("8", transformer, example=False)
steps = walk_map_for_people(map)
print(f"Part 1: {steps}\t\tExpecting: 24253")

map = read_multisection_input("8", transformer, example=False)
steps = walk_map_for_ghosts(map)
print(f"Part 1: {steps}\tExpecting: 12357789728873")
