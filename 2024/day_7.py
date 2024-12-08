#!/usr/bin/python3

from utils import read_input


def transformer(line):
    [test_value, equation] = line.split(': ')
    numbers = [int(n) for n in equation.split()]
    return [int(test_value), numbers]


def binary(num):
    return bin(num)[2:]


def ternary(num):
    quotient = num / 3
    remainder = num % 3
    if quotient == 0:
        return ''
    return ternary(int(quotient)) + str(int(remainder))


def calculation_matches(test_value, equation):
    total = equation[0]
    for pos in range(1, len(equation) - 1):
        if equation[pos] == '0':
            total *= equation[pos + 1]
        elif equation[pos] == '1':
            total += equation[pos + 1]
        elif equation[pos] == '2':
            total = int(str(total) + str(equation[pos + 1]))
        if total > test_value:
            return False

    if total == test_value:
        return True
    return False


def callibrate_simple(operation):
    [test_value, numbers] = operation

    max_len = len(numbers) - 1
    for i in range(2 ** (len(numbers) - 1)):
        ops = binary(i)
        ops = ops.rjust(max_len, '0')
        equation = numbers + list(ops)
        equation[::2] = numbers
        equation[1::2] = list(ops)
        if calculation_matches(test_value, equation):
            return test_value

    return 0


def callibrate_complex(operation):
    [test_value, numbers] = operation

    max_len = len(numbers) - 1
    for i in range(3 ** (len(numbers) - 1)):
        ops = ternary(i)
        ops = ops.rjust(max_len, '0')
        equation = numbers + list(ops)
        equation[::2] = numbers
        equation[1::2] = list(ops)
        if calculation_matches(test_value, equation):
            return test_value

    return 0


input = read_input('7', transformer, example=True)
total = 0
for i in input:
    total += callibrate_simple(i)
print(f'Part 1 Example:\t{total}\t\tIs Correct? {total == 3749}')

input = read_input('7', transformer, example=False)
total = 0
for i in input:
    total += callibrate_simple(i)
print(f'Part 1 Actual:\t{total}\tIs Correct? {total == 12940396350192}')

input = read_input('7', transformer, example=True)
total = 0
for i in input:
    total += callibrate_complex(i)
print(f'Part 2 Example:\t{total}\t\tIs Correct? {total == 11387}')

input = read_input('7', transformer, example=False)
total = 0
for i in input:
    total += callibrate_complex(i)
print(f'Part 2 Actual:\t{total}\tIs Correct? {total == 106016735664498}')
