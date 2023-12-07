#!/usr/bin/python3

import re
from utils import read_input


def transformer(line):
    """
    Scan each line and split into a card ID, the winning numbers, and
    the numbers we have.
    Example: "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83"
    """
    values = []
    for s in line.split('\n'):
        id = int(s[5:].split(': ')[0])
        all_numbers = s.split(': ')[1]
        winning_numbers = re.findall(r'\d+', all_numbers.split(' | ')[0])
        my_numbers = re.findall(r'\d+', all_numbers.split(' | ')[1])
        values = [id, winning_numbers, my_numbers]
    return values


def scan_cards(starting_cards):
    """
    For each card, calculate the score from the number of matches from our
    numbers to the winning numbers. Create additional copies of cards based
    on the number of matches found. Return the sum of all the scores and the
    total number of cards we ended up with after making copies.
    """
    # Track how many of each card we have, starting with 1 card each.
    # As we find matches, the number of copies created for each card is
    # added to the existing card count.
    max_cards = len(starting_cards)
    ending_cards = [1] * max_cards

    total_score = 0
    for card in starting_cards:
        id, our_numbers, winning_numbers = card

        # Determine how many of our numbers are in the winning numbers.
        score, matches = [0, 0]
        for o in our_numbers:
            for w in winning_numbers:
                if o == w: matches += 1
        score = 2 ** (matches - 1) if matches else 0
        total_score += score

        # Make copies of cards based on the number of matches we found.
        for i in range(ending_cards[id - 1]):
            c = id
            while c < id + matches and c < max_cards:
                ending_cards[c] += 1
                c += 1

    return [total_score, sum(ending_cards)]


input = read_input("4", transformer, example=True)
total_score, total_cards = scan_cards(input)
print(f"Part 1 Example: {total_score}\tExpecting: 13")
print(f"Part 2 Example: {total_cards}\tExpecting: 30\n")

input = read_input("4", transformer, example=False)
total_score, total_cards = scan_cards(input)
print(f"Part 1: {total_score}\t\tExpecting: 26346")
print(f"Part 2: {total_cards}\t\tExpecting: 8467762")
