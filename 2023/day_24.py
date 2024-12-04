#!/usr/bin/python3

from utils import read_input


def transformer(line):
    """
    Input Format: x, y, z @ vx, vy, vz
    """
    [location, vector] = line.split(" @ ")
    [x, y, z] = [int(s) for s in location.split(", ")]
    [vx, vy, vz] = [int(s) for s in vector.split(", ")]
    return (x, y, z), (vx, vy, vz)


def to_line(P1, P2):
    A = P1[1] - P2[1]
    B = P2[0] - P1[0]
    C = P1[0] * P2[1] - P2[0] * P1[1]
    return A, B, -C


def find_intersection(L1, L2):
    D = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return x, y
    return False


def future_paths_inside_test_area(input, min, max, debug):
    future_paths = 0
    for idx, row in enumerate(input):
        [loc1, vec1] = [row[0], row[1]]
        L1 = to_line((loc1[0], loc1[1]), (loc1[0] + vec1[0], loc1[1] + vec1[1]))
        for loc2, vec2 in input[idx + 1:]:
            if debug:
                print(f'Hailstone A: {loc1[0]}, {loc1[1]}, {loc1[2]} @ {vec1[0]}, {vec1[1]}, {vec1[2]}')
                print(f'Hailstone B: {loc2[0]}, {loc2[1]}, {loc2[2]} @ {vec2[0]}, {vec2[1]}, {vec2[2]}')
            L2 = to_line((loc2[0], loc2[1]), (loc2[0] + vec2[0], loc2[1] + vec2[1]))
            R = find_intersection(L1, L2)
            if not R:
                if debug:
                    print('Hailstones\' paths are parallel; they never intersect.\n')
                continue
            hailstone_a = hailstone_b = False
            if vec1[0] < 0 and R[0] > loc1[0]: hailstone_a = True
            if vec1[0] > 0 and R[0] < loc1[0]: hailstone_a = True
            if vec1[1] < 0 and R[1] > loc1[1]: hailstone_a = True
            if vec1[1] > 0 and R[1] < loc1[1]: hailstone_a = True
            if vec2[0] < 0 and R[0] > loc2[0]: hailstone_b = True
            if vec2[0] > 0 and R[0] < loc2[0]: hailstone_b = True
            if vec2[1] < 0 and R[1] > loc2[1]: hailstone_b = True
            if vec2[1] > 0 and R[1] < loc2[1]: hailstone_b = True
            if hailstone_a:
                if debug:
                    if hailstone_b:
                        print('Hailstones\' paths crossed in the past for both hailstones.\n')
                    else:
                        print('Hailstones\' paths crossed in the past for hailstone A.\n')
                continue
            if hailstone_b:
                if debug:
                    print('Hailstones\' paths crossed in the past for hailstone B.\n')
                continue
            crossing = 'paths will cross outside the test area'
            if R[0] >= min and R[0] <= max:
                if R[1] >= min and R[1] <= max:
                    crossing = 'paths will cross inside the test area'
                    future_paths += 1
            if debug:
                print(f'Hailstones\' {crossing} (at x={R[0]:,g}, y={R[1]:,g}).\n')
    return future_paths


input = read_input('24', transformer, example=True)
count = future_paths_inside_test_area(input, 7, 27, False)
print(f'Part 1 Example:\t{count}\tIs Correct? {count == 2}')

input = read_input('24', transformer, example=False)
count = future_paths_inside_test_area(input, 2E14, 4E14, False)
print(f'Part 1 Example:\t{count}\tIs Correct? {count == 19523}')
