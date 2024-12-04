#!/usr/bin/python3

from functools import reduce
from utils import read_input


def transformer1(line):
    """
    Return the list of numbers found on each line.
    """
    values = []
    for s in line.split('\n'):
        all_numbers = s.split(':')[1]
        values = [int(n) for n in all_numbers.split()]
    return values


def transformer2(line):
    """
    Combine all the numbers on the line into a single larger number
    and return that number as the only element in the list.
    """
    values = []
    for s in line.split('\n'):
        all_numbers = s.split(':')[1].replace(" ", "")
        values = [int(n) for n in all_numbers.split()]
    return values


def find_winners(race_time, record_distance):
    """
    Given the time it takes for the race to complete and the record distance
    seen by other contestants in the race, determine how many races can be won
    by holding the starting button longer, 1ms at a time for each attempt.
    Since the race time can be really long, scan forwards and backwards for the
    first occurrence of the win and then calculate the number of winning games
    by their difference.
    """
    first_winner = 0
    for hold_time in range(1, race_time - 1):
        travel_time = race_time - hold_time
        distance_traveled = hold_time * travel_time
        if distance_traveled > record_distance:
            first_winner = hold_time
            break

    last_winner = 0
    for hold_time in reversed(range(1, race_time - 1)):
        travel_time = race_time - hold_time
        distance_traveled = hold_time * travel_time
        if distance_traveled > record_distance:
            last_winner = hold_time
            break

    return last_winner - first_winner + 1


def multiply(x, y):
    return x * y


input = read_input("6", transformer1, example=True)
winning_races = []
for i in range(len(input[0])):
    winning_races.append(find_winners(input[0][i], input[1][i]))
ways_to_win = reduce(multiply, winning_races)
print(f"Part 1 Example: {ways_to_win}\tExpecting: 288")

input = read_input("6", transformer2, example=True)
winning_races = []
for i in range(len(input[0])):
    winning_races.append(find_winners(input[0][i], input[1][i]))
ways_to_win = reduce(multiply, winning_races)
print(f"Part 2 Example: {ways_to_win}\tExpecting: 71503\n")

input = read_input("6", transformer1, example=False)
winning_races = []
for i in range(len(input[0])):
    winning_races.append(find_winners(input[0][i], input[1][i]))
ways_to_win = reduce(multiply, winning_races)
print(f"Part 1: {ways_to_win}\t\tExpecting: 6209190")

input = read_input("6", transformer2, example=False)
winning_races = []
for i in range(len(input[0])):
    winning_races.append(find_winners(input[0][i], input[1][i]))
ways_to_win = reduce(multiply, winning_races)
print(f"Part 2: {ways_to_win}\tExpecting: 28545089")
