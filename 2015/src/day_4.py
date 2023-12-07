#!/usr/bin/python3

from utils import read_input
import hashlib


def transformer1(line):
    """
    Append a number to the input string, starting with 1 and incrementing
    it by 1 each time through the loop. Perform an md5sum on the new string.
    When the md5 hash begins with 5 zero's, return the number appended to
    the string that produced that hash.
    """
    number = 1
    for s in line.split('\n'):
        while True:
            new_s = f"{s}{number}"
            m = hashlib.md5()
            m.update(new_s.encode("utf-8"))
            md5 = m.hexdigest()
            if md5[:5] == "00000": break
            number += 1
    return number


def transformer2(line):
    """
    Append a number to the input string, starting with 1 and incrementing
    it by 1 each time through the loop. Perform an md5sum on the new string.
    When the md5 hash begins with 6 zero's, return the number appended to
    the string that produced that hash.
    """
    number = 1
    for s in line.split('\n'):
        while True:
            new_s = f"{s}{number}"
            m = hashlib.md5()
            m.update(new_s.encode("utf-8"))
            md5 = m.hexdigest()
            if md5[:6] == "000000": break
            number += 1
    return number


input = read_input("4", transformer1, example=True)
expected_answers = [609043, 1048970]
for number in input:
    print(f"Part 1 Example: {number}\tExpecting: {expected_answers.pop(0)}")
print()

input = read_input("4", transformer2, example=True)
expected_answers = [6742839, 5714438]
for number in input:
    print(f"Part 2 Example: {number}\tExpecting: {expected_answers.pop(0)}")
print()

input = read_input("4", transformer1, example=False)
expected_answers = [254575]
for number in input:
    print(f"Part 1: {number}\t\tExpecting: {expected_answers.pop(0)}")

input = read_input("4", transformer2, example=False)
expected_answers = [1038736]
for number in input:
    print(f"Part 2: {number}\t\tExpecting: {expected_answers.pop(0)}")
