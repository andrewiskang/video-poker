import random
from collections import defaultdict


class Card(object):
    # a Card has two characteristics: a rank (number) and a suit
    def __init__(self, rank_value, suit):
        # initializes a Card with specified rank value and suit
        self.rank_value = rank_value
        ranks = {1:"A", 2:"2", 3:"3", 4:"4", 5:"5", 6:"6", 7:"7", 8:"8",
        9:"9", 10:"10", 11:"J", 12:"Q", 13:"K"}
        self.rank = ranks[rank_value]
        self.suit = suit

    def __eq__(self, other):
        # overrides == function for comparison purposes
        if isinstance(self,other.__class__):
            return (self.rank_value == other.rank_value) and (self.suit == other.suit)
        return False

    def __ne__(self, other):
        # overrides != function for comparison purposes
        return not self.__eq__(other)

    def info(self):
        # returns card info as a string in the form "<rank> of <suit>"
        return self.rank + " of " + self.suit

    def print_card(self):
        # prints out card info
        print(self.info())

class Deck(set):
    # a Deck contains cards that can be drawn into or pulled out of a Hand
    def random_draw(self):
        # draw one Card from Deck at random
        return random.sample(self, 1)[0]

    def draw_hand(self):
        # given a deck, draws a Hand of 5 Cards
        hand = Hand()
        new_cards = random.sample(self, 5)
        for i in range(5):
            hand.append(new_cards[i])
            self.remove(new_cards[i])
        return hand

    def redraw(self, hand, indices):
        # redraws Cards based on selected indices within the given Hand
        # return all selected Cards back to the Deck before Cards are redrawn
        for i in indices:
            self.add(hand[i])

        # if Card index was selected, redraw Card and remove from the Deck
        # if Card index was not selected, keep same Card in Hand
        new_hand = Hand()
        for i in range(5):
            if i in indices:
                new_card = random.sample(self, 1)[0]
                new_hand.append(new_card)
                self.remove(new_card)
            else:
                new_hand.append(hand[i])

        return new_hand

    @staticmethod
    def full_deck():
    # returns a Deck of 52 cards: 13 ranks of 4 suits each
        deck = Deck()
        rank_values = range(1, 14)
        suits = {"Spades", "Hearts", "Clubs", "Diamonds"}
        for rank_value in rank_values:
            for suit in suits:
                deck.add(Card(rank_value, suit))
        return deck

class Hand(list):
    # a Hand contains 5 Cards from a Deck of 52 Cards, with no duplicates
    def print_hand(self):
        # prints out a visual representation of the Cards in the given Hand
        card_info = []
        for card in self:
            card_info.append(card.info())
        print("    ".join(card_info))

    def outcome(self):
        # returns the winning outcome of a Hand, and None if losing Hand

        # store a tally of ranks and suits in two separate Dictionaries
        rank_tally = defaultdict(int)
        for card in self:
            rank_tally[card.rank_value] += 1
        suit_tally = defaultdict(int)
        for card in self:
            suit_tally[card.suit] += 1

        # store max frequency of ranks and suits for evaluation purposes
        max_rank_value = max(rank_tally, key=rank_tally.get)
        max_rank_tally = rank_tally[max_rank_value]
        max_suit = max(suit_tally, key=suit_tally.get)
        max_suit_tally = suit_tally[max_suit]
        # also store ranks and rank frequency
        ranks = sorted(rank_tally.keys())
        rank_tallies = sorted(rank_tally.values())

        # initial bools to help determine outcome

        # a flush is 5 of the same suit
        is_flush = (max_suit_tally == 5)
        # a straight is 5 consecutive ranks or a Royal (10, J, Q, K, A)
        lowest_rank = ranks[0]
        is_straight = (ranks == range(lowest_rank, lowest_rank+5) or
                       ranks == [1, 10, 11, 12, 13])

        # logic progression to determine winning outcome of given Hand

        # a straight flush is both a straight and a flush
        if is_flush and is_straight:
            # a royal flush is 10, J, Q, K, A, all with the same suit
            if ranks == [1, 10, 11, 12, 13]:
                return "Royal Flush"
            else:
                return "Straight Flush"
        # a four of a kind is 4 of the same rank (max rank tally = 4)
        if max_rank_tally == 4:
            return "Four of a Kind"
        # a full house is one three of a kind and one pair
        if rank_tallies == [2, 3]:
            return "Full House"
        # a flush is 5 of the same suit
        if is_flush:
            return "Flush"
        # a straight is 5 consecutive ranks or a Royal (10, J, Q, K, A)
        if is_straight:
            return "Straight"
        # a three of a kind is 3 of the same rank (max rank tally = 3)
        if max_rank_tally == 3:
            return "Three of a Kind"
        # a two pair is... two pairs
        if rank_tallies == [1, 2, 2]:
            return "Two Pair"
        # Jacks or Better is one J, Q, K, A pair
        if (rank_tallies == [1, 1, 1, 2] and
            max_rank_value in [1, 11, 12, 13]):
            return "Jacks or Better"
        return None

class Payout(dict):
    # a Payout table lists all winning outcomes with their respective payouts
    def __init__(self, royal_flush=800, straight_flush=50,
                 four_of_a_kind=25, full_house=9, flush=6, straight=4,
                 three_of_a_kind=3, two_pair=2, jacks_or_better=1):
        # initializes a Payout table given specific payout amounts
        # returns full pay (9/6) Jacks or Better by default
        self.table = {"Royal Flush" : royal_flush,
                      "Straight Flush" : straight_flush,
                      "Four of a Kind" : four_of_a_kind,
                      "Full House" : full_house,
                      "Flush" : flush,
                      "Straight" : straight,
                      "Three of a Kind" : three_of_a_kind,
                      "Two Pair" : two_pair,
                      "Jacks or Better" : jacks_or_better}

"""
class Game(object):
    # a Game contains specific payout tables and scoring logic for each Hand
    def __init__(self, royal_flush=800, straight_flush=50,
    four_of_a_kind=25, full_house=9, flush=6, straight=4, three_of_a_kind=3,
    two_pair=2, jacks_or_better=1, coin=0.25, five_credit_override):
        # initializes a Game with a given

    def bug(self):"""
