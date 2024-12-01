#!/usr/bin/python3

from utils import read_input


def transformer(line):
    """
    Scan the line and return both numbers found.
    Example: "3   4" returns 3 and 4
    """
    return line.split()


input = read_input("1", transformer, example=True)
first = sorted([i[0] for i in input])
last = sorted([i[1] for i in input])
[distance_p1, similarity_p1] = [0, 0]
for idx, f in enumerate(first):
    distance_p1 += abs(int(f) - int(last[idx]))
    count = 0
    for l in last:
        if f == l:
            count += 1
    similarity_p1 += int(f) * count

input = read_input("1", transformer, example=False)
first = sorted([i[0] for i in input])
last = sorted([i[1] for i in input])
[distance_p2, similarity_p2] = [0, 0]
for idx, f in enumerate(first):
    distance_p2 += abs(int(f) - int(last[idx]))
    count = 0
    for l in last:
        if f == l:
            count += 1
    similarity_p2 += int(f) * count

print(f'Part 1 Example:\t{distance_p1}\t\tExpecting: 11\t\tIs Correct? {distance_p1 == 11}')
print(f'Part 1 Actual:\t{distance_p2}\t\tExpecting: 1879048\tIs Correct? {distance_p2 == 1879048}')
print(f'Part 2 Example:\t{similarity_p1}\t\tExpecting: 31\t\tIs Correct? {similarity_p1 == 31}')
print(f'Part 2 Actual:\t{similarity_p2}\tExpecting: 21024792\tIs Correct? {similarity_p2 == 21024792}')
