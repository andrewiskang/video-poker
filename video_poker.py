


class Card(object):
    # a card has two characteristics: a rank (number) and a suit
    def __init__(self, rank, suit):
        # return a Card with specified rank and suit
        self.rank = rank
        self.suit = suit

    def __eq__(self, other):
        # overrides == function for comparison purposes
        if isinstance(self,other.__class__):
            return (self.rank == other.rank) and (self.suit == other.suit)
        return False

    def __ne__(self, other):
        # overrides != function for comparison purposes
        return not self.__eq__(other)

    def print_card(self):
        # prints out Card rank and suit
        print(self.rank + " of " + self.suit)

def full_deck():
    # returns a deck of 52 cards: 13 ranks of 4 suits each
    deck = set()
    ranks = {"A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"}
    suits = {"Spades", "Hearts", "Clubs", "Diamonds"}
    for rank in ranks:
        for suit in suits:
            deck.add(Card(rank, suit))
    return deck
