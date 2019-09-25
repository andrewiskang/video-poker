import random
from collections import defaultdict

RANKS = {1:'A',
         2:'2',
         3:'3',
         4:'4',
         5:'5',
         6:'6',
         7:'7',
         8:'8',
         9:'9',
         10:'10',
         11:'J',
         12:'Q',
         13:'K'}
SUITS = {'S': 'Spades',
         'H': 'Hearts',
         'C': 'Clubs',
         'D': 'Diamonds'}


class Card(object):
    # a Card has two characteristics: a rank (number) and a suit
    def __init__(self, cardString):
        # initializes a Card with specified rank value and suit
        self.string = cardString
        self.rank = RANKS[rankValue(cardString)]
        self.suit = SUITS[suitInitial(cardString)]

    def __eq__(self, other):
        # overrides == function for comparison purposes
        if isinstance(self,other._Class__):
            return (self.rankValue == other.rankValue) and \
                   (self.suitInitial == other.suitInitial)
        return False

    def __ne__(self, other):
        # overrides != function for comparison purposes
        return not self.__eq__(other)

    def fullName(self):
        # returns Card name as a string in the form '<rank> of <suit>'
        return self.rank + ' of ' + self.suit

    def printName(self):
        # prints out full card name
        print(self.fullName())

    @staticmethod
    def rankValue(cardString):
        # given a rank-suit string, return the rank value of the given string (int)
        return int(cardString[:-1])
    @staticmethod
    def suitInitial(cardString):
        # given a rank-suit string, return the suit of the given string (string)
        return (cardString[-1])


class Deck(list):
    # a Deck contains card strings to be drawn into or pulled out of a hand
    def __init__(self):
        # returns a Deck of 52 cards: 13 ranks of 4 suits each
        self = [str(rankValue) + suitInitial for rankValue in RANKS.keys() for suitInitial in SUITS.keys()]

    def newHand(self):
        # given a Deck, shuffles and draws 5 cards from the top of the Deck
        random.shuffle(self)
        newCards = self[:5]
        return newCards

    def drawCards(self, hand=[], holdIndices=[]):
        # redraws cards not in holdIndices parameter within the given Hand
        # to draw a new hand, no parameters are necessary
        if not hand:
            return self.newHand()

        # shuffle deck and draw cards
        drawIndices = list({0,1,2,3,4} - set(holdIndices))
        random.shuffle(self)
        for i in drawIndices:
            hand[i] = self[i]
        return hand


class Hand(list):
    # a Hand contains 5 card strings from a deck of 52 cards
    def printHand(self):
        # prints out a visual representation of the Cards in the given Hand
        cardInfo = []
        for cardString in self:
            card = Card(cardString)
            cardInfo.append(card.fullName())
        print('    '.join(cardInfo))

    def outcome(self):
        # returns the winning outcome of a Hand, and None if losing Hand
        # if Hand is empty, return None
        if self == []:
            return None

        # store a tally of ranks and suits in two separate Dictionaries
        rankTally = defaultdict(int)
        suitTally = defaultdict(int)
        for cardString in self:
            rankTally[Card.rankValue(cardString)] += 1
        for cardString in self:
            suitTally[Card.suitInitial(cardString)] += 1

        # store max frequency of ranks and suits for evaluation purposes
        maxRankValue = max(rankTally, key=rankTally.get)
        maxRankTally = rankTally[maxRankValue]
        maxSuit = max(suitTally, key=suitTally.get)
        maxSuitTally = suitTally[maxSuit]
        # also store ranks and rank frequency
        ranks = sorted(rankTally.keys())
        rankTallies = sorted(rankTally.values())

        # initial bools to help determine outcome

        # a flush is 5 of the same suit
        isFlush = (maxSuitTally == 5)
        # a straight is 5 consecutive ranks or a Royal (10, J, Q, K, A)
        lowestRank = ranks[0]
        isStraight = (ranks == range(lowestRank, lowestRank+5) or
                       ranks == [1, 10, 11, 12, 13])

        # logic progression to determine winning outcome of given Hand

        # a straight flush is both a straight and a flush
        if isFlush and isStraight:
            # a royal flush is 10, J, Q, K, A, all with the same suit
            if ranks == [1, 10, 11, 12, 13]:
                return 'Royal Flush'
            else:
                return 'Straight Flush'
        # a four of a kind is 4 of the same rank (max rank tally = 4)
        if maxRankTally == 4:
            return 'Four of a Kind'
        # a full house is one three of a kind and one pair
        if rankTallies == [2, 3]:
            return 'Full House'
        # a flush is 5 of the same suit
        if isFlush:
            return 'Flush'
        # a straight is 5 consecutive ranks or a Royal (10, J, Q, K, A)
        if isStraight:
            return 'Straight'
        # a three of a kind is 3 of the same rank (max rank tally = 3)
        if maxRankTally == 3:
            return 'Three of a Kind'
        # a two pair is... two pairs
        if rankTallies == [1, 2, 2]:
            return 'Two Pair'
        # Jacks or Better is one J, Q, K, A pair
        if (rankTallies == [1, 1, 1, 2] and
            maxRankValue in [1, 11, 12, 13]):
            return 'Jacks or Better'
        return None


class Payout(dict):
    # a Payout table lists all winning outcomes with their respective payouts
    def __missing__(self, key):
        # defaults all missing key values to 0
        return 0

    # default paytable if values are not provided
    def __init__(self, payout={}):
        self['Royal Flush'] = payout.get('Royal Flush', 800)
        self['Straight Flush'] = payout.get('Straight Flush', 50)
        self['Four of a Kind'] = payout.get('Four of a Kind', 25)
        self['Full House'] = payout.get('Full House', 9)
        self['Flush'] = payout.get('Flush', 6)
        self['Straight'] = payout.get('Straight', 4)
        self['Three of a Kind'] = payout.get('Three of a Kind', 3)
        self['Two Pair'] = payout.get('Two Pair', 2)
        self['Jacks or Better'] = payout.get('Jacks or Better', 1)

    def printPayout(self):
        # prints out the payouts for each winning outcome
        print('PAYOUT TABLE:')
        print('  Royal Flush:         ' + str(self['Royal Flush']))
        print('  Straight Flush:      ' + str(self['Straight Flush']))
        print('  Four of a Kind:      ' + str(self['Four of a Kind']))
        print('  Full House:          ' + str(self['Full House']))
        print('  Flush:               ' + str(self['Flush']))
        print('  Straight:            ' + str(self['Straight']))
        print('  Three of a Kind:     ' + str(self['Three of a Kind']))
        print('  Two Pair:            ' + str(self['Two Pair']))
        print('  Jacks or Better:     ' + str(self['Jacks or Better']))


class Game(object):
    # a Game contains specific payout tables and scoring logic for each Hand
    def __init__(self, deck=Deck(), hand=[], bankroll=1000,
                 numCredits=5, payout=Payout()):
        # initializes a Game that holds the following information:
        # deck, current hand, bankroll, # credits being played, payout table
        self.deck = deck
        self.hand = hand
        self.bankroll = bankroll
        self.numCredits = numCredits
        self.payout = payout
