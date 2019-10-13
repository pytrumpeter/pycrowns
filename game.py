from collections import namedtuple
from random import shuffle
import sys

SUITS = {'H', 'D', 'S', 'C', 'P'}
VALUES = {('3', 3), ('4', 4), ('5', 5), ('6', 6), ('7', 7), ('8', 8), ('9', 9), ('10', 10), ('J', 11), ('Q', 12), ('K', 13)}

round_number =  10

Card = namedtuple('Card', {'suit': None, 'value': None, 'int_value': None})
Card.__repr__ = lambda x: str(x.value) + str(x.suit)

class Player:
    def __init__(self):
        self.hand = []
        self.wild_cards = []
        self.points = 0


class Game:
    def __init__(self):
        self.deck = []

    def make_deck(self, suits, values):
        for suit in suits:
            for value in values:
                card = Card(suit, value[0], value[1])
                self.deck.append(card)
        for i in range(3):
            card = Card('Joker', 'Joker', 14)
            self.deck.append(card)
        return self.deck

    def shuffle(self):
        shuffle(self.deck)

    def deal(self):
        try:
            return game.deck.pop(0)
        except:
            print("Sorry, no more cards!")
            sys.exit(0)

def show_hand(cards):
    for c in cards:
        print(c, end=" ")

def check_for_run(hand):
    last_card = None
    run = []
    for card in hand:
        if last_card:
            if last_card.int_value == card.int_value and last_card.suit == card.suit:
                continue
            if last_card.int_value == card.int_value - 1 and last_card.suit == card.suit:
                #print('possible run')
                run.append(card)
            else:
                if len(run) > 2:
                    #print('got a run!')
                    return run
                run = [card]

        else:
            run = [card]
        last_card = card
    if len(run) > 2:
        return run
    return []
        # print(run)
        # possible_downrun = [c for c in player1.hand if c.value == card.int_value - 1]
        #
        # possible_uprun = [c for c in player1.hand if c.value == card.int_value - 1]


def check_for_set(hand):
    last_card = None
    run = []
    for card in hand:
        if last_card:
            #print("comparing " + str(last_card.int_value) + " with " + str(card.int_value))
            if last_card.int_value == card.int_value:
                #print('possible set')
                run.append(card)
            else:
                if len(run) > 2:
                    #print('got a set!')
                    return run
                run = [card]
        else:
            run = [card]
            #print('\ngetting started: ', run)
        last_card = card
    if len(run) > 2:
        return run
    return []

def discard(leftovers, hand):
    print("heres what i could discard: ", leftovers)
    try:
        hand.remove(leftovers[0])
    except IndexError:
        print("Out of hand")
    else:
        print('discarding ', leftovers[0])

def check_for_set_wild(leftovers, wild_cards):
    if not leftovers or not wild_cards:
        return None
    print("Wild cards: ", wild_cards)
    print("Leftovers: ", leftovers)
    last_card = None
    if len(leftovers) > 1:
        for card in leftovers:
            if last_card:
                if last_card.int_value == card.int_value:
                    print("Found a wild match")
                    new_set = [last_card, card, wild_cards.pop()]
                    leftovers.remove(last_card)
                    leftovers.remove(card)
                    print("LEFTOVERS IS NOW ", leftovers)
                    return new_set
            last_card = card
    else:
        if len(wild_cards) > 1:
            print("Sticking together two wilds and a leftover")
            return [leftovers[0], wild_cards.pop(), wild_cards.pop()]

def check_for_run_wild(leftovers, wild_cards):
    leftovers = sorted(leftovers, key=lambda x: x.int_value)
    leftovers = sorted(leftovers, key=lambda x: x.suit)
    print("check for run: Wild cards: ", wild_cards)
    print("Leftovers: ", leftovers)
    last_card = None
    for card in leftovers:
        if last_card:
            if last_card.int_value == card.int_value and last_card.suit == card.suit:
                continue
            if last_card.int_value == card.int_value - 1 and last_card.suit == card.suit:
                #print('possible run')
                new_set = [last_card, card, wild_cards.pop()]
                leftovers.remove(last_card)
                leftovers.remove(card)
                print("LEFTOVERS IS NOW ", leftovers)
                return new_set
        last_card = card

