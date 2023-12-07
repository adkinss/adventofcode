#!/usr/bin/python3

from utils import read_input


def transformer1(line):
    """
    Create a map of houses visited by Santa from the directions provided.
    Return the map of houses and number of presents given to each house.
    """
    values = []
    for s in line.split('\n'):
        map = dict()
        map["0,0"] = 1
        x, y = [0, 0]
        for c in s:
            if c == ">": x += 1
            if c == "v": y += 1
            if c == "<": x -= 1
            if c == "^": y -= 1
            if f"{x},{y}" in map: map[f"{x},{y}"] += 1
            else: map[f"{x},{y}"] = 1
        values.append(map)
    return values


def transformer2(line):
    """
    Create a map of houses visited by Santa and Robo-Santa from the directions
    provided. Alternate who is moving with each character read, starting with
    Santa.  Return a map of houses and number of presents given to each house.
    """
    values = []
    for s in line.split('\n'):
        map = dict()
        map["0,0"] = 1
        sx, sy, rx, ry = [0, 0, 0, 0]
        santas_move = 1
        for c in s:
            if santas_move == 1:
                if c == ">": sx += 1
                if c == "v": sy += 1
                if c == "<": sx -= 1
                if c == "^": sy -= 1
                if f"{sx},{sy}" in map: map[f"{sx},{sy}"] += 1
                else: map[f"{sx},{sy}"] = 1
                santas_move = 0
            else:
                if c == ">": rx += 1
                if c == "v": ry += 1
                if c == "<": rx -= 1
                if c == "^": ry -= 1
                if f"{rx},{ry}" in map: map[f"{rx},{ry}"] += 1
                else: map[f"{rx},{ry}"] = 1
                santas_move = 1
        values.append(map)
    return values


input = read_input("3a", transformer1, example=True)
expected_answers = [2, 4, 2]
for trip in input:
    print(f"Part 1 Example: {len(trip[0])}\tExpecting: {expected_answers.pop(0)}")
print()

input = read_input("3b", transformer2, example=True)
expected_answers = [3, 3, 11]
for trip in input:
    print(f"Part 2 Example: {len(trip[0])}\tExpecting: {expected_answers.pop(0)}")
print()

input = read_input("3", transformer1, example=False)
expected_answers = [2572]
for trip in input:
    print(f"Part 1: {len(trip[0])}\t\tExpecting: {expected_answers.pop(0)}")

input = read_input("3", transformer2, example=False)
expected_answers = [2631]
for trip in input:
    print(f"Part 2: {len(trip[0])}\t\tExpecting: {expected_answers.pop(0)}")
