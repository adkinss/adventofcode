#!/usr/bin/python3

from utils import read_stream
import re


def transformer1(line):
    return re.findall('(mul\\(\\d{1,3},\\d{1,3}\\))', line)


def transformer2(line):
    """
    Simplify regex searching by:
     1. Replace do() and don't() with < and > (single character)
     2. Start the line with < and end the line with >
    This avoids edge cases and doing multiple searches.
    """
    line = re.sub(r'[<>]', '', line)
    line = line.replace('do()', '>')
    line = line.replace('don\'t()', '<')
    line = '>' + line

    results = []
    for section in re.findall('>([^<>]*)', line):
        instructions = re.findall('(mul\\(\\d{1,3},\\d{1,3}\\))', section)
        results += instructions
    return results


def mul(pattern):
    result = re.findall('mul\\((\\d{1,3}),(\\d{1,3})\\)', pattern)
    return int(result[0][0]) * int(result[0][1])


input = read_stream('3a', transformer1, example=True)
total = sum([mul(i) for i in input])
print(f'Part 1 Example:\t{total}\t\tIs Correct? {total == 161}')

input = read_stream('3', transformer1, example=False)
total = sum([mul(i) for i in input])
print(f'Part 1 Actual:\t{total}\tIs Correct? {total == 170778545}')

input = read_stream('3b', transformer2, example=True)
total = sum([mul(i) for i in input])
print(f'Part 2 Example:\t{total}\t\tIs Correct? {total == 48}')

input = read_stream('3', transformer2, example=False)
total = sum([mul(i) for i in input])
print(f'Part 2 Actual:\t{total}\tIs Correct? {total == 82868252}')
