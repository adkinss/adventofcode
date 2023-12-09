#!/usr/bin/python3

from utils import read_input


def transformer1(line):
    """
    Return the score for a given hand based on hand type and order of cards.
    """
    card_map = {
        "2": "M", "3": "L", "4": "K", "5": "J", "6": "I", "7": "H", "8": "G",
        "9": "F", "T": "E", "J": "D", "Q": "C", "K": "B", "A": "A"
    }

    values = []
    for s in line.split('\n'):
        hand, bid = s.split(' ')
        cards = []
        mapping = ""
        for card in hand:
            card_seen_before = False
            for c in cards:
                if card == c[0]:
                    card_seen_before = True
                    c[1] += 1
                    break
            if not card_seen_before:
                cards.append([card, 1])
            mapping += card_map[card]

        num, max = [len(cards), 0]
        for c in cards:
            if c[1] > max:
                max = c[1]

        hand_type = "X"
        if num == 1 and max == 5: hand_type = "A"  # Five of a Kind
        if num == 2 and max == 4: hand_type = "B"  # Four of a Kind
        if num == 2 and max == 3: hand_type = "C"  # Full House
        if num == 3 and max == 3: hand_type = "D"  # Three of a Kind
        if num == 3 and max == 2: hand_type = "E"  # Two Pair
        if num == 4 and max == 2: hand_type = "F"  # One Pair
        if num == 5 and max == 1: hand_type = "G"  # High Card
        mapping = hand_type + mapping

        # print(f"hand:{hand} bid:{bid}\t#cards:{num} max:{max} map:{mapping}")
        # print(f"{mapping} {hand} {bid} {cards}")
        values = [hand, int(bid), mapping]

    return values


def transformer2(line):
    """
    Return the score for a given hand based on hand type and order of cards.
    Treat "J" cards as Jokers and not Jacks that can represent any card.
    When looking at hand type with Jokers present, pick the best hand type that
    can be made using the Jokers. When scoring the cards based on ordering,
    treat the Jokers as the lowest card in the deck.
    """
    card_map = {
        "J": "M", "2": "L", "3": "K", "4": "J", "5": "I", "6": "H", "7": "G",
        "8": "F", "9": "E", "T": "D", "Q": "C", "K": "B", "A": "A"
    }

    values = []
    for s in line.split('\n'):
        hand, bid = s.split(' ')
        cards = []
        mapping = ""
        for card in hand:
            card_seen_before = False
            for c in cards:
                if card == c[0]:
                    card_seen_before = True
                    c[1] += 1
                    break
            if not card_seen_before:
                cards.append([card, 1])
            mapping += card_map[card]

        num, max, jokers = [len(cards), 0, 0]
        for c in cards:
            if c[0] == "J":
                jokers += c[1]
                continue
            if c[1] > max:
                max = c[1]
        if jokers > 0:
            num -= 1

        if num == 1 and max == 5 and jokers == 0: mapping = "A" + mapping  # Five of a Kind
        if num == 2 and max == 4 and jokers == 0: mapping = "B" + mapping  # Four of a Kind
        if num == 2 and max == 3 and jokers == 0: mapping = "C" + mapping  # Full House
        if num == 3 and max == 3 and jokers == 0: mapping = "D" + mapping  # Three of a Kind
        if num == 3 and max == 2 and jokers == 0: mapping = "E" + mapping  # Two Pair
        if num == 4 and max == 2 and jokers == 0: mapping = "F" + mapping  # One Pair
        if num == 5 and max == 1 and jokers == 0: mapping = "G" + mapping  # High Card
        if num == 0 and max == 0 and jokers == 5: mapping = "A" + mapping  # Nothing upgraded to Five of Kind
        if num == 1 and max == 1 and jokers == 4: mapping = "A" + mapping  # High Card upgraded to Five of a Kind
        if num == 1 and max == 2 and jokers == 3: mapping = "A" + mapping  # One Pair upgraded to Five of a Kind
        if num == 1 and max == 3 and jokers == 2: mapping = "A" + mapping  # Three of a Kind upgraded to Five of a Kind
        if num == 1 and max == 4 and jokers == 1: mapping = "A" + mapping  # Four of a Kind upgraded to Five of a Kind
        if num == 2 and max == 1 and jokers == 3: mapping = "B" + mapping  # High Card upgraded to Four of a Kind
        if num == 2 and max == 2 and jokers == 1: mapping = "C" + mapping  # Two Pair upgraded to Full House
        if num == 2 and max == 2 and jokers == 2: mapping = "B" + mapping  # One Pair upgraded to Four of a Kind
        if num == 2 and max == 3 and jokers == 1: mapping = "B" + mapping  # Three of a Kind upgraded to Four of a Kind
        if num == 3 and max == 1 and jokers == 2: mapping = "D" + mapping  # High Card upgraded to Three of a Kind
        if num == 3 and max == 2 and jokers == 1: mapping = "D" + mapping  # One Pair upgraded to Three of a Kind
        if num == 4 and max == 1 and jokers == 1: mapping = "F" + mapping  # High Card upgraded to One Pair

        values = [hand, int(bid), mapping]
    return values


def calculate_total_winnings(input):
    """
    Sort the hands from weakest to strongest hands and then calculate the
    total winnings based on the rank of the hand.
    """
    n = len(input)
    for i in range(n):
        for j in range(n - 1):
            if input[j][2] < input[j + 1][2]:
                input[j], input[j + 1] = input[j + 1], input[j]

    rank = 1
    total_winnings = 0
    for c in input:
        total_winnings += rank * c[1]
        rank += 1

    return total_winnings


input = read_input("7", transformer1, example=True)
total_winnings = calculate_total_winnings(input)
print(f"Part 1 Example: {total_winnings}\tExpecting: 6440")

input = read_input("7", transformer2, example=True)
total_winnings = calculate_total_winnings(input)
print(f"Part 2 Example: {total_winnings}\tExpecting: 5905\n")

input = read_input("7", transformer1, example=False)
total_winnings = calculate_total_winnings(input)
print(f"Part 1: {total_winnings}\tExpecting: 248569531")

input = read_input("7", transformer2, example=False)
total_winnings = calculate_total_winnings(input)
print(f"Part 2: {total_winnings}\tExpecting: 250382098")
