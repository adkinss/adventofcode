#!/usr/bin/python3

from utils import read_multisection_input


def transformer(section):
    return section.rstrip()


def page_ordering(section):
    rules = {}
    for line in section.split('\n'):
        [before, after] = line.split('|')
        if after not in rules:
            rules[after] = []
        rules[after].append(before)
    return rules


def updates_already_in_order(rules, updates):
    total = 0
    for update in updates.split('\n'):
        pages = update.split(',')
        is_already_in_order = True
        for current in range(len(pages)):
            if pages[current] in rules:
                for p in pages[current + 1:]:
                    if p in rules[pages[current]]:
                        is_already_in_order = False
                        break
        if is_already_in_order:
            middle = pages[int(len(pages) / 2)]
            total += int(middle)
    return total


def fix_incorrectly_ordered_updates(rules, updates):
    total = 0
    for update in updates.split('\n'):
        pages = update.split(',')
        is_already_in_order = True
        while True:
            ordering_has_been_fixed = True
            for current in range(len(pages)):
                if pages[current] in rules:
                    for p in pages[current + 1:]:
                        if p in rules[pages[current]]:
                            is_already_in_order = False
                            new_pages = []
                            for x in pages:
                                if x == pages[current]:
                                    new_pages.append(p)
                                    new_pages.append(pages[current])
                                elif x != p:
                                    new_pages.append(x)
                            pages = new_pages
                            is_already_in_order = False
                            ordering_has_been_fixed = False
                            break
            if ordering_has_been_fixed:
                if not is_already_in_order:
                    middle = pages[int(len(pages) / 2)]
                    total += int(middle)
                break
    return total


input = read_multisection_input('5', transformer, example=True)
rules = page_ordering(input[0])
total = updates_already_in_order(rules, input[1])
print(f'Part 1 Example:\t{total}\tIs Correct? {total == 143}')

input = read_multisection_input('5', transformer, example=False)
rules = page_ordering(input[0])
total = updates_already_in_order(rules, input[1])
print(f'Part 1 Actual:\t{total}\tIs Correct? {total == 5329}')

input = read_multisection_input('5', transformer, example=True)
rules = page_ordering(input[0])
total = fix_incorrectly_ordered_updates(rules, input[1])
print(f'Part 2 Example:\t{total}\tIs Correct? {total == 123}')

input = read_multisection_input('5', transformer, example=False)
rules = page_ordering(input[0])
total = fix_incorrectly_ordered_updates(rules, input[1])
print(f'Part 2 Actual:\t{total}\tIs Correct? {total == 5833}')
