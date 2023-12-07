#!/usr/bin/python3

from utils import read_input


def transformer(line):
    """
    Each game contains an ID and one or more sets of cubes. Each set of cubes
    may contain one or more cube colors.  For each game, return the game ID,
    whether the game is possible with the cubes we have (12 red cubes, 13 green
    cubes, and 14 blue cubes), and the power of the cubes (maximum number of
    cubes of each color we saw multiplied together).
    Example: "Game 5: 1 red, 2 blue; 4 red, 10 red, 1 green, 5 blue"
    """
    for s in line.split('\n'):
        id = int(s[5:].split(': ')[0])
        left = s.split(': ')[1]

        max_red, max_green, max_blue = [0, 0, 0]
        possible = True

        for group in left.split('; '):
            red, green, blue = [0, 0, 0]

            for cubes in group.split(', '):
                count = int(cubes.split(' ')[0])
                color = cubes.split(' ')[1]
                if color == "red": red += count
                if color == "green": green += count
                if color == "blue": blue += count

            if red > 12 or green > 13 or blue > 14:
                possible = False

            if red > max_red: max_red = red
            if green > max_green: max_green = green
            if blue > max_blue: max_blue = blue

        power = max_red * max_green * max_blue
    return [id, possible, power]


input = read_input("2", transformer, example=True)
total_id, total_power = [0, 0]
for game in input:
    total_power += game[2]
    if game[1]: total_id += game[0]
print(f"Part 1 Example: {total_id}\tExpecting: 8")
print(f"Part 2 Example: {total_power}\tExpecting: 2286\n")

input = read_input("2", transformer, example=False)
total_id, total_power = [0, 0]
for game in input:
    total_power += game[2]
    if game[1]: total_id += game[0]
print(f"Part 1: {total_id}\t\tExpecting: 3059")
print(f"Part 2: {total_power}\t\tExpecting: 65371")
