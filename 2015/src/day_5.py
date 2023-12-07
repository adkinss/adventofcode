#!/usr/bin/python3

from utils import read_input


def transformer1(line):
    """
    Examine the line and determine if it is a nice string or a naughty string.
    Nice strings must adhere to all of the following rules:
      1. Contains at least three vowels (aeiou). Repeat vowels are okay.
      2. Contains at least one letter that appears twice in a row.
      3. Does not contain the strings ab, cd, pq or xy.
    Return a 1 if the line is a nice string, or a 0 if it is a naughty string.
    """
    values = []
    for s in line.split('\n'):
        vowels = 0
        prev_c = ""
        double_letter = False
        bad_string = False

        for c in s:
            if c in "aeiou": vowels += 1
            if c == prev_c: double_letter = True
            if c == "b" and prev_c == "a": bad_string = True
            if c == "d" and prev_c == "c": bad_string = True
            if c == "q" and prev_c == "p": bad_string = True
            if c == "y" and prev_c == "x": bad_string = True
            prev_c = c

        result = 1
        if vowels < 3: result = 0
        if not double_letter: result = 0
        if bad_string: result = 0
        values = result

    return values


def transformer2(line):
    """
    Examine the line and determine if it is a nice string or a naughty string.
    Nice strings must adhere to all of the following rules:
      1. Contains a pair of any two letters that appear twice in the string
         without overlapping, like xyxy (xy) or abxaby (ab), but not aaa (aa).
      2. Contains at least one letter which repeats with excatly one letter
         between them, like xyx, abcdefeghi (efe), or even aaa.
    Return a 1 if the line is a nice string, or a 0 if it is a naughty string.
    """
    values = []
    for s in line.split('\n'):
        prev_c = ""
        prev_prev_c = ""
        found_pair = False
        found_repeat = False

        pos = 0
        for c in s:
            if prev_c != "":
                # scan forward to see if there are other pairs
                rest = s[pos + 1:]
                for rest_pos in range(len(rest)):
                    if f"{prev_c}{c}" == rest[rest_pos:rest_pos + 2]:
                        found_pair = True
                        break
            if prev_prev_c == c:
                found_repeat = True
            prev_prev_c = prev_c
            prev_c = c
            pos += 1

        result = 0
        if found_pair and found_repeat: result = 1
        values = result

    return values


input = read_input("5a", transformer1, example=True)
total = sum(input)
print(f"Part 1 Example: {total}\tExpecting: 2")

input = read_input("5b", transformer2, example=True)
total = sum(input)
print(f"Part 2 Example: {total}\tExpecting: 2")
print()

input = read_input("5", transformer1, example=False)
total = sum(input)
print(f"Part 1: {total}\t\tExpecting: 238")

input = read_input("5", transformer2, example=False)
total = sum(input)
print(f"Part 2: {total}\t\tExpecting: 69")