if __name__ == '__main__':
    game = Game()

    deck1 = game.make_deck(SUITS, VALUES)
    deck2 = game.make_deck(SUITS, VALUES)

    player1 = Player()
    player2 = Player()

    game.shuffle()

    for x in range(round_number):
        deal = game.deal()
        if deal.int_value == round_number or deal.int_value == 14:
            player1.wild_cards.append(deal)
            print("Wild card: ", deal)
        else:
            player1.hand.append(deal)

    show_hand(player1.hand)

    rounds = 0

    while True:
        rounds += 1
        runs = []
        sets = []
        wild_cards = player1.wild_cards.copy()

        # sort hand
        vsort_value = sorted(player1.hand, key=lambda x: x.int_value)
        #print("I'll be set evaluating ", vsort_value)
        while True:
            run = check_for_set(vsort_value)
            #print("THE SET", run)
            for c in run:
                try:
                    vsort_value.remove(c)
                except ValueError:
                    pass
            if not run:
                break
            sets.append(run)
        while wild_cards:
            new_set = check_for_set_wild(vsort_value, wild_cards)
            print("VSORT_VALUE IS NOW ", vsort_value)
            if new_set:
                sets.append(new_set)
            else:
                while wild_cards and sets:
                    sets[0].append(wild_cards.pop())
                    print("Paring up wild card with a set: {}".format(sets[0]))
                break

        vsort_suit = sorted(vsort_value, key=lambda x: x.int_value)
        vsort_suit = sorted(vsort_suit, key=lambda x: x.suit)
        while True:
            run = check_for_run(vsort_suit)
            for c in run:
                try:
                    vsort_suit.remove(c)
                except ValueError:
                    pass
            if not run:
                break
            runs.append(run)
        while wild_cards:
            new_run = check_for_run_wild(vsort_suit, wild_cards)
            if new_run:
                runs.append(new_run)
            else:
                while wild_cards and runs:
                    runs[0].append(wild_cards.pop())
                    print("Pairing up wild card with a set: {}".format(runs[0]))
                break

        print('runs:')
        for r in runs:
            show_hand(r)
        print('sets:')
        for s in sets:
            show_hand(s)

        cards_used = sum([len(r) for r in runs+sets])
        print('taking cards: ', cards_used)

        if cards_used == round_number or len(vsort_suit) < 1:
            break

        runs = []
        sets = []
        wild_cards = player1.wild_cards.copy()

        vsort_suit2 = sorted(player1.hand, key=lambda x: x.int_value)
        vsort_suit2 = sorted(vsort_suit2, key=lambda x: x.suit)
        while True:
            run = check_for_run(vsort_suit2)
            for c in run:
                vsort_suit2.remove(c)
            if not run:
                break
            runs.append(run)
        while wild_cards:
            new_run = check_for_run_wild(vsort_suit2, wild_cards)
            if new_run:
                runs.append(new_run)
            else:
                while wild_cards and runs:
                    runs[0].append(wild_cards.pop())
                    print("Pairing up wild card with a set: {}".format(runs[0]))
                break

        vsort_value2 = sorted(vsort_suit2, key=lambda x: x.int_value)
        while True:
            run = check_for_set(vsort_value2)
            for c in run:
                vsort_value2.remove(c)
            if not run:
                break
            sets.append(run)
        while wild_cards:
            new_set = check_for_set_wild(vsort_value2, wild_cards)
            if new_set:
                sets.append(new_set)
            else:
                while wild_cards and sets:
                    sets[0].append(wild_cards.pop())
                    print("Paring up wild card with a set: {}".format(sets[0]))
                break

        print('runs:')
        for r in runs:
            show_hand(r)
        print('\nsets:')
        for s in sets:
            show_hand(s)

        cards_used2 = sum([len(r) for r in runs + sets])
        #print('taking cards: ', cards_used2)

        if cards_used2 == round_number or len(vsort_value2) < 1:
            break

        if cards_used > cards_used2:
            discard(vsort_suit, player1.hand)
        else:
            discard(vsort_value2, player1.hand)
        new_card = game.deal()
        print("Drew: ", new_card)
        if new_card.int_value == 14 or new_card.int_value == round_number:
            player1.wild_cards.append(new_card)
        else:
            player1.hand.append(new_card)

        print("NEXT TURN")
        print(show_hand(player1.hand + player1.wild_cards))

    print(f'WON in {rounds} rounds!')