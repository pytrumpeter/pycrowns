from collections import namedtuple
from random import shuffle
import sys

RUN = 'run'
SET = 'set'

SUITS = {'♥', '♦', '♣', '★', '♠'}
VALUES = {('3', 3), ('4', 4), ('5', 5), ('6', 6), ('7', 7), ('8', 8), ('9', 9), ('10', 10), ('J', 11), ('Q', 12), ('K', 13)}

round_number = 10

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

    def check_for_set(self):
        last_card = None
        run = []
        for card in self.unmatched:
            if last_card:
                if last_card.int_value == card.int_value:
                    run.append(card)
                else:
                    if len(run) > 2:
                        return run
                    run = [card]
            else:
                run = [card]
            last_card = card
        if len(run) > 2:
            return run
        return []

    def check_for_run(self):
        last_card = None
        run = []
        for card in self.unmatched:
            if last_card:
                if last_card.int_value == card.int_value and last_card.suit == card.suit:
                    continue
                if last_card.int_value == card.int_value - 1 and last_card.suit == card.suit:
                    run.append(card)
                else:
                    if len(run) > 2:
                        return run
                    run = [card]

            else:
                run = [card]
            last_card = card
        if len(run) > 2:
            return run
        return []

    def get_runs_or_sets(self, thing):
        sets = []
        while True:
            if thing == RUN:
                run = self.check_for_run()
            else:
                run = self.check_for_set()
            for c in run:
                try:
                    self.unmatched.remove(c)
                except ValueError:
                    pass
            if not run:
                break
            sets.append(run)
        return sets

    def check_wild_cards(self, setrun, wild_cards):
        while wild_cards:
            if setrun == RUN:
                setrun_obj = self.runs
                new_setrun = check_for_run_wild(self.unmatched, wild_cards)
            else:
                setrun_obj = self.sets
                new_setrun = check_for_set_wild(self.unmatched, wild_cards)

            if new_setrun:
                setrun_obj.append(new_setrun)
            else:
                if not setrun_obj:
                    break
                while wild_cards and setrun_obj:
                    setrun_obj[0].append(wild_cards.pop())
                    print("Pairing up wild card with a {}: {}".format(setrun, setrun_obj[0]))

    def play_round(self, player):
        self.player = player
        self.rounds = 0
        self.unmatched = None
        self.sets = []
        self.runs = []

        while True:
            self.rounds += 1
            self.runs = []
            self.sets = []
            wild_cards = player.wild_cards.copy()

            # sort hand
            self.unmatched = sorted(self.player.hand, key=lambda x: x.int_value)

            self.sets = self.get_runs_or_sets(SET)

            self.check_wild_cards(SET, wild_cards)

            value_sort = sorted(self.unmatched, key=lambda x: x.int_value)
            self.unmatched = sorted(value_sort, key=lambda x: x.suit)

            self.runs = self.get_runs_or_sets(RUN)

            self.check_wild_cards(RUN, wild_cards)

            print("FIRST PASS")
            print('runs:')
            for r in self.runs:
                show_hand(r)
            print('sets:')
            for s in self.sets:
                show_hand(s)

            first_runs = self.runs
            first_sets = self.sets

            cards_used = sum([len(r) for r in self.runs + self.sets])
            print(f'Using {cards_used} cards')

            if cards_used == round_number or len(self.unmatched) < 1:
                break

            self.sets = []
            wild_cards = player1.wild_cards.copy()

            first_unmatched = self.unmatched

            # Start second pass, runs first then sets

            self.unmatched = sorted(self.player.hand, key=lambda x: x.int_value)
            self.unmatched = sorted(self.unmatched, key=lambda x: x.suit)

            self.runs = self.get_runs_or_sets(RUN)

            self.check_wild_cards(RUN, wild_cards)

            self.unmatched = sorted(self.unmatched, key=lambda x: x.int_value)

            self.sets = self.get_runs_or_sets(SET)

            self.check_wild_cards(SET, wild_cards)

            print("SECOND PASS:")
            print('\nruns:')
            for r in self.runs:
                show_hand(r)
            print('\nsets:')
            for s in self.sets:
                show_hand(s)

            cards_used2 = sum([len(r) for r in self.runs + self.sets])
            print(f'Using {cards_used2} cards')

            if cards_used2 == round_number or len(self.unmatched) < 1:
                break

            if cards_used > cards_used2:
                discard(first_unmatched, player1.hand)
            else:
                discard(self.unmatched, player1.hand)
            new_card = game.deal()

            print("**** Drew: ", new_card)
            if new_card.int_value == 14 or new_card.int_value == round_number:
                player1.wild_cards.append(new_card)
            else:
                player1.hand.append(new_card)

            print("**** NEXT TURN")
            print(show_hand(player1.hand + player1.wild_cards))


def show_hand(cards):
    for c in cards:
        print(c, end=" ")


def discard(leftovers, hand):
    print("Heres what i could discard: ", leftovers)
    try:
        hand.remove(leftovers[0])
    except IndexError:
        print("Out of hand")
    else:
        print('**discarding ', leftovers[0])


def check_for_set_wild(leftovers, wild_cards):
    if not leftovers or not wild_cards:
        return None
    print("Wild cards: ", wild_cards)
    print("Leftovers: ", leftovers)
    last_card = None

    # Check for cases where there are two of a set and not three
    if len(leftovers) > 1:
        for card in leftovers:
            if last_card:
                if last_card.int_value == card.int_value:
                    print("Found a wild match")
                    new_set = [last_card, card, wild_cards.pop()]
                    print(new_set)
                    leftovers.remove(last_card)
                    leftovers.remove(card)
                    print("LEFTOVERS IS NOW ", leftovers)
                    return new_set
            last_card = card
    else:
        # If there are two wild cards, pick a card and put it with them
        if len(wild_cards) > 1:
            print("Sticking together two wilds and a leftover")
            return [leftovers[0], wild_cards.pop(), wild_cards.pop()]


def check_for_run_wild(leftovers, wild_cards):
    leftovers = sorted(leftovers, key=lambda x: x.int_value)
    leftovers = sorted(leftovers, key=lambda x: x.suit)
    last_card = None
    for card in leftovers:
        if last_card:
            print(last_card)
            if last_card.int_value == card.int_value and last_card.suit == card.suit:
                continue
            if last_card.int_value == card.int_value - 1 and last_card.suit == card.suit:
                new_set = [last_card, card, wild_cards.pop()]
                leftovers.remove(last_card)
                leftovers.remove(card)
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

    game.rounds = 0

    game.play_round(player1)

    print(f'\nWON in {game.rounds} rounds!')
