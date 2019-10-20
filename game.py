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
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.wild_cards = []
        self.points = 0


class Game:
    def __init__(self):
        self.deck = []
        self.discard_pile = None

    def pickup_discard(self):
        return self.discard_pile.pop()

    def discard(self, leftovers):
        print("Heres what i could discard: ", leftovers)
        try:
            self.player.hand.remove(leftovers[0])
            self.discard_pile.append(leftovers[0])
        except IndexError:
            print("Out of hand")
        else:
            print('**discarding ', leftovers[0])

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

    def sort_by_suit(self, cards):
        value_sort = sorted(cards, key=lambda x: x.int_value)
        return sorted(value_sort, key=lambda x: x.suit)

    def sort_by_rank(self, cards):
        return sorted(cards, key=lambda x: x.int_value)

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

    def check_wild_cards(self, setrun):
        while self.wild_cards_copy:
            if setrun == RUN:
                setrun_obj = self.runs
                new_setrun = check_for_run_wild(self.unmatched, self.wild_cards_copy)
            else:
                setrun_obj = self.sets
                new_setrun = check_for_set_wild(self.unmatched, self.wild_cards_copy)

            if new_setrun:
                setrun_obj.append(new_setrun)
            else:
                if not setrun_obj:
                    break
                while self.wild_cards_copy and setrun_obj:
                    setrun_obj[0].append(self.wild_cards_copy.pop())
                    print("Pairing up wild card with a {}: {}".format(setrun, setrun_obj[0]))

    def play_human_round(self, player):
        self.player = player
        while True:
            print(f"**** {self.player.name}'s turn")
            if round_number < len(self.player.hand + self.player.wild_cards):
                for i, c in enumerate(self.player.hand + self.player.wild_cards):
                    print(f"{i}) {c}")
                print("\nType the number of the card you wish to discard")

            print(show_hand(self.player.hand + self.player.wild_cards))
            try:
                print(f"Current discard is {self.discard_pile[-1]}")
            except:
                pass
            choice = input("What would you like to do?")

            try:
                discard = int(choice)
            except ValueError:
                if choice.upper() == 'P':
                    self.player.hand.append(self.pickup_discard())
                elif choice.upper() == 'G':
                    print(f"cards used by run/set: {self.evaluate_runs_then_sets()}")
                    print(f"cards used by set/run: {self.evaluate_sets_then_runs()}")
                    self.won()
                elif choice.upper() == 'S':
                    self.player.hand = self.sort_by_suit(self.player.hand)
                elif choice.upper() == 'R':
                    self.player.hand = self.sort_by_rank(self.player.hand)
                elif choice.upper() == 'D':
                    new_card = self.deal()
                    if new_card.int_value == 14 or new_card.int_value == round_number:
                        self.player.wild_cards.append(new_card)
                    else:
                        self.player.hand.append(new_card)
            else:
                # continue the discard part
                if discard + 1 > len(self.player.hand):
                    discard -= len(self.player.hand)
                    discard_chunk = self.player.wild_cards
                else:
                    discard_chunk = self.player.hand
                print(f"discarding {discard_chunk} {discard}")
                print(f"You are discarding {discard_chunk[discard]}")
                self.discard_pile.append(discard_chunk[discard])
                discard_chunk.remove(discard_chunk[discard])
                break

    def play_computer_round(self, player):
        self.player = player
        print(f"**** {self.player.name}'s turn")
        print(show_hand(self.player.hand + self.player.wild_cards))
        print("\n")
        self.unmatched = []

        cards_used = self.evaluate_sets_then_runs()

        if cards_used == round_number or len(self.unmatched) < 1:
            self.won()

        first_unmatched = self.unmatched

        # Start second pass, runs first then sets

        cards_used2 = self.evaluate_runs_then_sets()

        if cards_used2 == round_number or len(self.unmatched) < 1:
            self.won()

        if cards_used > cards_used2:
            self.discard(first_unmatched)
        else:
            self.discard(self.unmatched)
        new_card = game.deal()

        print("**** Drew: ", new_card)
        if new_card.int_value == 14 or new_card.int_value == round_number:
            self.player.wild_cards.append(new_card)
        else:
            self.player.hand.append(new_card)

        print("**** NEXT TURN")
        print(show_hand(self.player.hand + self.player.wild_cards))

    def evaluate_sets_then_runs(self):
        # sort hand
        self.unmatched = self.sort_by_rank(self.player.hand)
        self.wild_cards_copy = self.player.wild_cards.copy()
        self.runs = []
        self.sets = []

        self.sets = self.get_runs_or_sets(SET)

        self.check_wild_cards(SET)

        self.unmatched = self.sort_by_suit(self.unmatched)

        self.runs = self.get_runs_or_sets(RUN)

        self.check_wild_cards(RUN)

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

        return cards_used

    def evaluate_runs_then_sets(self):
        self.unmatched = self.sort_by_suit(self.player.hand)
        self.wild_cards_copy = self.player.wild_cards.copy()
        self.runs = []
        self.sets = []

        self.runs = self.get_runs_or_sets(RUN)

        self.check_wild_cards(RUN)

        self.unmatched = self.sort_by_rank(self.unmatched)

        self.sets = self.get_runs_or_sets(SET)

        self.check_wild_cards(SET)

        print("SECOND PASS:")
        print('\nruns:')
        for r in self.runs:
            show_hand(r)
        print('\nsets:')
        for s in self.sets:
            show_hand(s)

        cards_used = sum([len(r) for r in self.runs + self.sets])
        print(f'Using {cards_used} cards')

        return cards_used

    def won(self):
        print(f'\nWON in {rounds} rounds!')
        sys.exit(0)


def show_hand(cards):
    for c in cards:
        print(c, end=" ")


def check_for_set_wild(leftovers, wild_cards):
    if not leftovers or not wild_cards:
        return None
    last_card = None

    # Check for cases where there are two of a set and not three
    # and a wildcard is available
    if len(leftovers) > 1:
        for card in leftovers:
            if last_card:
                if last_card.int_value == card.int_value:
                    print("Found a wild match")
                    new_set = [last_card, card, wild_cards.pop()]
                    print(new_set)
                    leftovers.remove(last_card)
                    leftovers.remove(card)
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
    rounds = 0

    deck1 = game.make_deck(SUITS, VALUES)
    deck2 = game.make_deck(SUITS, VALUES)

    player1 = Player('Bob')
    player2 = Player('Bub')

    game.shuffle()

    for x in range(round_number):
        deal = game.deal()
        if deal.int_value == round_number or deal.int_value == 14:
            player1.wild_cards.append(deal)
        else:
            player1.hand.append(deal)

    for x in range(round_number):
        deal = game.deal()
        if deal.int_value == round_number or deal.int_value == 14:
            player2.wild_cards.append(deal)
        else:
            player2.hand.append(deal)

    game.discard_pile = [game.deal()]

    game.rounds = 0

    while True:
        rounds += 1
        game.play_human_round(player1)
        game.play_computer_round(player2)
