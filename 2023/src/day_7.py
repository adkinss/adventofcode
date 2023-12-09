#!/usr/bin/python3

from utils import read_input


def transformer(line):
    """
    Convert the hand to a list of cards and how many of each card was seen.
    Return the hand, bid and the list of cards and counts that were found.
    """
    cards = []
    for s in line.split('\n'):
        hand, bid = s.split(' ')
        for card in hand:
            card_seen_before = False
            for c in cards:
                if card == c[0]:
                    card_seen_before = True
                    c[1] += 1
                    break
            if not card_seen_before:
                cards.append([card, 1])

    return [hand, int(bid), cards]


def hand_strength(hand):
    """
    Given a list of cards, calculate the strength of the cards based on hand
    type (Five of a Kind, Four of a Kind, Full House, etc) and ordering of
    cards. Return a string that can be used as a ranking when comparing this
    hand with other hands.
    """
    # Jokers will be represented as "*" and considered worse than a "2".
    card_map = {
        "*": "N", "2": "M", "3": "L", "4": "K", "5": "J", "6": "I", "7": "H",
        "8": "G", "9": "F", "T": "E", "J": "D", "Q": "C", "K": "B", "A": "A"
    }

    # Convert each card in the card string to a mapping that will make it
    # easier to sort cards later. This represents the strength of the hand.
    strength = ""
    for card in hand[0]:
        strength += card_map[card]

    # Count the number of unique cards, the maximum number of cards we see
    # within each unique card, and the number of jokers. Exclude Jokers from
    # the unique cards and max number counts. For example, *AABC gives us
    # 3 unique cards, a maximum of 2 cards (the two A's) and two Jokers.
    num, max, jokers = [len(hand[2]), 0, 0]
    for c in hand[2]:
        if c[0] == "*":
            jokers += c[1]
            continue
        if c[1] > max:
            max = c[1]
    if jokers > 0:
        num -= 1

    # Determine the rank of the hand without Jokers.
    if num == 1 and max == 5 and jokers == 0: strength = "A" + strength  # AAAAA - Five of a Kind
    if num == 2 and max == 4 and jokers == 0: strength = "B" + strength  # AAAAB - Four of a Kind
    if num == 2 and max == 3 and jokers == 0: strength = "C" + strength  # AAABB - Full House
    if num == 3 and max == 3 and jokers == 0: strength = "D" + strength  # AAABC - Three of a Kind
    if num == 3 and max == 2 and jokers == 0: strength = "E" + strength  # AABBC - Two Pair
    if num == 4 and max == 2 and jokers == 0: strength = "F" + strength  # AABCD - One Pair
    if num == 5 and max == 1 and jokers == 0: strength = "G" + strength  # ABCDE - High Card

    # Determine the best rank possible when Jokers are present.
    if num == 0 and max == 0 and jokers == 5: strength = "A" + strength  # ***** - Jokers upgraded to Five of Kind
    if num == 1 and max == 1 and jokers == 4: strength = "A" + strength  # ****A - High Card upgraded to Five of a Kind
    if num == 1 and max == 2 and jokers == 3: strength = "A" + strength  # ***AA - One Pair upgraded to Five of a Kind
    if num == 1 and max == 3 and jokers == 2: strength = "A" + strength  # **AAA - Three of a Kind upgraded to Five of a Kind
    if num == 1 and max == 4 and jokers == 1: strength = "A" + strength  # *AAAA - Four of a Kind upgraded to Five of a Kind
    if num == 2 and max == 1 and jokers == 3: strength = "B" + strength  # ***AB - High Card upgraded to Four of a Kind
    if num == 2 and max == 2 and jokers == 1: strength = "C" + strength  # *AABB - Two Pair upgraded to Full House
    if num == 2 and max == 2 and jokers == 2: strength = "B" + strength  # **AAB - One Pair upgraded to Four of a Kind
    if num == 2 and max == 3 and jokers == 1: strength = "B" + strength  # *AAAB - Three of a Kind upgraded to Four of a Kind
    if num == 3 and max == 1 and jokers == 2: strength = "D" + strength  # **ABC - High Card upgraded to Three of a Kind
    if num == 3 and max == 2 and jokers == 1: strength = "D" + strength  # *AABC - One Pair upgraded to Three of a Kind
    if num == 4 and max == 1 and jokers == 1: strength = "F" + strength  # *ABCD - High Card upgraded to One Pair

    return strength


def convert_jacks_to_jokers(hands):
    """
    Go through all the cards of each hand and convert Jack cards to Jokers.
    """
    # Convert both the card string and the list of cards in each hand.
    for hand in hands:
        hand[0] = hand[0].replace("J", "*")
        for card in hand[2]:
            if card[0] == "J":
                card[0] = "*"


def calculate_total_winnings(hands):
    """
    Sort the hands from weakest to strongest hands and then calculate the
    total winnings based on the rank of the hand.
    """
    # Calculate the strength of each hand.
    for hand in hands:
        strength = hand_strength(hand)
        hand.append(strength)

    # Bubble sort on the strength of each hand, weakest hand to strongest.
    n = len(hands)
    for i in range(n):
        for j in range(n - 1):
            if hands[j][3] < hands[j + 1][3]:
                hands[j], hands[j + 1] = hands[j + 1], hands[j]

    # Calculate the total winnings by multiplying the rank of the hand
    # with the bid associated with that hand.
    rank = 1
    total_winnings = 0
    for hand in hands:
        total_winnings += rank * hand[1]
        rank += 1

    return total_winnings


hands = read_input("7", transformer, example=True)
total_winnings = calculate_total_winnings(hands)
print(f"Part 1 Example: {total_winnings}\tExpecting: 6440")

hands = read_input("7", transformer, example=True)
convert_jacks_to_jokers(hands)
total_winnings = calculate_total_winnings(hands)
print(f"Part 2 Example: {total_winnings}\tExpecting: 5905\n")

hands = read_input("7", transformer, example=False)
total_winnings = calculate_total_winnings(hands)
print(f"Part 1: {total_winnings}\tExpecting: 248569531")

hands = read_input("7", transformer, example=False)
convert_jacks_to_jokers(hands)
total_winnings = calculate_total_winnings(hands)
print(f"Part 2: {total_winnings}\tExpecting: 250382098")
