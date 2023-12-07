#!/usr/bin/python3

from utils import read_input


def transformer(line):
    """
    Calculate how much wrapping paper and ribbon is needed based on the
    size of each present.
    """
    values = []
    for s in line.split('\n'):
        l = int(s.split("x")[0])
        w = int(s.split("x")[1])
        h = int(s.split("x")[2])

        # Calculate how much wrapping paper is needed based on the surface
        # area. Add a little extra wrapping paper based on the smallest side.
        surface_area = 2 * l * w + 2 * w * h + 2 * h * l
        smallest_side = l * w
        if w * h < smallest_side: smallest_side = w * h
        if h * l < smallest_side: smallest_side = h * l
        values.append(surface_area + smallest_side)

        # Calculate how much ribbon is needed based on the smallest perimeter.
        smallest_perimeter = l + l + w + w
        if w + w + h + h < smallest_perimeter: smallest_perimeter = w + w + h + h
        if h + h + l + l < smallest_perimeter: smallest_perimeter = h + h + l + l
        values.append(smallest_perimeter + l * w * h)
    return values


presents = read_input("2", transformer, example=True)
wrapping_paper = sum(p[0] for p in presents)
ribbon = sum(p[1] for p in presents)
expected_answers = [101, 48]
print(f"Part 1 Example: {wrapping_paper}\tExpecting: {expected_answers.pop(0)}")
print(f"Part 2 Example: {ribbon}\tExpecting: {expected_answers.pop(0)}")
print()

presents = read_input("2", transformer, example=False)
wrapping_paper = sum(p[0] for p in presents)
ribbon = sum(p[1] for p in presents)
print(f"Part 1: {wrapping_paper}\t\tExpecting: 1588178")
print(f"Part 2: {ribbon}\t\tExpecting: 3783758")
