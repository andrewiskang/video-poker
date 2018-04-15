import random


class Card(object):
    # a Card has two characteristics: a rank (number) and a suit
    def __init__(self, rank, suit):
        # initializes a Card with specified rank and suit
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
        ranks = {"A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"}
        suits = {"Spades", "Hearts", "Clubs", "Diamonds"}
        for rank in ranks:
            for suit in suits:
                deck.add(Card(rank, suit))
        return deck

class Hand(list):
    # a Hand contains 5 Cards from a Deck of 52 Cards, with no duplicates


    def print_hand(self):
        # prints out a visual representation of the Cards in the given Hand
        card_info = []
        for card in self:
            card_info.append(card.info())
        print("    ".join(card_info))
