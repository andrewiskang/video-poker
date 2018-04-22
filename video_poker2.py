import random
from collections import defaultdict

RANKS = {1:"A",
         2:"2",
         3:"3",
         4:"4",
         5:"5",
         6:"6",
         7:"7",
         8:"8",
         9:"9",
         10:"10",
         11:"J",
         12:"Q",
         13:"K"}
SUITS = {"S": "Spades",
         "H": "Hearts",
         "C": "Clubs",
         "D": "Diamonds"}


class Card(object):
    # a Card has two characteristics: a rank (number) and a suit
    def __init__(self, card_string):
        # initializes a Card with specified rank value and suit
        self.string = card_string
        self.rank = RANKS[rank_value(card_string)]
        self.suit = SUITS[suit_initial(card_string)]

    def __eq__(self, other):
        # overrides == function for comparison purposes
        if isinstance(self,other.__class__):
            return (self.rank_value == other.rank_value) and
                   (self.suit_initial == other.suit_initial)
        return False

    def __ne__(self, other):
        # overrides != function for comparison purposes
        return not self.__eq__(other)

    def full_name(self):
        # returns Card name as a string in the form "<rank> of <suit>"
        return self.rank + " of " + self.suit

    def print_name(self):
        # prints out full card name
        print(self.full_name())

    @staticmethod
    def rank_value(card_string):
        # given a rank-suit string, return the rank value of the given string (int)
        return int(card_string[:-1])
    @staticmethod
    def suit_initial(card_string):
        # given a rank-suit string, return the suit of the given string (string)
        return (card_string[-1])


class Deck(list):
    # a Deck contains card strings to be drawn into or pulled out of a hand
    def new_hand(self):
        # given a Deck, shuffles and draws 5 cards from the top of the Deck
        random.shuffle(self)
        new_cards = self[:5]
        self = self[5:]
        return new_cards

    def draw_cards(self, hand=[], hold_indices=[]):
        # redraws cards not in hold_indices parameter within the given Hand
        # to draw a new hand, no parameters are necessary
        if hand == []:
            return self.new_hand()

        # return cards back to the Deck and shuffle before cards are redrawn
        remove_indices = list({0,1,2,3,4} - set(hold_indices))
        for i in remove_indices:
            self.append(hand[i])
        random.shuffle(self)

        # for cards to be removed, draw and remove a card from the Deck
        if i in remove_indices:
            new_card = self[0]
            hand[i] = new_card
            self = self[1:]
        return hand

    @staticmethod
    def new_deck():
    # returns a Deck of 52 cards: 13 ranks of 4 suits each
        deck = Deck()
        rank_values = RANKS.keys()
        suit_initials = SUITS.keys()
        for rank_value in rank_values:
            for suit_initial in suit_initials:
                deck.append(str(rank_value) + suit_initial)
        return deck


class Hand(list):
    # a Hand contains 5 card strings from a deck of 52 cards
    def print_hand(self):
        # prints out a visual representation of the Cards in the given Hand
        card_info = []
        for card_string in self:
            card = Card(card_string)
            card_info.append(card.full_name())
        print("    ".join(card_info))

    def outcome(self):
        # returns the winning outcome of a Hand, and None if losing Hand

        # store a tally of ranks and suits in two separate Dictionaries
        rank_tally = defaultdict(int)
        suit_tally = defaultdict(int)
        for card_string in self:
            rank_tally[Card.rank_value(card_string)] += 1
        for card_string in self:
            suit_tally[Card.suit_initial(card_string)] += 1

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

class Payout(object):
    # a Payout table lists all winning outcomes with their respective payouts
    def __init__(self, royal_flush=800, straight_flush=50,
                 four_of_a_kind=25, full_house=9, flush=6, straight=4,
                 three_of_a_kind=3, two_pair=2, jacks_or_better=1):
        # initializes a Payout table given specific payout amounts
        # returns full pay (9/6) Jacks or Better by default
        self.table = defaultdict(int)
        self.table["Royal Flush"] = royal_flush
        self.table["Straight Flush"] = straight_flush
        self.table["Four of a Kind"] = four_of_a_kind
        self.table["Full House"] = full_house
        self.table["Flush"] = flush
        self.table["Straight"] = straight
        self.table["Three of a Kind"] = three_of_a_kind
        self.table["Two Pair"] = two_pair
        self.table["Jacks or Better"] = jacks_or_better

    def print_payout(self):
        # prints out the payouts for each winning outcome
        print("PAYOUT TABLE:")
        print("  Royal Flush:         " + str(self.table["Royal Flush"]))
        print("  Straight Flush:      " + str(self.table["Straight Flush"]))
        print("  Four of a Kind:      " + str(self.table["Four of a Kind"]))
        print("  Full House:          " + str(self.table["Full House"]))
        print("  Flush:               " + str(self.table["Flush"]))
        print("  Straight:            " + str(self.table["Straight"]))
        print("  Three of a Kind:     " + str(self.table["Three of a Kind"]))
        print("  Two Pair:            " + str(self.table["Two Pair"]))
        print("  Jacks or Better:     " + str(self.table["Jacks or Better"]))


class Game(object):
    # a Game contains specific payout tables and scoring logic for each Hand
    def __init__(self, deck=Deck.new_deck(), hand=[], bankroll=1000,
                 num_credits=5, payout=Payout()):
        # initializes a Game that holds the following information:
        # deck, current hand, bankroll, # credits being played, payout table
        self.deck = deck
        self.hand = hand
        self.bankroll = bankroll
        self.num_credits = num_credits
        self.payout = payout
