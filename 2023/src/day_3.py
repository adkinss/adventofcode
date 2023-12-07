#!/usr/bin/python3

from utils import read_input


def transformer(line):
    values = []
    for s in line.split('\n'):
        for c in s:
            values.append(c)
    return values


def scanner(schematic):
    """
    Scan the schematic looking for valid part numbers and gear ratios.
    Return the sum of valid part numbers and the sum of gear ratios found.
    """
    # Pad the entire schematic with a row and column of ".".
    # This makes it so we don't have to check when we are at the edge for math.
    total_rows = len(input) + 2
    total_cols = len(input[0]) + 2
    for row in schematic:
        row.insert(0, ".")
        row.append(".")
    schematic.insert(0, ["."] * total_cols)
    schematic.append(["."] * total_cols)

    # Keep track of all the valid part numbers we find for Part 1
    # Keep track of each star and its associated numbers for Part 2
    part_numbers = []
    stars = dict()

    # Scan the schematic for all numbers and stars.
    for y in range(total_rows):
        valid_part = False
        star_coords = ""
        number = 0

        for x in range(total_cols):
            c = schematic[y][x]
            if c.isdigit():
                # We found a digit. Grow the number we have with the new digit.
                # Mark the number valid if any digits are neighboring a symbol.
                number = number * 10 + int(c)
                if schematic[y - 1][x - 1] not in ".0123456789": valid_part = True
                if schematic[y - 1][x] not in ".0123456789": valid_part = True
                if schematic[y - 1][x + 1] not in ".0123456789": valid_part = True
                if schematic[y][x - 1] not in ".0123456789": valid_part = True
                if schematic[y][x + 1] not in ".0123456789": valid_part = True
                if schematic[y + 1][x - 1] not in ".0123456789": valid_part = True
                if schematic[y + 1][x] not in ".0123456789": valid_part = True
                if schematic[y + 1][x + 1] not in ".0123456789": valid_part = True

                # If any digit borders a star, save the star's location.
                if schematic[y - 1][x - 1] == "*": star_coords = f"{y-1},{x-1}"
                if schematic[y - 1][x] == "*": star_coords = f"{y-1},{x}"
                if schematic[y - 1][x + 1] == "*": star_coords = f"{y-1},{x+1}"
                if schematic[y][x - 1] == "*": star_coords = f"{y},{x-1}"
                if schematic[y][x + 1] == "*": star_coords = f"{y},{x+1}"
                if schematic[y + 1][x - 1] == "*": star_coords = f"{y+1},{x-1}"
                if schematic[y + 1][x] == "*": star_coords = f"{y+1},{x}"
                if schematic[y + 1][x + 1] == "*": star_coords = f"{y+1},{x+1}"
            else:
                # We landed on a non-digit.
                if number > 0:
                    # This is the first non-digit character after a number.
                    # See if the number is a valid part and save it.
                    # Associate the number with any stars it is bordering.
                    if valid_part:
                        part_numbers.append(number)
                        if star_coords:
                            if star_coords in stars:
                                stars[star_coords].append(number)
                            else:
                                stars[star_coords] = [number]

                    # Reset everything before scanning for another number.
                    valid_part = False
                    star_coords = ""
                    number = 0

    # We are done scanning the schematic.
    # Find all the stars with exactly two numbers and calculate the gear ratio.
    gear_ratios = []
    for star in stars:
        if len(stars[star]) == 2:
            gear_ratios.append(stars[star][0] * stars[star][1])

    return sum(part_numbers), sum(gear_ratios)


input = read_input("3", transformer, example=True)
part_numbers, gear_ratio = scanner(input)
print(f"Part 1 Example: {part_numbers}\tExpecting: 4361")
print(f"Part 2 Example: {gear_ratio}\tExpecting: 467835\n")

input = read_input("3", transformer, example=False)
part_numbers, gear_ratio = scanner(input)
print(f"Part 1: {part_numbers}\t\tExpecting: 550934")
print(f"Part 2: {gear_ratio}\tExpecting: 81997870")
