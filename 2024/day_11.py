#!/usr/bin/python3

from utils import read_stream
from functools import lru_cache


def transformer(line):
    return [int(l) for l in line.split()]


def blink_iteratively(stones, blinks):
    for b in range(blinks):
        new_stones = []
        for stone in stones:
            if stone == 0:
                new_stones.append(1)
            elif len(str(stone)) % 2 == 0:
                l = int(len(str(stone)) / 2)
                new_stones.append(int(str(stone)[:l]))
                new_stones.append(int(str(stone)[l:]))
            else:
                new_stones.append(stone * 2024)
        stones = new_stones
    return stones


@lru_cache(maxsize=50000)
def blink_recursively(stone, blinks, blink):
    if blink > blinks:
        return 1

    if stone == 0:
        return blink_recursively(1, blinks, blink + 1)
    elif len(str(stone)) % 2 == 0:
        l = int(len(str(stone)) / 2)
        total = 0
        total += blink_recursively(int(str(stone)[:l]), blinks, blink + 1)
        total += blink_recursively(int(str(stone)[l:]), blinks, blink + 1)
        return total
    else:
        return blink_recursively(stone * 2024, blinks, blink + 1)


stones = read_stream('11', transformer, example=True)
total = len(blink_iteratively(stones, 25))
print(f'Part 1 Example:\t{total}\t\tIs Correct? {total == 55312}')

stones = read_stream('11', transformer, example=False)
total = len(blink_iteratively(stones, 25))
print(f'Part 1 Actual:\t{total}\t\tIs Correct? {total == 233050}')

stones = read_stream('11', transformer, example=True)
total = 0
for s in stones:
    total += blink_recursively(s, 25, 1)
print(f'Part 2 Example:\t{total}\t\tIs Correct? {total == 55312}')

stones = read_stream('11', transformer, example=False)
total = 0
for s in stones:
    total += blink_recursively(s, 75, 1)
print(f'Part 2 Actual:\t{total}\tIs Correct? {total == 276661131175807}')
