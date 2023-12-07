#!/usr/bin/python3

from utils import read_input

numbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def transformer1(line):
    """
    Scan the line for the first and last digits and return that as a number.
    Example: "twone3four5twone" returns 35
    """
    values = []
    for s in line.split('\n'):
        value = 0
        for c in s:
            if c.isdigit():
                value = int(c) * 10
                break
        for c in s[::-1]:
            if c.isdigit():
                value += int(c)
                break
        values.append(value)
    return values


def transformer2(line):
    """
    Scan the line for the first and last digits and return that as a number.
    Digits can either be numeric or spelled out. Backward scans should look for
    spelled out digits in reverse form (i.e. 1 would be "eno").
    Example: "twone3four5twone" returns 21
    """
    values = []
    for forward_s in line.split('\n'):
        backward_s = forward_s[::-1]
        value = 0

        new_forward_s = ""
        i = 0
        while i < len(forward_s):
            found = False
            for n in numbers:
                if forward_s[i:i + len(n)] == n:
                    found = True
                    new_forward_s += str(numbers.index(n) + 1)
                    i += len(n)
                    break
            if not found:
                new_forward_s += forward_s[i]
                i += 1

        for c in new_forward_s:
            if c.isdigit():
                value = int(c) * 10
                break

        new_backward_s = ""
        i = 0
        while i < len(backward_s):
            found = False
            for n in numbers:
                if backward_s[i:i + len(n)] == n[::-1]:
                    found = True
                    new_backward_s += str(numbers.index(n) + 1)
                    i += len(n)
                    break
            if not found:
                new_backward_s += backward_s[i]
                i += 1
        backward_s = backward_s[::-1]

        for c in new_backward_s:
            if c.isdigit():
                value += int(c)
                break

        values.append(value)
    return values


input = read_input("1a", transformer1, example=True)
total = sum(sum(v) for v in input)
print(f'Part 1 Example: {total}\tExpecting: 142')
print()

input = read_input("1b", transformer2, example=True)
total = sum(sum(v) for v in input)
print(f'Part 2 Example: {total}\tExpecting: 281')

input = read_input("1c", transformer2, example=True)
total = sum(sum(v) for v in input)
print(f'Part 2 Example: {total}\tExpecting: 1132\n')

input = read_input("1", transformer1)
total = sum(sum(v) for v in input)
print(f'Part 1: {total}\t\tExpecting: 54632')

input = read_input("1", transformer2)
total = sum(sum(v) for v in input)
print(f'Part 2: {total}\t\tExpecting: 54019')
